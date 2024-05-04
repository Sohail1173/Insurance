import os,sys
from InsurancePremium.exception import CustomException
from InsurancePremium.logger import logging
from datetime import datetime

FILE_NAME = "insurance.csv"
TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"
TRANSFORMER_OBJECT_FILE_NAME = "transformer.pkl"
TARGET_ENCODER_OBJECT_FILE_NAME = "target_encoder.pkl"
MODEL_FILE_NAME = "model.pkl"

class TrainingPipelineConfig:
    
    def __init__(self):
        try:
            self.artifact_dir = os.path.join(os.getcwd(),"artifact",f"{datetime.now().strftime('%m%d%Y__%H%M%S')}")
        except Exception  as e:
            raise CustomException(e,sys)    


class DataIngestionConfig:
    
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.data_file_name="data.zip"
            self.data_download_url=r"https://drive.google.com/file/d/1fcpUvif1mxJ7vBASIVR_oro1g1LupPEB/view?usp=sharing"
            self.prefix="https://drive.google.com/uc?/export=download&id="
            self.data_ingestion_dir = os.path.join(training_pipeline_config.artifact_dir , "data_ingestion")
            self.feature_store_file_path = os.path.join(self.data_ingestion_dir,"feature_store")
            self.train_file_path = os.path.join(self.data_ingestion_dir,"dataset",TRAIN_FILE_NAME)
            self.test_file_path = os.path.join(self.data_ingestion_dir,"dataset",TEST_FILE_NAME)
            self.test_size = 0.2
            self.data_set_dir=os.path.join(self.data_ingestion_dir,"dataset")
            
        except Exception  as e:
            raise CustomException(e,sys)  


    def to_dict(self,)->dict:
        try:
            return self.__dict__
        except Exception  as e:
            raise CustomException(e,sys)  
        
   


class DataValidationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_validation_dir=os.path.join(training_pipeline_config.artifact_dir,
                                              "data_validation")
        self.report_file_path=os.path.join(self.data_validation_dir,"report.yaml")
        self.base_file_path=os.path.join("insurance.csv")
        self.missing_threshold:float=0.2
class DataTransformationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):

        self.data_transformation_dir=os.path.join(training_pipeline_config.artifact_dir,"data_transformation")
        self.data_transformation_object_path=os.path.join(self.data_transformation_dir,"transformed",TRANSFORMER_OBJECT_FILE_NAME)
        self.transform_train_path=os.path.join(self.data_transformation_dir,"transformed",TRAIN_FILE_NAME.replace("csv","npz"))
        self.transform_test_path=os.path.join(self.data_transformation_dir,"transformed",TEST_FILE_NAME.replace("csv","npz"))
        self.target_encoder_path=os.path.join(self.data_transformation_dir,"target_encoder",TARGET_ENCODER_OBJECT_FILE_NAME)
        
class ModelTrainerConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.model_trainer_dir=os.path.join(training_pipeline_config.artifact_dir
                                            ,"model_trainer")
        self.model_path=os.path.join(self.model_trainer_dir,"model",MODEL_FILE_NAME)
        self.expected_score=0.7
        self.overfitting_threshold=0.3


class ModelEvaluationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.change_threshold=0.01