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

## Installation

### 1. Clone the repository
```bash
git clone <repository_link>
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. (Optional) Configure environment variables

- To set the timezone (default: UTC):
```bash
export TIMEZONE="Europe/Paris"
```
- To use your own OpenFIGI API key:
```bash
export OPENFIGI_API_KEY="your_api_key"
```

---

## Usage

### Main Script

Run the main script:

```bash
python main.py
```

This will:
- Download data for a given ISIN
- Compute all indicators for multiple periods
- Save the results as JSON (`indicators_results.json`)

---

### Customization

Edit `main.py` to:
- Change the ISIN
- Change the analysis period (`start`, `end`)
- Add or remove indicators from the list

---

## Example Output

```json
{
  "YTD": {
    "performance": 0.045,
    "volatility": 0.18,
    "annualized_return": 0.042,
    "max_drawdown": -0.09
  },
  "3M": {
    "performance": 0.012,
    "volatility": 0.14
  }
}
```

---

## Adding a New Indicator

To add a custom indicator, create a new class that inherits from `BaseIndicator` in `Indicators.py` and implement the `compute(df)` method:

```python
class MyCustomIndicator(BaseIndicator):
    @property
    def name(self):
        return "my_custom_indicator"
    def compute(self, df):
        # custom calculation
        return ...
```

Then add your indicator to the `indicators` list in `main.py`.

