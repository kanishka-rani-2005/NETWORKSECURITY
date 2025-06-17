from networksecurity.constants.training_pipeline import SAVED_MODEL_DIR, MODEL_FILE_NAME
import os 
import sys
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.artifact_entity import ModelTrainerArtifact
from typing import Any

class NetworkModel:
    """
    Wrapper class for combining preprocessing and model prediction.
    """
    def __init__(self, preprocessor: Any, model: Any):
        try:
            if preprocessor is None or model is None:
                raise ValueError("Preprocessor and model must not be None")
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def predict(self, x):
        """
        Apply preprocessing to input data and return model predictions.
        """
        try:
            x_transformed = self.preprocessor.transform(x)
            return self.model.predict(x_transformed)
        except Exception as e:
            raise NetworkSecurityException(e, sys)