import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Quotex 1m Scalper", layout="wide")
st.title("📊 Quotex 1-Min Signal Assistant")

symbol = st.text_input("Enter Symbol (e.g. BTC-USD, EURUSD=X):", "BTC-USD")

try:
    # 1 min candle er jonno 7 days data download kora secure
    df = yf.download(symbol, period="7d", interval="1m")

    if not df.empty:
        # Sudhu matro ekebare shesh-er 60 ti 1-min candle dekhabo
        df = df.tail(60)

        # RSI Calculation
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (100 + rs))

        # Chart with Fixed Range
        fig = go.Figure(data=[go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name='1m Candles'
        )])
        
        fig.update_layout(xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

        # Signal Logic
        current_rsi = df['RSI'].iloc[-1]
        st.subheader(f"Current RSI: {current_rsi:.2f}")

        if current_rsi < 30:
            st.success("🔥 SIGNAL: UP (1 MIN BUY)")
        elif current_rsi > 70:
            st.error("🔥 SIGNAL: DOWN (1 MIN SELL)")
        else:
            st.warning("⚖️ SIGNAL: WAIT (Neutral)")
            
    else:
        st.warning("No data found! Refreshing...")
except Exception as e:
    st.error(f"Error: {e}")
