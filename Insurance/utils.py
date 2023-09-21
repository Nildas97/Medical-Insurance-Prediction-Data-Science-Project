# importing libraries
import pandas as pd
import numpy as np
import os, sys
from Insurance.exception import InsuranceException
from Insurance.logger import logging
from Insurance.config import mongo_client
import yaml
import dill


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


# =======================================Data_Validation=======================================
# defining write_yaml_file function
def write_yaml_file(file_path, data: dict):
    """
    create: yaml file
    data: dictionary
    """
    try:
        # defining the directory
        file_dir = os.path.dirname(file_path)
        # creating the directory
        os.makedirs(file_dir, exist_ok=True)
        # open and dump it in file write
        with open(file_path, "w") as file_write:
            yaml.dump(data, file_write)

    except Exception as e:
        raise InsuranceException(e, sys)


def convert_column_float(df: pd.DataFrame, exclude_columns: list) -> pd.DataFrame:
    """
    convert: column data to float
    return: dataframe
    """
    try:
        for column in df.columns:
            if column not in exclude_columns:
                if df[column].dtypes != "O":
                    df[column] = df[column].astype("float")
        return df
    except Exception as e:
        raise InsuranceException(e, sys)


# =======================================Data_Transformation=======================================


def save_object(file_path: str, obj: object) -> None:
    """
    Save: object
    file_path: str location of file to save
    return: None
    """
    try:
        # creating the directory if exists ignore
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        # open and dump it in file object
        with open(file_path, "wb") as file_obj:
            return dill.dump(obj, file_obj)
    except Exception as e:
        raise InsuranceException(e, sys)


def load_object(file_path: str) -> object:
    """
    load: object
    file_path: str location of file to save
    return: as object to save
    """
    try:
        # checking if the file not available
        if not os.path.exists(file_path):
            raise Exception(f"the file: {file_path} is not available")
        # if the file is available then load the file
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise InsuranceException(e, sys)


def save_numpy_array_data(file_path: str, array: np.array):
    """
    Save numpy array data to file
    file_path: str location of file to save
    return: np.array data to save
    """
    try:
        # defining the directory
        dir_path = os.path.dirname(file_path)
        # creating the directory
        os.makedirs(dir_path, exist_ok=True)
        # open and save it in numpy array
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise InsuranceException(e, sys)


# =======================================Model_Training=======================================
# model trainer for loading the data
def load_numpy_array_data(file_path: str) -> np.array:
    """
    load numpy array data from file
    file_path: str location of file to load
    return: np.array data loaded
    """
    try:
        # opening the file as object in rb mode and return file_object
        # now we wil go to the model_trainer file
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise InsuranceException(e, sys)
