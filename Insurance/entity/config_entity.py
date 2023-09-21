# importing libraries
import os, sys
from Insurance.exception import InsuranceException
from Insurance.logger import logging
from datetime import datetime

# file name and file extension name
FILE_NAME = "insurance.csv"
TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"
TRANSFORMER_OBJECT_FILE_NAME = "transformer.pkl"
TARGET_ENCODER_OBJECT_FILE_NAME = "target_encoder.pkl"
MODEL_FILE_NAME = "model.pkl"


# creating training_pipeline_config class
class TrainingPipelineConfig:
    """
    Description: Create folder for storing output data
    """

    # defining init function aka constructor
    def __init__(self):
        try:
            # creating folders based on date and time
            self.artifact_dir = os.path.join(
                os.getcwd(), "artifact", f"{datetime.now().strftime('%m%d%Y__%H%M%S')}"
            )
        except Exception as e:
            raise InsuranceException(e, sys)


# creating data_ingestion_config class
class DataIngestionConfig:
    """
    Description: Create folder for storing base data, train data and test data
    """

    # defining init function aka constructor
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        try:
            # calling the dataset
            self.database_name = "INSURANCE"

            # calling the dataset collection
            self.collection_name = "INSURANCE_PROJECT"

            # creating data_ingestion folder to store all types of data
            self.data_ingestion_dir = os.path.join(
                training_pipeline_config.artifact_dir, "data_ingestion"
            )

            # creating feature store folder inside data_ingestion folder to store base data
            self.feature_store_file_path = os.path.join(
                self.data_ingestion_dir, "feature_store", FILE_NAME
            )

            # creating dataset folder inside data_ingestion folder to store training data
            self.train_file_path = os.path.join(
                self.data_ingestion_dir, "dataset", TRAIN_FILE_NAME
            )

            # creating dataset folder inside data_ingestion folder to store testing data
            self.test_file_path = os.path.join(
                self.data_ingestion_dir, "dataset", TEST_FILE_NAME
            )

            # creating custom test size
            self.test_size = 0.2
        except Exception as e:
            raise InsuranceException(e, sys)

    # converting all data into dictionary format
    def to_dict(self) -> dict:
        try:
            return self.__dict__
        except Exception as e:
            raise InsuranceException(e, sys)


# creating data validation config class
class DataValidationConfig:
    """
    Description: create folder for storing data validation report
    """

    # defining init function aka constructor
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        # creating data validation folder to store data validation report
        self.data_validation_dir = os.path.join(
            training_pipeline_config.artifact_dir, "data_validation"
        )
        # report_file_path from artifact file
        # storing report data inside data validation folder
        self.report_file_path = os.path.join(self.data_validation_dir, "report.yaml")
        # missing threshold
        self.missing_threshold: float = 0.2
        # base_file_path
        self.base_file_path = os.path.join("Insurance.csv")


# creating data transformation class
class DataTransformationConfig:
    """
    Description: create folder for storing data transformation data
    """

    # defining init function aka constructor
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        # creating data transformation folder
        self.data_transformation_dir = os.path.join(
            training_pipeline_config.artifact_dir, "data_transformation"
        )
        # creating transformer folder inside data transformation folder
        self.transform_object_path = os.path.join(
            self.data_transformation_dir, "transformer", TRANSFORMER_OBJECT_FILE_NAME
        )
        # creating transformed folder inside data transformation folder to store train file
        self.transform_train_path = os.path.join(
            self.data_transformation_dir,
            "transformed",
            TRAIN_FILE_NAME.replace("csv", "npz"),
        )
        # creating transformed folder inside data transformation folder to store test file
        self.transform_test_path = os.path.join(
            self.data_transformation_dir,
            "transformed",
            TEST_FILE_NAME.replace("csv", "npz"),
        )
        # creating target encoder folder inside data transformation folder to store target encoder file
        self.target_encoder_path = os.path.join(
            self.data_transformation_dir,
            "target_encoder",
            TARGET_ENCODER_OBJECT_FILE_NAME,
        )


# creating ModelTrainingConfig class
class ModelTrainingConfig:
    """
    Description: creating folder for storing model training data
    """

    # defining init function aka constructor
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        # creating model trainer folder
        self.model_trainer_dir = os.path.join(
            training_pipeline_config.artifact_dir, "model_trainer"
        )
        # creating model folder inside model trainer folder
        self.model_path = os.path.join(self.model_trainer_dir, "model", MODEL_FILE_NAME)

        # setting accuracy
        self.expected_accuracy = 0.7

        # setting threshold for overfitting
        self.overfitting_threshold = 0.3


# creating ModelEvaluationConfig class
class ModelEvaluationConfig:
    """
    Desciption: creating folder for storing model evaluation data
    """

    # defining init function aka constructor
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.change_threshold = 0.01


# creating ModelPusherConfig class
class ModelPusherConfig:
    """
    Description: creating folder for storing model pusher data
    """

    # defining init function aka constructor
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        # creating a model pusher folder
        self.model_pusher_dir = os.path.join(
            training_pipeline_config.artifact_dir, "model_pusher"
        )
        # creating saved_model folder
        self.saved_model_dir = os.path.join("saved_models")
        # creating pusher_model folder
        self.pusher_model_dir = os.path.join(self.model_pusher_dir, "saved_models")
        # saving the model after pushing it
        # see at the DataTransformationConfig section above
        # saving the data after training it
        self.pusher_model_path = os.path.join(self.pusher_model_dir, MODEL_FILE_NAME)
        # saving the transformer data after pushing it
        self.pusher_transformer_path = os.path.join(
            self.pusher_model_dir, TRANSFORMER_OBJECT_FILE_NAME
        )
        # saving the target_encoder data after pushing it
        self.pusher_target_encoder_path = os.path.join(
            self.pusher_model_dir, TARGET_ENCODER_OBJECT_FILE_NAME
        )
