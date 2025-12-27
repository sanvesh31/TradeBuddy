import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

#PAGE CONFIG
st.set_page_config(
    page_title="TradeBuddy",
    page_icon="📊",
    layout="centered"
)

#CENTERED LOGO 
st.markdown(
    """
    <div style="display:flex; justify-content:center; margin-top:10px;">
        <img src="https://i.ibb.co/pjpJb30Q/logo.png" width="170">
    </div>
    """,
    unsafe_allow_html=True
)

# HEADER
st.markdown(
    """
    <h1 style='text-align:center;color:#00ffcc;'>📊 TradeBuddy</h1>
    <h4 style='text-align:center;'>Smart Trading Assistant for Beginners</h4>
    <p style='text-align:center;'>Created By <b>Sanvesh Roy</b></p>
    <hr>
    """,
    unsafe_allow_html=True
)

# USER INPUT
st.subheader("🔎 Trade Inputs")

stock = st.text_input("Stock Symbol (Example: TCS.NS, INFY.NS)")
investment = st.number_input("Investment Amount (₹)", min_value=1000.0, step=500.0)
holding_days = st.slider("Expected Holding Period (Days)", 1, 30, 7)

if st.button("📈 Analyze Trade"):

    if stock.strip() == "":
        st.error("Please enter a stock symbol")
    else:
        ticker = yf.Ticker(stock)

        # REAL-TIME PRICE (1 MIN DATA)
        live_data = ticker.history(period="1d", interval="1m")

        if live_data.empty:
            st.error("Live data not available for this stock")
        else:
            current_price = float(live_data['Close'].iloc[-1])

            #  HISTORICAL DATA
            hist = ticker.history(period="1mo")

            if hist.empty:
                st.error("Historical data not available")
            else:
                buy_price = float(hist['Close'].iloc[0])
                quantity = investment / buy_price

                #CURRENT PROFIT / LOSS
                current_value = quantity * current_price
                current_pl = current_value - investment
                current_pl_pct = (current_pl / investment) * 100

                # EXPECTED PROFIT (DATA DRIVEN)
                monthly_return = (hist['Close'].iloc[-1] - hist['Close'].iloc[0]) / hist['Close'].iloc[0]
                expected_return = (monthly_return / 30) * holding_days
                expected_price = current_price * (1 + expected_return)
                expected_value = expected_price * quantity
                expected_profit = expected_value - investment

                # OUTPUT
                st.subheader("📊 Trade Summary")

                c1, c2, c3 = st.columns(3)
                c1.metric("Live Price", f"₹{current_price:.2f}")
                c2.metric("Quantity", f"{quantity:.2f}")
                c3.metric("Current P/L", f"₹{current_pl:.2f}", f"{current_pl_pct:.2f}%")

                st.write(f"**Expected Price after {holding_days} days:** ₹{expected_price:.2f}")
                st.write(f"**Expected Profit:** ₹{expected_profit:.2f}")

                #  CHART
                st.subheader("📈 1 Month Price Trend")
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.plot(hist.index, hist['Close'], label="Close Price")
                ax.set_ylabel("Price (₹)")
                ax.legend()
                st.pyplot(fig)

                # DECISION
                if expected_profit > 0:
                    st.success("✅ Based on recent trend, trade looks profitable.")
                else:
                    st.warning("⚠️ Recent trend shows risk. Trade carefully.")

# FOOTER
st.markdown(
    """
    <hr>
    <p style='text-align:center;font-size:12px;'>
    Data Source: Yahoo Finance | Educational Use Only
    </p>
    """,
    unsafe_allow_html=True
)
