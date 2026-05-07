import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# Page configuration
st.set_page_config(page_title="Quotex Trading Helper", layout="wide")
st.title("📊 Quotex Binary Signal Assistant")

# Input for symbol
symbol = st.text_input("Enter Symbol (e.g. BTC-USD, EURUSD=X):", "BTC-USD")

# Fetch data
try:
    df = yf.download(symbol, period="1d", interval="1m")

    if not df.empty:
        # RSI Calculation (Best for Binary Trading)
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (100 + rs))

        # Chart
        fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name='Market')])
        st.plotly_chart(fig, use_container_width=True)

        # Signal Logic for Quotex
        current_rsi = df['RSI'].iloc[-1]
        st.subheader(f"Current RSI: {current_rsi:.2f}")

        if current_rsi < 30:
            st.success("🔥 SIGNAL: UP (BUY) - Market is Oversold")
        elif current_rsi > 70:
            st.error("🔥 SIGNAL: DOWN (SELL) - Market is Overbought")
        else:
            st.warning("⚖️ SIGNAL: WAIT - Neutral Market")
            
    else:
        st.warning("No data found! Please check the symbol name.")
except Exception as e:
    st.error(f"Error: {e}")
