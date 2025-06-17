import os 
import sys

import dill
import pickle # in-built

from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException

import yaml
import numpy as np


def read_yaml_file(file_path:str)->dict:
    try:
        with open(file_path, 'rb') as yaml_file:
            yaml_data = yaml.safe_load(yaml_file)
            return yaml_data
    except Exception as e:
        logging.error(f"Error reading yaml file: {str(e)}")
        raise NetworkSecurityException(f"Error reading yaml file: {str(e)}") from e
    


def write_yaml_file(file_path:str,content:object,replace:bool=False)->None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path, 'w') as yaml_file:
            yaml.dump(content, yaml_file)
    except Exception as e:
        logging.error(f"Error writing yaml file: {str(e)}")
        raise NetworkSecurityException(f"Error writing yaml file: {str(e)}") from e