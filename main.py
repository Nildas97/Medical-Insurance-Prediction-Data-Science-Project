# importing libraries
from Insurance.logger import logging
from Insurance.exception import InsuranceException
import os, sys
from Insurance.utils import get_collection_as_dataframe
from Insurance.entity.config_entity import DataIngestionConfig
from Insurance.entity import config_entity
from Insurance.components.data_ingestion import DataIngestion

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
    except Exception as e:
        print(e)
