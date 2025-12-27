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

# ---------------- CENTERED LOGO ----------------
st.markdown(
    """
    <div style="display:flex; justify-content:center; margin-top:10px;">
        <img src="https://i.ibb.co/pjpJb30Q/logo.png" width="160">
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------- HEADER ----------------
st.markdown(
    """
    <h1 style='text-align:center;color:#00ffcc;'>📊 TradeBuddy</h1>
    <h4 style='text-align:center;'>Smart Trading Assistant</h4>
    <p style='text-align:center;'>Created By <b>Sanvesh Roy</b></p>
    <hr>
    """,
    unsafe_allow_html=True
)

# ---------------- COMPANY NAME → SYMBOL MAP ----------------
stock_map = {
    "Reliance Industries": "RELIANCE.NS",
    "Tata Consultancy Services": "TCS.NS",
    "HDFC Bank": "HDFCBANK.NS",
    "ICICI Bank": "ICICIBANK.NS",
    "Infosys": "INFY.NS",
    "Bharti Airtel": "BHARTIARTL.NS",
    "State Bank of India": "SBIN.NS",
    "ITC Limited": "ITC.NS",
    "Axis Bank": "AXISBANK.NS",
    "Asian Paints": "ASIANPAINT.NS",
    "Hindustan Unilever": "HINDUNILVR.NS",
    "Kotak Mahindra Bank": "KOTAKBANK.NS",
    "Bajaj Finance": "BAJFINANCE.NS",
    "Larsen & Toubro": "LT.NS",
    "Maruti Suzuki": "MARUTI.NS",
    "Titan Company": "TITAN.NS",
    "UltraTech Cement": "ULTRACEMCO.NS",
    "Mahindra & Mahindra": "M&M.NS",
    "Asian Paints": "ASIANPAINT.NS",
    "SUN Pharma": "SUNPHARMA.NS",
    "Tata Steel": "TATASTEEL.NS",
    "Power Grid Corporation": "POWERGRID.NS",
    "Oil & Natural Gas Corporation": "ONGC.NS",
    "Coal India": "COALINDIA.NS",
    "Adani Enterprises": "ADANIENT.NS",
    "Adani Total Gas": "ATGL.NS",
    "Adani Green Energy": "ADANIGREEN.NS",
    "Adani Ports & SEZ": "ADANIPORTS.NS",
    "Britannia Industries": "BRITANNIA.NS",
    "Cipla": "CIPLA.NS",
    "Divi's Laboratories": "DIVISLAB.NS",
    "Hero MotoCorp": "HEROMOTOCO.NS",
    "Eicher Motors": "EICHERMOT.NS",
    "Grasim Industries": "GRASIM.NS",
    "Bajaj Auto": "BAJAJ-AUTO.NS",
    "HCL Technologies": "HCLTECH.NS",
    "Tech Mahindra": "TECHM.NS",
    "Nestle India": "NESTLEIND.NS",
    "Bharti Airtel Preference": "AIRTELPP.NS",
    "LIC Housing Finance": "LICHSGFIN.NS",
    "Bank of Baroda": "BANKBARODA.NS",
    "Bharat Petroleum": "BPCL.NS",
    "HDFC Life": "HDFCLIFE.NS",
    "SBI Life Insurance": "SBILIFE.NS"
}


# ---------------- USER INPUT ----------------
st.subheader("🔎 Trade Inputs")

company_name = st.selectbox(
    "Select Company",
    list(stock_map.keys())
)

investment = st.number_input(
    "Investment Amount (₹)",
    min_value=1000.0,
    step=500.0
)

holding_days = st.slider(
    "Expected Holding Period (Days)",
    1, 30, 7
)

# ---------------- ANALYZE BUTTON ----------------
if st.button("📈 Analyze Trade"):

    symbol = stock_map[company_name]
    ticker = yf.Ticker(symbol)

    # -------- REAL-TIME PRICE (1 MIN INTERVAL) --------
    live_data = ticker.history(period="1d", interval="1m")

    if live_data.empty:
        st.error("Live market data not available currently")
    else:
        current_price = float(live_data['Close'].iloc[-1])

        # -------- HISTORICAL DATA (1 MONTH) --------
        hist = ticker.history(period="1mo")

        if hist.empty:
            st.error("Historical data not available")
        else:
            buy_price = float(hist['Close'].iloc[0])
            quantity = investment / buy_price

            # -------- CURRENT PROFIT / LOSS --------
            current_value = quantity * current_price
            current_pl = current_value - investment
            current_pl_pct = (current_pl / investment) * 100

            # -------- EXPECTED PROFIT (DATA DRIVEN) --------
            monthly_return = (
                hist['Close'].iloc[-1] - hist['Close'].iloc[0]
            ) / hist['Close'].iloc[0]

            expected_return = (monthly_return / 30) * holding_days
            expected_price = current_price * (1 + expected_return)
            expected_profit = (expected_price - buy_price) * quantity

            # ---------------- OUTPUT ----------------
            st.subheader("📊 Trade Summary")

            c1, c2, c3 = st.columns(3)
            c1.metric("Live Price", f"₹{current_price:.2f}")
            c2.metric("Quantity", f"{quantity:.2f}")
            c3.metric(
                "Current P/L",
                f"₹{current_pl:.2f}",
                f"{current_pl_pct:.2f}%"
            )

            st.write(f"**Expected Price after {holding_days} days:** ₹{expected_price:.2f}")
            st.write(f"**Expected Profit:** ₹{expected_profit:.2f}")

            # ---------------- CHART ----------------
            st.subheader("📈 Last 1 Month Price Trend")
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.plot(hist.index, hist['Close'], label="Closing Price")
            ax.set_ylabel("Price (₹)")
            ax.legend()
            st.pyplot(fig)

            # ---------------- DECISION ----------------
            if expected_profit > 0:
                st.success("✅ Based on recent trend, trade looks profitable.")
            else:
                st.warning("⚠️ Recent trend indicates risk. Trade carefully.")

# ---------------- FOOTER ----------------
st.markdown(
    """
    <hr>
    <p style='text-align:center;font-size:12px;'>
    Data Source: Yahoo Finance | Educational Purpose Only
    </p>
    """,
    unsafe_allow_html=True
)
