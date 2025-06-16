import os 
import sys
import json


from dotenv import load_dotenv
load_dotenv() # initialize the object 
MONGO_DB_URL=os.getenv('MONGO_DB_URL') # get url we hvae generated 
print(MONGO_DB_URL)


import certifi
ca=certifi.where()

import pandas as pd
import numpy as np
import pymongo

from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException


class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            logging.error(e)
            raise NetworkSecurityException(e,sys)
        
    def csv_to_json_convertor(self,file_path):
        try:
            df = pd.read_csv(file_path)
            df.reset_index(drop=True,inplace=True)
            data =list(json.loads(df.T.to_json()).values())
            return data
        except Exception as e:
            logging.error(e)
            raise NetworkSecurityException(e,sys)
        
    def insert_data_to_mongodb(self, records, database, collection):
        try:
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            db = self.mongo_client[database]
            coll = db[collection]

            result = coll.insert_many(records)
            return len(result.inserted_ids)

        except Exception as e:
            logging.error(e)
            raise NetworkSecurityException(e, sys)
        



if __name__=="__main__":
    FILE_PATH="NetworkData\phisingData.csv"
    DATABASE="Cluster0"
    COLLECTION="NetworkData"
    data=NetworkDataExtract()
    records=data.csv_to_json_convertor(FILE_PATH)
    print(records)
    no_of_records=data.insert_data_to_mongodb(records, DATABASE, COLLECTION)
    print(no_of_records)
