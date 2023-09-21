# importing libraries
from typing import Optional
from Insurance.exception import InsuranceException
from Insurance.logger import logging
from Insurance.entity.config_entity import (
    TRANSFORMER_OBJECT_FILE_NAME,
    TARGET_ENCODER_OBJECT_FILE_NAME,
    MODEL_FILE_NAME,
)
import os, sys


# creating model resolver class
class ModelResolver:
    """
    Description: stores data of current model to compare with previous model
    """

    # defining init function aka constructor
    def __init__(
        self,
        # creating save_models folder, to compare old model with new model
        model_registry: str = "saved_models",
        # creating transformer folder to store transform data
        transformer_dir_name="transformer",
        # creating target_encoder folder to store encoder data
        target_encoder_dir_name="target_encoder",
        # creating model folder to store model data
        model_dir_name="model",
    ):
        self.model_registry = model_registry
        os.makedirs(self.model_registry, exist_ok=True)
        self.transformer_dir_name = transformer_dir_name
        self.target_encoder_dir_name = target_encoder_dir_name
        self.model_dir_name = model_dir_name

    # defining latest_directory function for saving new saved model
    def get_latest_dir_path(self) -> Optional[str]:
        try:
            # defining model_registry
            dir_name = os.listdir(self.model_registry)
            # checking length wise directory name if available
            if len(dir_name) == 0:
                return None
            # creating new saved_model folder
            # saving new saved_model everytime it runs
            dir_name = list(map(int, dir_name))
            latest_dir_name = max(dir_name)
            return os.path.join(self.model_registry, f"{latest_dir_name}")
        except Exception as e:
            raise InsuranceException(e, sys)

    # defining get_latest_model_path function
    def get_latest_model_path(self):
        try:
            # calling latest_directory
            latest_dir = self.get_latest_dir_path()
            # if it doesnot exists return None
            if latest_dir is None:
                raise Exception("Model is not available")
            # returns model_file folder inside latest folder
            return os.path.join(
                latest_dir,
                self.model_dir_name,
                MODEL_FILE_NAME,
            )
        except Exception as e:
            raise InsuranceException(e, sys)

    # defining get_latest_transformer_path function
    def get_latest_transformer_path(self):
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir is None:
                raise Exception("Transform data is not available")
            return os.path.join(
                latest_dir,
                self.transformer_dir_name,
                TRANSFORMER_OBJECT_FILE_NAME,
            )
        except Exception as e:
            raise InsuranceException(e, sys)

    # defining get_latest_target_encoder_path function
    def get_latest_target_encoder_path(self):
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir is None:
                raise Exception("Target encoder data is not available")
            return os.path.join(
                latest_dir,
                self.target_encoder_dir_name,
                TARGET_ENCODER_OBJECT_FILE_NAME,
            )
        except Exception as e:
            raise InsuranceException(e, sys)

    #
    def get_latest_save_dir_path(self) -> str:
        try:
            # calling latest directory
            latest_dir = self.get_latest_dir_path()
            # if it doesnot exists
            if latest_dir is None:
                # create one folder inside
                return os.path.join(self.model_registry, f"{0}")
            latest_dir_num = int(os.path.basename(self.get_latest_dir_path()))
            return os.path.join(self.model_registry, f"{latest_dir_num + 1}")
        except Exception as e:
            raise InsuranceException(e, sys)

    def get_latest_save_model_path(self):
        try:
            # checking the latest save directory path available or not
            latest_dir = self.get_latest_save_dir_path()
            return os.path.join(latest_dir, self.model_dir_name, MODEL_FILE_NAME)
        except Exception as e:
            raise InsuranceException(e, sys)

    def get_latest_save_transform_path(self):
        try:
            # checking the latest save directory path available or not
            latest_dir = self.get_latest_save_dir_path()
            return os.path.join(
                latest_dir, self.transformer_dir_name, TRANSFORMER_OBJECT_FILE_NAME
            )
        except Exception as e:
            raise InsuranceException(e, sys)

    def get_latest_save_target_encoder_path(self):
        try:
            # checking the latest save directory path available or not
            latest_dir = self.get_latest_save_dir_path()
            return os.path.join(
                latest_dir,
                self.target_encoder_dir_name,
                TARGET_ENCODER_OBJECT_FILE_NAME,
            )
        except Exception as e:
            raise InsuranceException(e, sys)
