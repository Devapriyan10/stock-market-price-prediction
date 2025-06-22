# streamlit_app.py (AUTH Section reverted to secure hash + SQLite3)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from backend.auth.auth_manager import login_user, register_user, create_user_table
from backend.utils.predictor import predict_and_recommend
from backend.utils.portfolio_manager import save_to_portfolio

# === Constants ===
COMPANY_CSV = "data/company_list.csv"
DATA_DIR = "data/historical_data"
PORTFOLIO_DIR = "data/user_portfolios"

# === Page Config ===
st.set_page_config(page_title="📈 Stock Market Prediction System", layout="wide")

# === Theme Toggle ===
if "theme" not in st.session_state:
    st.session_state.theme = "light"

with st.sidebar:
    theme_choice = st.radio("🎨 Select Theme", ["Light", "Dark"], index=0 if st.session_state.theme == "light" else 1)
    st.session_state.theme = theme_choice.lower()

def apply_theme(theme):
    if theme == "dark":
        st.markdown("""
            <style>
                body, .stApp {
                    background-color: #0e1117;
                    color: #ffffff;
                }
                .stButton>button, .stDownloadButton>button {
                    background-color: #1f77b4;
                    color: white;
                }
            </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <style>
                body, .stApp {
                    background-color: #ffffff;
                    color: #000000;
                }
                .stButton>button, .stDownloadButton>button {
                    background-color: #4CAF50;
                    color: white;
                }
            </style>
        """, unsafe_allow_html=True)

apply_theme(st.session_state.theme)

# === Session Setup ===
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

create_user_table()

# === SIDEBAR AUTH ===
with st.sidebar:
    st.title("🔐 Login / Register")
    login_tab, register_tab = st.tabs(["Login", "Register"])

    with login_tab:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if login_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Logged in successfully!")
            else:
                st.error("Invalid credentials")

    with register_tab:
        new_user = st.text_input("New Username")
        new_pass = st.text_input("New Password", type="password")
        if st.button("Register"):
            success, msg = register_user(new_user, new_pass)
            st.success(msg) if success else st.error(msg)

    if st.session_state.logged_in:
        st.success(f"🔓 Logged in as {st.session_state.username}")
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()

# === MAIN PAGE ===
if not st.session_state.logged_in:
    st.warning("⚠️ Please log in from the sidebar to access the prediction system.")
    st.stop()

st.markdown("<h1 style='text-align: center;'>📈 Stock Market Prediction System</h1>", unsafe_allow_html=True)
st.divider()

company_df = pd.read_csv(COMPANY_CSV)
company_names = company_df["Company Name"].tolist()
selected_company = st.selectbox("🔍 Select a Company", company_names)

data_path = f"{DATA_DIR}/{selected_company.replace(' ', '_')}.csv"
try:
    stock_df = pd.read_csv(data_path)
    stock_df["Date"] = pd.to_datetime(stock_df["Date"])

    st.subheader(f"📊 5-Year Stock Trend for {selected_company}")
    fig, ax = plt.subplots()
    ax.plot(stock_df["Date"], stock_df["Close"], color="blue", linewidth=2)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price (INR)")
    ax.set_title(selected_company)
    ax.grid(True)
    st.pyplot(fig)

except Exception as e:
    st.error(f"❌ Error loading stock data: {e}")

target_year = st.slider("🎯 Select Target Year", min_value=2025, max_value=2035, value=2026)

if st.button("🔮 Predict & Recommend"):
    try:
        result = predict_and_recommend(selected_company, target_year)

        st.success(f"📅 Target Year: {result['target_year']}")
        st.info(f"💰 Current Price: ₹{result['current_price']}")
        st.info(f"📈 Predicted Price: ₹{result['predicted_price']}")
        st.warning(f"💡 Recommendation: {result['recommendation']}")

        if st.button("💾 Save to Portfolio"):
            save_to_portfolio(st.session_state.username, result)
            st.success("✅ Saved to your portfolio!")

    except Exception as e:
        st.error(f"❌ Prediction failed: {e}")

portfolio_path = f"{PORTFOLIO_DIR}/{st.session_state.username}.csv"
if os.path.exists(portfolio_path):
    st.subheader("📂 Your Saved Portfolio")
    portfolio_df = pd.read_csv(portfolio_path)
    st.dataframe(portfolio_df, use_container_width=True)

    st.download_button("⬇️ Export Portfolio as CSV",
                       data=portfolio_df.to_csv(index=False),
                       file_name=f"{st.session_state.username}_portfolio.csv",
                       mime="text/csv")