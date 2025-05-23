import os
import requests
import yfinance as yf
import pandas as pd
from dotenv import load_dotenv
import pytz
from datetime import datetime
from fund_analyser.utils import logger

# --- Env setup ---
load_dotenv()
OPENFIGI_API_KEY = os.environ.get("OPENFIGI_API_KEY", "775b5750-1e5f-42f8-88b6-000ccbb6a577")
TIMEZONE = os.environ.get("TIMEZONE", "Europe/Paris")

def isin_to_tickers(isin: str) -> list:
    """Query OpenFIGI to get possible tickers for an ISIN."""
    url = "https://api.openfigi.com/v3/mapping"
    headers = {
        "Content-Type": "application/json",
        "X-OPENFIGI-APIKEY": OPENFIGI_API_KEY,
    }
    data = [{"idType": "ID_ISIN", "idValue": isin}]
    try:
        response = requests.post(url, json=data, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception as e:
        logger.error(f"OpenFIGI request failed: {e}")
        return []
    results = response.json()
    if not results or not results[0].get('data'):
        logger.warning(f"No ticker found for ISIN {isin}.")
        return []
    tickers = []
    for d in results[0]['data']:
        if 'ticker' in d and 'exchCode' in d:
            tickers.append(f"{d['ticker']}.{d['exchCode']}")
        elif 'ticker' in d:
            tickers.append(d['ticker'])
    return tickers

def select_yahoo_ticker(tickers: list) -> str | None:
    """Select the ticker."""
    for t in tickers:
        if t.endswith(".PA"):
            return t
    for t in tickers:
        if t.endswith(".FP"):
            return t.replace(".FP", ".PA")
    for t in tickers:
        if '.' not in t and t.isalnum():
            return t
    return tickers[0] if tickers else None

def fetch_yahoo_history(ticker, start="2023-01-01", end=None, tz=TIMEZONE):
    """
    Download price history from Yahoo Finance.
    'end' is excluded.
    """
    tzinfo = pytz.timezone(tz)
    if end is None:
        end = datetime.now(tzinfo).strftime("%Y-%m-%d")
    logger.info(f"Downloading {ticker} from {start} to {end} (end excluded), timezone: {tz}")
    df = yf.download(ticker, start=start, end=end, progress=False)
    if df.empty:
        logger.warning(f"No Yahoo data for {ticker}.")
        return None
    df.reset_index(inplace=True)
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"]).dt.tz_localize("UTC").dt.tz_convert(tzinfo)
    return df[["Date", "Close"]]

def fetch data(isin, start="2023-01-01", end=None):
    """ISIN -> ticker -> Yahoo Finance history."""
    tickers = isin_to_tickers(isin)
    if not tickers:
        return None
    ticker_yahoo = select_yahoo_ticker(tickers)
    if not ticker_yahoo:
        logger.error(f"No Yahoo ticker usable for ISIN {isin}.")
        return None
    logger.info(f"Selected Yahoo ticker: {ticker_yahoo}")
    return fetch_yahoo_history(ticker_yahoo, start, end)



