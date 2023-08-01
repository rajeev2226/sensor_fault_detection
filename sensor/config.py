from dataclasses import dataclass
import pymongo
import os

MONGO_DB_ENV_KEY="MONGO_DB_URL"

@dataclass
class EnviromentVariable:
    mongo_db_url:str=os.getenv(MONGO_DB_ENV_KEY)

env_var=EnviromentVariable()
mongo_client=pymongo.MongoClient(env_var.mongo_db_url)
