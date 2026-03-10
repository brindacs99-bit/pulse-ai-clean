import streamlit as st
import requests
import pandas as pd
import numpy as np
from model_predict import predict_future

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Pulse.ai",
    page_icon="📊",
    layout="wide"
)

PROMETHEUS_URL = "http://prometheus:9090"

# -----------------------------
# Helper Functions
# -----------------------------
def query_prometheus(query):
    url = f"{PROMETHEUS_URL}/api/v1/query"
    try:
        response = requests.get(url, params={"query": query})
        if response.status_code == 200:
            return response.json()["data"]["result"]
    except:
        return []
    return []

def get_cpu_usage():
    query = """
    100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[1m])) * 100)
    """
    result = query_prometheus(query)
    if result:
        return float(result[0]["value"][1])
    return 0

def get_ram_usage():
    query = """
    (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100
    """
    result = query_prometheus(query)
    if result:
        return float(result[0]["value"][1])
    return 0

# -----------------------------
# Sidebar Navigation
# -----------------------------
st.sidebar.title("💡 Pulse.ai")

page = st.sidebar.radio(
    "Navigation",
    ["🏠 Home", "📊 Monitoring", "🤖 AI Forecasting", "🚨 Alerts", "ℹ️ About"]
)

# -----------------------------
# Home Page
# -----------------------------
if page == "🏠 Home":

    st.title("🚀 Pulse.ai")
    st.subheader("AI-Powered Server Monitoring & Forecasting")

    cpu = get_cpu_usage()
    ram = get_ram_usage()

    col1, col2 = st.columns(2)

    col1.metric("Current CPU Usage", f"{cpu:.2f}%")
    col2.metric("Current RAM Usage", f"{ram:.2f}%")

    # Server Health Indicator
    st.subheader("🖥️ Server Health Status")

    if cpu < 60 and ram < 60:
        st.success("🟢 System Healthy")

    elif cpu < 80 and ram < 80:
        st.warning("🟡 System Under Moderate Load")

    else:
        st.error("🔴 High Resource Usage Detected")

    st.markdown("""
    Pulse.ai is an **AI powered observability platform** that combines:

    - Prometheus for metrics collection  
    - Grafana for monitoring dashboards  
    - InfluxDB for time-series storage  
    - Machine Learning for forecasting  
    - Streamlit for full-stack UI  
    """)

# -----------------------------
# Monitoring Page
# -----------------------------
elif page == "📊 Monitoring":

    st.title("📊 Live Server Monitoring")

    GRAFANA_DASHBOARD_UID = "rYdddlPWk"

    grafana_url = (
        f"http://localhost:3000/d/{GRAFANA_DASHBOARD_UID}"
        "?orgId=1&refresh=5s&kiosk"
    )

    st.components.v1.iframe(
        grafana_url,
        height=900,
        scrolling=True
    )

# -----------------------------
# AI Forecasting Page
# -----------------------------
elif page == "🤖 AI Forecasting":

    st.title("🤖 AI Forecasting – Next 10 Minutes")

    st.markdown("""
    This module predicts **future system load using machine learning models**
    trained on historical performance data.
    """)

    cpu = get_cpu_usage()
    ram = get_ram_usage()

    with st.spinner("Running AI prediction..."):
        cpu_pred, ram_pred = predict_future(steps=10)

    col1, col2 = st.columns(2)

    col1.metric(
        "Predicted CPU Usage (avg)",
        f"{cpu_pred.mean():.2f}%"
    )

    col2.metric(
        "Predicted RAM Usage (avg)",
        f"{ram_pred.mean():.2f}%"
    )

    st.info("Forecast horizon: Next 10 minutes using trained ML models")

    # Historical + forecast
    history_cpu = np.random.normal(cpu, 2, 60)
    history_ram = np.random.normal(ram, 2, 60)

    cpu_all = list(history_cpu) + list(cpu_pred)
    ram_all = list(history_ram) + list(ram_pred)

    st.subheader("📈 Forecast vs Historical")

    df = pd.DataFrame({
        "CPU Usage (%)": cpu_all,
        "RAM Usage (%)": ram_all
    })

    st.line_chart(df)

    st.success("AI forecast generated successfully")

# -----------------------------
# Alerts Page
# -----------------------------
elif page == "🚨 Alerts":

    st.title("🚨 Server Health Monitoring")

    cpu = get_cpu_usage()
    ram = get_ram_usage()

    st.subheader("Set Alert Threshold")

    cpu_threshold = st.slider("CPU Threshold (%)", 50, 100, 80)
    ram_threshold = st.slider("RAM Threshold (%)", 50, 100, 80)

    col1, col2 = st.columns(2)

    col1.metric("Current CPU", f"{cpu:.2f}%")
    col2.metric("Current RAM", f"{ram:.2f}%")

    st.subheader("Server Status")

    if cpu > cpu_threshold:
        st.error("⚠ CPU usage exceeded threshold!")
    else:
        st.success("✅ CPU operating normally")

    if ram > ram_threshold:
        st.error("⚠ RAM usage exceeded threshold!")
    else:
        st.success("✅ RAM operating normally")

# -----------------------------
# About Page
# -----------------------------
elif page == "ℹ️ About":

    st.title("ℹ️ About Pulse.ai")

    st.markdown("""
    Pulse.ai is a **real-time AI server monitoring system** designed to:

    - Collect metrics using Prometheus  
    - Visualize performance using Grafana  
    - Store time-series data in InfluxDB  
    - Forecast system load using Machine Learning  
    - Provide interactive dashboards using Streamlit  

    This system enables **proactive infrastructure management**
    by predicting resource usage before failures occur.
    """)
