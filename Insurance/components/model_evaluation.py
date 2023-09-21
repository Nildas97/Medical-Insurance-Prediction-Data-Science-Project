# importing libraries
from Insurance.entity import config_entity, artifact_entity
from Insurance.exception import InsuranceException
from Insurance.config import TARGET_COLUMN
from Insurance.logger import logging
from sklearn.metrics import r2_score
from Insurance.utils import *
from Insurance.predictor import ModelResolver
import os, sys
import pandas as pd
import numpy as np


class ModelEvaluation:
    """
    Description: Evaluates the previous model with current model
    """

    def __init__(
        self,
        model_evaluation_config: config_entity.ModelEvaluationConfig,
        data_ingestion_artifact: artifact_entity.DataIngestionArtifact,
        data_transformation_artifact: artifact_entity.DataTransformationArtifact,
        model_trainer_artifact: artifact_entity.ModelTrainerArtifact,
    ):
        try:
            logging.info(f"{'>>'*20}  Model Evaluation {'<<'*20}")
            self.model_evaluation_config = model_evaluation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_artifact = model_trainer_artifact
            self.model_resolver = ModelResolver()
        except Exception as e:
            raise InsuranceException(e, sys)

    def initiate_model_evaluation(self) -> artifact_entity.ModelEvaluationArtifact:
        try:
            logging.info(
                "if saved model folder has model the we will compare "
                "which model is best trained or the model from saved model folder"
            )
            latest_dir_path = self.model_resolver.get_latest_dir_path()
            # if the latest model is not available
            # means the new model accuracy is not greater than old model
            # that is why latest directory is not created, so no new folder created
            if latest_dir_path == None:
                # here in the model evaluation artifact model is accepted but not improved accuracy
                model_evaluation_artifact = artifact_entity.ModelEvaluationArtifact(
                    is_model_accepted=True, improved_accuracy=None
                )
                logging.info(f"Model evaluation artifact: {model_evaluation_artifact}")

                return model_evaluation_artifact

            # comparing previous model accuracy and new model accuracy
            # previous model data
            logging.info("Finding location of transformer, model and target encoder")
            transformer_path = self.model_resolver.get_latest_transformer_path()
            model_path = self.model_resolver.get_latest_model_path()
            target_encoder_path = self.model_resolver.get_latest_target_encoder_path()

            # loading the previous model
            logging.info(
                "Previous trained objects of transformer, model and target encoder"
            )
            transformer = load_object(file_path=transformer_path)
            model = load_object(file_path=model_path)
            target_encoder = load_object(file_path=target_encoder_path)

            # new model data
            logging.info("Currently trained model objects")
            current_transformer = load_object(
                file_path=self.data_transformation_artifact.transform_object_path
            )
            current_model = load_object(
                file_path=self.model_trainer_artifact.model_path
            )
            current_target_encoder = load_object(
                file_path=self.data_transformation_artifact.target_encoder_path
            )

            # comparing will be done on the test data
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            # removing target column to create dependent and independent data
            target_df = test_df[TARGET_COLUMN]
            # define y_true as target_df
            y_true = target_df

            # converting categorical data into numerical data
            """We need to create label encoder object for each categorical variable. We will check later"""
            input_features_name = list(transformer.feature_names_in_)

            for i in input_features_name:
                # if there is any data having object datatypes
                if test_df[i].dtypes == "object":
                    # fit and transform test_df data using target_encoder
                    test_df[i] = target_encoder.fit_transform(test_df[i])

            # transforming input features
            input_arr = transformer.transform(test_df[input_features_name])
            # predict the model
            y_pred = model.predict(input_arr)
            print(f"Prediction using previous model: {y_pred[:5]}")

            # previous model score
            previous_model_score = r2_score(y_true=y_true, y_pred=y_pred)
            logging.info(
                f"Accuracy using previous trained model: {previous_model_score}"
            )

            # checking accuracy of current model
            input_features_name = list(current_transformer.feature_names_in_)

            # transforming input features
            input_arr = current_transformer.transform(test_df[input_features_name])
            # predict the model
            y_pred = current_model.predict(input_arr)
            # defining target_df
            y_true = target_df
            print(f"Prediction using trained model: {y_pred[:5]}")

            # current_model_score
            current_model_score = r2_score(y_true=y_true, y_pred=y_pred)
            logging.info(f"Accuracy using current trained model: {current_model_score}")

            # final comparison between both model
            if current_model_score <= previous_model_score:
                logging.info("Current trained model is not better than previous model")
                raise Exception("Current model is not better than previous model")

            model_evaluation_artifact = artifact_entity.ModelEvaluationArtifact(
                is_model_accepted=True,
                improved_accuracy=current_model_score - previous_model_score,
            )
            logging.info(f"Model eval artifact: {model_evaluation_artifact}")
            return model_evaluation_artifact
        except Exception as e:
            raise InsuranceException(e, sys)
