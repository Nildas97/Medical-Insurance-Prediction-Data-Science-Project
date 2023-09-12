import os, sys
from Insurance.exception import InsuranceException
from Insurance.logger import logging
from datetime import datetime

FILE_NAME = "insurance.csv"
TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"


# creating training_pipeline_config class
class TrainingPipelineConfig:
    """
    Description: Training Pipeline Config file

    """

    # calling init function
    def __init__(self):
        try:
            self.artifact_dir = os.path.join(
                os.getcwd(), "artifact", f"{datetime.now().strftime('%m%d%Y__%H%M%S')}"
            )
        except Exception as e:
            raise InsuranceException(e, sys)


# creating data_ingestion_config class
class DataIngestionConfig:
    """
    Description: Read and divide the data

    divides the data into training, testing and validation data
    """

    # calling init function
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        try:
            # calling the dataset
            self.database_name = "INSURANCE"

            # calling the dataset collection
            self.collection_name = "INSURANCE_PROJECT"

            # creating data_ingestion_directory to call the data
            self.data_ingestion_dir = os.path.join(
                training_pipeline_config.artifact_dir, "data_ingestion"
            )

            # creating feature_store_file_path to store data
            self.feature_store_file_path = os.path.join(
                self.data_ingestion_dir, "feature_store", FILE_NAME
            )

            # creating training_file_path to store training data
            self.train_file_path = os.path.join(
                self.data_ingestion_dir, "dataset", TRAIN_FILE_NAME
            )

            # creating testing_file_path to store testing data
            self.test_file_path = os.path.join(
                self.data_ingestion_dir, "dataset", TEST_FILE_NAME
            )

            # creating custom test size
            self.test_size = 0.2
        except Exception as e:
            raise InsuranceException(e, sys)

    # converting data into dictionary format
    def to_dict(self) -> dict:
        try:
            return self.__dict__
        except Exception as e:
            raise InsuranceException(e, sys)


class DataValidationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.data_validation_dir = os.path.join(
            training_pipeline_config.artifact_dir, "data_validation"
        )
        self.report_file_path = os.path.join(self.data_validation_dir, "report.yaml")
        self.missing_threshold: float = 0.2
        self.base_file_path = os.path.join("Insurance.csv")
