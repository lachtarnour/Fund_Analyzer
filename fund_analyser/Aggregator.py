import os
from typing import List
import pandas as pd
import numpy as np
from fund_analyser.Indicators import BaseIndicator
from fund_analyser.utils import logger

# Get the timezone from environment, default to UTC
TIMEZONE = os.environ.get("TIMEZONE", "UTC")

class FinancialIndicatorsAggregator:
    def __init__(self, indicators: List[BaseIndicator]):
        self.indicators = indicators

    @staticmethod
    def get_periods(as_of=None, tz=None):
        # All calculations in UTC
        if as_of is not None:
            end_date = pd.Timestamp(as_of)
            if end_date.tzinfo is None:
                end_date = end_date.tz_localize("UTC")
            else:
                end_date = end_date.tz_convert("UTC")
        else:
            end_date = pd.Timestamp.utcnow().normalize()

        periods = {
            "YTD": end_date.replace(month=1, day=1),
            "3M": end_date - pd.DateOffset(months=3),
            "6M": end_date - pd.DateOffset(months=6),
            "1Y": end_date - pd.DateOffset(years=1),
            "3Y": end_date - pd.DateOffset(years=3),
        }
        # If user requests a timezone, convert at the end (optional)
        if tz and tz.upper() != "UTC":
            for k in periods:
                periods[k] = periods[k].tz_convert(tz)
        return periods

    def compute_all(self, df: pd.DataFrame, as_of=None):
        if df is None or df.empty or "Date" not in df.columns or "Close" not in df.columns:
            logger.warning("Input DataFrame is empty or missing required columns.")
            return {period: {indicator.name: None for indicator in self.indicators} for period in self.get_periods(tz=TIMEZONE).keys()}

        df = df.sort_values("Date")
        # Always localize to UTC at ingestion
        if not pd.api.types.is_datetime64_any_dtype(df["Date"]):
            df["Date"] = pd.to_datetime(df["Date"])
        if df["Date"].dt.tz is None:
            df["Date"] = df["Date"].dt.tz_localize("UTC")

        tz = TIMEZONE
        # Allow conversion to a user-specified timezone if not UTC
        if tz and tz.upper() != "UTC":
            df["Date"] = df["Date"].dt.tz_convert(tz)

        end = pd.Timestamp(as_of) if as_of else df["Date"].max()
        if end.tzinfo is None:
            end = end.tz_localize(df["Date"].dt.tz)
        else:
            end = end.tz_convert(df["Date"].dt.tz)

        periods = self.get_periods(as_of or end, tz)
        results = {}

        for period_name, start in periods.items():
            mask = (df["Date"] >= start) & (df["Date"] <= end)
            period_df = df.loc[mask]
            res = {}
            if period_df.shape[0] < 2 or period_df["Close"].dropna().shape[0] < 2:
                for indicator in self.indicators:
                    res[indicator.name] = None
            else:
                for indicator in self.indicators:
                    try:
                        value = indicator.compute(period_df)
                        # Always return float or None
                        if isinstance(value, pd.Series):
                            value = value.iloc[0]
                        if pd.isna(value):
                            value = None
                        elif isinstance(value, (np.floating, np.integer)):
                            value = float(value)
                        res[indicator.name] = value
                    except Exception as e:
                        logger.warning(f"Error for {indicator.name} on {period_name}: {e}")
                        res[indicator.name] = None
            results[period_name] = res
        return results
