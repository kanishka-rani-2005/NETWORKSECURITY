import os 
import sys

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.entity.artifact_entity import ModelTrainerArtifact,ClassificationMetricArtifact,DataTransformationArtifact


from networksecurity.utils.main_utils.utils import save_object,load_object,evaluate_models
from networksecurity.utils.main_utils.utils import load_numpy_array_data
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_report
from networksecurity.utils.ml_utils.model.estimator import NetworkModel


from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.ensemble import AdaBoostClassifier,RandomForestClassifier,GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier


print("Debug - type of NetworkModel:", type(NetworkModel))
print("Debug - NetworkModel:", NetworkModel)


class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig,data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact
        except Exception as e:
            logging.error(e)
            raise NetworkSecurityException(e,sys)
        

    def train_model(self,x_train,y_train,x_test,y_test):
        try:

            models={
                "logistic_regression":LogisticRegression(verbose=1),
                "decision_tree":DecisionTreeClassifier(),
                "support_vector_machine":SVC(),
                "ada_boost":AdaBoostClassifier(),
                "random_forest":RandomForestClassifier(verbose=1),
                "gradient_boosting":GradientBoostingClassifier(verbose=1),
                "k_nearest_neighbors":KNeighborsClassifier()
            }

            param_grids = {
                "logistic_regression": {
                    "C": [0.01, 0.1],
                    "solver": ["liblinear", "lbfgs"],
                    "max_iter": [100, 200]
                },

                "decision_tree": {
                    'criterion':['gini', 'entropy', 'log_loss'],
                    "max_depth": [3, 5, None],
                    "min_samples_split": [2,10]
                },

                "support_vector_machine": {
                    "C": [0.1, 1, 10],
                    "kernel": ["linear", "rbf"],
                    "gamma": ["scale", "auto"]
                },

                "ada_boost": {
                    'learning_rate':[.1,.01,.001],
                    'n_estimators': [8,16,32,64,128,256]
                },

                "random_forest": {
                    "n_estimators": [50, 100],
                    "max_depth": [None, 5, 10],
                    "min_samples_split": [2, 5]
                },

                "gradient_boosting": {
                    # 'loss':['log_loss', 'exponential'],
                    'learning_rate':[.1,.01,.05,.001],
                    'subsample':[0.6,0.7,0.75,0.85,0.9],
                    # 'criterion':['squared_error', 'friedman_mse'],
                    # 'max_features':['auto','sqrt','log2'],
                    'n_estimators': [8,16,32,64,128,256]
                },

                "k_nearest_neighbors": {
                    "n_neighbors": [3, 5],
                    "weights": ["uniform", "distance"],
                    "p": [1, 2]  
                }
            }

            model_report:dict=evaluate_models(X_train=x_train,Y_train=y_train,X_test=x_test,Y_test=y_test,models=models,param=param_grids)

            best_model_score=max(sorted(model_report.values()))

            best_model_name = list(model_report.keys())[
            list(model_report.values()).index(best_model_score)
            ]
            best_model=models[best_model_name]

            logging.info(f"Best model is : {best_model_name} and score is {best_model_score}")
            y_train_pred=best_model.predict(x_train)
            y_test_pred=best_model.predict(x_test)

            
            
            classification_train_metric=get_classification_report(y_true=y_train,y_pred=y_train_pred)
            classification_test_metric=get_classification_report(y_true=y_test,y_pred=y_test_pred)

            logging.info(f"Train data scores :{classification_train_metric}")
            logging.info(f"Test data scores :{classification_test_metric}")
            

            logging.info('Loading preprocessor.')
            preprocessor=load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
            dirname=os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(dirname,exist_ok=True)

            logging.info('Saving Network Model')
            network_model_instance =NetworkModel(preprocessor=preprocessor,model=best_model)
            save_object(file_path=self.model_trainer_config.trained_model_file_path,obj=network_model_instance )
            save_object("final_model/model.pkl",best_model)
            

            model_trainer_artifact=ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                test_metric_artifact=classification_test_metric,
                train_metric_artifact=classification_train_metric,
            )

            logging.info(f"Model Trainer artifact {model_trainer_artifact} ...")

            return model_trainer_artifact

            
        except Exception as e:
            logging.error(e)
            raise NetworkSecurityException(e,sys)

    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            train_file_path=self.data_transformation_artifact.transformed_train_file_path
            test_file_path=self.data_transformation_artifact.transformed_test_file_path


            logging.info('Loading numpy array from train/test file path')
            train_array=load_numpy_array_data(train_file_path)
            test_array=load_numpy_array_data(test_file_path)

            x_train,x_test,y_train,y_test=(
                train_array[:,:-1],
                test_array[:,:-1],
                train_array[:,-1],
                test_array[:,-1]
            )

            logging.info(f"{x_train.shape} ,{x_test.shape},{y_test.shape},{y_train.shape}")
            logging.info('Succesfully spliting X train Y train X test Y test .')

            model_trainer_artifact=self.train_model(x_train,y_train,x_test,y_test)

            return model_trainer_artifact

        except Exception as e:
            logging.error(e)
            raise NetworkSecurityException(e,sys)