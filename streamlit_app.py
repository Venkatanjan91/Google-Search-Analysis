import streamlit as st
import pandas as pd
import time
from pytrends.request import TrendReq

# -------------------
# Streamlit UI Config
# -------------------
st.set_page_config(
    page_title="Google Search Analysis",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Google Search Trends Analysis")
st.write("Analyze Google search interest over time using **PyTrends**.")

# -------------------
# User Input
# -------------------
keyword = st.text_input("🔍 Enter a search keyword:", "Python")
timeframe = st.selectbox("⏰ Select timeframe:", ["today 12-m", "today 5-y", "all"])
geo = st.text_input("🌍 Enter country code (e.g., 'US', 'IN') or leave blank for worldwide:", "")

# -------------------
# Function to fetch trends
# -------------------
def get_trends_data(keyword, timeframe, geo):
    pytrends = TrendReq(hl="en-US", tz=360, requests_args={'timeout': (10, 25)})
    try:
        # Build payload with delay
        pytrends.build_payload([keyword], cat=0, timeframe=timeframe, geo=geo, gprop="")
        time.sleep(2)  # Prevent rate limiting

        df = pytrends.interest_over_time()
        return df

    except Exception as e:
        st.error(f"⚠️ Something went wrong: {e}")
        return pd.DataFrame()

# -------------------
# Run Analysis
# -------------------
if st.button("Run Analysis"):
    if keyword.strip() == "":
        st.warning("Please enter a valid keyword.")
    else:
        with st.spinner("Fetching data from Google Trends..."):
            df = get_trends_data(keyword, timeframe, geo)

        if df.empty:
            st.warning("No data found for this keyword. Try another search term.")
        else:
            st.success(f"✅ Data fetched successfully for '{keyword}'!")

            # Drop isPartial column if exists
            if "isPartial" in df.columns:
                df = df.drop(columns=["isPartial"])

            # Show data
            st.subheader("📈 Search Interest Over Time")
            st.line_chart(df)

            st.subheader("📋 Raw Data")
            st.dataframe(df)
