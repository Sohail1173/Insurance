from InsurancePremium.entity.config_entity import TrainingPipelineConfig,DataIngestionConfig,DataValidationConfig,DataTransformationConfig,ModelTrainerConfig, \
ModelEvaluationConfig
from InsurancePremium.components.data_ingestion import DataIngestion
from InsurancePremium.logger.logging import logging
from InsurancePremium.exception import CustomException
from InsurancePremium.components.data_validation import DataValidation
from InsurancePremium.components.data_transformation import DataTransformation
from InsurancePremium.components.model_trainer import ModelTrainer
from InsurancePremium.components.model_evaluation import ModelEvaluation
import os,sys


def start_training_pipeline():
    logging.info("entred the start_training_pipeline")
    try:
        training_pipeline_config=TrainingPipelineConfig()
        
        data_ingestion_config  =DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        # print(data_ingestion_config)
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        data_ingestion_artifact = data_ingestion.download_data()
        # data validation
        data_validation_config =DataValidationConfig(training_pipeline_config=training_pipeline_config)
        data_validation=DataValidation(data_validation_config=data_validation_config,
        
        data_ingestion_artifact=data_ingestion_artifact)
        data_validation_artifact=data_validation.initiate_data_validation()

        data_transformation_config =DataTransformationConfig(training_pipeline_config=training_pipeline_config)
        data_transformation=DataTransformation(data_transformation_config=data_transformation_config,
        data_ingestion_artifact=data_ingestion_artifact)
        data_transformation_artifact=data_transformation.initiate_data_transformation()
        

        model_trainer_config=ModelTrainerConfig(training_pipeline_config=training_pipeline_config)
        model_trainer=ModelTrainer(model_trainer_config=model_trainer_config,
        data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact=model_trainer.initiate_model_trainer()
        logging.info("Exited the training pipeline")


        model_evaluation_config=ModelEvaluationConfig(training_pipeline_config=training_pipeline_config)
        model_eval=ModelEvaluation(model_evaluation_config=model_evaluation_config,
        data_ingestion_artifact=data_ingestion_artifact,
        data_transformation_artifact=data_transformation_artifact,
        model_trainer_artifact=model_trainer_artifact)
        model_eval_artifact=model_eval.inititate_model_evaluation()
    except Exception as e:
        raise CustomException(e,sys)