import streamlit as st
import pandas as pd
import plotly.express as px
import os
import numpy as np

# صفحه و ظاهر
st.set_page_config(page_title="Retail AI Dashboard", layout="wide")
st.title("📊 Retail AI Dashboard")
st.markdown("Interactive dashboard for Retail AI Project: Sales, Forecasting & Customer Segmentation")

# Sidebar navigation
section = st.sidebar.radio("Navigation", ["Overview", "Analysis", "Forecasting", "RFM & Clustering", "Anomalies"])

# --- Utility Functions ---
@st.cache_data
def load_csv(path):
    if os.path.exists(path):
        return pd.read_csv(path)
    return pd.DataFrame()

# --- Overview ---
if section == "Overview":
    st.header("Pipeline Overview")
    st.markdown("""
    This dashboard presents the Retail AI Pipeline results:
    - Data cleaning and preprocessing
    - Sales analysis & visualization
    - Forecasting daily sales
    - Customer segmentation (RFM & Clustering)
    - Anomaly detection
    """)
    st.subheader("Available Output Files")
    if os.path.exists("output"):
        files = os.listdir("output")
        for f in files:
            st.markdown(f"- {f}")
            if f.endswith(".csv"):
                st.download_button(f"Download {f}", open(os.path.join("output", f), "rb"), f)

# --- Analysis ---
elif section == "Analysis":
    st.header("Sales Analysis")
    col1, col2 = st.columns(2)
    if os.path.exists("output/invoice_total_distribution.png"):
        col1.image("output/invoice_total_distribution.png", caption="Invoice Total Distribution", use_column_width=True)
    with col2:
        st.subheader("Regression Metrics")
        st.metric("Linear MAE", "18404")
        st.metric("Linear RMSE", "31748")
        st.metric("Random Forest MAE", "17529")
        st.metric("Random Forest RMSE", "28788")

# --- Forecasting ---
elif section == "Forecasting":
    st.header("Sales Forecasting")
    forecast = load_csv("output/sales_forecast.csv")
    if not forecast.empty:
        forecast["Date"] = pd.to_datetime(forecast["Date"])
        
        # --- اصلاح باگ اینجاست: تبدیل به فرمت استاندارد پایتون ---
        min_date = forecast["Date"].min().to_pydatetime()
        max_date = forecast["Date"].max().to_pydatetime()

        date_range = st.slider(
            "Select Date Range", 
            min_value=min_date, 
            max_value=max_date,
            value=(min_date, max_date), 
            format="YYYY-MM-DD"
        )
        
        # فیلتر کردن (تبدیل دوباره برای مقایسه با ستون پانداز)
        df_filtered = forecast[
            (forecast["Date"] >= pd.Timestamp(date_range[0])) & 
            (forecast["Date"] <= pd.Timestamp(date_range[1]))
        ]

        # نمایش کارت‌ها (Metrics)
        col_m1, col_m2, col_m3 = st.columns(3) # برای چیدمان بهتر کارت‌ها
        total_sales = df_filtered["TotalPrice"].sum()
        predicted_sales = df_filtered["Prediction"].sum()
        avg_sales = df_filtered["TotalPrice"].mean()
        
        col_m1.metric("Total Sales (Real)", f"${total_sales:,.0f}")
        col_m2.metric("Total Sales (Predicted)", f"${predicted_sales:,.0f}")
        col_m3.metric("Average Daily Sales", f"${avg_sales:,.0f}")

        # Interactive chart
        fig = px.line(df_filtered, x="Date", y=["TotalPrice", "Prediction"],
                      labels={"value":"Sales", "variable":"Legend"}, 
                      title="Forecast vs Real Sales")
        st.plotly_chart(fig, use_container_width=True)

        # Dataframe + download
        st.subheader("Forecast Data")
        st.dataframe(df_filtered.head(20))
        st.download_button("Download Forecast CSV", df_filtered.to_csv(index=False), "sales_forecast.csv")

# --- RFM & Clustering ---
elif section == "RFM & Clustering":
    st.header("Customer Segmentation")
    col1, col2 = st.columns(2)
    rfm = load_csv("output/rfm_table.csv")
    clusters = load_csv("output/customer_clusters.csv")

    if not rfm.empty:
        col1.subheader("RFM Table (Top 20)")
        col1.dataframe(rfm.head(20))
        col1.download_button("Download RFM Table", rfm.to_csv(index=False), "rfm_table.csv")
    if not clusters.empty:
        col2.subheader("Customer Clusters (Top 20)")
        col2.dataframe(clusters.head(20))
        col2.download_button("Download Customer Clusters", clusters.to_csv(index=False), "customer_clusters.csv")
    if os.path.exists("output/rfm_clusters_plot.png"):
        st.image("output/rfm_clusters_plot.png", caption="RFM Clusters", use_column_width=True)

# --- Anomalies ---
elif section == "Anomalies":
    st.header("Anomaly Detection")
    col1, col2 = st.columns(2)
    anomalies = load_csv("output/anomalies.csv")
    if os.path.exists("output/anomaly_plot.png"):
        col1.image("output/anomaly_plot.png", caption="Sales Anomalies", use_column_width=True)
    if not anomalies.empty:
        col2.subheader("Anomalies Table (Top 20)")
        col2.dataframe(anomalies.head(20))
        col2.download_button("Download Anomalies CSV", anomalies.to_csv(index=False), "anomalies.csv")
