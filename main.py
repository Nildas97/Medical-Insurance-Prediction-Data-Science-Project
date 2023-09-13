# importing libraries
from Insurance.logger import logging
from Insurance.exception import InsuranceException
import os, sys
from Insurance.utils import get_collection_as_dataframe
from Insurance.entity.config_entity import DataIngestionConfig
from Insurance.entity import config_entity
from Insurance.components.data_ingestion import DataIngestion
from Insurance.components.data_validation import DataValidation
from Insurance.components.data_transformation import DataTransformation

# defining the test_logger_and_exception function
# def test_logger_and_exception():
#     """
#     Description:
#         Returns test files of logging and exception

#     Raises:
#         InsuranceException: handling exception
#     """
#     try:
#         logging.debug("Starting point of the test_logger_and_exception")
#         result = 3 / 0
#         print(result)
#         logging.debug("Ending point of the test_logger_and_exception")
#     except Exception as e:
#         logging.debug(str(e))
#         raise InsuranceException(e, sys)


# calling name function
if __name__ == "__main__":
    try:
        # test_logger_and_exception()
        # get_collection_as_dataframe(
        #     database_name="INSURANCE", collection_name="INSURANCE_PROJECT"
        # )

        # TRAINING_PIPELINE_CONFIG
        training_pipeline_config = config_entity.TrainingPipelineConfig()

        # DATA_INGESTION
        # first we will call data_ingestion_config file
        data_ingestion_config = config_entity.DataIngestionConfig(
            training_pipeline_config=training_pipeline_config
        )
        print(data_ingestion_config.to_dict())

        # now defining data_ingestion class
        # it is coming from data_ingestion_config
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)

        # initiating data_ingestion_artifact
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

        # DATA VALIDATION
        # first we will call data_validation_config file
        data_validation_config = config_entity.DataValidationConfig(
            training_pipeline_config=training_pipeline_config
        )
        # now defining data_validation class
        # it is coming from data_validation_config, data is from data_ingestion_artifact
        data_validation = DataValidation(
            data_validation_config=data_validation_config,
            data_ingestion_artifact=data_ingestion_artifact,
        )
        # initiating data_validation_artifact
        data_validation_artifact = data_validation.initiate_data_validation()

        # DATA TRANSFORMATION
        # first we will call data_transformation_config file
        data_transformation_config = config_entity.DataTransformationConfig(
            training_pipeline_config=training_pipeline_config
        )
        # now defining data_transformation class
        # it is coming from data_transformation_config, data is from data_Transformation_artifact
        data_transformation = DataTransformation(
            data_transformation_config=data_transformation_config,
            data_ingestion_artifact=data_ingestion_artifact,
        )
        # initiating data_transformation_artifact
        data_transformation_artifact = (
            data_transformation.initiate_data_transformation()
        )
    except Exception as e:
        print(e)
