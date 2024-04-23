from InsurancePremium.entity.config_entity import TrainingPipelineConfig,DataIngestionConfig
from InsurancePremium.components.data_ingestion import DataIngestion
from InsurancePremium.logger.logging import logging
from InsurancePremium.exception import CustomException


def start_training_pipeline():
    logging.info("entred the start_training_pipeline")
    try:
        training_pipeline_config=TrainingPipelineConfig()
        data_ingestion_config  =DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        # print(data_ingestion_config)
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        data_ingestion_artifact = data_ingestion.download_data()
        logging.info("Exited the training pipeline")
    except Exception as e:
        raise CustomException