import logging
import os
from datetime import datetime
LOG_DIR="InsuranceLogs"
TIME_STAMP=f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
LOG_FILE_NAME=f"log_{TIME_STAMP}.log"
os.makedirs(LOG_DIR,exist_ok=True)
LOG_FILE_PATH=os.path.join(LOG_DIR,LOG_FILE_NAME)
logging.basicConfig(level=logging.INFO,filename=LOG_FILE_PATH,filemode="w",
format="[%(asctime)s] %(name)s-%(levelname)s %(message)s")