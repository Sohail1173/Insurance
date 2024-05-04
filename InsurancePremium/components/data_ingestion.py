from InsurancePremium.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig
from InsurancePremium.constants.training_pipeline import *
from sklearn.model_selection import  train_test_split
from InsurancePremium.constants.training_pipeline import *
from InsurancePremium.exception import CustomException
from InsurancePremium.logger.logging import logging
from InsurancePremium.entity.artifact_entity import DataIngestionArtifact
import gdown,zipfile
import pandas as pd
import sys

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
       
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise e
    
    def download_data(self):
        logging.info("Entered the download_data method")

        try:
            data_url=self.data_ingestion_config.data_download_url
            logging.info("got the data url")
            data_download_dir=self.data_ingestion_config.data_ingestion_dir
            zip_file_name=self.data_ingestion_config.data_file_name
            os.makedirs(data_download_dir, exist_ok=True)
            logging.info("created the data download directory")
            file_id=data_url.split("/")[-2]
            pre=self.data_ingestion_config.prefix
            data_file=f"{data_download_dir}/{zip_file_name}"
            logging.info(f"downloading the data from {data_url} to {data_download_dir}")
            gdown.download(pre+file_id,data_file)
            logging.info("data download successful")
            feature_store=self.data_ingestion_config.feature_store_file_path
            print(feature_store)
            os.makedirs(feature_store,exist_ok=True)
            logging.info("extracting  the data from zip file")
            with zipfile.ZipFile(data_file,"r") as file:
                data=file.extractall(feature_store)

                logging.info("data extracted")
            df=pd.read_csv(f"{feature_store}/insurance.csv")
            
            train_df,test_df=train_test_split(df,test_size=self.data_ingestion_config.test_size
                                              ,random_state=42)
            logging.info("Data divided into train and test")
            data_dir=self.data_ingestion_config.data_set_dir
            os.makedirs(data_dir,exist_ok=True)

            train_df.to_csv(self.data_ingestion_config.train_file_path,index=False,header=True)
            test_df.to_csv(self.data_ingestion_config.test_file_path,index=False,header=True)
            os.remove(data_file)
            logging.info("got the train.csv and test.csv file successfully")
            data_ingestion_artifact=DataIngestionArtifact(
                feature_store_file_path=self.data_ingestion_config.feature_store_file_path,
                train_file_path=self.data_ingestion_config.train_file_path,
                test_file_path=self.data_ingestion_config.test_file_path)
            logging.info(f"Data Ingestion Artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact
            
        except Exception as e:
            raise e