# importing libraries
from Insurance.entity import config_entity, artifact_entity
from Insurance.exception import InsuranceException
from Insurance.config import TARGET_COLUMN
from Insurance.logger import logging
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler
from sklearn.preprocessing import LabelEncoder
from Insurance import utils
import os, sys
import pandas as pd
import numpy as np


# creating data transformation class
class DataTransformation:
    """
    Description: DataTransformation class
    """

    def __init__(
        self,
        data_transformation_config: config_entity.DataTransformationConfig,
        data_ingestion_artifact: artifact_entity.DataIngestionArtifact,
    ):
        try:
            logging.info(f"{'>>'*20} Data Transformation {'<<'*20}")
            self.data_transformation_config = data_transformation_config
            self.data_ingestion_artifact = data_ingestion_artifact

        except Exception as e:
            raise InsuranceException(e, sys)

    @classmethod
    # defining get_data_transformer_object function
    def get_data_transformer_object(cls) -> Pipeline:
        """
        Description: getting data transformation object

        Raises:
            InsuranceException: exception handling

        Returns:
            Pipeline: returns complete transformed data
        """
        try:
            logging.info("imputing missing values using simple imputer")
            simple_imputer = SimpleImputer(strategy="constant", fill_value=0)

            logging.info("detecting outlier using robust scaler")
            robust_scaler = RobustScaler()

            logging.info("defining pipeline using simple imputer and robust scaler")
            pipeline = Pipeline(
                steps=[("Imputer", simple_imputer), ("RobustScaler", robust_scaler)]
            )
            return pipeline
        except Exception as e:
            raise InsuranceException(e, sys)

    # defining initiate_data_transformation function
    def initiate_data_transformation(
        self,
    ) -> artifact_entity.DataTransformationArtifact:
        """
        Description: initiating all the data transformation processes
        Raises:
            InsuranceException: exception handling

        Returns:
            artifact_entity.DataTransformationArtifact: store all processed data
        """
        try:
            logging.info("reading training and testing data from artifact folder")
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            # seperating base data into dependent variable and independent variable
            logging.info(
                "dropping target column from train and test data from config folder"
            )
            # independent variable as input feature
            logging.info("defining input feature")
            input_feature_train_df = train_df.drop(TARGET_COLUMN, axis=1)
            input_feature_test_df = test_df.drop(TARGET_COLUMN, axis=1)

            # dependent variable as target feature
            logging.info("defining target feature")
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_test_df = test_df[TARGET_COLUMN]

            logging.info("data transformation using label encoder")
            label_encoder = LabelEncoder()

            logging.info("transforming target feature data")
            target_feature_train_arr = target_feature_train_df.squeeze()
            target_feature_test_arr = target_feature_test_df.squeeze()

            logging.info("converting categorical data into numerical data")
            for column in input_feature_train_df.columns:
                if input_feature_test_df[column].dtypes == "O":
                    input_feature_train_df[column] = label_encoder.fit_transform(
                        input_feature_train_df[column]
                    )
                    input_feature_test_df[column] = label_encoder.fit_transform(
                        input_feature_test_df[column]
                    )
                else:
                    input_feature_train_df[column] = input_feature_train_df[column]
                    input_feature_test_df[column] = input_feature_test_df[column]

            logging.info("calling original data for fitting the pipeline")
            transformation_pipeline = DataTransformation.get_data_transformer_object()
            transformation_pipeline.fit(input_feature_train_df)

            input_feature_train_arr = transformation_pipeline.transform(
                input_feature_train_df
            )
            input_feature_test_arr = transformation_pipeline.transform(
                input_feature_test_df
            )

            logging.info("converting string data into numpy array")
            train_arr = np.c_[input_feature_train_arr, target_feature_train_arr]
            test_arr = np.c_[input_feature_test_arr, target_feature_test_arr]

            logging.info("saving the transform_train_path")
            utils.save_numpy_array_data(
                file_path=self.data_transformation_config.transform_train_path,
                array=train_arr,
            )

            logging.info("saving the transform_test_path")
            utils.save_numpy_array_data(
                file_path=self.data_transformation_config.transform_test_path,
                array=test_arr,
            )

            logging.info("saving the transform_object_path")
            utils.save_object(
                file_path=self.data_transformation_config.transform_object_path,
                obj=transformation_pipeline,
            )

            logging.info("saving the target_encoder_path")
            utils.save_object(
                file_path=self.data_transformation_config.target_encoder_path,
                obj=label_encoder,
            )

            # saving all the files into artifact
            logging.info("Data transformation artifact: {data_transformation_artifact}")
            data_transformation_artifact = artifact_entity.DataTransformationArtifact(
                transform_object_path=self.data_transformation_config.transform_object_path,
                transform_train_path=self.data_transformation_config.transform_train_path,
                transform_test_path=self.data_transformation_config.transform_test_path,
                target_encoder_path=self.data_transformation_config.target_encoder_path,
            )
            return data_transformation_artifact
        except Exception as e:
            raise InsuranceException(e, sys)
