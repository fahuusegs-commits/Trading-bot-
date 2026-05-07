import streamlit as st
import yfinance as yf
import pandas_ta as ta
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Page Setup
st.set_page_config(page_title="Pro AI Trader", layout="wide")
st.title("🚀 Professional AI Chart Analyzer & Signal Generator")
st.markdown("---")

# Sidebar - Settings
st.sidebar.header("User Settings")
symbol = st.sidebar.text_input("Stock/Crypto Symbol (e.g., BTC-USD, TSLA, ETH-USD):", value="BTC-USD")
timeframe = st.sidebar.selectbox("Select Timeframe:", ("1h", "1d", "15m", "5m"))
days_back = st.sidebar.slider("Analysis Period (Days):", 10, 365, 60)

# Data Fetching
start_date = datetime.now() - timedelta(days=days_back)
data = yf.download(symbol, start=start_date, interval=timeframe)

if not data.empty:
    # --- Technical Indicators Calculation ---
    data['RSI'] = ta.rsi(data['Close'], length=14)
    data['EMA_20'] = ta.ema(data['Close'], length=20)
    data['EMA_50'] = ta.ema(data['Close'], length=50)
    
    # MACD
    macd = ta.macd(data['Close'])
    data = data.join(macd)
    
    # Bollinger Bands
    bbands = ta.bbands(data['Close'], length=20, std=2)
    data = data.join(bbands)

    # --- Trading Strategy Logic (The "90%" Logic) ---
    # Amra ekhane check korbo sob indicator ekshathe ki signal dicche
    last_row = data.iloc[-1]
    prev_row = data.iloc[-2]
    
    buy_signal = 0
    sell_signal = 0
    
    # Condition 1: RSI (Oversold/Overbought)
    if last_row['RSI'] < 35: buy_signal += 1
    if last_row['RSI'] > 65: sell_signal += 1
    
    # Condition 2: EMA Crossover (Trend)
    if last_row['EMA_20'] > last_row['EMA_50']: buy_signal += 1
    else: sell_signal += 1
    
    # Condition 3: MACD Crossover
    if last_row['MACD_12_26_9'] > last_row['MACDs_12_26_9']: buy_signal += 1
    else: sell_signal += 1

    # --- Dashboard UI ---
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Current Price", f"${last_row['Close']:.2f}")
    with col2:
        st.metric("RSI (Strength)", f"{last_row['RSI']:.2f}")
    with col3:
        # Final Recommendation Logic
        if buy_signal >= 2:
            st.success("🎯 SIGNAL: STRONG BUY")
            confidence = "High" if buy_signal == 3 else "Medium"
        elif sell_signal >= 2:
            st.error("🎯 SIGNAL: STRONG SELL")
            confidence = "High" if sell_signal == 3 else "Medium"
        else:
            st.warning("🎯 SIGNAL: WAIT / NEUTRAL")
            confidence = "Low"

    # --- Charts ---
    st.subheader(f"Technical Chart: {symbol}")
    fig = go.Figure()

    # Candlestick
    fig.add_trace(go.Candlestick(x=data.index, open=data['Open'], high=data['High'],
                                 low=data['Low'], close=data['Close'], name="Market"))
    
    # Bollinger Bands
    fig.add_trace(go.Scatter(x=data.index, y=data['BBU_20_2.0'], line=dict(color='gray', width=1), name="BB Upper"))
    fig.add_trace(go.Scatter(x=data.index, y=data['BBL_20_2.0'], line=dict(color='gray', width=1), name="BB Lower"))
    
    # EMA
    fig.add_trace(go.Scatter(x=data.index, y=data['EMA_20'], line=dict(color='blue'), name="EMA 20"))
    
    fig.update_layout(height=600, template="plotly_dark", xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

    # --- Analysis Summary ---
    with st.expander("See Detailed Analysis"):
        st.write(f"**Confidence Level:** {confidence}")
        st.write(f"**Trend:** {'Bullish' if last_row['EMA_20'] > last_row['EMA_50'] else 'Bearish'}")
        st.write("**Strategy used:** RSI, EMA Crossover, and MACD Confirmation.")

else:
    st.error("Invalid Symbol or No Data Found!")
