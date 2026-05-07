import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Quotex AI Assistant", layout="wide")
st.title("📊 Quotex 1-Min Pro Signal")


symbol = st.selectbox("Select Pair:", ["BTC-USD", "ETH-USD", "EURUSD=X", "GBPUSD=X", "JPY=X"])

try:

    df = yf.download(symbol, period="1d", interval="2m") 

    if not df.empty:
        df = df.tail(50)
        
        # RSI Calculation
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (100 + rs))

        # Chart
        fig = go.Figure(data=[go.Candlestick(
            x=df.index, open=df['Open'], high=df['High'], 
            low=df['Low'], close=df['Close'], name='Candles'
        )])
        fig.update_layout(xaxis_rangeslider_visible=False, height=400)
        st.plotly_chart(fig, use_container_width=True)

        # RSI Signal
        current_rsi = df['RSI'].iloc[-1]
        st.metric(label="Current RSI", value=f"{current_rsi:.2f}")

        if current_rsi < 35:
            st.success("🟢 CALL (UP) SIGNAL - Market Oversold")
        elif current_rsi > 65:
            st.error("🔴 PUT (DOWN) SIGNAL - Market Overbought")
        else:
            st.warning("⚖️ NEUTRAL - NO TRADE")
    else:
        st.error("Data not available. Please wait 10 seconds and Refresh.")
except Exception as e:
    st.info("Searching for live data... Please Refresh browser.")
