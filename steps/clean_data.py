import logging 
import pandas as pd
from zenml import step
from typing import Tuple
from typing_extensions import Annotated
from src.data_cleaning import DataCleaning,DataDivideStrategy,DataPreProcessStrategy


@step
def clean_df(df: pd.DataFrame) -> Tuple[
    Annotated[pd.DataFrame, "X_train"],
    Annotated[pd.DataFrame, "X_test"],
    Annotated[pd.Series, "y_train"],
    Annotated[pd.Series, "y_test"],
]:
    try:
        # Preprocess the data using the DataPreProcessStrategy
        process_strategy = DataPreProcessStrategy()
        data_cleaning = DataCleaning(df, process_strategy)
        processed_data = data_cleaning.handle_data()

        # Divide the processed data into train and test sets using DataDivideStrategy
        divide_strategy = DataDivideStrategy()
        data_cleaning = DataCleaning(processed_data, divide_strategy)
        X_train, X_test, y_train, y_test = data_cleaning.handle_data()

        logging.info("Data cleaning and splitting completed")
    
        # Return the train and test splits
        return X_train, X_test, y_train, y_test
    
    except Exception as e:
        logging.error(f"Error in cleaning and splitting data: {e}")
        raise e
