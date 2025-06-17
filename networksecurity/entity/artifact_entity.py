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