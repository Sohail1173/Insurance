import logging
from datetime import datetime
import os
# LOGDIR="InsuLogs"
# TIMESTAMP=f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
# # TIMESTAMP=f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
# log_time_dir=os.path.join(LOGDIR,TIMESTAMP)
# os.makedirs(log_time_dir,exist_ok=True)
# file_name=f"log_{TIMESTAMP}.log"
# # logfile=os.path.join(file_name,TIMESTAMP)
# file_dir=os.path.join(log_time_dir,file_name)
# logging.basicConfig(level=logging.INFO,filename=file_dir,filemode="w",format="[%(asctime)s-%(levelname)s]-%(message)s")
import pandas as pd

base=pd.read_csv(r"C:\Users\91808\Downloads\Insurance\artifact\05012024__192259\data_ingestion\feature_store\insurance.csv")
train_df=pd.read_csv(r"C:\Users\91808\Downloads\Insurance\artifact\05012024__192259\data_ingestion\dataset\train.csv")
test_df=pd.read_csv(r"C:\Users\91808\Downloads\Insurance\artifact\05012024__192259\data_ingestion\dataset\test.csv")

def drop_missing_values_columns(df:pd.DataFrame,report_key_name:str):
            validation_error=dict()
            threshold=0.2
            null_report=df.isna().sum()/df.shape[0]
            logging.info(f"selecting coumn name which contains null above to {threshold}")
            drop_column_names=null_report[null_report>threshold].index
            logging.info(f"column to drop :{list(drop_column_names)}")
            validation_error[report_key_name]=list(drop_column_names)
            df.drop(list(drop_column_names),axis=1,inplace=True)

            if len(df.columns)==0:
                return None
            return df
print(drop_missing_values_columns(df=base,
                        report_key_name="missing_values_within_base_dataset"))


