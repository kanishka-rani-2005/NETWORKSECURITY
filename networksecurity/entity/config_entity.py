from datetime import datetime
import os
import sys

from networksecurity.logging.logger import logging
from networksecurity.constants import training_pipeline
from networksecurity.exception.exception import NetworkSecurityException

# to check if working correct or not 
print("Pipeline :",training_pipeline.PIPELINE_NAME)
print("Artifact dirname :",training_pipeline.ARTIFACT_DIR)
print("Collection name :",training_pipeline.DATA_INGESTION_COLLECTION_NAME)
print("Database name :",training_pipeline.DATA_INGESTION_DATABASE_NAME)

class TrainingPipelineConfig:
    def __init__(self,timestamp=datetime.now()):
        try:
            timestamp=timestamp.strftime("%m_%d_%Y_%M_%S")
            self.pipeline_name=training_pipeline.PIPELINE_NAME
            self.artifact_name=training_pipeline.ARTIFACT_DIR
            self.artifact_dir=os.path.join(self.artifact_name,timestamp)
            self.timestamp:str=timestamp
        except Exception as e:
            logging.error(e)
            raise NetworkSecurityException(e,sys)
        

class DataIngestionConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            # "artifacts/ingested"
            self.data_ingestion_dir:str=os.path.join(
                training_pipeline_config.artifact_dir,training_pipeline.DATA_INGESTION_INGESTED_DIR)
            # "artifacts/feature_store/phisingData.csv"
            self.feature_store_dir:str=os.path.join(
                training_pipeline_config.artifact_dir,training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR,training_pipeline.FILE_NAME)
            
            # "artifacts/ingested/ingested/train.csv"
            self.training_file_path:str=os.path.join(self.data_ingestion_dir,training_pipeline.DATA_INGESTION_INGESTED_DIR,training_pipeline.DATA_INGESTION_TRAIN_FILE_NAME)
            
            # "artifacts/ingested/ingested/test.csv"
            self.testing_file_path:str=os.path.join(self.data_ingestion_dir,training_pipeline.DATA_INGESTION_INGESTED_DIR,training_pipeline.DATA_INGESTION_TEST_FILE_NAME)

            self.train_test_ratio:float=training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
            # self.collection_name = "network_data"
            # self.database_name = "NetworkSecurity"
            self.collection_name:str=training_pipeline.DATA_INGESTION_COLLECTION_NAME
            self.database_name:str=training_pipeline.DATA_INGESTION_DATABASE_NAME
                                                     
        except Exception as e:
            logging.error(e)
            raise NetworkSecurityException(e,sys)

class DataValidationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.data_validation_dir:str=os.path.join(training_pipeline_config.artifact_dir,training_pipeline.DATA_VALIDATION_DIR_NAME)
            self.valid_data_dir:str=os.path.join(self.data_validation_dir,training_pipeline.DATA_VALIDATION_VALID_DIR)
            self.invalid_data_dir:str=os.path.join(self.data_validation_dir,training_pipeline.DATA_VALIDATION_INVALID_DIR)
            self.valid_train_file_path:str=os.path.join(self.valid_data_dir,training_pipeline.DATA_INGESTION_TRAIN_FILE_NAME)
            self.valid_test_file_path:str=os.path.join(self.valid_data_dir,training_pipeline.DATA_INGESTION_TEST_FILE_NAME)
            self.invalid_train_file_path:str=os.path.join(self.invalid_data_dir,training_pipeline.DATA_INGESTION_TRAIN_FILE_NAME)
            self.invalid_test_file_path:str=os.path.join(self.invalid_data_dir,training_pipeline.DATA_INGESTION_TEST_FILE_NAME)
            self.drift_report_file_path:str=os.path.join(
                self.data_validation_dir,
                training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR,
                training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME
            )
        except Exception as e:
            logging.error(e)
            raise NetworkSecurityException(e,sys)

