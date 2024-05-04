import pandas as pd

# from InsurancePremium.logger.logging import logging
# from InsurancePremium.exception import CustomException
# import os,sys
# import yaml
# import numpy as np
# import dill

# def write_yaml_file(file_path,data:dict):
#     try:
#         file_dir=os.path.join(file_path)
#         os.makedirs(file_dir,exist_ok=True)
#         with open(file_path,"w") as file_writer:
#             yaml.dump(data,file_writer)
#     except Exception as e:
#         raise CustomException(e,sys)
TARGET_COLUMN="expenses"