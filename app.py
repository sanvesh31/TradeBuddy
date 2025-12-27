import streamlit as st
import yfinance as yf
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
        <img src="https://i.ibb.co/pjpJb30Q/logo.png" width="140">
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------- HEADER ----------------
st.markdown(
    """
    <h1 style='text-align:center;color:#00ffcc;'>TradeBuddy</h1>
    <h4 style='text-align:center;'>Smart Trading Assistant for Beginners</h4>
    <p style='text-align:center;'>Created By <b>Sanvesh Roy</b></p>
    <hr>
    """,
    unsafe_allow_html=True
)

# ---------------- STOCK MAP (INDIAN MARKET - MAJOR STOCKS) ----------------
stock_map = {
    "Reliance Industries": "RELIANCE.NS",
    "Tata Consultancy Services": "TCS.NS",
    "Infosys": "INFY.NS",
    "HDFC Bank": "HDFCBANK.NS",
    "ICICI Bank": "ICICIBANK.NS",
    "State Bank of India": "SBIN.NS",
    "ITC Limited": "ITC.NS",
    "Axis Bank": "AXISBANK.NS",
    "Bharti Airtel": "BHARTIARTL.NS",
    "Hindustan Unilever": "HINDUNILVR.NS",
    "Kotak Mahindra Bank": "KOTAKBANK.NS",
    "Bajaj Finance": "BAJFINANCE.NS",
    "Larsen & Toubro": "LT.NS",
    "Maruti Suzuki": "MARUTI.NS",
    "Titan Company": "TITAN.NS",
    "UltraTech Cement": "ULTRACEMCO.NS",
    "Mahindra & Mahindra": "M&M.NS",
    "Sun Pharma": "SUNPHARMA.NS",
    "Tata Steel": "TATASTEEL.NS",
    "Power Grid Corporation": "POWERGRID.NS",
    "ONGC": "ONGC.NS",
    "Coal India": "COALINDIA.NS",
    "Adani Enterprises": "ADANIENT.NS",
    "Adani Ports": "ADANIPORTS.NS",
    "Britannia Industries": "BRITANNIA.NS",
    "Cipla": "CIPLA.NS",
    "Hero MotoCorp": "HEROMOTOCO.NS",
    "Eicher Motors": "EICHERMOT.NS",
    "Grasim Industries": "GRASIM.NS",
    "Bajaj Auto": "BAJAJ-AUTO.NS",
    "HCL Technologies": "HCLTECH.NS",
    "Tech Mahindra": "TECHM.NS",
    "Nestle India": "NESTLEIND.NS",
    "Bank of Baroda": "BANKBARODA.NS",
    "BPCL": "BPCL.NS",
    "HDFC Life": "HDFCLIFE.NS",
    "SBI Life Insurance": "SBILIFE.NS"
}

# ---------------- DATA FETCH (RATE-LIMIT SAFE) ----------------
@st.cache_data(ttl=300)
def fetch_stock_data(symbol):
    ticker = yf.Ticker(symbol)
    return ticker.history(period="1mo")

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

# ---------------- ANALYSIS ----------------
if st.button("📈 Analyze Trade"):

    symbol = stock_map[company_name]

    try:
        hist = fetch_stock_data(symbol)

        if hist.empty:
            st.error("Market data not available right now.")
        else:
            buy_price = float(hist['Close'].iloc[0])
            current_price = float(hist['Close'].iloc[-1])

            # -------- MINIMUM PRICE CHECK --------
            if current_price < 100:
                st.warning("⚠️ Stock price is below ₹100. TradeBuddy recommends avoiding low-priced stocks.")
            else:
                quantity = investment / buy_price
                current_value = quantity * current_price

                current_pl = current_value - investment
                current_pl_pct = (current_pl / investment) * 100

                # -------- EXPECTED PROFIT (TREND BASED) --------
                total_return = (hist['Close'].iloc[-1] - hist['Close'].iloc[0]) / hist['Close'].iloc[0]
                daily_return = total_return / len(hist)

                expected_price = current_price * (1 + daily_return * holding_days)
                expected_profit = (expected_price - buy_price) * quantity

                # -------- OUTPUT --------
                st.subheader("📊 Trade Summary")

                c1, c2, c3 = st.columns(3)
                c1.metric("Current Price", f"₹{current_price:.2f}")
                c2.metric("Quantity", f"{quantity:.2f}")
                c3.metric("Current P/L", f"₹{current_pl:.2f}", f"{current_pl_pct:.2f}%")

                st.write(f"**Expected Price after {holding_days} days:** ₹{expected_price:.2f}")
                st.write(f"**Expected Profit:** ₹{expected_profit:.2f}")

                # -------- CHART --------
                st.subheader("📈 Last 1 Month Price Trend")
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.plot(hist.index, hist['Close'])
                ax.set_ylabel("Price (₹)")
                st.pyplot(fig)

                # -------- DECISION --------
                if expected_profit > 0:
                    st.success("✅ Based on recent trend, this trade may be profitable.")
                else:
                    st.warning("⚠️ Trend indicates risk. Trade carefully.")

    except Exception:
        st.error("Data source temporarily blocked. Please try again later.")

# ---------------- FOOTER ----------------
st.markdown(
    """
    <hr>
    <p style='text-align:center;font-size:12px;'>
    Data Source: Yahoo Finance | For Educational Use Only
    </p>
    """,
    unsafe_allow_html=True
)
