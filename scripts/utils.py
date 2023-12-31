import logging
from typing import Optional, Dict, Union
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Setting up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Utils:
    @staticmethod
    def log_decorator(func):
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                logger.info(f"{func.__name__} executed successfully.")
                return result
            except Exception as e:
                logger.error(f"Error in {func.__name__}: {str(e)}")
                raise
        return wrapper

    @log_decorator
    def load_data(self, data_path: str, dtype: Optional[Dict[str, Union[str, int, float]]] = None) -> pd.DataFrame:
        """
        Load data from a csv file.
        """
        try:
            df = pd.read_csv(data_path, dtype=dtype)
        except FileNotFoundError:
            logger.error("File not found.")
            raise
        return df

    @log_decorator
    def save_data(self, df: pd.DataFrame, data_path: str, index: bool = False) -> None:
        """
        Save data to a csv file.
        """
        try:
            df.to_csv(data_path, index=index)
            logger.info("Data saved successfully!")
        except Exception as e:
            logger.error(f"Saving failed: {str(e)}")
            raise
    
        # Function to calculate missing values by column
    @log_decorator
    def missing_values_table(self, df: pd.DataFrame) -> pd.DataFrame:
        # Total missing values
        mis_val = df.isnull().sum()

        # Percentage of missing values
        mis_val_percent = 100 * df.isnull().sum() / len(df)

        # dtype of missing values
        mis_val_dtype = df.dtypes

        # Make a table with the results
        mis_val_table = pd.concat([mis_val, mis_val_percent, mis_val_dtype], axis=1)

        # Rename the columns
        mis_val_table_ren_columns = mis_val_table.rename(
        columns = {0 : 'Missing Values', 1 : '% of Total Values', 2: 'Dtype'})

        # Sort the table by percentage of missing descending
        mis_val_table_ren_columns = mis_val_table_ren_columns[
            mis_val_table_ren_columns.iloc[:,1] != 0].sort_values(
        '% of Total Values', ascending=False).round(1)

        # Print some summary information
        print ("Your selected dataframe has " + str(df.shape[1]) + " columns.\n"      
            "There are " + str(mis_val_table_ren_columns.shape[0]) +
            " columns that have missing values.")

        # Return the dataframe with missing information
        return mis_val_table_ren_columns

    @staticmethod
    def format_float(value: float) -> str:
        return f'{value:,.2f}'

    def find_agg(self,df:pd.DataFrame, agg_column:str, agg_metric:str, col_name:str, top:int, order=False )->pd.DataFrame:
        
        new_df = df.groupby(agg_column)[agg_column].agg(agg_metric).reset_index(name=col_name).\
                            sort_values(by=col_name, ascending=order)[:top]
        
        return new_df

    def convert_bytes_to_megabytes(self,df, bytes_data):

        """
            This function takes the dataframe and the column which has the bytes values
            returns the megabytesof that value
            
            Args:
            -----
            df: dataframe
            bytes_data: column with bytes values
            
            Returns:
            --------
            A series
        """
        
        megabyte = 1*10e+5
        df[bytes_data] = df[bytes_data] / megabyte
        
        return df[bytes_data]

    def plot_hist(self, df: pd.DataFrame, column: str, color: str) -> None:
        """
        Plot a histogram with kernel density estimate for the specified column in the DataFrame.

        Parameters:
        - df (pd.DataFrame): The DataFrame containing the data.
        - column (str): The column for which the histogram is to be plotted.
        - color (str): The color of the histogram.

        Returns:
        - None
        """
        plt.figure(figsize=(12, 7))
        sns.histplot(data=df, x=column, color=color, kde=True)
        plt.title(f'Distribution of {column}', size=20, fontweight='bold')
        plt.xlabel(column.capitalize())  # Add x-axis label
        plt.ylabel('Frequency')  # Add y-axis label
        plt.grid(axis='y', linestyle='--', alpha=0.7)  # Add grid for better readability
        plt.show()

    def plot_count(self,df:pd.DataFrame, column:str) -> None:
        plt.figure(figsize=(12, 7))
        sns.countplot(data=df, x=column)
        plt.title(f'Distribution of {column}', size=20, fontweight='bold')
        plt.show()
        
    def plot_bar(self,df:pd.DataFrame, x_col:str, y_col:str, title:str, xlabel:str, ylabel:str)->None:
        plt.figure(figsize=(12, 7))
        sns.barplot(data = df, x=x_col, y=y_col)
        plt.title(title, size=20)
        plt.xticks(rotation=75, fontsize=14)
        plt.yticks( fontsize=14)
        plt.xlabel(xlabel, fontsize=16)
        plt.ylabel(ylabel, fontsize=16)
        plt.show()

    @log_decorator
    def plot_heatmap(self, df: pd.DataFrame, title: str, cbar: bool = False) -> None:
        plt.figure(figsize=(12, 7))
        sns.heatmap(df, annot=True, cmap='viridis', vmin=0, vmax=1, fmt='.2f', linewidths=.7, cbar=cbar)
        plt.title(title, size=18, fontweight='bold')
        plt.show()

    def plot_box(self,df:pd.DataFrame, x_col:str, title:str) -> None:
        plt.figure(figsize=(12, 7))
        sns.boxplot(data = df, x=x_col)
        plt.title(title, size=20)
        plt.xticks(rotation=75, fontsize=14)
        plt.show()

    def plot_box_multi(self,df:pd.DataFrame, x_col:str, y_col:str, title:str) -> None:
        plt.figure(figsize=(12, 7))
        sns.boxplot(data = df, x=x_col, y=y_col)
        plt.title(title, size=20)
        plt.xticks(rotation=75, fontsize=14)
        plt.yticks( fontsize=14)
        plt.show()

    @log_decorator
    def plot_scatter(self, df: pd.DataFrame, x_col: str, y_col: str, title: str, hue: str, style: str) -> None:
        plt.figure(figsize=(12, 7))
        sns.scatterplot(data=df, x=x_col, y=y_col, hue=hue, style=style)
        plt.title(title, size=20)
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        plt.show()