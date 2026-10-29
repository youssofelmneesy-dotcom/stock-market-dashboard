# Stock Market Dashboard 📈

An interactive Python dashboard for exploring historical stock prices and quarterly revenue for Tesla, Amazon, AMD, and GameStop.

The project combines data extraction, data processing, CSV storage, interactive visualization, and dashboard development.

## Features

- **Stock Data Extraction:** Retrieve historical daily stock data using `yfinance`.
- **Quarterly Revenue Extraction:** Collect quarterly revenue data using web scraping, with Yahoo Finance as a fallback source.
- **Data Storage:** Save extracted stock and revenue data as CSV files.
- **Interactive Visualizations:** Explore stock prices and quarterly revenue using Plotly.
- **Company Overview:** View stock price and revenue charts together.
- **Stock Performance Comparison:** Compare the relative historical performance of the selected companies.
- **Interactive Dashboard:** Select companies, refresh data, and inspect the underlying datasets through Streamlit.

## Companies Covered

| Company                | Ticker |
| ---------------------- | ------ |
| Tesla                  | TSLA   |
| Amazon                 | AMZN   |
| Advanced Micro Devices | AMD    |
| GameStop               | GME    |

## Technologies Used

- Python
- Pandas
- yfinance
- Requests
- Beautiful Soup
- Plotly
- Streamlit
- HTML parsing with lxml
- CSV data storage

## Project Structure

```text
Stock Market Dashboard/
├── app.py
├── stock_data.py
├── revenue_data.py
├── visualization.py
├── requirements.txt
└── data/
    ├── stock/
    └── revenue/
```

- `stock_data.py`: Retrieves and saves historical stock data.
- `revenue_data.py`: Extracts quarterly revenue and saves it to CSV files.
- `visualization.py`: Creates interactive charts and stock comparisons.
- `app.py`: Connects the components and displays the Streamlit dashboard.
- `requirements.txt`: Lists the Python dependencies.
- `data/`: Stores the extracted datasets.

## Installation

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd "Stock Market Dashboard"
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your repository URL.

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

### 3. Activate the environment

**macOS / Linux**

```bash
source .venv/bin/activate
```

**Windows**

```bash
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

## Usage

### Extract stock data

```bash
python stock_data.py
```

### Extract quarterly revenue

```bash
python revenue_data.py
```

### Launch the dashboard

```bash
streamlit run app.py
```

Streamlit will provide a local URL, usually `http://localhost:8501`.

## Data Sources

- Yahoo Finance through `yfinance`
- Stock Analysis through HTTP requests and Beautiful Soup, when accessible

If web scraping is blocked or unavailable, the revenue extraction module attempts to retrieve quarterly revenue from Yahoo Finance.

Data availability and completeness depend on the external providers.

## Notes and Limitations

- Historical stock prices and quarterly revenue represent different financial measures.
- Revenue data may be unavailable for some companies or reporting periods.
- External websites may change their page structure or restrict automated requests.
- Stock data and revenue data may have different reporting dates and update schedules.
- This project is intended for educational and analytical purposes. It is not financial advice.

## Future Improvements

- Add date-range filters.
- Add downloadable CSV exports from the dashboard.
- Improve data validation and error reporting.
- Add more companies and financial indicators.
- Add automated tests and a more robust data-refresh workflow.

## Author

Developed as a Python data analysis and visualization project.


