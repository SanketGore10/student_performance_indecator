import sys
import os
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer #use to create pipeline
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.exception import CustomException
from src.logger import logging
from src.utils import save_obj

@dataclass
class DataTransformatonConfig:
    preprocessor_obj_path = os.path.join('artifact', "Preprocessor.pkl") # use to save preprocessor pickel file to this path

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformatonConfig()

    def get_dataTransformer_object(self):
        try:
            num_feature = ["writing_score", "reading_score"]
            cat_feature = ["gender", 
                           "race_ethnicity", 
                           "parentel_level_of_education",
                           "lunch", 
                           "test_preparation_course"
                           ]
            
            #creating pipeline to transform the data

            num_pipe = Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler())
                    ]
                )
            
            logging.info("Numerical feature Scaling completed")
            
            logging.info(f"Numerical Feature: {num_feature}")

            cat_pip = Pipeline(
               
                steps=[
                    ("imputer",SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder",OneHotEncoder()),
                    ("scaler",StandardScaler(with_mean=False))
                ]
                
            )
            
            logging.info("Categorical feature encoding completed")
            
            logging.info(f"Categorical Feature: {cat_feature}")

            preprocessor = ColumnTransformer(
                [
                    ("num_pipe", num_pipe, num_feature),
                    ("cat_pipe",cat_pip,cat_feature)
                ]
            )
            return preprocessor
            
        except Exception as e:
            raise CustomException(e,sys)

    def initiate_data_transformation(self,train_path,test_path):

        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            
            logging.info("train and test dataset is read")

            logging.info("Obtaining preprocessor object")
            
            preprocessor_obj = self.get_dataTransformer_object()
            target_col = "math_score"
                       
            input_feature_train_df = train_df.drop(columns=[target_col],axis=1)
            target_feature_train_df = train_df[target_col]

            input_feature_test_df = test_df.drop(columns=[target_col],axis=1)
            target_feature_test_df = test_df[target_col]

            logging.info("Applying Preprocessor obj on train test data")
            logging.info(type(input_feature_train_df))
            
            #input_feature_train_df = pd.DataFrame(input_feature_train_df)
            input_feature_train_arr = preprocessor_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessor_obj.transform(input_feature_test_df)

            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]
           
            save_obj(
                file_path = self.data_transformation_config.preprocessor_obj_path,
                obj = preprocessor_obj
            ) 
            
            logging.info("Saved Preprocessing Object")

            return (train_arr, test_arr, self.data_transformation_config.preprocessor_obj_path)

        except Exception as e:
            raise CustomException(e,sys)
