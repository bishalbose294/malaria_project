class AppConstants:
    def login_TableColumns(
        self,
    ):
        return [
            "username",
            "password",
            "patient_id",
        ]

    def patient_TableColumns(
        self,
    ):
        return [
            "name",
            "email",
            "phone_number",
            "age",
            "address",
            "state",
            "pincode",
        ]

    def cell_microscopy_result_TableColumns(
        self,
    ):
        return [
            "patient_id",
            "name_of_image",
            "infected",
            "number_of_rbc",
            "trophozoite",
            "unidentified",
            "ring",
            "schizont",
            "gametocyte",
            "leukocyte",
            "total_infection",
            "result_date",
        ]

    def detection_bbox_TableColumns(
        self,
    ):
        return [
            "image_id",
            "xmin_coord",
            "ymin_coord",
            "xmax_coord",
            "ymax_coord",
            "category",
        ]

    def class_ids(
        self,
    ):
        return {
            "rbc": 1,
            "trophozoite": 2,
            "unidentified": 3,
            "ring": 4,
            "schizont": 5,
            "gametocyte": 6,
            "leukocyte": 7,
        }
