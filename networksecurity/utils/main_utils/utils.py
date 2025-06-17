import os 
import sys

import dill
import pickle # in-built

from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException

import yaml
import numpy as np

from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score

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
    

def load_object(file_path:str)->object:
    try:
        if not os.path.exists(file_path):
            logging.error(f"File {file_path} does not exist")
            raise NetworkSecurityException(f"File {file_path} does not exist") 
        logging.info('Entered the load_object method of MainUtils class.')
        with open(file_path,"rb") as file_obj:
            obj=pickle.load(file_obj)
            logging.info("Exited the load_object method of MainUtils class")
            return obj
    except Exception as e:
        logging.error(f"Error loading object: {str(e)}")
        raise NetworkSecurityException(f"Error loading object: {str(e)}") from e
    

def load_numpy_array_data(file_path:str)->np.array:
    try:
        if not os.path.exists(file_path):
            logging.error(f"File {file_path} does not exist")
            raise NetworkSecurityException(f"File {file_path} does not exist")
        logging.info('Entered the load_numpy_array_data method of MainUtils class.')
        with open(file_path,"rb") as file_obj:
            array=np.load(file_obj)
            logging.info("Exited the load_numpy_array_data method of MainUtils class")
            return array
    except Exception as e:
        logging.error(f"Error loading numpy array: {str(e)}")
        raise NetworkSecurityException(f"Error loading numpy array: {str(e)}") from e



def evaluate_models(X_train,Y_train,X_test,Y_test,models,param):
    try:
        report={}
        logging.info("Choosing Best model with its best params.")
        for model_name,model in models.items():
            model_name=model_name
            model.fit(X_train,Y_train)
            para=param[model_name]

            gs=GridSearchCV(model,para,cv=3)
            gs.fit(X_train,Y_train)


            model.set_params(**gs.best_params_)
            
            logging.info(f'Model with its best parameters {model} .')

            model.fit(X_train,Y_train)


            y_train_pred=model.predict(X_train)
            y_test_pred=model.predict(X_test)

            # train_model_score=r2_score(Y_train,y_train_pred)
            test_model_score=r2_score(Y_test,y_test_pred)

            report[model_name]=test_model_score

            logging.info(f"Model {model_name} R2 score: {test_model_score}")
            
        return report


        
    except Exception as e:
        logging.error(e)
        raise NetworkSecurityException(f"Error evaluating models: {str(e)}") from e