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

            # creating feature store folder to store base data
            self.feature_store_file_path = os.path.join(
                self.data_ingestion_dir, "feature_store", FILE_NAME
            )

            # creating dataset folder to store training data
            self.train_file_path = os.path.join(
                self.data_ingestion_dir, "dataset", TRAIN_FILE_NAME
            )

            # creating dataset folder to store testing data
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
        # creating transformer folder
        self.transform_object_path = os.path.join(
            self.data_transformation_dir, "transformer", TRANSFORMER_OBJECT_FILE_NAME
        )
        # creating transformed folder to store train file
        self.transform_train_path = os.path.join(
            self.data_transformation_dir,
            "transformed",
            TRAIN_FILE_NAME.replace("csv", "npz"),
        )
        # creating transformed folder to store test file
        self.transform_test_path = os.path.join(
            self.data_transformation_dir,
            "transformed",
            TEST_FILE_NAME.replace("csv", "npz"),
        )
        # creating target encoder folder to store encoder file
        self.target_encoder_path = os.path.join(
            self.data_transformation_dir,
            "target_encoder",
            TARGET_ENCODER_OBJECT_FILE_NAME,
        )
