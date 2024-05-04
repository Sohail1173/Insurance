import pandas as pd
from InsurancePremium.logger.logging import logging
from InsurancePremium.exception import CustomException
import os,sys,yaml
import numpy as np
import dill

def write_yaml_file(file_path,data:dict):
    try: 
        file_dir=os.path.dirname(file_path)
        os.makedirs(file_dir,exist_ok=True)
        with open(file_path, 'w') as file_writer:
            yaml.dump(data,file_writer)

        
    except Exception as e:
        raise CustomException(e,sys) from e
    
def convert_column_float(df:pd.DataFrame,exclude_column:list)->pd.DataFrame:
    try:
        for column in df.columns:
            if column not in exclude_column:
                if df[column].dtypes !="O":
                    df[column]=df[column].astype(float)
        return df
    except Exception as e:
        raise CustomException(e,sys) from e
    


def save_object(file_path:str,obj:object)->None:
    try:
        logging.info("Entered the save_object method of utils")
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"wb") as file_obj:
            dill.dump(obj,file_obj)
            logging.info("Exitd the save_object method of utils")
    except Exception as e:
        raise CustomException(e,sys) from e
    


def load_object(file_path:str)->object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"file:{file_path} is not exists")
        with open(file_path,"rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise CustomException(e,sys) from e
    

def save_numpy_array_data(file_path:str,array:np.array):
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as file_obj:
            np.save(file_obj,array)
    except Exception as e:
        raise CustomException(e,sys) from e
    

def load_numpy_array_data(file_path:str)->np.array:
    try:
       
        with open(file_path,"rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise CustomException(e,sys) from e