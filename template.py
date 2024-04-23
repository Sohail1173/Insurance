import os
import logging
from pathlib import Path
logging.basicConfig(level=logging.INFO,
    format="[%(asctime)s-%(levelname)s]: %(message)s")

project_name="InsurancePremium"
list_of_file=[

f"InsurancePremium/__init__.py",
f"{project_name}/components/data_ingestion.py",
f"{project_name}/components/data_validation.py",
f"{project_name}/components/data_transformation.py",
f"{project_name}/components/model_trainer.py",
f"{project_name}/components/model_evaluation.py",
f"{project_name}/components/__init__.py",
f"{project_name}/entity/__init__.py",
f"{project_name}/entity/config_entity.py",
f"{project_name}/entity/artifact_entity.py",
f"{project_name}/logger/__init__.py",
f"{project_name}/exception/__init__.py",
f"{project_name}/pipeline/__init__.py",
f"{project_name}/pipeline/training_pipeline.py",
f"{project_name}/pipeline/prediction_pipeline.py",
f"{project_name}/utils.py",
"configs/configs.yaml",
"setup.py",
"app.py",
"requirements.txt"

]

for file in list_of_file:
    file=Path(file)
    filedir,filename=os.path.split(file)
    if filedir!="":
        os.makedirs(filedir,exist_ok=True)
        logging.info(f"directories at:{filedir} of file {filename}")
    if  (not os.path.exists(file)) or (os.path.getsize(file)==0):

        with open(file,"w") as f:
            pass
        logging.info(f"files {filename} for path {file}")

    else:
        logging.info(f"files {filename} for path {file} already exists")
