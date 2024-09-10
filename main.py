import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from stock_data import fetch_stock_data, get_company_info

st.set_page_config(page_title="Stock Data Visualization", layout="wide")

st.title("Stock Data Visualization App")

# User input for stock symbol
stock_symbol = st.text_input("Enter a stock symbol (e.g., AAPL, GOOGL):", "AAPL").upper()

if stock_symbol:
    # Fetch stock data
    df, info = fetch_stock_data(stock_symbol)
    
    if df is not None and info is not None:
        # Display company information
        st.header(f"{info['longName']} ({stock_symbol})")
        st.write(f"Sector: {info['sector']}")
        st.write(f"Industry: {info['industry']}")
        st.write(f"Website: {info['website']}")
        
        # Display key financial information
        col1, col2, col3 = st.columns(3)
        col1.metric("Current Price", f"${info['currentPrice']:.2f}")
        col2.metric("Market Cap", f"${info['marketCap']:,.0f}")
        col3.metric("Trailing P/E", f"{info['trailingPE']:.2f}")

        col4, col5, col6 = st.columns(3)
        col4.metric("Forward P/E", f"{info['forwardPE']:.2f}")
        col5.metric("PEG Ratio", f"{info['pegRatio']:.2f}")
        col6.metric("Price to Book", f"{info['priceToBook']:.2f}")
        
        # Display stock price chart
        st.subheader("Stock Price History")
        fig = go.Figure(data=go.Scatter(x=df.index, y=df['Close'], mode='lines'))
        fig.update_layout(xaxis_title="Date", yaxis_title="Close Price (USD)")
        st.plotly_chart(fig, use_container_width=True)
        
        # Display financial data table
        st.subheader("Financial Data")
        financial_data = pd.DataFrame({
            "Metric": ["Trailing P/E", "Forward P/E", "PEG Ratio", "Price to Book", "Enterprise to Revenue", "Enterprise to EBITDA"],
            "Value": [
                info['trailingPE'],
                info['forwardPE'],
                info['pegRatio'],
                info['priceToBook'],
                info['enterpriseToRevenue'],
                info['enterpriseToEbitda']
            ]
        })
        st.dataframe(financial_data)
        
        # Display historical data table
        st.subheader("Historical Data")
        st.dataframe(df)
        
        # Download CSV button
        csv = df.to_csv(index=True)
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name=f"{stock_symbol}_stock_data.csv",
            mime="text/csv",
        )
    else:
        st.error("Unable to fetch stock data. Please check the stock symbol and try again.")

else:
    st.info("Please enter a stock symbol to view its data.")

# Add footer
st.markdown("---")
st.markdown("Data provided by Yahoo Finance")
