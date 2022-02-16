import os
from app.results import Results
from app.model_global import ModelClass
from app.model_global import ModelConfig
from configuration.contstants import AppConstants
from mrcnn.config import *
from mrcnn.visualize import *
from mrcnn.config import *
from mrcnn.model import *
from mrcnn.utils import *
from PIL import Image
from app.configUtil import ConfigConnect
from app.dbUtil import DbConnect
import skimage
import pandas as pd
import numpy as np
import cv2


class MLProcess:
    def __init__(
        self,
    ):
        config = ConfigConnect()
        root = config.get_section_config("root")["cwd"]
        info_folder = config.get_section_config("DIR")["info_folder"]
        name_of_file = config.get_section_config("FILE")["info"]
        info_file = os.path.join(root, info_folder, name_of_file)
        self.info = pd.read_csv(info_file)

    def load_image(
        self,
        result_id,
    ):

        dbConnect = DbConnect()
        dbConnect.createConnection()
        dbConnect.setSchema("mca")
        dbConnect.setTableName("cell_microscopy_result")

        columnList = ["name_of_image"]
        primaryKey = "id"
        pkValue = result_id
        data = dbConnect.fetchOne(columnList, primaryKey, pkValue)

        dbConnect.closeConnection()

        name_of_image = data[0]

        config = ConfigConnect()

        root = config.get_section_config("root")["cwd"]
        image_folder = config.get_section_config("DIR")["images_folder"]

        filePath = os.path.join(root, image_folder, name_of_image)

        # Load image
        img = Image.open(open(filePath, "rb"))
        img.load()
        image = np.asarray(img, dtype="int32")

        # If grayscale. Convert to RGB for consistency.
        if image.ndim != 3:
            image = skimage.color.gray2rgb(image)

        # If has an alpha channel, remove it for consistency
        if image.shape[-1] == 4:
            image = image[..., :3]
        return image, name_of_image

    def extract_boxes(
        self,
        result_id,
    ):

        dbConnect = DbConnect()
        dbConnect.createConnection()
        dbConnect.setSchema("mca")
        dbConnect.setTableName("cell_microscopy_result")

        columnList = ["name_of_image"]
        primaryKey = "id"
        pkValue = result_id
        data = dbConnect.fetchOne(columnList, primaryKey, pkValue)

        dbConnect.closeConnection()

        name_of_image = data[0]

        # extract each bounding box
        boxes = list()
        classes = list()

        for _, row in self.info[self.info.image_name == name_of_image].iterrows():
            xmin = row.xmin
            xmax = row.xmax
            ymin = row.ymin
            ymax = row.ymax
            class_name = str(row.category)
            coors = [ymin, xmin, ymax, xmax]
            boxes.append(coors)
            classes.append(class_name)
        return boxes, classes

    def load_mask(self, result_id):

        const = AppConstants()
        class_id_dict = const.class_ids()

        image, _ = self.load_image(result_id)
        # load XML
        boxes, classes = self.extract_boxes(result_id)
        # create one array for all masks, each on a different channel
        masks = np.zeros([image.shape[0], image.shape[1], len(boxes)], dtype="uint8")
        # create masks
        class_ids = list()
        for i in range(len(boxes)):
            box = boxes[i]
            row_s, row_e = box[1], box[3]
            col_s, col_e = box[0], box[2]
            masks[row_s:row_e, col_s:col_e, i] = 1
            class_ids.append(class_id_dict[classes[i]])
        return masks, np.asarray(class_ids)

    def model_predict(
        self,
        result_id,
    ):
        image, name_of_image = self.load_image(result_id)

        boxes, classes = self.extract_boxes(result_id)

        masks, class_ids = self.load_mask(result_id)

        model_cfg = ModelConfig()

        inp_image, _, scale, padding, crop = resize_image(
            image,
            min_dim=model_cfg.IMAGE_MIN_DIM,
            min_scale=model_cfg.IMAGE_MIN_SCALE,
            max_dim=model_cfg.IMAGE_MAX_DIM,
            mode=model_cfg.IMAGE_RESIZE_MODE,
        )
        
        config = tf.compat.v1.ConfigProto(
            device_count={"GPU": 1},
            intra_op_parallelism_threads=1,
            allow_soft_placement=True,
        )

        config.gpu_options.allow_growth = True
        config.gpu_options.per_process_gpu_memory_fraction = 0.6

        session = tf.compat.v1.Session(config=config)
        graph = tf.compat.v1.get_default_graph()

        model = ModelClass(session, graph)

        results = model.predict_model(inp_image)

        r = results[0]
        bbox = boxes
        masks = masks
        class_names = classes
        scores = r["scores"]
        
        const = AppConstants()
        class_id_dict = const.class_ids()
        infected = False
        freq = {}
        for item in list(class_id_dict.keys()):
            freq[item] = class_names.count(item)
            if item != "rbc" and freq[item] > 0:
                infected = True

        image_id = result_id
        number_of_rbc = freq["rbc"]
        trophozoite = freq["trophozoite"]
        unidentified = freq["unidentified"]
        ring = freq["ring"]
        schizont = freq["schizont"]
        gametocyte = freq["gametocyte"]
        leukocyte = freq["leukocyte"]

        self.save_prediction_image(
            image,
            bbox,
            class_names,
            name_of_image,
        )
        res = Results()
        res.updateRecordToDB(
            image_id,
            infected,
            number_of_rbc,
            trophozoite,
            unidentified,
            ring,
            schizont,
            gametocyte,
            leukocyte,
        )

        return (True, "Records Updated in DB and Prediction saved in Folder.")

    def save_prediction_image(
        self,
        image,
        boxes,
        class_names,
        name_of_image,
    ):
        masked_image = image.astype(np.uint8).copy()

        N = len(boxes)

        for i in range(N):
            color = (0, 255, 0)
            if class_names[i].lower().strip() != "rbc":
                color = (0, 0, 255)

            # Bounding box
            if not np.any(boxes[i]):
                # Skip this instance. Has no bbox. Likely lost in image cropping.
                continue
            y1, x1, y2, x2 = boxes[i]

            cv2.rectangle(masked_image, (y1, x1), (y2, x2), color, 2)
            score = None
            label = class_names[i]
            caption = "{} {:.3f}".format(label, score) if score else label

            cv2.putText(
                masked_image,
                caption,
                (y1, x1 + 8),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (255, 0, 0),
                2,
            )

        config = ConfigConnect()
        root = config.get_section_config("Root")["cwd"]
        predicted_images_folder = config.get_section_config("dir")[
            "predicted_images_folder"
        ]
        image_save_location = os.path.join(
            root,
            predicted_images_folder,
            name_of_image,
        )
        cv2.imwrite(image_save_location, masked_image)

    pass
