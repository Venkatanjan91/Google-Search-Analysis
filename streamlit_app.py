import streamlit as st
from pytrends.request import TrendReq
import pandas as pd
import plotly.express as px
import time

# ------------------------------
# Page Config
# ------------------------------
st.set_page_config(page_title="Google Search Trends", page_icon="🔎", layout="wide")

# ------------------------------
# Sidebar Inputs
# ------------------------------
st.sidebar.title("⚙️ Settings")
dark_mode = st.sidebar.toggle("🌙 Dark Mode", value=False)

keywords = st.sidebar.text_input("Enter keywords (comma separated):", "Python, JavaScript, Data Science")
timeframe = st.sidebar.selectbox(
    "Select timeframe:",
    ["now 7-d", "today 1-m", "today 3-m", "today 12-m", "today 5-y", "all"]
)
geo = st.sidebar.text_input("Enter country code (leave empty for global):", "")

st.sidebar.markdown("---")
st.sidebar.info("💡 Example country codes: `US`, `IN`, `GB`")

# ------------------------------
# Theme Styles
# ------------------------------
if dark_mode:
    background = "#0e1117"
    text_color = "#f8f9fa"
    plotly_theme = "plotly_dark"
else:
    background = "#f8f9fa"
    text_color = "#212529"
    plotly_theme = "plotly_white"

st.markdown(
    f"""
    <style>
        .stApp {{
            background-color: {background};
            color: {text_color};
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: {text_color};
            font-family: 'Helvetica Neue', sans-serif;
        }}
        .stButton button {{
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
            border-radius: 10px;
            padding: 0.6em 1.2em;
            transition: 0.3s;
        }}
        .stButton button:hover {{
            background-color: #45a049;
            transform: scale(1.05);
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------------------
# Main App
# ------------------------------
st.title("🔎 Google Search Trends Dashboard")
st.caption("Switch between **Light/Dark Mode** for a personalized experience ✨")

pytrends = TrendReq(hl="en-US", tz=360)

kw_list = [kw.strip() for kw in keywords.split(",") if kw.strip()]

if st.button("🚀 Run Analysis"):

    if not kw_list:
        st.error("Please enter at least one keyword.")
    else:
        try:
            # Interest over time
            time.sleep(3)
            pytrends.build_payload(kw_list=kw_list, timeframe=timeframe, geo=geo)
            df = pytrends.interest_over_time()

            if df.empty:
                st.warning("No data found for the given inputs.")
            else:
                df = df.reset_index()

                # Line Chart
                st.subheader("📈 Interest Over Time")
                fig = px.line(
                    df,
                    x="date",
                    y=kw_list,
                    template=plotly_theme,
                    title="Search Interest Over Time"
                )
                st.plotly_chart(fig, use_container_width=True)

                # Regional Interest
                st.subheader("🌍 Regional Interest")
                region_df = pytrends.interest_by_region(resolution="COUNTRY", inc_low_vol=True, inc_geo_code=False)

                if not region_df.empty:
                    region_df = region_df.reset_index()
                    fig2 = px.choropleth(
                        region_df,
                        locations="geoName",
                        locationmode="country names",
                        color=kw_list[0],
                        color_continuous_scale="Viridis",
                        template=plotly_theme,
                        title=f"Regional Popularity of {kw_list[0]}"
                    )
                    st.plotly_chart(fig2, use_container_width=True)
                else:
                    st.info("No regional data available for these keywords.")

                # Related Queries
                st.subheader("🔍 Related Queries")
                related_queries = pytrends.related_queries()
                for kw in kw_list:
                    time.sleep(3)
                    if related_queries and related_queries.get(kw):
                        if related_queries[kw].get("top") is not None:
                            st.markdown(f"**{kw} – Top Queries**")
                            st.dataframe(related_queries[kw]["top"])
                        if related_queries[kw].get("rising") is not None:
                            st.markdown(f"**{kw} – Rising Queries**")
                            st.dataframe(related_queries[kw]["rising"])

        except Exception as e:
            st.error(f"⚠️ Something went wrong: {e}")

# ------------------------------
# Footer
# ------------------------------
st.markdown("---")
st.caption("✨ Built with love using Streamlit & PyTrends")
