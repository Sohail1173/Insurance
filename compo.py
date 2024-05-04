from datetime import datetime
class TrainingPipelineConfig:
    def __init__(self):
        self.artifact_dir=os.path.join(os.getcwd(),"artifact",f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}")

class DataIngestionConfig:
    
    def __init__(self,train_pipeline_cofig:TrainingPipelineConfig):

        self.artifact_dir=train_pipeline_cofig.artifact_dir
        self.data_ingestion_dir=os.path.join(self.artifact_dir,"data_ingestion")
        self.feature_store_file_path=os.path.join(self.data_ingestion_dir,"feature_store")
        

class DataIngestion:
    def __init__(self,data_ingestion_config=DataIngestionConfig):
        self.data_ingestion_config=data_ingestion_config

        data_download_url=self.data_ingestion_config.download_url
        zip_file_name=self.data_ingestion_config.zip_field


def start_training_pipeline():
    training_pipeline_config=TrainingPipelineConfig()
    data
    
                                                  