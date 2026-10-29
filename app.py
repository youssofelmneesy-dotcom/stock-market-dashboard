
import streamlit as st

from stock_data import (
    COMPANIES,
    download_all_stocks,
)
from revenue_data import download_all_revenues
from visualization import (
    create_stock_chart,
    create_revenue_chart,
    create_company_overview,
    create_stock_comparison,
)


st.set_page_config(
    page_title="Stock Market Dashboard",
    page_icon="📈",
    layout="wide",
)


@st.cache_data(ttl=3600)
def load_all_stock_data():
    return download_all_stocks()


@st.cache_data(ttl=86400)
def load_all_revenue_data():
    return download_all_revenues()


st.title("📈 Stock Market Dashboard")

st.write(
    "Explore historical stock prices and quarterly revenue "
    "for Tesla, Amazon, AMD, and GameStop."
)

st.caption(
    "Educational project. Financial data availability depends "
    "on the source and the time of retrieval."
)

if st.button("Refresh data"):
    load_all_stock_data.clear()
    load_all_revenue_data.clear()
    st.rerun()


with st.spinner("Loading stock and revenue data..."):
    stock_results = load_all_stock_data()
    revenue_results = load_all_revenue_data()


selected_company = st.selectbox(
    "Select a company",
    list(COMPANIES.keys()),
)

stock_result = stock_results[selected_company]
revenue_result = revenue_results[selected_company]

stock_data = stock_result["data"]
revenue_data = revenue_result["data"]

if stock_result["error"]:
    st.error(
        f"Could not load stock data: {stock_result['error']}"
    )
    st.stop()

if revenue_result["error"]:
    st.warning(
        f"Could not load revenue data: {revenue_result['error']}"
    )

if stock_data.empty:
    st.error("No stock data is available for this company.")
    st.stop()


latest_close = stock_data["Close"].iloc[-1]

col1, col2, col3 = st.columns(3)

col1.metric("Company", selected_company)
col2.metric("Ticker", COMPANIES[selected_company])
col3.metric("Latest available close", f"${latest_close:,.2f}")


st.subheader("Company Overview")

overview_fig = create_company_overview(
    stock_data,
    revenue_data,
    selected_company,
)
st.plotly_chart(overview_fig, use_container_width=True)


left, right = st.columns(2)

with left:
    st.subheader("Historical Stock Price")
    st.plotly_chart(
        create_stock_chart(stock_data, selected_company),
        use_container_width=True,
    )

with right:
    st.subheader("Quarterly Revenue")

    if revenue_data.empty:
        st.info("Quarterly revenue data is unavailable.")
    else:
        st.plotly_chart(
            create_revenue_chart(
                revenue_data,
                selected_company,
            ),
            use_container_width=True,
        )


with st.expander("View stock data"):
    st.dataframe(stock_data.tail(20), use_container_width=True)

with st.expander("View revenue data"):
    st.dataframe(revenue_data, use_container_width=True)

st.subheader("Compare All Four Stocks")

available_stocks = {
    name: result["data"]
    for name, result in stock_results.items()
    if result["error"] is None and not result["data"].empty
}

comparison_fig = create_stock_comparison(available_stocks)

if comparison_fig is not None:
    st.plotly_chart(
        comparison_fig,
        use_container_width=True,
    )
else:
    st.info("No stock data is available for comparison.")


st.subheader("Data Sources and Status")

for company in COMPANIES:
    stock_info = stock_results[company]
    revenue_info = revenue_results[company]

    with st.expander(company):
        st.write("Ticker:", COMPANIES[company])

        if stock_info["error"]:
            st.error("Stock data failed: " + stock_info["error"])
        else:
            st.success("Stock data loaded")
            st.write("Stock CSV:", stock_info["file"])

        if revenue_info["error"]:
            st.error("Revenue data failed: " + revenue_info["error"])
        elif revenue_info["data"].empty:
            st.warning("No quarterly revenue data returned.")
        else:
            st.success("Revenue data loaded")
            st.write("Revenue CSV:", revenue_info["file"])
            st.write(
                "Source:",
                ", ".join(
                    revenue_info["data"]["Source"].dropna().unique()
                ),
            )


st.caption(
    "Historical stock prices and reported revenue are different "
    "measures. This dashboard is for learning and is not investment advice."
)

