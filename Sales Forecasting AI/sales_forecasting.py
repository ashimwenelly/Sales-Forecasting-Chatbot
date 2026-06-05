import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing


def load_sales_data(csv_path: Path) -> pd.DataFrame:
    try:
        df = pd.read_csv(csv_path, parse_dates=["Order Date"], dayfirst=False, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(csv_path, parse_dates=["Order Date"], dayfirst=False, encoding="latin1")

    df = df.dropna(subset=["Order Date", "Sales", "Quantity"])
    df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df = df.dropna(subset=["Sales", "Quantity"])
    return df


def build_monthly_series(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["Order Month"] = df["Order Date"].dt.to_period("M").dt.to_timestamp()
    monthly = (
        df.groupby("Order Month")[['Sales', 'Quantity']]
          .sum()
          .sort_index()
    )
    monthly.index.name = 'Period'
    return monthly


def fit_forecast(series: pd.Series, periods: int) -> pd.Series:
    model = ExponentialSmoothing(
        series,
        trend="add",
        seasonal="add",
        seasonal_periods=12,
        initialization_method="estimated",
    )
    fitted = model.fit(optimized=True)
    forecast = fitted.forecast(periods)
    return forecast


def create_forecast_report(monthly: pd.DataFrame, forecast_months: int) -> pd.DataFrame:
    sales_forecast = fit_forecast(monthly['Sales'], forecast_months)
    quantity_forecast = fit_forecast(monthly['Quantity'], forecast_months)

    forecast_index = pd.date_range(
        start=monthly.index.max() + pd.offsets.MonthBegin(1),
        periods=forecast_months,
        freq='MS',
    )

    output = pd.DataFrame({
        'Sales Forecast': sales_forecast.values,
        'Quantity Forecast': quantity_forecast.values,
    }, index=forecast_index)
    output.index.name = 'Month'
    return output


def plot_forecast(monthly: pd.DataFrame, forecast: pd.DataFrame, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(2, 1, figsize=(12, 9), sharex=True)

    monthly['Sales'].plot(ax=ax[0], label='Historical Sales', marker='o')
    forecast['Sales Forecast'].plot(ax=ax[0], label='Forecasted Sales', marker='x')
    ax[0].set_title('Monthly Revenue Forecast')
    ax[0].set_ylabel('Revenue')
    ax[0].legend()

    monthly['Quantity'].plot(ax=ax[1], label='Historical Quantity', marker='o')
    forecast['Quantity Forecast'].plot(ax=ax[1], label='Forecasted Quantity', marker='x')
    ax[1].set_title('Monthly Quantity Forecast')
    ax[1].set_ylabel('Quantity')
    ax[1].legend()

    fig.tight_layout()
    plot_path = output_dir / 'sales_quantity_forecast.png'
    fig.savefig(plot_path)
    plt.close(fig)
    print(f"Saved forecast chart to: {plot_path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Train a sales forecasting model and predict future sales and quantity.'
    )
    parser.add_argument(
        '--input',
        type=Path,
        default=Path('stores_sales_forecasting.csv'),
        help='Path to the input sales CSV file.',
    )
    parser.add_argument(
        '--months',
        type=int,
        default=12,
        help='Number of future months to forecast.',
    )
    parser.add_argument(
        '--output',
        type=Path,
        default=Path('forecast_results.csv'),
        help='Path where the forecast output CSV will be saved.',
    )
    parser.add_argument(
        '--plot-dir',
        type=Path,
        default=Path('forecast_plots'),
        help='Directory where forecast plots will be saved.',
    )
    args = parser.parse_args()

    if not args.input.exists():
        raise FileNotFoundError(f'Input file not found: {args.input}')

    print(f'Loading data from: {args.input}')
    df = load_sales_data(args.input)
    monthly = build_monthly_series(df)

    print('Training forecasting models...')
    forecast = create_forecast_report(monthly, args.months)

    forecast.to_csv(args.output, index=True, float_format='%.2f')
    print(f'Saved forecast results to: {args.output}')

    plot_forecast(monthly, forecast, args.plot_dir)

    print('\nForecast for next {0} months:'.format(args.months))
    print(forecast.round(2).to_string())


if __name__ == '__main__':
    main()
