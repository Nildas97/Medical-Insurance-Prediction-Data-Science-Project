# importing libraries
import pandas as pd
import pandas as pd
import numpy as np
import os, sys
from Insurance.entity.config_entity import DataIngestionConfig
from Insurance.entity.artifact_entity import DataIngestionArtifact
from Insurance.entity import artifact_entity
from Insurance.entity import config_entity
from Insurance.exception import InsuranceException
from Insurance.logger import logging
from Insurance import utils
from sklearn.model_selection import train_test_split


# creating DataIngestion class
class DataIngestion:
    # defining init function to call data_ingestion_config from config_entity file
    def __init__(self, data_ingestion_config: config_entity.DataIngestionConfig):
        try:
            logging.info(f"{'>>'*20} Data Validation {'<<'*20}")
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise InsuranceException(e, sys)

    # defining initiate_data_ingestion function
    def initiate_data_ingestion(self) -> artifact_entity.DataIngestionArtifact:
        try:
            # fetching the data from get_collection_as_dataframe class in dataframe format
            logging.info(f"Export collection data as pandas dataframe")
            df: pd.DataFrame = utils.get_collection_as_dataframe(
                database_name=self.data_ingestion_config.database_name,
                collection_name=self.data_ingestion_config.collection_name,
            )
            logging.info("Save data in feature store")
            # replacing na with NAN
            df.replace(to_replace="na", value=np.NAN, inplace=True)

            # save dataframe df in feature store folder/directory
            logging.info("Create feature store folder if not available")
            feature_store_dir = os.path.dirname(
                self.data_ingestion_config.feature_store_file_path
            )
            # create feature_store_directory if exists skip the section
            os.makedirs(feature_store_dir, exist_ok=True)

            # saving the dataframe df in csv format taken from feature_store_path
            logging.info("Save df to feature store folder")
            df.to_csv(
                path_or_buf=self.data_ingestion_config.feature_store_file_path,
                index=False,
                header=True,
            )

            # dividing the data into train set and test set
            logging.info("Splitting the data into train and test set")
            train_df, test_df = train_test_split(
                df, test_size=self.data_ingestion_config.test_size, random_state=1
            )

            # Create dataset directory folder if not exists
            logging.info("Create dataset directory folder if not exists")
            dataset_dir = os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dataset_dir, exist_ok=True)

            # train and test data are saved to feature store folder
            logging.info("Saving dataset to feature store folder")
            train_df.to_csv(
                path_or_buf=self.data_ingestion_config.train_file_path,
                index=False,
                header=True,
            )
            logging.info("Saving test dataset to feature store folder")
            test_df.to_csv(
                path_or_buf=self.data_ingestion_config.test_file_path,
                index=False,
                header=True,
            )

            # prepare artifact folder
            data_ingestion_artifact = artifact_entity.DataIngestionArtifact(
                feature_store_file_path=self.data_ingestion_config.feature_store_file_path,
                train_file_path=self.data_ingestion_config.train_file_path,
                test_file_path=self.data_ingestion_config.test_file_path,
            )
            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")

            return data_ingestion_artifact
        except Exception as e:
            raise InsuranceException(e, sys)
