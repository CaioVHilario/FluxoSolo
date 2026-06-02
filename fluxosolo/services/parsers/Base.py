from abc import ABC, abstractmethod
from typing import ClassVar

import pandas as pd


class BaseParser(ABC):
    DB_columns: ClassVar[list[str]] = [
        "date",
        "transaction_type",
        "details",
        "value",
        "bank",
        "category",
    ]

    def parser(self, bytes_content: bytes) -> pd.DataFrame:

        raw_df = self._extract_data(bytes_content)
        return self._standardize_structure(raw_df)

    @abstractmethod
    def _extract_data(self, bytes_content: bytes) -> pd.DataFrame:
        pass

    def _standardize_structure(self, df: pd.DataFrame) -> pd.DataFrame:

        if not set(self.DB_columns).issubset(df.columns):
            raise ValueError(
                f"Parser don't return the required columns {self.DB_columns}"
            )

        return df[self.DB_columns].copy()
