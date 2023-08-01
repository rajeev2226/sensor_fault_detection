from sensor.entity.config_entity import (TrainingPipelineConfig,
                                         DataIngestionConfig,
                                         DataValidationConfig,
                                         DataTransformationConfig,
                                         ModelTrainerConfig)
from sensor.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact,ModelTrainerArtifact
import os,sys
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.components.data_injestion import DataIngestion
from sensor.components.data_validation import DataValidation
from sensor.components.data_transformation import DataTransformation
from sensor.components.model_trainer import ModelTrainer
class TrainingPipeline:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.training_pipeline_config=training_pipeline_config
        except Exception as e:
            raise SensorException(e,sys)
        
    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            data_ingestion_config= DataIngestionConfig(self.training_pipeline_config)
            data_ingestion=DataIngestion(data_ingestion_config)
            data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
            return data_ingestion_artifact
        except Exception as e:
            raise SensorException(e,sys)
    def start_data_validation(self,dataIngestion_artifact)->DataValidationArtifact:
        try:
            data_validation_config=DataValidationConfig(
                training_pipeline_config=self.training_pipeline_config
            )
            data_validation=DataValidation(data_validation_config=data_validation_config,data_ingestion_artifact=dataIngestion_artifact)

            return data_validation.initiate_data_validation()
        
        except Exception as e:
            raise SensorException(e,sys)

        
    def start_data_transformation(self,data_validation_artifact:DataValidationArtifact)->DataTransformationArtifact:
        try:
            data_transformation_config = DataTransformationConfig(
                training_pipeline_config=self.training_pipeline_config
                )
            
            data_transformation = DataTransformation(data_transformation_config=data_transformation_config,
             data_validation_artifact=data_validation_artifact
             )
            
            return data_transformation.initiate_data_transformation()
        except Exception as e:
            raise SensorException(e, sys)
    
    def start_model_trainer(self,data_transformation_artifact:DataTransformationArtifact)->ModelTrainerArtifact:
        try:
            model_trainer_config = ModelTrainerConfig(
                training_pipeline_config=self.training_pipeline_config
                )
            
            model_trainer = ModelTrainer(model_trainer_config=model_trainer_config,
             data_transformation_artifact=data_transformation_artifact
             )
            
            return model_trainer.initiate_model_trainer()
        except Exception as e:
            raise SensorException(e, sys)

    def start(self):
        try:
            data_ingestion_artifact =self.start_data_ingestion()
            data_validation_artifact=self.start_data_validation(data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(
                data_validation_artifact=data_validation_artifact
            )
            model_trainer_artifact=self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)

        except Exception as e:
            raise SensorException(e,sys)
