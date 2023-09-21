# importing libraries
from Insurance.logger import logging
from Insurance.exception import InsuranceException
import os, sys
from Insurance.utils import get_collection_as_dataframe
from Insurance.entity.config_entity import DataIngestionConfig
from Insurance.entity import config_entity
from Insurance.components.data_ingestion import DataIngestion
from Insurance.components.data_validation import DataValidation
from Insurance.components.data_transformation import DataTransformation
from Insurance.components.model_trainer import ModelTrainer
from Insurance.components.model_evaluation import ModelEvaluation
from Insurance.components.model_pusher import ModelPusher


# calling name function
if __name__ == "__main__":
    try:
        # TRAINING_PIPELINE_CONFIG
        training_pipeline_config = config_entity.TrainingPipelineConfig()

        # DATA_INGESTION
        # first we will call data_ingestion_config file
        data_ingestion_config = config_entity.DataIngestionConfig(
            training_pipeline_config=training_pipeline_config
        )
        print(data_ingestion_config.to_dict())

        # now defining data_ingestion class
        # it is coming from data_ingestion_config
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)

        # initiating data_ingestion_artifact
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

        # DATA VALIDATION
        # first we will call data_validation_config file
        data_validation_config = config_entity.DataValidationConfig(
            training_pipeline_config=training_pipeline_config
        )
        # now defining data_validation class
        # it is coming from data_validation_config,
        # data is from data_ingestion_artifact
        data_validation = DataValidation(
            data_validation_config=data_validation_config,
            data_ingestion_artifact=data_ingestion_artifact,
        )
        # initiating data_validation_artifact
        data_validation_artifact = data_validation.initiate_data_validation()

        # DATA TRANSFORMATION
        # first we will call data_transformation_config file
        data_transformation_config = config_entity.DataTransformationConfig(
            training_pipeline_config=training_pipeline_config
        )
        # now defining data_transformation class
        # it is coming from data_transformation_config,
        # data is from data_ingestion_artifact
        data_transformation = DataTransformation(
            data_transformation_config=data_transformation_config,
            data_ingestion_artifact=data_ingestion_artifact,
        )
        # initiating data_transformation_artifact
        data_transformation_artifact = (
            data_transformation.initiate_data_transformation()
        )

        # MODEL TRAINER
        # first we will call model_trainer_config file
        model_trainer_config = config_entity.ModelTrainingConfig(
            training_pipeline_config=training_pipeline_config
        )
        # now defining model_trainer class
        # it is coming from model_trainer_config,
        # data is from data_transformation_artifact
        model_trainer = ModelTrainer(
            model_trainer_config=model_trainer_config,
            data_transformation_artifact=data_transformation_artifact,
        )
        # initiating model_trainer_artifact
        model_trainer_artifact = model_trainer.initiate_model_trainer()

        # MODEL EVALUATION
        # first we will call model_evaluation_config file
        model_evaluation_config = config_entity.ModelEvaluationConfig(
            training_pipeline_config=training_pipeline_config
        )
        # now defining model_evaluation class
        # it is coming from model_evaluation_config,
        # data is from data_ingestion_artifact,
        # data_transformation_artifact and model_trainer_artifact
        model_evaluation = ModelEvaluation(
            model_evaluation_config=model_evaluation_config,
            data_ingestion_artifact=data_ingestion_artifact,
            data_transformation_artifact=data_transformation_artifact,
            model_trainer_artifact=model_trainer_artifact,
        )
        # initiating model_evaluation_artifact
        model_evaluation_artifact = model_evaluation.initiate_model_evaluation()

        # MODEL PUSHER
        # first we will call model_pusher_config file
        model_pusher_config = config_entity.ModelPusherConfig(
            training_pipeline_config=training_pipeline_config
        )
        # now defining model_pusher class
        # it is coming from model_pusher_config,
        # data is from data_transformation_artifact,
        # and model_trainer_artifact
        model_pusher = ModelPusher(
            model_pusher_config=model_pusher_config,
            data_transformation_artifact=data_transformation_artifact,
            model_trainer_artifact=model_trainer_artifact,
        )
        # initiating model_pusher_artifact
        model_pusher_artifact = model_pusher.initiate_model_pusher()

    except Exception as e:
        print(e)
