import os
from fund_analyser.fetch_data import fetch_data
from fund_analyser.Indicators import (
    PerformanceIndicator,
    VolatilityIndicator,
    AnnualizedReturnIndicator,
    MaxDrawdownIndicator,
)
from fund_analyser.Aggregator import FinancialIndicatorsAggregator

def main():
    #parameters
    isin = "IE0002XZSHO1"
    start = "2022-01-01"
    end = "2025-04-01"

    #fetch_data
    df = fetch_data(isin, start, end)

    #initilize indicators
    indicators = [
        PerformanceIndicator(),
        VolatilityIndicator(),
        AnnualizedReturnIndicator(),
        MaxDrawdownIndicator(),
    ]

    #initialize the aggregator 
    aggregator = FinancialIndicatorsAggregator(indicators)

    #calculate indicators
    results = aggregator.compute_all(df)

    #print results
    print("Computed results:")
    for period, result in results.items():
        print(f"Period: {period}")
        for indicator_name, value in result.items():
            print(f"  {indicator_name}: {value}")
    #save results to JSON
    output_path = "indicators_results.json"
    aggregator.save_results_json(output_path)
    print(f"Results saved to {output_path}")

if __name__ == "__main__":
    main()
