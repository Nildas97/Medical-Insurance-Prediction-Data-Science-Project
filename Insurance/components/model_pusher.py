# importing libraries
from Insurance.entity import config_entity, artifact_entity
from Insurance.exception import InsuranceException
from Insurance.config import TARGET_COLUMN
from Insurance.logger import logging
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from Insurance.utils import *
from Insurance.predictor import ModelResolver
from Insurance.entity.artifact_entity import (
    DataTransformationArtifact,
    ModelTrainerArtifact,
    ModelPusherArtifact,
)
from Insurance.entity.config_entity import ModelPusherConfig
import os, sys
import pandas as pd
import numpy as np


class ModelPusher:
    """
    Description: Pushes the model into the production
    """

    def __init__(
        self,
        model_pusher_config: ModelPusherConfig,
        data_transformation_artifact: DataTransformationArtifact,
        model_trainer_artifact: ModelTrainerArtifact,
    ):
        try:
            logging.info(f"{'>>'*20} Model Pusher {'<<'*20}")
            self.model_pusher_config = model_pusher_config
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_artifact = model_trainer_artifact
            self.model_resolver = ModelResolver(
                model_registry=self.model_pusher_config.saved_model_dir
            )
        except Exception as e:
            raise InsuranceException(e, sys)

    def initiate_model_pusher(
        self,
    ) -> ModelPusherArtifact:
        try:
            # loading transformer data, model and target_encoder data
            logging.info(f"Loading transformer model and target encoder")
            transformer = load_object(
                file_path=self.data_transformation_artifact.transform_object_path
            )
            model = load_object(file_path=self.model_trainer_artifact.model_path)
            target_encoder = load_object(
                file_path=self.data_transformation_artifact.target_encoder_path
            )

            # saving the loaded data
            logging.info(f"Saving model into model pusher directory")
            save_object(
                file_path=self.model_pusher_config.pusher_transformer_path,
                obj=transformer,
            )

            save_object(file_path=self.model_pusher_config.pusher_model_path, obj=model)

            save_object(
                file_path=self.model_pusher_config.pusher_target_encoder_path,
                obj=target_encoder,
            )

            # saving the model
            logging.info(f"Saving model in saved model dir")
            transformer_path = self.model_resolver.get_latest_save_transform_path()
            model_path = self.model_resolver.get_latest_save_model_path()
            target_encoder_path = (
                self.model_resolver.get_latest_save_target_encoder_path()
            )

            save_object(file_path=transformer_path, obj=transformer)
            save_object(file_path=model_path, obj=model)
            save_object(file_path=target_encoder_path, obj=target_encoder)

            model_pusher_artifact = ModelPusherArtifact(
                pusher_model_dir=self.model_pusher_config.pusher_model_dir,
                saved_model_dir=self.model_pusher_config.saved_model_dir,
            )
            logging.info(f"Model pusher artifact: {model_pusher_artifact}")
            return model_pusher_artifact
        except Exception as e:
            raise InsuranceException(e, sys)