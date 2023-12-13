import logging
import pandas as pd
import numpy as np
from sklearn.preprocessing import Normalizer, MinMaxScaler, StandardScaler

# Setting up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataCleaner:

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
    def drop_duplicate(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        drop duplicate rows
        """
        df.drop_duplicates(inplace=True)
        return df

    @log_decorator
    def convert_to_datetime(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        convert column to datetime
        """
        df[['start', 'end']] = df[['start', 'end']].apply(pd.to_datetime)
        return df

    @log_decorator
    def convert_to_string(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        convert columns to string
        """
        df[['bearer_id', 'imsi', 'msisdn/number', 'imei', 'handset_type']] = df[
            ['bearer_id', 'imsi', 'msisdn/number', 'imei', 'handset_type']].astype(str)
        return df

    @log_decorator
    def remove_whitespace_column(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        remove whitespace from columns
        """
        df.columns = [column.replace(' ', '_').lower() for column in df.columns]
        return df

    @log_decorator
    def percent_missing(self, df: pd.DataFrame) -> float:
        """
        calculate the percentage of missing values from dataframe
        """
        total_cells = np.product(df.shape)
        missing_count = df.isnull().sum()
        total_missing = missing_count.sum()
        return round(total_missing / total_cells * 100, 2)

    @log_decorator
    def get_numerical_columns(self, df: pd.DataFrame) -> list:
        """
        get numerical columns
        """
        return df.select_dtypes(include=['number']).columns.to_list()

    @log_decorator
    def get_categorical_columns(self, df: pd.DataFrame) -> list:
        """
        get categorical columns
        """
        return df.select_dtypes(include=['object', 'datetime64[ns]']).columns.to_list()

    @log_decorator
    def percent_missing_column(self, df: pd.DataFrame, col: str) -> float:
        """
        calculate the percentage of missing values for the specified column
        """
        try:
            col_len = len(df[col])
        except KeyError:
            logger.error(f"{col} not found")
            raise
        missing_count = df[col].isnull().sum()
        return round(missing_count / col_len * 100, 2)

    @log_decorator
    def fill_missing_values_categorical(self, df: pd.DataFrame, method: str) -> pd.DataFrame:
        """
        fill missing values with specified method
        """
        categorical_columns = df.select_dtypes(include=['object', 'datetime64[ns]']).columns

        if method == "ffill":
            for col in categorical_columns:
                df[col] = df[col].fillna(method='ffill')
            return df
        elif method == "bfill":
            for col in categorical_columns:
                df[col] = df[col].fillna(method='bfill')
            return df
        elif method == "mode":
            for col in categorical_columns:
                df[col] = df[col].fillna(df[col].mode()[0])
            return df
        else:
            logger.error("Method unknown")
            raise ValueError("Method unknown")

    @log_decorator
    def fill_missing_values_numeric(self, df: pd.DataFrame, method: str, columns: list = None) -> pd.DataFrame:
        """
        fill missing values with specified method
        """
        if columns is None:
            numeric_columns = self.get_numerical_columns(df)
        else:
            numeric_columns = columns

        if method == "mean":
            for col in numeric_columns:
                df[col].fillna(df[col].mean(), inplace=True)
        elif method == "median":
            for col in numeric_columns:
                df[col].fillna(df[col].median(), inplace=True)
        else:
            logger.error("Method unknown")
            raise ValueError("Method unknown")

        return df

    @log_decorator
    def remove_nan_categorical(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        remove columns with nan values for categorical columns
        """
        categorical_columns = self.get_categorical_columns(df)
        for col in categorical_columns:
            df = df[df[col] != 'nan']
        return df

    @log_decorator
    def normalizer(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        normalize numerical columns
        """
        norm = Normalizer()
        return pd.DataFrame(norm.fit_transform(df[self.get_numerical_columns(df)]), columns=self.get_numerical_columns(df))

    @log_decorator
    def min_max_scaler(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        scale numerical columns
        """
        minmax_scaler = MinMaxScaler()
        return pd.DataFrame(minmax_scaler.fit_transform(df[self.get_numerical_columns(df)]),
                            columns=self.get_numerical_columns(df))

    @log_decorator
    def standard_scaler(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        scale numerical columns
        """
        standard_scaler = StandardScaler()
        return pd.DataFrame(standard_scaler.fit_transform(df[self.get_numerical_columns(df)]),
                            columns=self.get_numerical_columns(df))

    @log_decorator
    def handle_outliers(self, df: pd.DataFrame, col: str, method: str = 'IQR') -> pd.DataFrame:
        """
        Handle Outliers of a specified column using Turkey's IQR method
        """
        df = df.copy()
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)

        lower_bound = q1 - ((1.5) * (q3 - q1))
        upper_bound = q3 + ((1.5) * (q3 - q1))
        if method == 'mode':
            df[col] = np.where(df[col] < lower_bound, df[col].mode()[0], df[col])
            df[col] = np.where(df[col] > upper_bound, df[col].mode()[0], df[col])
        elif method == 'median':
            df[col] = np.where(df[col] < lower_bound, df[col].median, df[col])
            df[col] = np.where(df[col] > upper_bound, df[col].median, df[col])
        else:
            df[col] = np.where(df[col] < lower_bound, lower_bound, df[col])
            df[col] = np.where(df[col] > upper_bound, upper_bound, df[col])

        return df
