from InsurancePremium.entity import config_entity,artifact_entity
from InsurancePremium.exception    import CustomException
from InsurancePremium.logger.logging import logging
from InsurancePremium.utils import load_object
from sklearn.metrics import r2_score
import pandas as pd
import sys,os
from InsurancePremium.config import TARGET_COLUMN
from InsurancePremium.predictor import ModelResolver

class ModelEvaluation:
    def __init__(self,model_evaluation_config:config_entity.ModelEvaluationConfig,
                 data_ingestion_artifact:artifact_entity.DataIngestionArtifact,
                 data_transformation_artifact:artifact_entity.DataTransformationArtifact,
                 model_trainer_artifact:artifact_entity.DataTrainerArtifact):
        try:
            logging.info("Model Evaluation")
            self.model_evaluation_config=model_evaluation_config
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_transformation_artifact=data_transformation_artifact
            self.model_trainer_artifact=model_trainer_artifact
            self.model_resolver=ModelResolver()
        except Exception as e:
            raise CustomException(e,sys)
        


    def inititate_model_evaluation(self)->artifact_entity.ModelEvaluationArtifact:
        try:
            logging.info("model comparison")
            latest_dir_path=self.model_resolver.get_latest_dir_path()
            if latest_dir_path==None:
                model_eval_artifact=artifact_entity.ModelEvaluationArtifact(is_model_accepted=True,improved_accuracy=None)
                logging.info(f"model evaluation artifact:{model_eval_artifact}")
                return model_eval_artifact
            
            logging.info("Finding location of transformer model and target encoder")
            transformer_path=self.model_resolver.get_latest_model_path()
            model_path=self.model_resolver.get_latest_model_path()
            target_encoder_path=self.model_resolver.get_latest_target_encoder_path()
            

            logging.info("previous trained objects of transformer,model and target encoder")
            transformer=load_object(file_path=transformer_path)
            model=load_object(file_path=model_path)
            target_encoder=load_object(file_path=target_encoder_path)

            logging.info("previously trained  objects of transformer,model and target encoder")
            current_transformer=load_object(file_path=self.data_transformation_artifact.transform_object_path)
            current_model=load_object(file_path=self.model_trainer_artifact.model_path)
            current_target_encoder=load_object(file_path=self.data_transformation_artifact.transform_encoder_path)

            test_df=pd.read_csv(self.data_ingestion_artifact.test_file_path)
            target_df=test_df[TARGET_COLUMN]
            y_true=target_df

            # label encoder for categorical features
            input_feature_name=list(transformer.feature_names_in_)
            for i  in input_feature_name:
                if test_df[i].dtypes=="object":
                    test_df[i]=target_encoder.fit_tranform(test_df[i])
            
            input_arr=transformer.transform(test_df[input_feature_name])
            y_pred=model.predict(input_arr)
            print(f"predictions using previous trained model {y_pred[:5]}")
            previous_model_score=r2_score(y_true=y_true,y_pred=y_pred)
            logging.info(f"Accuracy using previous trained model :{previous_model_score}")

            input_feature_name=list(current_transformer.feature_names_in_)
            input_arr=current_transformer.transform(test_df[input_feature_name])
            y_pred=current_model.predict(input_arr)
            y_true=target_df


            print(f"prediction using trained model:{y_pred[:5]}")
            current_model_score=r2_score(y_true=y_true,y_pred=y_pred)
            logging.info(f"Accuracy using current trained model :{current_model_score}")
            if current_model_score<=previous_model_score:
                logging.info("Current trained model is not better than previous trained model")
                raise Exception("Current trained model is not better than previous trained model")
            model_eval_artifact=artifact_entity.ModelEvaluationArtifact(is_model_accepted=True,
            improved_accuracy=current_model_score-previous_model_score)
            logging.info("model evval artifact:{model_eval_artifact}")
            return model_eval_artifact


        except Exception as e:
            raise CustomException(e,sys)