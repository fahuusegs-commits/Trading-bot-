import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Mobile Trading Bot", layout="wide")
st.title("📈 AI Trading Assistant")

symbol = st.text_input("Enter Symbol (e.g. BTC-USD):", "BTC-USD")
df = yf.download(symbol, period="1d", interval="15m")

if not df.empty:
    # Basic Indicator (SMA)
    df['SMA_20'] = df['Close'].rolling(window=20).mean()
    
    # Chart
    fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
    fig.add_trace(go.Scatter(x=df.index, y=df['SMA_20'], name='SMA 20', line=dict(color='orange')))
    st.plotly_chart(fig, use_container_width=True)
    
    # Simple Logic
    current_price = df['Close'].iloc[-1]
    sma_price = df['SMA_20'].iloc[-1]
    
    if current_price > sma_price:
        st.success("Signal: BUY 🟢")
    else:
        st.error("Signal: SELL 🔴")
else:
    st.warning("No data found!")
