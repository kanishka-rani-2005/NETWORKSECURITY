from dataclasses import dataclass
import os 
import sys
import numpy as np

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging



@dataclass
class DataIngestionArtifact:
    """DataIngestionArtifact class to store data ingestion artifacts"""
    trained_file_path:str
    test_file_path:str

@dataclass
class DataValidationArtifact:
    """DataValidationArtifact class to store data validation artifacts"""
    validation_status:bool
    valid_train_file_path:str
    valid_test_file_path:str
    invalid_train_file_path:str
    invalid_test_file_path:str
    drift_report_file_path:str


@dataclass
class DataTransformationArtifact:
    transformed_object_file_path:str # preprocessor 
    transformed_train_file_path:str # traning np array
    transformed_test_file_path:str # test array


@dataclass
class ClassificationMetricArtifact:
    f1_score:float
    precision_score:float
    recall_score:float

@dataclass
class ModelTrainerArtifact:
    trained_model_file_path:str
    train_metric_artifact:ClassificationMetricArtifact
    test_metric_artifact:ClassificationMetricArtifact   
