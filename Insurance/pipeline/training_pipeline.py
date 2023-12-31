# importing libraries
from Insurance.logger import logging
from Insurance.exception import InsuranceException
from Insurance.utils import get_collection_as_dataframe
import sys, os
from Insurance.entity import config_entity
from Insurance.components.data_ingestion import DataIngestion
from Insurance.components.data_validation import DataValidation
from Insurance.components.data_transformation import DataTransformation
from Insurance.components.model_trainer import ModelTrainer
from Insurance.components.model_evaluation import ModelEvaluation
from Insurance.components.model_pusher import ModelPusher


# defining start_training_pipeline function to start the pipeline
def start_training_pipeline():
    """
    Description: Starts training pipeline
    """
    try:
        training_pipeline_config = config_entity.TrainingPipelineConfig()

        # DATA INGESTION
        # calling data ingestion config
        data_ingestion_config = config_entity.DataIngestionConfig(
            training_pipeline_config=training_pipeline_config
        )
        print(data_ingestion_config.to_dict())
        # calling data ingestion class
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        # calling initiate data ingestion function
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

        # DATA VALIDATION
        data_validation_config = config_entity.DataValidationConfig(
            training_pipeline_config=training_pipeline_config
        )
        data_validation = DataValidation(
            data_validation_config=data_validation_config,
            data_ingestion_artifact=data_ingestion_artifact,
        )
        data_validation_artifact = data_validation.initiate_data_validation()

        # DATA TRANSFORMATION
        data_transformation_config = config_entity.DataTransformationConfig(
            training_pipeline_config=training_pipeline_config
        )
        data_transformation = DataTransformation(
            data_transformation_config=data_transformation_config,
            data_ingestion_artifact=data_ingestion_artifact,
        )
        data_transformation_artifact = (
            data_transformation.initiate_data_transformation()
        )

        # MODEL TRAINER
        model_trainer_config = config_entity.ModelTrainingConfig(
            training_pipeline_config=training_pipeline_config
        )
        model_trainer = ModelTrainer(
            model_trainer_config=model_trainer_config,
            data_transformation_artifact=data_transformation_artifact,
        )
        model_trainer_artifact = model_trainer.initiate_model_trainer()

        # MODEL EVALUATION
        model_evaluation_config = config_entity.ModelEvaluationConfig(
            training_pipeline_config=training_pipeline_config
        )
        model_evaluation = ModelEvaluation(
            model_evaluation_config=model_evaluation_config,
            data_ingestion_artifact=data_ingestion_artifact,
            data_transformation_artifact=data_transformation_artifact,
            model_trainer_artifact=model_trainer_artifact,
        )
        model_evaluation_artifact = model_evaluation.initiate_model_evaluation()

        # MODEL PUSHER
        model_pusher_config = config_entity.ModelPusherConfig(training_pipeline_config)
        model_pusher = ModelPusher(
            model_pusher_config=model_pusher_config,
            data_transformation_artifact=data_transformation_artifact,
            model_trainer_artifact=model_trainer_artifact,
        )
        model_pusher_artifact = model_pusher.initiate_model_pusher()

    except Exception as e:
        raise InsuranceException(e, sys)
