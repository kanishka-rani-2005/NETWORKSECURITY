import os
import sys
import numpy as np
import pandas as pd
from typing  import List
import pymongo

from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException

from sklearn.model_selection import train_test_split
from dotenv import load_dotenv
load_dotenv()


MONGO_DB_URL=os.getenv("MONGO_DB_URL")

logging.info('DATA INGESTION START.')

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig): 
        try:
            logging.info('Get Location')
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            logging.error(e)
            raise NetworkSecurityException(e,sys)
        
    def export_collection_as_dataframe(self):
        try:
            logging.info('Read data from Mongodb.')
            database_name=self.data_ingestion_config.database_name
            logging.info('Get database and collection name.')
            collection_name=self.data_ingestion_config.collection_name
            logging.info('Mongo client using url.')
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)
            collection=self.mongo_client[database_name][collection_name]

            logging.info('Convert data to dataframe.')
            df=pd.DataFrame(list(collection.find()))

            logging.info('Dropping id from data .')
            if "_id" in df.columns.to_list():
                df.drop(columns=["_id"],inplace=True)

            df.replace({'na':np.nan},inplace=True)
            logging.info('Dataframe Returning.')            
            return df
        except Exception as e:
            logging.error(e)
            raise NetworkSecurityException(e,sys)


    def export_data_into_feature_store(self,dataframe:pd.DataFrame):
        try:
            logging.info('Export data into feature store.')
            feature_store_file_path=self.data_ingestion_config.feature_store_dir
            dir_path=os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            logging.info('Storing Dataframe to feature store file path.')
            print(type(dataframe))
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            logging.info('Data exported to feature store.')
            return dataframe
        except Exception as e:
            logging.error(e)
            raise NetworkSecurityException(e,sys)
              
    def split_data_as_train_test(self,dataframe:pd.DataFrame):
        try:
            train_set,test_set=train_test_split(
                dataframe,test_size=self.data_ingestion_config.train_test_ratio,
                random_state=42
            )
            logging.info('Performed train test split on dataframe')

            logging.info('Excited split_data_as_train_test method od DATA_NGESTION class.')

            dir_path=os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path,exist_ok=True)

            logging.info(f"Exporting train test file path.")

            train_set.to_csv(
                self.data_ingestion_config.training_file_path,
                index=False,
                header=True
            )

            test_set.to_csv(
                self.data_ingestion_config.testing_file_path,
                index=False,
                header=True
            )

            logging.info('Exported train and test file path .')


        except Exception as e:
            logging.error(e)
            raise NetworkSecurityException(e,sys)

     
        
    def initiate_data_ingestion(self):
        try:
            logging.info('Data ingestion initiated.')
            logging.info('Get dataframe.')
            dataframe=self.export_collection_as_dataframe()
            logging.info('Export data into feature store.')
            dataframe=self.export_data_into_feature_store(dataframe)
            logging.info('Data split initiated.')
            self.split_data_as_train_test(dataframe)

            logging.info('Data ingestion artifact.')
            data_ingestion_artifact=DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,test_file_path=self.data_ingestion_config.testing_file_path)

            logging.info('Data ingestion completed.')

            return data_ingestion_artifact
        

        except Exception as e:
            logging.error(e)
            raise NetworkSecurityException(e,sys)
        
 