from InsurancePremium.entity.config_entity import DataIngestionConfig,DataValidationConfig
from InsurancePremium.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from InsurancePremium.exception import CustomException
from InsurancePremium.logger.logging import logging
from scipy.stats import ks_2samp
from typing import Optional
import os,sys
import pandas as pd
import numpy as np
from InsurancePremium.config import TARGET_COLUMN
from InsurancePremium import utils

class DataValidation:

    def __init__(self,data_validation_config:DataValidationConfig,
                data_ingestion_artifact:DataIngestionArtifact):
        try:
            logging.info("DataValidation")
            self.data_validation_config=data_validation_config
            self.data_ingestion_artifact=data_ingestion_artifact
            self.validation_error=dict()
        except Exception as e:
            raise CustomException(e,sys)
        
   

    def drop_missing_values_columns(self,df:pd.DataFrame,report_key_name:str)->Optional[pd.DataFrame]:
        try:
            threshold=self.data_validation_config.missing_threshold
            null_report=df.isna().sum()/df.shape[0]
            logging.info(f"selecting coumn name which contains null above to {threshold}")
            drop_column_names=null_report[null_report>threshold].index
            logging.info(f"column to drop :{list(drop_column_names)}")
            self.validation_error[report_key_name]=list(drop_column_names)
            df.drop(list(drop_column_names),axis=1,inplace=True)

            if len(df.columns)==0:
                return None
            return df
        
        except  Exception as e:
            raise CustomException(e,sys)
 
    def is_required_columns_exists(self,base_df:pd.DataFrame,
                                  current_df:pd.DataFrame,report_key_name:str)->bool:
        try:
            base_columns=base_df.columns
            current_columns=current_df.columns
            missing_columns=[]
            for base_column in base_columns:
                if base_column not in current_columns:
                    logging.info(f"Column:[{base_column} is not available]")
                    missing_columns.append(base_column)

            if len(missing_columns)>0:
                self.validation_error[report_key_name]=missing_columns
                return False
            return True
        except Exception as e:
            raise CustomException(e,sys)
        
    

    def data_drft(self,base_df:pd.DataFrame,current_df:pd.DataFrame,
                  report_key_name:str):
        try:
            drift_report=dict()
            base_columns=base_df.columns
            current_columns=current_df.columns
            print(current_columns)

            for base_column in base_columns:
                base_data,current_data=base_df[base_column],current_df[base_column]
                logging.info(f"Hypothesis{base_columns}:{base_data.dtype},{current_data.dtype}")
                same_distribution=ks_2samp(base_data,current_data)

                if same_distribution.pvalue>0.05:
                    drift_report[base_column]={
                        "pvalues":float(same_distribution.pvalue),
                        "same_distribution":True
                    }
                else:
                    drift_report[base_column]={
                        "pvalues":float(same_distribution.pvalue),
                        "same_distribution":False
                    }
            self.validation_error[report_key_name]=drift_report
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            logging.info(f"Reading base dataframe")
            base_df=pd.read_csv(self.data_validation_config.base_file_path)
            base_df.replace({"na":np.NAN},inplace=True)
            logging.info(f"Replace na value in base df")
            logging.info(f"Drop null values column from base df")
            base_df=self.drop_missing_values_columns(df=base_df,
                        report_key_name="missing_values_within_base_dataset")
            logging.info(f"Reading train datafrmae")
            train_df=pd.read_csv(self.data_ingestion_artifact.train_file_path)
            logging.info("Reading test data")
            test_df=pd.read_csv(self.data_ingestion_artifact.test_file_path)

            logging.info(f"Drop null vlaues columns from train_df")
            train_df=self.drop_missing_values_columns(df=train_df,
                        report_key_name="missing_values_within_train_dataset")
            
            logging.info(f"Drop null vlaues columns from test_df")
            test_df=self.drop_missing_values_columns(df=test_df,
                        report_key_name="missing_values_within_test_dataset")
        
        
            exclude_columns =[TARGET_COLUMN]
            base_df=utils.convert_column_float(df=base_df,exclude_column=exclude_columns)
            # print(base_df)
            train_df=utils.convert_column_float(df=train_df,exclude_column=exclude_columns)
            # print(train_df)
            test_df=utils.convert_column_float(df=test_df,exclude_column=exclude_columns)
            # print(test_df)
            


            logging.info(f"Is all required column present in train df")
            train_df_columns_status=self.is_required_columns_exists(
                base_df=base_df,current_df=train_df,
                report_key_name="missing_columns within train datast")
            print(train_df_columns_status)
            logging.info(f"Is all required column present in test df")
            test_df_columns_status=self.is_required_columns_exists(
                base_df=base_df,current_df=test_df,
                report_key_name="missing_columns within test datast")
            print(test_df_columns_status)
            
            if train_df_columns_status:
                logging.info(f"As all column are available in train df hence detecting data drift")
                self.data_drft(base_df=base_df,current_df=train_df
                               ,report_key_name="data_drft_within_train_dataset")
            if test_df_columns_status:
                logging.info(f"As all column are available in test df hence detecting data drift")
                self.data_drft(base_df=base_df,current_df=test_df
                               ,report_key_name="data_drft_within_test_dataset")
            logging.info("write report in yaml file")
            utils.write_yaml_file(file_path=self.data_validation_config.report_file_path,
            data=self.validation_error)

            data_validationn_artifact=DataValidationArtifact(report_file_path=
                                                            self.data_validation_config.report_file_path)
            logging.info(f"Data Validation artifact:{data_validationn_artifact}")
            return data_validationn_artifact
        except Exception as e:
            raise CustomException(e,sys)


