import os,sys
from datetime import datetime
from sensor.exception import SensorException
from sensor.logger import logging
TRAIN_FILE_NAME="train.csv"
TEST_FILE_NAME="test.csv"

TRANSFORMER_OBJECT_FILE_NAME="transformer.pkl"
TARGET_ENCODER_OBJECT_FIE_NAME="target_encoder.pkl"
MODEL_FILE_NAME="model.pkl"

class TrainingPipelineConfig:
    def __init__(self):
        timestamp=datetime.now().strftime("%m_%d_%y_%H_%M_%S")
        self.artifact_dir = os.path.join("artifact",timestamp)

class DataIngestionConfig:

    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        data_ingestion_dir = os.path.join(training_pipeline_config.artifact_dir,"data_ingestion")
        self.dataset_dir=os.path.join(data_ingestion_dir,"dataset")
        self.train_file_path=os.path.join(self.dataset_dir,TRAIN_FILE_NAME)
        self.test_file_path=os.path.join(self.dataset_dir,TEST_FILE_NAME)
        self.database_name="sensor"
        self.collection_name="sensor_readings"
        self.test_size=0.2


class DataValidationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        data_validation_dir = os.path.join(training_pipeline_config.artifact_dir,"data_validation")
        self.valid_dir=os.path.join(data_validation_dir,"valid")
        self.invalid_dir=os.path.join(data_validation_dir,"invalid")
        self.valid_train_file_path=os.path.join(self.valid_dir,TRAIN_FILE_NAME)
        self.invalid_train_file_path=os.path.join(self.invalid_dir,TRAIN_FILE_NAME)
        self.valid_test_file_path=os.path.join(self.valid_dir,TEST_FILE_NAME)
        self.invalid_test_file_path=os.path.join(self.invalid_dir,TEST_FILE_NAME)

        self.report_file_name=os.path.join(data_validation_dir,"report","report.yaml")
        self.missing_thresold=70
        self.schema_file_path=os.path.join("schema.yaml")


class DataTransformationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        data_transformation_dir = os.path.join(training_pipeline_config.artifact_dir,"data_transformation")
        self.transform_obj_dir = os.path.join(data_transformation_dir,"transformer")
        self.transform_object_path=os.path.join(self.transform_obj_dir,TRANSFORMER_OBJECT_FILE_NAME)
        self.transform_data=os.path.join(data_transformation_dir,"transform_data")
        self.transform_train_path=os.path.join(self.transform_data,TRAIN_FILE_NAME.replace("csv","npz"))
        self.transform_test_path=os.path.join(self.transform_data,TEST_FILE_NAME.replace("csv","npz"))
        self.target_encoder_path=os.path.join(self.transform_data,"target_encoder",TARGET_ENCODER_OBJECT_FIE_NAME)
        self.schema_file_path=os.path.join("schema.yaml")


class ModelTrainerConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            model_trainer_dir=os.path.join(training_pipeline_config.artifact_dir,"model_trainer")
            self.model_path=os.path.join(model_trainer_dir,"model",MODEL_FILE_NAME)
            self.expected_score=0.7
            self.overfitting_thresold=0.1
        except Exception as e:
            raise SensorException(e,sys)




        
