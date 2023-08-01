from sensor.utils import dump_csv_file_to_mongodb_clooection
from sensor.logger import logging
from sensor.exception import SensorException
import sys,os

def storing_record_in_mongo():
    try:
        file_path="aps_failure_training_set1.csv"
        database_name="sensor"
        collection_name="sensor_readings"

        dump_csv_file_to_mongodb_clooection(file_path,database_name,collection_name)
    except Exception as e:
        raise e
    
def test_exception_and_logger():
    try:
        x=1/0
    except Exception as e:
        raise SensorException(e,sys)

if __name__ == '__main__':
    try:
        #test_exception_and_logger()
        storing_record_in_mongo()
    except Exception as e:
        logging.info(f"error : {e}")
        print(e)

    