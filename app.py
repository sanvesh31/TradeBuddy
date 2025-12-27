import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="TradeBuddy",
    page_icon="📊",
    layout="centered"
)

# ---------------- HEADER ----------------
st.markdown(
    """
    <h1 style='text-align:center;color:#00ffcc;'>📊 TradeBuddy</h1>
    <h4 style='text-align:center;'>Smart Trading Assistant for Beginners</h4>
    <p style='text-align:center;'>Created By <b>Sanvesh Roy</b></p>
    <hr>
    """,
    unsafe_allow_html=True
)

# ---------------- USER INPUT ----------------
st.subheader("🔎 Enter Trade Details")

stock = st.text_input("Stock Symbol (Example: TCS.NS, INFY.NS)")
investment = st.number_input("Investment Amount (₹)", min_value=1000.0, step=500.0)
holding_days = st.slider("Holding Period (Days)", 1, 30, 7)

if st.button("📈 Analyze Trade"):

    if stock == "":
        st.error("Please enter a stock symbol")
    else:
        with st.spinner("Fetching market data..."):
            data = yf.download(stock, period="3mo")

        if data.empty:
            st.error("Invalid stock symbol or data not available")
        else:
            current_price = float(data['Close'][-1])
            quantity = investment / current_price

            # Moving Average
            data['SMA20'] = data['Close'].rolling(20).mean()
            sma_value = float(data['SMA20'][-1])

            # Trend logic
            if current_price > sma_value:
                trend = "UPTREND 📈"
                growth = 0.05
            else:
                trend = "DOWNTREND 📉"
                growth = -0.03

            # Profit calculation
            expected_price = current_price * (1 + growth)
            expected_value = expected_price * quantity
            profit = expected_value - investment
            profit_percent = (profit / investment) * 100

            # ---------------- OUTPUT ----------------
            st.subheader("📊 Trade Summary")

            c1, c2, c3 = st.columns(3)
            c1.metric("Current Price", f"₹{current_price:.2f}")
            c2.metric("Quantity", f"{quantity:.2f}")
            c3.metric("Trend", trend)

            st.write(f"**Expected Price after {holding_days} days:** ₹{expected_price:.2f}")
            st.write(f"**Expected Profit / Loss:** ₹{profit:.2f}")
            st.write(f"**Profit Percentage:** {profit_percent:.2f}%")

            # ---------------- CHART ----------------
            st.subheader("📈 Price Trend")
            fig, ax = plt.subplots()
            ax.plot(data['Close'], label="Close Price")
            ax.plot(data['SMA20'], label="20-Day SMA")
            ax.legend()
            st.pyplot(fig)

            # ---------------- ADVICE ----------------
            if profit > 0:
                st.success("✅ Trade looks profitable for short-term holding.")
            else:
                st.warning("⚠️ Risky trade. Consider HOLD or EXIT.")

# ---------------- FOOTER ----------------
st.markdown(
    """
    <hr>
    <p style='text-align:center;font-size:12px;'>
    Educational Purpose Only | Not Financial Advice
    </p>
    """,
    unsafe_allow_html=True
)
