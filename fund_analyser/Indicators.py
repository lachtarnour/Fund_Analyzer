from abc import ABC, abstractmethod
import pandas as pd
from typing import List
import numpy as np

class BaseIndicator(ABC):
    @abstractmethod
    def compute(self, df: pd.DataFrame) -> float:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    def check_df_valid(self, df: pd.DataFrame, columns: List[str], min_length: int = 2) -> bool:
        # Checks that required columns exist and have enough non-null values
        for col in columns:
            if col not in df.columns:
                return False
            if df[col].dropna().shape[0] < min_length:
                return False
        return True

class PerformanceIndicator(BaseIndicator):
    """Performance as (last close / first close) - 1."""
    @property
    def name(self):
        return "performance"
    
    def compute(self, df):
        # Validate input data
        if not self.check_df_valid(df, columns=["Close"], min_length=2):
            return np.nan
        close = df["Close"].dropna()
        # (last close / first close) - 1
        return (close.iloc[-1] / close.iloc[0]) - 1


class VolatilityIndicator(BaseIndicator):
    """Annualized volatility based on daily log returns."""
    @property
    def name(self):
        return "volatility"
    
    def compute(self, df):
        if not self.check_df_valid(df, columns=["Close"], min_length=2):
            return np.nan
        close = df["Close"].dropna()
        returns = np.log(close).diff().dropna()
        if returns.empty:
            return np.nan
        return returns.std() * np.sqrt(252)

class AnnualizedReturnIndicator(BaseIndicator):
    """Annualized return based on period length."""
    @property
    def name(self):
        return "annualized_return"
    
    def compute(self, df):
        if not self.check_df_valid(df, columns=["Close", "Date"], min_length=2):
            return np.nan
        close = df["Close"].dropna()
        dates = pd.to_datetime(df.loc[close.index, "Date"])
        dt = (dates.iloc[-1] - dates.iloc[0]).days
        if dt <= 0:
            return np.nan
        total_return = close.iloc[-1] / close.iloc[0]
        return total_return ** (365.25 / dt) - 1

class MaxDrawdownIndicator(BaseIndicator):
    """Maximum drawdown as minimum drop from previous highs."""
    @property
    def name(self):
        return "max_drawdown"
    
    def compute(self, df):
        if not self.check_df_valid(df, columns=["Close"], min_length=2):
            return np.nan
        close = df["Close"].dropna()
        running_max = close.cummax()
        drawdown = close / running_max - 1
        return drawdown.min()
    
    