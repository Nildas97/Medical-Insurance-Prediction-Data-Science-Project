# importing libraries
from Insurance.exception import InsuranceException
from Insurance.config import TARGET_COLUMN
from Insurance.logger import logging
from sklearn.metrics import r2_score
from Insurance.utils import *
from Insurance.predictor import ModelResolver
import os, sys
import pandas as pd
import numpy as np
from datetime import datetime


# saving the batch prediction data in a folder
PREDICTION_DIR = "prediction"


# defining the start_batch_prediction function to start batch prediction
def start_batch_prediction(input_file_path):
    """
    Description: Starts batch prediction
    """
    try:
        # creating the prediction folder to
        os.makedirs(PREDICTION_DIR, exist_ok=True)
        logging.info(f"Creating model resolver object")
        # selecting the best model from saved_models folder
        model_resolver = ModelResolver(model_registry="saved_models")
        logging.info(f"Reading file :{input_file_path}")

        # DATA LOADING
        # reading the data
        df = pd.read_csv(input_file_path)
        # handling the null values
        df.replace({"na": np.NAN}, inplace=True)

        # DATA VALIDATION
        # loading the data
        logging.info(f"Loading transformer to transform dataset")
        transformer = load_object(
            file_path=model_resolver.get_latest_transformer_path()
        )
        logging.info(f"Target encoder to convert predicted column into categorical")
        target_encoder = load_object(
            file_path=model_resolver.get_latest_target_encoder_path()
        )

        """We need to create label encoder object for each categorical variable. We will check later"""
        input_features_name = list(transformer.feature_names_in_)
        for i in input_features_name:
            if df[i].dtypes == "object":
                df[i] = target_encoder.fit_transform(df[i])

        # defining input array
        input_arr = transformer.transform(df[input_features_name])

        # defining data for prediction
        logging.info(f"Loading model to make prediction")
        model = load_object(file_path=model_resolver.get_latest_model_path())

        # predict the data
        prediction = model.predict(input_arr)

        df["prediction"] = prediction

        # changing the file format from .csv to .csv with datetime
        prediction_file_name = os.path.basename(input_file_path).replace(
            "csv", f"{datetime.now().strftime('%m%d%Y__%H%M%S')}.csv"
        )

        # creating prediction folder
        prediction_file_name = os.path.join(PREDICTION_DIR, prediction_file_name)

        # converting it into csv file
        df.to_csv(prediction_file_name, index=False, header=True)

        return prediction_file_name

    except Exception as e:
        raise InsuranceException(e, sys)
