import os
import sys
import numpy as np
import pandas as pd

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from sklearn.pipeline import Pipeline
from sklearn.impute import KNNImputer

from networksecurity.constants.training_pipeline import TARGET_COLUMN
from networksecurity.constants.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS
from networksecurity.entity.artifact_entity import DataTransformationArtifact,DataValidationArtifact

from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.utils.main_utils.utils import save_numpy_array,save_object


class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,data_transformation_config:DataTransformationConfig):
        try:
            self.data_transformation_config:DataTransformationConfig=data_transformation_config
            self.data_validation_artifact:DataValidationArtifact=data_validation_artifact

        except Exception as e: 
            logging.info(e)
            raise NetworkSecurityException(e,sys)
        
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            logging.info(f"Reading data from {file_path} .")
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    def get_data_tranformer_object(cls)->Pipeline:
        try:
            logging.info('Start get_data_tranformer_object.')
            
            imputer:KNNImputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info('Initialize kNN iMputer.')

            preprocessor:Pipeline=Pipeline([("imputer",imputer)])
            logging.info('Initialize preprocessor.')
            return preprocessor

        except Exception as e:
            logging.info(e)
            raise NetworkSecurityException(e,sys)
        
    def initiate_data_transformation(self)->DataTransformationArtifact:
        try:
            logging.info('Data Transformation Initiate.')
            train_df=DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df=DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            input_feature_train_df=train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_train_df=train_df[TARGET_COLUMN]
            target_feature_train_df=target_feature_train_df.replace(-1,0)

            input_feature_test_df=test_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_test_df=test_df[TARGET_COLUMN]

            preprocessor=self.get_data_tranformer_object()
            preprocessor_object=preprocessor.fit(input_feature_train_df)
            transformed_input_feature_train_df=preprocessor_object.transform(input_feature_train_df)

            transformed_input_feature_test_df=preprocessor_object.transform(input_feature_test_df)



            train_arr=np.c_[transformed_input_feature_train_df,np.array(target_feature_train_df)]
            test_arr=np.c_[transformed_input_feature_test_df,np.array(target_feature_test_df)]

            save_numpy_array(self.data_transformation_config.transformed_train_file_path,array=train_arr)
            save_numpy_array(self.data_transformation_config.transformed_test_file_path,array=test_arr)
            save_object(self.data_transformation_config.tranformed_object_file_path,preprocessor)
            logging.info('Data Transformation Complete.')
            
            data_transformation_artifact=DataTransformationArtifact(
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
                transformed_object_file_path=self.data_transformation_config.tranformed_object_file_path
            )
            return data_transformation_artifact

            

            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        