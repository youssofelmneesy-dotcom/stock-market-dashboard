
from pathlib import Path

import pandas as pd
import yfinance as yf


BASE_DIR = Path(__file__).resolve().parent
STOCK_DIR = BASE_DIR / "data" / "stock"

COMPANIES = {
    "Tesla": "TSLA",
    "Amazon": "AMZN",
    "AMD": "AMD",
    "GameStop": "GME",
}


def get_stock_data(ticker: str) -> pd.DataFrame:
    """Download the maximum available daily stock history."""

    stock = yf.Ticker(ticker)
    data = stock.history(period="max", auto_adjust=False)

    if data.empty:
        raise ValueError(f"No stock data found for {ticker}")

    data = data.reset_index()

    if "Date" not in data.columns and "Datetime" in data.columns:
        data = data.rename(columns={"Datetime": "Date"})

    data["Date"] = (
        pd.to_datetime(data["Date"], utc=True)
        .dt.tz_localize(None)
    )

    return data


def save_stock_data(ticker: str, data: pd.DataFrame) -> Path:
    """Save stock history as a CSV file."""

    STOCK_DIR.mkdir(parents=True, exist_ok=True)

    file_path = STOCK_DIR / f"{ticker.lower()}_stock_data.csv"
    data.to_csv(file_path, index=False)

    return file_path


def download_all_stocks() -> dict:
    """Download and save stock history for all companies."""

    results = {}

    for company, ticker in COMPANIES.items():
        try:
            data = get_stock_data(ticker)
            file_path = save_stock_data(ticker, data)

            results[company] = {
                "ticker": ticker,
                "data": data,
                "file": str(file_path),
                "error": None,
            }

        except Exception as error:
            results[company] = {
                "ticker": ticker,
                "data": pd.DataFrame(),
                "file": None,
                "error": str(error),
            }

    return results


if __name__ == "__main__":
    results = download_all_stocks()

    for company, result in results.items():
        print(f"\n--- {company} ({result['ticker']}) ---")

        if result["error"]:
            print("Error:", result["error"])
            continue

        data = result["data"]

        print(data.head())
        print("Data shape:", data.shape)
        print("Saved to:", result["file"])
