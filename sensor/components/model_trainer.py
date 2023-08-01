from sensor.entity.config_entity import ModelTrainerConfig
from sensor.entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact
from sensor.logger import logging
from sensor.exception import SensorException
import os,sys
from sensor.utils import load_numpy_array,save_object
from xgboost import XGBClassifier
from sklearn.metrics import f1_score


class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig,
                 data_transformation_artifact:DataTransformationArtifact):
        try:
            logging.info(f"{'>>'*20} Model Trainer {'<<'*20}")
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact
        except Exception as e:
            raise SensorException(e,sys)
        

    @staticmethod
    def train_model(x,y):
        try:
            xgb_clf=XGBClassifier()
            xgb_clf.fit(x,y)
            return xgb_clf
        except Exception as e:
            raise SensorException(e,sys)
        
    def initiate_model_trainer(self,)->ModelTrainerArtifact:
        try:
            logging.info(f"loading train and test array")
            train_arr=load_numpy_array(file_path=self.data_transformation_artifact.transform_train_path)
            test_arr=load_numpy_array(file_path=self.data_transformation_artifact.transform_test_path)

            logging.info(f"Splitting data into train and train input and target data")
            x_train,y_train=train_arr[:,:-1],train_arr[:,-1]
            x_test,y_test=test_arr[:,:-1],test_arr[:,-1]

            logging.info(f"train the model")
            model=ModelTrainer.train_model(x=x_train,y=y_train)

            logging.info(f"Calculating f1 train score")
            yhat_train= model.predict(x_train)
            f1_train_score=f1_score(y_true=y_train,y_pred=yhat_train)

            logging.info(f"Calculating f1_test score")
            yhat_test=model.predict(x_test)
            f1_test_score=f1_score(y_true=y_test,y_pred=yhat_test)

            logging.info(f"Checking our model underfitting or not")
            if f1_test_score<self.model_trainer_config.expected_score:
                raise Exception(f"Model is not good as it is not able to give \
                                expected accuracy: {self.model_trainer_config.expected_score}: model accuracy score: {f1_test_score}")
            logging.info(f"Checking our model overfitting or not")
            diff = abs(f1_train_score-f1_test_score)
            if diff>self.model_trainer_config.overfitting_thresold:
                raise Exception(f"train and Test score diff: {diff} is more than overifitted thresold {self.model_trainer_config.overfitting_thresold}")
            
            save_object(file_path=self.model_trainer_config.model_path,obj=model)

            ### Prepare artifact
            logging.info(f"Prepare artifact")
            model_trainer_artifact=ModelTrainerArtifact(model_path=self.model_trainer_config.model_path,
                                                        f1_train_score=f1_train_score,f1_test_score=f1_test_score)
            logging.info(f"Model Trainer artifact : {model_trainer_artifact}")
            return model_trainer_artifact

        except Exception as e:
            raise SensorException(e,sys)

