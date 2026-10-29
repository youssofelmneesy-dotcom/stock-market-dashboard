
from pathlib import Path

import pandas as pd
import requests
import yfinance as yf
from bs4 import BeautifulSoup


BASE_DIR = Path(__file__).resolve().parent
REVENUE_DIR = BASE_DIR / "data" / "revenue"


def parse_revenue(value):
    """Convert formatted revenue values to numbers."""

    text = str(value).strip().replace(",", "").replace("$", "")

    if not text or text.lower() in {"nan", "none", "-", "n/a"}:
        return None

    multiplier = 1

    if text[-1:].upper() == "T":
        multiplier = 1_000_000_000_000
        text = text[:-1]
    elif text[-1:].upper() == "B":
        multiplier = 1_000_000_000
        text = text[:-1]
    elif text[-1:].upper() == "M":
        multiplier = 1_000_000
        text = text[:-1]
    elif text[-1:].upper() == "K":
        multiplier = 1_000
        text = text[:-1]

    try:
        return float(text) * multiplier
    except ValueError:
        return None


def scrape_revenue(ticker: str) -> pd.DataFrame:
    """Try to scrape quarterly revenue from Stock Analysis."""

    url = (
        f"https://stockanalysis.com/stocks/"
        f"{ticker.lower()}/revenue/?p=quarterly"
    )

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=20,
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table")

        if table is not None:
            rows = []

            for row in table.select("tbody tr"):
                cells = row.find_all("td")

                if len(cells) < 2:
                    continue

                date = pd.to_datetime(
                    cells[0].get_text(strip=True),
                    errors="coerce",
                )

                revenue = parse_revenue(
                    cells[1].get_text(strip=True)
                )

                if pd.notna(date) and revenue is not None:
                    rows.append({
                        "Date": date,
                        "Revenue": revenue,
                        "Source": "Stock Analysis",
                    })

            if rows:
                return (
                    pd.DataFrame(rows)
                    .drop_duplicates(subset=["Date"])
                    .sort_values("Date")
                    .reset_index(drop=True)
                )

    except requests.RequestException as error:
        print(f"Scraping failed for {ticker}: {error}")

    print(f"Trying Yahoo Finance revenue data for {ticker}...")
    return get_revenue_from_yfinance(ticker)


def get_revenue_from_yfinance(ticker: str) -> pd.DataFrame:
    """Get quarterly total revenue from Yahoo Finance."""

    company = yf.Ticker(ticker)
    statements = company.quarterly_income_stmt

    if statements.empty:
        return pd.DataFrame(
            columns=["Date", "Revenue", "Source"]
        )

    revenue_rows = [
        row for row in statements.index
        if str(row).strip().lower() == "total revenue"
    ]

    if not revenue_rows:
        revenue_rows = [
            row for row in statements.index
            if "revenue" in str(row).lower()
        ]

    if not revenue_rows:
        return pd.DataFrame(
            columns=["Date", "Revenue", "Source"]
        )

    series = statements.loc[revenue_rows[0]]

    data = pd.DataFrame({
        "Date": pd.to_datetime(series.index),
        "Revenue": pd.to_numeric(
            series.values,
            errors="coerce",
        ),
        "Source": "Yahoo Finance",
    })

    return (
        data.dropna(subset=["Date", "Revenue"])
        .drop_duplicates(subset=["Date"])
        .sort_values("Date")
        .reset_index(drop=True)
    )


def save_revenue_data(
    ticker: str,
    data: pd.DataFrame,
) -> Path:
    """Save quarterly revenue as CSV."""

    REVENUE_DIR.mkdir(parents=True, exist_ok=True)

    file_path = REVENUE_DIR / f"{ticker.lower()}_revenue_data.csv"
    data.to_csv(file_path, index=False)

    return file_path


def download_all_revenues() -> dict:
    """Extract and save quarterly revenue for all companies."""

    from stock_data import COMPANIES

    results = {}

    for company, ticker in COMPANIES.items():
        try:
            data = scrape_revenue(ticker)
            file_path = save_revenue_data(ticker, data)

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
    results = download_all_revenues()

    for company, result in results.items():
        print(f"\n--- {company} ({result['ticker']}) ---")

        if result["error"]:
            print("Error:", result["error"])
            continue

        print(result["data"].tail())
        print("Saved to:", result["file"])


