import os 
import sys
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.artifact_entity import DataValidationArtifact
from networksecurity.entity.artifact_entity import DataIngestionArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.constants.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.main_utils.utils import read_yaml_file,write_yaml_file

from scipy.stats import ks_2samp # for data drift 
from dataclasses import dataclass

import pandas as pd


@dataclass
class DataValidation:
    """DataValidation class to perform data validation on the data ingested from the source system."""
    # input data_ingestion_artifact
    # output  data_validation_config
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_config=data_validation_config
            self.schema_config=read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            logging.error(e)
            raise NetworkSecurityException(e,sys)
        

    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            logging.error(e)
            raise NetworkSecurityException(e,sys)
        

    def validate_number_of_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            number_of_columns=len(self.schema_config['columns'])
            logging.info(f"Required no of columns : {number_of_columns}")
            logging.info(f"Dataframe has columns :{len(dataframe.columns)}")

            return number_of_columns==len(dataframe.columns)
        
        except Exception as e:
            logging.error(e)
            raise NetworkSecurityException(e,sys)
        

    def detect_dataset_drift(self,base_df,current_df,threshold=0.05)->bool:
        try:
            status=True
            report={}

            for column in base_df.columns:
                d1=base_df[column]
                d2=current_df[column]
                is_same_dist=ks_2samp(d1,d2)

                if threshold<=is_same_dist.pvalue:
                    is_found=False
                else:
                    is_found=True
                    status=False
                report.update({
                    column:{
                        "p_value":is_same_dist.pvalue,
                        "is_drift_found":is_found
                    }
                })
            drift_report_file_path= self.data_validation_config.drift_report_file_path

            dir_path=os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)

            write_yaml_file(file_path=drift_report_file_path,content=report)

            logging.info(f"Drift report saved at {drift_report_file_path}")
        except Exception as e:
            logging.error(e)
            raise NetworkSecurityException(e,sys)

    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            logging.info('Starting the data Validation.')
            train_file_path,test_file_path=self.data_ingestion_artifact.trained_file_path,self.data_ingestion_artifact.test_file_path

            ## read data from train and test
            logging.info('Reading train ans test data from their respective file paths .')
            train_dataframe=DataValidation.read_data(train_file_path)
            test_dataframe=DataValidation.read_data(test_file_path)

            logging.info('Check if number of columns is equal or not .')
            status =self.validate_number_of_columns(dataframe=train_dataframe)

            if not status:
                raise ValueError("Train dataframe does not contain all required columns.")


            status =self.validate_number_of_columns(dataframe=test_dataframe)

            if not status:
                raise ValueError("Test dataframe does not contain all required columns.")
            logging.info("Checking numerical columns presence in train and test datasets.")
            
            expected_numerical_columns = self.schema_config.get("numerical_columns", [])
            train_numerical_cols=[col for col in expected_numerical_columns if col in train_dataframe.columns]
            test_numerical_cols=[col for col in expected_numerical_columns if col in test_dataframe.columns]


            if len(train_numerical_cols)==0:
                raise ValueError("No numerical columns found in train dataset.")
            if len(test_numerical_cols)==0:
                raise ValueError("No numerical columns found in test dataset.")
            
            logging.info(f"Numerical columns in train df are {train_numerical_cols}")
            logging.info(f"Numerical columns in test df are {test_numerical_cols}")


            logging.info('Checking for draft in data. ')
            status = self.detect_dataset_drift(base_df=train_dataframe,current_df=test_dataframe)
            
            dir_path=os.path.dirname(self.data_validation_config.valid_train_file_path)

            os.makedirs(dir_path,exist_ok=True)
            logging.info(f"Validating the data.")

            train_dataframe.to_csv(self.data_validation_config.valid_train_file_path,index=False,header=True)

            test_dataframe.to_csv(self.data_validation_config.valid_test_file_path,index=False,header=True)

            data_validation_artifact=DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )
            
            return data_validation_artifact

            pass
        except Exception as e:
            logging.error(e)
            raise NetworkSecurityException(e,sys)

