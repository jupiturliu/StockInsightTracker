import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from stock_data import fetch_stock_data, get_company_info

st.set_page_config(page_title="Stock Data Visualization", layout="wide")

st.title("Stock Data Visualization App")

# User input for multiple stock symbols
stock_symbols = st.text_input("Enter stock symbols separated by commas (e.g., AAPL, GOOGL, MSFT):", "AAPL, GOOGL").upper()

if stock_symbols:
    symbols = [symbol.strip() for symbol in stock_symbols.split(',')]
    
    # Fetch stock data for all symbols
    stock_data = {}
    for symbol in symbols:
        df, info = fetch_stock_data(symbol)
        if df is not None and info is not None:
            stock_data[symbol] = {'df': df, 'info': info}
    
    if stock_data:
        # Display comparative stock price chart
        st.subheader("Comparative Stock Price History")
        fig = go.Figure()
        for symbol, data in stock_data.items():
            fig.add_trace(go.Scatter(x=data['df'].index, y=data['df']['Close'], mode='lines', name=symbol))
        fig.update_layout(xaxis_title="Date", yaxis_title="Close Price (USD)")
        st.plotly_chart(fig, use_container_width=True)
        
        # Display comparative financial data table
        st.subheader("Comparative Financial Data")
        comparative_data = []
        for symbol, data in stock_data.items():
            info = data['info']
            comparative_data.append({
                "Symbol": symbol,
                "Current Price": f"${info['currentPrice']:.2f}",
                "Market Cap": f"${info['marketCap']:,.0f}",
                "Trailing P/E": f"{info['trailingPE']:.2f}",
                "Forward P/E": f"{info['forwardPE']:.2f}",
                "PEG Ratio": f"{info['pegRatio']:.2f}",
                "Price to Book": f"{info['priceToBook']:.2f}"
            })
        comparative_df = pd.DataFrame(comparative_data)
        st.dataframe(comparative_df)
        
        # Individual stock details
        for symbol, data in stock_data.items():
            with st.expander(f"Detailed Information for {symbol}"):
                info = data['info']
                st.subheader(f"{info['longName']} ({symbol})")
                st.write(f"Sector: {info['sector']}")
                st.write(f"Industry: {info['industry']}")
                st.write(f"Website: {info['website']}")
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Current Price", f"${info['currentPrice']:.2f}")
                col2.metric("Market Cap", f"${info['marketCap']:,.0f}")
                col3.metric("Trailing P/E", f"{info['trailingPE']:.2f}")
                
                # Display individual stock price chart with technical indicators
                st.subheader("Stock Price History with Technical Indicators")
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=data['df'].index, y=data['df']['Close'], mode='lines', name='Close Price'))
                fig.add_trace(go.Scatter(x=data['df'].index, y=data['df']['SMA20'], mode='lines', name='SMA 20', line=dict(dash='dash')))
                fig.add_trace(go.Scatter(x=data['df'].index, y=data['df']['SMA50'], mode='lines', name='SMA 50', line=dict(dash='dash')))
                fig.add_trace(go.Scatter(x=data['df'].index, y=data['df']['SMA200'], mode='lines', name='SMA 200', line=dict(dash='dash')))
                fig.update_layout(xaxis_title="Date", yaxis_title="Price (USD)")
                st.plotly_chart(fig, use_container_width=True)
                
                # Display RSI chart
                st.subheader("Relative Strength Index (RSI)")
                fig_rsi = go.Figure()
                fig_rsi.add_trace(go.Scatter(x=data['df'].index, y=data['df']['RSI'], mode='lines', name='RSI'))
                fig_rsi.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Overbought (70)")
                fig_rsi.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Oversold (30)")
                fig_rsi.update_layout(xaxis_title="Date", yaxis_title="RSI")
                st.plotly_chart(fig_rsi, use_container_width=True)
                
                # Display historical data table
                st.subheader("Historical Data")
                st.dataframe(data['df'])
                
                # Download CSV button
                csv = data['df'].to_csv(index=True)
                st.download_button(
                    label=f"Download {symbol} data as CSV",
                    data=csv,
                    file_name=f"{symbol}_stock_data.csv",
                    mime="text/csv",
                )
    else:
        st.error("Unable to fetch stock data. Please check the stock symbols and try again.")
else:
    st.info("Please enter stock symbols separated by commas to view and compare their data.")

# Add footer
st.markdown("---")
st.markdown("Data provided by Yahoo Finance")
