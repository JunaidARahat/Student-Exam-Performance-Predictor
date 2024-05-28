from collections import namedtuple
from datetime import datetime
import uuid
from student.configuration import Configuartion
from student.logger import logging, get_log_file_name
from student.exception import StudentException
from threading import Thread
from typing import List

from multiprocessing import Process
from student.entity.artifact_entity import DataIngestionArtifact,ModelEvaluationArtifact
from student.entity.artifact_entity import DataValidationArtifact,DataTransformationArtifact,ModelTrainerArtifact
from student.components.data_ingestion import DataIngestion
from student.components.data_validation import DataValidation
from student.components.data_transformation import DataTransformation
from student.components.model_trainer import ModelTrainer
from student.components.model_evaluation import ModelEvaluation


import os, sys
from collections import namedtuple
from datetime import datetime
import pandas as pd
from student.constants import EXPERIMENT_DIR_NAME, EXPERIMENT_FILE_NAME





class Pipeline(Thread):
    
    def __init__(self, config: Configuartion) -> None:
        try:
            os.makedirs(config.training_pipeline_config.artifact_dir, exist_ok=True)
        
            super().__init__(daemon=False, name="pipeline")
            self.config = config
        except Exception as e:
            raise StudentException(e, sys) from e
        
    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            data_ingestion = DataIngestion(data_ingestion_config=self.config.get_data_ingestion_config())
            return data_ingestion.initiate_data_ingestion()
        except Exception as e:
            raise StudentException(e, sys) from e
    
    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        try:
            data_validation = DataValidation(data_validation_config=self.config.get_data_validation_config(),
                                             data_ingestion_artifact=data_ingestion_artifact
                                             )
            return data_validation.initiate_data_validation()
        except Exception as e:
            raise StudentException(e, sys) from e
        
    def start_data_transformation(self,
                                  data_ingestion_artifact: DataIngestionArtifact,
                                  data_validation_artifact: DataValidationArtifact
                                  ) -> DataTransformationArtifact:
        try:
            data_transformation = DataTransformation(
                data_transformation_config=self.config.get_data_transformation_config(),
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_artifact=data_validation_artifact
            )
            return data_transformation.initiate_data_transformation()
        except Exception as e:
            raise StudentException(e, sys)
    
    def start_model_trainer(self, data_transformation_artifact: DataTransformationArtifact) -> ModelTrainerArtifact:
        try:
            model_trainer = ModelTrainer(model_trainer_config=self.config.get_model_trainer_config(),
                                         data_transformation_artifact=data_transformation_artifact
                                         )
            return model_trainer.initiate_model_trainer()
        except Exception as e:
            raise StudentException(e, sys) from e
    
    def start_model_evaluation(self, data_ingestion_artifact: DataIngestionArtifact,
                               data_validation_artifact: DataValidationArtifact,
                               model_trainer_artifact: ModelTrainerArtifact) -> ModelEvaluationArtifact:
        try:
            model_eval = ModelEvaluation(
                model_evaluation_config=self.config.get_model_evaluation_config(),
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_artifact=data_validation_artifact,
                model_trainer_artifact=model_trainer_artifact)
            return model_eval.initiate_model_evaluation()
        except Exception as e:
            raise StudentException(e, sys) from e

        
    
    def run_pipeline(self):
        try:
            
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_artifact=data_validation_artifact
            )
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)
    
        except Exception as e:
          raise StudentException(e, sys) from e
           


    def run(self):
        try:
            self.run_pipeline()
        except Exception as e:
            raise e
        
    
    