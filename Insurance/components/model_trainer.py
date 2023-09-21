# importing libraries
from Insurance.entity import config_entity, artifact_entity
from Insurance.exception import InsuranceException
from Insurance.config import TARGET_COLUMN
from Insurance.logger import logging
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from Insurance import utils
import os, sys
import pandas as pd
import numpy as np


# creating model trainer class
class ModelTrainer:
    """
    Description: Trains the model
    """

    # defining the init function aka the constructor
    # calling configurations from model_trainer_config
    # calling data from data_transformation_artifact
    def __init__(
        self,
        model_trainer_config: config_entity.ModelTrainingConfig,
        data_transformation_artifact: artifact_entity.DataTransformationArtifact,
    ):
        try:
            # defining model trainer config and data transformation artifact
            logging.info(f"{'>>'*20} Model Trainer {'<<'*20}")
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise InsuranceException(e, sys)

    # defining train model function
    def train_model(self, x, y):
        try:
            # defining the model, i.e. linear regression model
            lr = LinearRegression()
            # fitting the model
            lr.fit(x, y)
            return lr
        except Exception as e:
            raise InsuranceException(e, sys)

    # defining the initiate model trainer function
    def initiate_model_trainer(self) -> artifact_entity.ModelTrainerArtifact:
        try:
            # loading the transform train data from data transformation artifact
            logging.info("Loading transform train data and transform test data")
            train_arr = utils.load_numpy_array_data(
                file_path=self.data_transformation_artifact.transform_train_path
            )
            # loading the transform test data from data transformation artifact
            test_arr = utils.load_numpy_array_data(
                file_path=self.data_transformation_artifact.transform_test_path
            )

            # for x_train and x_test all data except target column
            # for y_train and y_test just target column
            logging.info(
                "Splitting input and target feature from both train and test data"
            )
            # splitting the data into x_train & y_train
            x_train, y_train = train_arr[:, :-1], train_arr[:, -1]

            # splitting the data into x_test & y_test
            x_test, y_test = test_arr[:, :-1], test_arr[:, -1]

            # defining the model
            logging.info("Train the model")
            model = self.train_model(x=x_train, y=y_train)

            # calculating f1 train score
            logging.info("Calculating f1 train score")
            yhat_train = model.predict(x_train)

            # calculating r2 score on x_train data
            r2_train_score = r2_score(y_true=y_train, y_pred=yhat_train)

            # calculating f1 test score
            logging.info("Calculating f1 test score")
            yhat_test = model.predict(x_test)

            # calculating r2 score on x_test data
            r2_test_score = r2_score(y_true=y_test, y_pred=yhat_test)

            logging.info(
                f"train score:{r2_train_score} and tests score {r2_test_score}"
            )

            # now we need to check whether it is overfitting or underfitting
            # setting the threshold for accuracy
            logging.info("Checking if our model is underfitting or not")
            if r2_test_score < self.model_trainer_config.expected_accuracy:
                raise Exception(
                    f"Model is not giving expected accuracy expected_accuracy: {self.model_trainer_config.expected_accuracy}: model_actual_score: {r2_test_score}"
                )

            # checking the difference between r2_train_score and r2_test_score
            logging.info("Checking if our model is overfitting or not")
            diff = abs(r2_train_score - r2_test_score)

            # setting the threshold for overfitting
            if diff > self.model_trainer_config.overfitting_threshold:
                raise Exception(
                    f"Train model and Test model difference: {diff} is more than overfitting threshold: {self.model_trainer_config.overfitting_threshold}"
                )
            # saving the model
            logging.info("Saving model object")
            utils.save_object(file_path=self.model_trainer_config.model_path, obj=model)

            # model_trainer_artifact
            model_trainer_artifact = artifact_entity.ModelTrainerArtifact(
                model_path=self.model_trainer_config.model_path,
                r2_train_score=r2_train_score,
                r2_test_score=r2_test_score,
            )
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise InsuranceException(e, sys)
