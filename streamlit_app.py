import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import plotly.graph_objs as go
from nsepython import nsefetch
import pandas as pd
import datetime
from ta import add_all_ta_features
# Load top 100 companies from CSV
from jugaad_data.nse import stock_df
import pandas as pd

@st.cache_data
def load_companies():
    return pd.read_csv("top_100_indian_stocks.csv")

@st.cache_data
def fetch_data(symbol):
    try:
        df = stock_df(symbol=symbol, from_date=date(2019, 1, 1), to_date=date.today(), series="EQ")
        if df.empty:
            return pd.DataFrame()

        df.index = pd.to_datetime(df["DATE"])
        df = df.rename(columns={
            "OPEN": "Open", "HIGH": "High", "LOW": "Low", "CLOSE": "Close", "VOLUME": "Volume"
        })
        df = df[["Open", "High", "Low", "Close", "Volume"]].apply(pd.to_numeric, errors="coerce").dropna()
        return df

    except Exception as e:
        st.error(f"⚠️ Failed to fetch data for {symbol} via jugaad-data: {e}")
        return pd.DataFrame()


# App Title
st.title("📈 Indian Stock Market Prediction System")

companies = load_companies()
company_name = st.selectbox("Search Company", companies["Company Name"])
ticker = companies[companies["Company Name"] == company_name]["Ticker Symbol"].values[0]
df = fetch_data(ticker)

if df.empty:
    st.error(f"No data found for {company_name}. It might be delisted.")
    st.stop()

# Display raw data
st.subheader(f"📅 Historical Data for {company_name} ({ticker}) - Last 5 Years")
st.dataframe(df[["Close"]].tail(10))

# Plot close prices
fig = go.Figure()
fig.add_trace(go.Scatter(x=df.index, y=df["Close"], name="Close Price"))
st.plotly_chart(fig, use_container_width=True)

# Prepare features
df["Year"] = df.index.year
year_avg = df.groupby("Year")["Close"].mean().reset_index()

# Train prediction model
X = year_avg[["Year"]]
y = year_avg["Close"]
model = LinearRegression()
model.fit(X, y)

# Target year input
target_year = st.number_input("Enter a Year (e.g. 2026)", min_value=2025, max_value=2050, step=1)
future_pred = model.predict([[target_year]])[0]
latest_close = df["Close"].iloc[-1]

st.subheader("🔮 Price Prediction")
st.metric(label=f"Predicted Avg Close in {target_year}", value=f"₹{future_pred:.2f}")
st.metric(label="Latest Close Price", value=f"₹{latest_close:.2f}")

# Recommendation
if future_pred > latest_close:
    st.success("✅ Recommendation: BUY")
else:
    st.warning("⚠️ Recommendation: HOLD or SELL")
