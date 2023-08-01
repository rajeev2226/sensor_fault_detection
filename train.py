from sensor.pipeline.training_pipeline import TrainingPipeline
from sensor.entity.config_entity import TrainingPipelineConfig,DataTransformationConfig
from sensor.logger import logging
from sensor.exception import SensorException
from sensor.components.data_transformation import DataTransformation
import sys

if __name__=="__main__":
    try:
        training_pipeline_config=  TrainingPipelineConfig()
        training_pipleine = TrainingPipeline(training_pipeline_config)
        training_pipleine.start()


        
    except Exception as e:
        logging.info(e)
        raise SensorException(e,sys)
