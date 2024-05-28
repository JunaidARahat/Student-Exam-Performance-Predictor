import os
import sys

from student.exception import StudentException
from student.utils.main_utils import load_object

import pandas as pd


class StudentData:

    def __init__(self, gender: str,
                ethnicity : str,
                parental_level_of_education : str,
                lunch: str,
                test_preparation_course: str,
                reading_score : int,
                writing_score : int,
                math_score : int = None 
                ):
        try:
            self.gender = gender
            self.ethnicity = ethnicity
            self.parental_level_of_education = parental_level_of_education
            self.lunch = lunch
            self.test_preparation_course = test_preparation_course
            self.reading_score = reading_score
            self.writing_score = writing_score
            self.math_score = math_score

        except Exception as e:
            raise StudentException(e, sys) from e

    def get_student_input_data_frame(self):

        try:
            student_input_dict = self.get_student_data_as_dict()
            return pd.DataFrame(student_input_dict)
        except Exception as e:
            raise StudentException(e, sys) from e

    def get_student_data_as_dict(self):
        try:
            input_data = {
                "gender": [self.gender],
                "race/ethnicity": [self.ethnicity],
                "parental level of education": [self.parental_level_of_education],
                "lunch": [self.lunch],
                "test preparation course": [self.test_preparation_course],
                "reading score": [self.reading_score],
                "writing score": [self.writing_score],
                }
            return input_data
        except Exception as e:
            raise StudentException(e, sys)


class predictor:

    def __init__(self, model_dir: str):
        try:
            self.model_dir = model_dir
        except Exception as e:
            raise StudentException(e, sys) from e

    def get_latest_model_path(self):
        try:
            folder_name = list(map(int, os.listdir(self.model_dir)))
            latest_model_dir = os.path.join(self.model_dir, f"{max(folder_name)}")
            file_name = os.listdir(latest_model_dir)[0]
            latest_model_path = os.path.join(latest_model_dir, file_name)
            return latest_model_path
        except Exception as e:
            raise StudentException(e, sys) from e

    def predict(self, X):
        try:
            model_path = self.get_latest_model_path()
            model = load_object(file_path=model_path)
            predited_value = model.predict(X)
            return predited_value
        except Exception as e:
            raise StudentException(e, sys) from e