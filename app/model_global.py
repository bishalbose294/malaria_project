from app.configUtil import ConfigConnect
from mrcnn.model import MaskRCNN
from mrcnn.config import Config
from configuration.contstants import AppConstants
import os
import tensorflow as tf
from tensorflow.python.keras import backend as K


class ModelConfig(Config):
    # define the name of the configuration
    NAME = "malaria_cfg"
    # number of classes (background + cell)
    NUM_CLASSES = len(AppConstants().class_ids()) + 1
    # simplify GPU config
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1
    IMAGE_MIN_DIM = 512
    IMAGE_MAX_DIM = 512
    STEPS_PER_EPOCH = 500
    USE_MINI_MASK = False


class ModelClass:
    def __init__(
        self,
        session,
        graph,
    ):
        self.session = session
        self.graph = graph

        config = ConfigConnect()

        root = config.get_section_config("ROOT")["cwd"]
        model_weight_folder = config.get_section_config("DIR")["model_weight_folder"]
        model_weight = config.get_section_config("FILE")["model_weight"]
        model_directory = os.path.join(root, model_weight_folder)

        model_cfg = ModelConfig()
        self.generic_model = MaskRCNN(
            mode="inference", model_dir=model_directory, config=model_cfg
        )

        trained_weight = os.path.join(model_directory, model_weight)

        self.generic_model.load_weights(trained_weight, by_name=True)

        self.generic_model.keras_model._make_predict_function()


    def predict_model(
        self,
        inp_image,
    ):
        with self.graph.as_default():
            K.set_session(self.session)
            results = self.generic_model.detect([inp_image], verbose=1)
        return results
