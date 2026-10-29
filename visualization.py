
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def create_stock_chart(
    stock_data: pd.DataFrame,
    company_name: str,
):
    """Create an interactive historical closing-price chart."""

    fig = px.line(
        stock_data,
        x="Date",
        y="Close",
        title=f"{company_name} — Historical Stock Price",
        labels={
            "Date": "Date",
            "Close": "Closing Price (USD)",
        },
    )

    fig.update_layout(
        template="plotly_white",
        hovermode="x unified",
    )

    return fig


def create_revenue_chart(
    revenue_data: pd.DataFrame,
    company_name: str,
):
    """Create an interactive quarterly-revenue chart."""

    fig = px.bar(
        revenue_data,
        x="Date",
        y="Revenue",
        title=f"{company_name} — Quarterly Revenue",
        labels={
            "Date": "Quarter",
            "Revenue": "Revenue (USD)",
        },
    )

    fig.update_layout(
        template="plotly_white",
        hovermode="x unified",
    )

    return fig


def create_company_overview(
    stock_data: pd.DataFrame,
    revenue_data: pd.DataFrame,
    company_name: str,
):
    """Show stock price and quarterly revenue in one figure."""

    fig = make_subplots(
        rows=2,
        cols=1,
        subplot_titles=(
            f"{company_name} — Closing Price",
            f"{company_name} — Quarterly Revenue",
        ),
        vertical_spacing=0.15,
    )

    fig.add_trace(
        go.Scatter(
            x=stock_data["Date"],
            y=stock_data["Close"],
            name="Closing Price",
            mode="lines",
        ),
        row=1,
        col=1,
    )

    if not revenue_data.empty:
        fig.add_trace(
            go.Bar(
                x=revenue_data["Date"],
                y=revenue_data["Revenue"],
                name="Quarterly Revenue",
            ),
            row=2,
            col=1,
        )

    fig.update_yaxes(title_text="Price (USD)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue (USD)", row=2, col=1)

    fig.update_layout(
        height=750,
        template="plotly_white",
        hovermode="x unified",
    )

    return fig


def create_stock_comparison(stock_datasets: dict):
    """Compare normalized stock performance across companies."""

    frames = []

    for company_name, stock_data in stock_datasets.items():
        if stock_data.empty:
            continue

        data = stock_data[["Date", "Close"]].copy()
        data = data.dropna(subset=["Close"])

        if data.empty:
            continue

        first_price = data["Close"].iloc[0]

        if first_price == 0:
            continue

        data["Indexed Price"] = data["Close"] / first_price * 100
        data["Company"] = company_name

        frames.append(data[["Date", "Indexed Price", "Company"]])

    if not frames:
        return None

    comparison = pd.concat(frames, ignore_index=True)

    fig = px.line(
        comparison,
        x="Date",
        y="Indexed Price",
        color="Company",
        title="Stock Performance Comparison",
        labels={
            "Date": "Date",
            "Indexed Price": "Indexed Price (first observation = 100)",
        },
    )

    fig.update_layout(
        template="plotly_white",
        hovermode="x unified",
    )

    return fig


