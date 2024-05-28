from collections import namedtuple
from datetime import datetime
import uuid
from student.configuration import Configuartion
from student.logger import logging, get_log_file_name
from student.exception import StudentException
from threading import Thread
from typing import List

from multiprocessing import Process
from student.entity.artifact_entity import DataIngestionArtifact
from student.entity.artifact_entity import DataValidationArtifact
from student.components.data_ingestion import DataIngestion
from student.components.data_validation import DataValidation


import os, sys
from collections import namedtuple
from datetime import datetime
import pandas as pd



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
        
    
    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)

    
        except Exception as e:
          raise StudentException(e, sys) from e
           


    def run(self):
        try:
            self.run_pipeline()
        except Exception as e:
            raise e