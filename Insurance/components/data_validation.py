# importing libraries
from Insurance.entity import artifact_entity, config_entity
from Insurance.logger import logging
from Insurance.exception import InsuranceException
from typing import Optional
import os, sys
import pandas as pd
import numpy as np
from scipy.stats import ks_2samp
from Insurance.config import TARGET_COLUMN
from Insurance import utils


# creating data validation class
class DataValidation:
    """
    Description:
    """

    # defining constructor
    def __init__(
        self,
        data_validation_config: config_entity.DataValidationConfig,
        data_ingestion_artifact: artifact_entity.DataValidationArtifact,
    ):
        try:
            # logging.info(f"----------Data Validation----------")
            logging.info(f"{'>>'*20} Data Validation {'<<'*20}")
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.validation_error = dict()
        except Exception as e:
            raise InsuranceException(e, sys)

    # defining missing values function
    def drop_missing_value_columns(
        self, df: pd.DataFrame, report_key_name: str
    ) -> Optional[pd.DataFrame]:
        try:
            # setting the missing values threshold limit
            threshold = self.data_validation_config.missing_threshold

            # creating a null report
            null_report = df.isna().sum() / df.shape[0]
            logging.info(
                f"selecting column name which contains null above to {threshold}"
            )
            # dropping columns if null report is greater than threshold
            drop_columns_names = null_report[null_report > threshold].index
            logging.info(f"Columns to drop: {list(drop_columns_names)}")

            # getting the list of dropped column names
            self.validation_error[report_key_name] = list(drop_columns_names)

            # drop columns
            df.drop(list(drop_columns_names), axis=1, inplace=True)

            # if length of data columns has 0 null values
            if len(df.columns) == 0:
                return None
            return df

        except Exception as e:
            raise InsuranceException(e, sys)

    # defining is required columns exists or not
    def is_required_columns_exists(
        self, base_df: pd.DataFrame, current_df: pd.DataFrame, report_key_name: str
    ) -> bool:
        try:
            # base columns
            base_columns = base_df.columns
            # current columns
            current_columns = current_df.columns
            # missing columns
            missing_columns = []

            for base_column in base_columns:
                if base_column not in current_columns:
                    # logging.info(f"Columns: [{base} is not available]")
                    missing_columns.append(base_column)

                if len(missing_columns) > 0:
                    self.validation_error[report_key_name] = missing_columns
                    return False
                return True

        except Exception as e:
            raise InsuranceException(e, sys)

    # defining
    def data_drift(
        self, base_df: pd.DataFrame, current_df: pd.DataFrame, report_key_name: str
    ):
        try:
            drift_report = dict()
            base_columns = base_df.columns
            current_columns = current_df.columns

            for base_column in base_columns:
                base_data, current_data = (
                    base_df[base_column],
                    current_df[base_column],
                )

                same_distribution = ks_2samp(base_data, current_data)

                if same_distribution.pvalue > 0.05:
                    # null hypothesis accepts
                    drift_report[base_column] = {
                        "pvalues": float(same_distribution.pvalue),
                        "same_distribution": True,
                    }
                else:
                    drift_report[base_column] = {
                        "pvalues": float(same_distribution.pvalue),
                        "same_distribution": False,
                    }
            self.validation_error[report_key_name] = drift_report

        except Exception as e:
            raise InsuranceException(e, sys)

    def initiate_data_validation(self) -> artifact_entity.DataValidationArtifact:
        try:
            logging.info(f"Reading base dataframe")
            base_df = pd.read_csv(self.data_validation_config.base_file_path)

            logging.info(f"Replace na value in base df")
            base_df.replace({"na": np.NAN}, inplace=True)

            logging.info(f"Drop null values columns from base df")
            base_df = self.drop_missing_value_columns(
                df=base_df, report_key_name="Missing_values_within_base_dataset"
            )

            logging.info(f"Reading train dataframe")
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)

            logging.info(f"Reading test dataframe")
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            logging.info(f"Dropping missing values from train dataframe")
            train_df = self.drop_missing_value_columns(
                df=train_df, report_key_name="Missing_values_within_train_dataset"
            )

            logging.info(f"Dropping missing values from test dataframe")
            test_df = self.drop_missing_value_columns(
                df=test_df, report_key_name="Missing_values_within_test_dataset"
            )

            exclude_columns = [TARGET_COLUMN]
            logging.info(f"Converting object columns to float in base dataframe")
            base_df = utils.convert_column_float(
                df=base_df, exclude_columns=exclude_columns
            )

            logging.info(f"Converting object columns to float in train dataframe")
            train_df = utils.convert_column_float(
                df=train_df, exclude_columns=exclude_columns
            )

            logging.info(f"Converting object columns to float in test dataframe")
            test_df = utils.convert_column_float(
                df=test_df, exclude_columns=exclude_columns
            )

            logging.info(f"Is all required columns present in train df")
            train_df_columns_status = self.is_required_columns_exists(
                base_df=base_df,
                current_df=train_df,
                report_key_name="Missing_columns_within_train_dataset",
            )

            logging.info(f"Is all required columns present in test df")
            test_df_columns_status = self.is_required_columns_exists(
                base_df=base_df,
                current_df=test_df,
                report_key_name="Missing_columns_within_train_dataset",
            )

            if train_df_columns_status:
                logging.info(
                    f"As all column are available in train df hence detecting data drift"
                )
                self.data_drift(
                    base_df=base_df,
                    current_df=train_df,
                    report_key_name="data_drift_within_train_dataset",
                )

            if test_df_columns_status:
                logging.info(
                    f"As all column are available in train df hence detecting data drift"
                )
                self.data_drift(
                    base_df=base_df,
                    current_df=test_df,
                    report_key_name="data_drift_within_test_dataset",
                )

            # write your report
            logging.info("Write report in yaml file")
            utils.write_yaml_file(
                file_path=self.data_validation_config.report_file_path,
                data=self.validation_error,
            )

            data_validation_artifact = artifact_entity.DataValidationArtifact(
                report_file_path=self.data_validation_config.report_file_path
            )
            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise InsuranceException(e, sys)
