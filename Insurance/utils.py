# importing libraries
import pandas as pd
import numpy as np
import os, sys
from Insurance.exception import InsuranceException
from Insurance.logger import logging
from Insurance.config import mongo_client
import yaml


# defining get_collection_as_dataframe function
def get_collection_as_dataframe(
    database_name: str, collection_name: str
) -> pd.DataFrame:
    """
    Description:
        Returns collection as dataframe
    Args:
        database_name (str): database name
        collection_name (str): database folder name

    Raises:
        InsuranceException: exception handling

    Returns:
        df: Pandas dataframe of a collection
    """
    try:
        # reading the data from database
        logging.info(
            f"Reading data from database: {database_name} and collection: {collection_name}"
        )

        # creating dataframe by fetching data from mongo_client
        df = pd.DataFrame(list(mongo_client[database_name][collection_name].find()))

        # displaying total columns
        logging.info(f"Found columns: {df.columns}")

        if "_id" in df.columns:
            # dropping _id column from dataset
            logging.info("Dropping columns: _id")
            df = df.drop("_id", axis=1)

        # displaying total rows and columns
        logging.info(f"Rows and columns in df: {df.shape}")
        return df
    except Exception as e:
        raise InsuranceException(e, sys)


def write_yaml_file(file_path, data: dict):
    try:
        file_dir = os.path.dirname(file_path)
        os.makedirs(file_dir, exist_ok=True)
        with open(file_path, "w") as file_write:
            yaml.dump(data, file_write)

    except Exception as e:
        raise InsuranceException(e, sys)


def convert_column_float(df: pd.DataFrame, exclude_columns: list) -> pd.DataFrame:
    try:
        for column in df.columns:
            if column not in exclude_columns:
                if df[column].dtypes != "O":
                    df[column] = df[column].astype("float")
        return df
    except Exception as e:
        raise InsuranceException(e, sys)
