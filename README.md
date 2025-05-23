# Fund Analyzer

**Fund Analyzer** is a modular Python tool for automatic computation of key financial indicators (performance, volatility, annualized return, max drawdown, etc.) for any fund or ETF, given just an ISIN code.

---

## Features

- Fetches historical price data from Yahoo Finance based on ISIN (using the OpenFIGI API).
- Automatically computes multiple financial indicators over several time windows:  
  _YTD_, _3 months_, _6 months_, _1 year_, _3 years_.
- Outputs results as JSON, easily usable in dashboards or APIs.
- Full support for timezones (configurable with `TIMEZONE` environment variable).
- Modular and extensible architecture (add your own indicators easily).

---

## Project Structure
fund_analyser/
│
├── Aggregator.py      # Main orchestrator: periods, calculation, JSON export
├── fetch_data.py      # ISIN → ticker → Yahoo price history
├── Indicators.py      # Performance, Volatility, Annualized Return, Max Drawdown, etc.
├── utils.py           # Logger setup
│
├── main.py            # Example pipeline script (entry point)
│
└── README.md