"""
Split monthly sales data into training, validation and testing datasets.
Run this script to generate evidence files for Assignment Task 1.

Usage:
    python prepare_datasets.py
"""

from pathlib import Path

import pandas as pd

from sales_forecasting import load_sales_data, build_monthly_series

TRAIN_RATIO = 0.70
VAL_RATIO = 0.15
# Remaining 15% is used for testing


def split_monthly_series(monthly: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    n = len(monthly)
    train_end = int(n * TRAIN_RATIO)
    val_end = train_end + int(n * VAL_RATIO)

    train = monthly.iloc[:train_end].copy()
    validation = monthly.iloc[train_end:val_end].copy()
    test = monthly.iloc[val_end:].copy()
    return train, validation, test


def main() -> None:
    input_path = Path("stores_sales_forecasting.csv")
    output_dir = Path("datasets")
    output_dir.mkdir(exist_ok=True)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    df = load_sales_data(input_path)
    monthly = build_monthly_series(df)
    train, validation, test = split_monthly_series(monthly)

    train.to_csv(output_dir / "train_monthly_sales.csv")
    validation.to_csv(output_dir / "validation_monthly_sales.csv")
    test.to_csv(output_dir / "test_monthly_sales.csv")

    summary = pd.DataFrame(
        {
            "Dataset": ["Training", "Validation", "Testing", "Total"],
            "Months": [len(train), len(validation), len(test), len(monthly)],
            "Start": [
                train.index.min().strftime("%Y-%m"),
                validation.index.min().strftime("%Y-%m") if len(validation) else "-",
                test.index.min().strftime("%Y-%m") if len(test) else "-",
                monthly.index.min().strftime("%Y-%m"),
            ],
            "End": [
                train.index.max().strftime("%Y-%m"),
                validation.index.max().strftime("%Y-%m") if len(validation) else "-",
                test.index.max().strftime("%Y-%m") if len(test) else "-",
                monthly.index.max().strftime("%Y-%m"),
            ],
        }
    )
    summary.to_csv(output_dir / "dataset_split_summary.csv", index=False)

    print("Dataset split complete:")
    print(summary.to_string(index=False))
    print(f"\nFiles saved in: {output_dir.resolve()}")


if __name__ == "__main__":
    main()
