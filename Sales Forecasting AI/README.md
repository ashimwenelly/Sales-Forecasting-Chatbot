# Sales Forecasting AI

This project contains a forecasting script that uses the `stores_sales_forecasting.csv` dataset to predict future monthly revenue and quantity sold.

## Files

- `stores_sales_forecasting.csv` - source transactional dataset
- `sales_forecasting.py` - Python script that trains a time series model and generates future forecasts
- `forecast_results.csv` - generated forecast output after running the script
- `forecast_plots/` - saved forecast charts
- `requirements.txt` - required Python packages

## Usage

1. Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

2. Run the forecasting script:

```powershell
python sales_forecasting.py --input stores_sales_forecasting.csv --months 12
```

3. Output files:

- `forecast_results.csv` - contains the next `N` months of predicted sales and quantity
- `forecast_plots/sales_quantity_forecast.png` - chart of historical data and forecasts

## How it works

- Reads `stores_sales_forecasting.csv`
- Aggregates sales and quantity by month
- Uses `statsmodels` `ExponentialSmoothing` to forecast the next months
- Writes predictions to CSV and saves a plot
