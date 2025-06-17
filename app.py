from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig

from networksecurity.components.data_validation import DataValidation,DataValidationConfig

from networksecurity.components.data_transformation import DataTransformation,DataTransformationConfig


if __name__=="__main__":
    try:
        training_pipeline_config = TrainingPipelineConfig()
        logging.info("Data ingestion started successfully")
    
        data_ingestion_config = DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
       
        data_ingestion_artifact=data_ingestion.initiate_data_ingestion()

        print(data_ingestion_artifact)
        logging.info('Data ingestion completed.')


        logging.info('Data Validation initiate.')

        data_validation_config=DataValidationConfig(training_pipeline_config=training_pipeline_config)
        data_validation=DataValidation(data_ingestion_artifact,data_validation_config)

        data_validation_artifact=data_validation.initiate_data_validation()
        print(data_validation_artifact)
        logging.info('Data Validation complete.')

        logging.info('Start DATA TRANSFORMATION. ')
        data_transformation_config=DataTransformationConfig(training_pipeline_config)
        data_transformation=DataTransformation(data_validation_artifact,data_transformation_config)
        data_transformation_artifact=data_transformation.initiate_data_transformation()
        print(data_transformation_artifact)
        logging.info('Data Transformation complete.')

    except NetworkSecurityException as e:
        logging.error(f"Data ingestion failed with error: {e}")

  