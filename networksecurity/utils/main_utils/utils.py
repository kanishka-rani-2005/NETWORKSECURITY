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
    



def save_numpy_array(file_path:str,array:np.array):
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)

        with open(file_path,"wb") as file_obj:
            np.save(file_obj,array)
    except Exception as e:
        logging.error(f"Error saving numpy array: {str(e)}")
        raise NetworkSecurityException(f"Error saving numpy array: {str(e)}") from e
    

def save_object(file_path:str,obj:object)->None:
    try:
        logging.info('Entered teh save_object method of MainUtils class.')
        dir_path=os.path.dirname(file_path) 
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as file_obj:
            pickle.dump(obj,file_obj)

        logging.info("Exited the save_object of MainUtils class")
    except Exception as e:
        logging.error(f"Error saving object: {str(e)}")
        raise NetworkSecurityException(f"Error saving object: {str(e)}") from e