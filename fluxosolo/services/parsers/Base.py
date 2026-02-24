from abc import ABC, abstractmethod
import pandas as pd

class BaseParser(ABC):
    DB_columns = ['date', 'transaction', 'details', 'value', 'bank', 'category']

    
    def parser(self, filepath: str) -> pd.DataFrame:
        
        raw_df = self._extract_data(filepath)
        clean_df = self._standardize_structure(raw_df)

        return clean_df


    @abstractmethod
    def _extract_data(self, filepath: str) -> pd.DataFrame:
        pass


    def _standardize_structure(self, df: pd.DataFrame) -> pd.DataFrame:

        if not set(self.DB_columns).issubset(df.columns):
            raise ValueError(f"Parser don't return the required columns {self.DB_columns}")

        return df[self.DB_columns].copy()
