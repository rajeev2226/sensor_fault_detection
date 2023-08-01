from sensor.entity.artifact_entity import DataIngestionArtifact
from sensor.entity.config_entity import DataIngestionConfig
from sensor.exception import SensorException
from sensor.utils import export_collectio_to_dataframe
from sensor.logger import logging
import os,sys
import numpy as np
from sklearn.model_selection import train_test_split

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:

            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise SensorException(e,sys)


    def initiate_data_ingestion(self)->DataIngestionArtifact:
        try:
            logging.info("Exporting collection as Dataframe")
            df=export_collectio_to_dataframe(
                database_name=self.data_ingestion_config.database_name,
                collection_name=self.data_ingestion_config.collection_name,)
            logging.info("Replacing na with NAN")
            df.replace({"na":np.NAN},inplace=True)
            logging.info("Splitting Dataframe to train_df and test_df")
            train_df,test_df=train_test_split(df,test_size=self.data_ingestion_config.test_size)
            os.makedirs(self.data_ingestion_config.dataset_dir,exist_ok=True)
            logging.info("Converting Dtaaframe to csv")
            train_df.to_csv(self.data_ingestion_config.train_file_path,index=False,header=True)
            test_df.to_csv(self.data_ingestion_config.test_file_path,index=False,header=True)
            logging.info("Train file path and Test file path created")
            data_ingestion_artifact=DataIngestionArtifact(
                train_file_path= self.data_ingestion_config.train_file_path,
                test_file_path=self.data_ingestion_config.test_file_path
                )
            logging.info(f"Train file and Test file paths created {data_ingestion_artifact}")
            return data_ingestion_artifact
            
        except Exception as e:
            raise SensorException(e,sys)