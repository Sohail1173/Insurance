from InsurancePremium.entity import artifact_entity,config_entity
from InsurancePremium.exception import CustomException
from InsurancePremium.logger.logging import logging
from typing import  Optional
import os,sys
from sklearn.linear_model import LinearRegression
from InsurancePremium import utils
from sklearn.metrics import r2_score

class ModelTrainer:

    def __init__(self,model_trainer_config:config_entity.ModelTrainerConfig,
                 data_transformation_artifact:artifact_entity.DataTransformationArtifact):
        try:
            logging.info("ModelTrainer")
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact
        except Exception as e:
            raise CustomException(e,sys)
        
    def train_model(self,x,y):
        try:
            pass
        except Exception as e:
            raise CustomException(e,sys)
        

    def train_model(self,x,y):
        try:
            lr=LinearRegression()
            lr.fit(x,y)
            return lr
        except Exception as e:
            raise CustomException(e,sys)
        

    def initiate_model_trainer(self,)->artifact_entity.DataTrainerArtifact:
        try:
            logging.info("loading train and test array")
            train_arr=utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transform_train_path)
            test_arr=utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transform_test_path)

            logging.info("splitting both train and test arrays")
            x_train,y_train=train_arr[:,:-1],train_arr[:,-1]
            x_test,y_test=test_arr[:,:-1],test_arr[:,-1]
            logging.info("train the model")
            model=self.train_model(x=x_train,y=y_train)
            
            logging.info("calculating the f1 train score")
            y_train_pred=model.predict(x_train)
            r2_train_score=r2_score(y_true=y_train,y_pred=y_train_pred)

            logging.info("calculating the f1 test score")
            y_test_pred=model.predict(x_test)
            r2_test_score=r2_score(y_true=y_test,y_pred=y_test_pred)

            logging.info(f"train score:{r2_train_score} and test score:{r2_test_score}")

            logging.info(f"checking model is underfitting or not")
            if r2_test_score<self.model_trainer_config.expected_score:
                raise Exception(f" Model is not good as it is not able to give \
                expected accuracy:{self.model_trainer_config.expected_score}:model actual score:{r2_test_score}")
            logging.info("checking model is overfitting or not")
            diff=abs(r2_train_score-r2_test_score)

            if diff>self.model_trainer_config.overfitting_threshold:
                raise Exception(f"Train  and test score diff:{diff} is more than \
                overfitting threshold:{self.model_trainer_config.overfitting_th}")
            
            logging.info("save mode object")
            utils.save_object(file_path=self.model_trainer_config.model_path,obj=model)
            
            logging.info("prepare the artifact")
            model_trainer_artifact=artifact_entity.DataTrainerArtifact(model_path=self.model_trainer_config.model_path,
            r2_train_score=r2_train_score,r2_test_score=r2_test_score)
            logging.info(f"model trainer artifact:{model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise CustomException(e,sys)