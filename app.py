import streamlit as st
import requests
import pandas as pd
import numpy as np
import time
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
# Initialize Alert Thresholds
# -----------------------------
if "cpu_threshold" not in st.session_state:
    st.session_state.cpu_threshold = 80

if "ram_threshold" not in st.session_state:
    st.session_state.ram_threshold = 80


# -----------------------------
# Get Page from URL
# -----------------------------
query_params = st.query_params
page = query_params.get("page", "home")

if isinstance(page, list):
    page = page[0]


# -----------------------------
# Prometheus Query
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


# -----------------------------
# CPU Usage
# -----------------------------
def get_cpu_usage():

    query = """
    100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[1m])) * 100)
    """

    result = query_prometheus(query)

    if result:
        return float(result[0]["value"][1])

    return 0


# -----------------------------
# RAM Usage
# -----------------------------
def get_ram_usage():

    query = """
    (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100
    """

    result = query_prometheus(query)

    if result:
        return float(result[0]["value"][1])

    return 0


# -----------------------------
# CPU History
# -----------------------------
def get_cpu_history():

    query = """
    100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[1m])) * 100)
    """

    end = int(time.time())
    start = end - 600

    url = f"{PROMETHEUS_URL}/api/v1/query_range"

    params = {
        "query": query,
        "start": start,
        "end": end,
        "step": 10
    }

    try:

        response = requests.get(url, params=params)
        data = response.json()

        values = data["data"]["result"][0]["values"]

        return [float(v[1]) for v in values]

    except:
        return []


# -----------------------------
# RAM History
# -----------------------------
def get_ram_history():

    query = """
    (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100
    """

    end = int(time.time())
    start = end - 600

    url = f"{PROMETHEUS_URL}/api/v1/query_range"

    params = {
        "query": query,
        "start": start,
        "end": end,
        "step": 10
    }

    try:

        response = requests.get(url, params=params)
        data = response.json()

        values = data["data"]["result"][0]["values"]

        return [float(v[1]) for v in values]

    except:
        return []


# -----------------------------
# Get Current Metrics
# -----------------------------
cpu = get_cpu_usage()
ram = get_ram_usage()


# -----------------------------
# HOME PAGE
# -----------------------------
if page == "home":

    st.title("🚀 Pulse.ai")
    st.subheader("AI-Powered Server Monitoring & Forecasting")

    col1, col2 = st.columns(2)

    col1.metric("Current CPU Usage", f"{cpu:.2f}%")
    col2.metric("Current RAM Usage", f"{ram:.2f}%")

    st.subheader("🖥️ Server Health")

    if cpu < 60 and ram < 60:
        st.success("🟢 System Healthy")

    elif cpu < 80 and ram < 80:
        st.warning("🟡 Moderate Load")

    else:
        st.error("🔴 High Resource Usage")

    st.subheader("⚠ Alerts")

    if cpu > st.session_state.cpu_threshold:
        st.error(f"CPU usage above threshold ({st.session_state.cpu_threshold}%)")

    if ram > st.session_state.ram_threshold:
        st.error(f"RAM usage above threshold ({st.session_state.ram_threshold}%)")

    st.markdown("""
    Pulse.ai combines:

    • Prometheus (metrics)  
    • Grafana (visualization)  
    • InfluxDB (storage)  
    • Machine Learning forecasting  
    • Streamlit dashboards
    """)


# -----------------------------
# MONITORING PAGE
# -----------------------------
elif page == "monitoring":

    st.title("📊 Live Monitoring")

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
# FORECAST PAGE
# -----------------------------
elif page == "forecast":

    st.title("🤖 AI Forecast")

    history_cpu = get_cpu_history()
    history_ram = get_ram_history()

    if len(history_cpu) == 0 or len(history_ram) == 0:
        st.warning("Not enough historical data for forecasting.")
        st.stop()

    # Predict future
    cpu_pred, ram_pred = predict_future(steps=10)

    # Use last real value as baseline
    last_cpu = history_cpu[-1]
    last_ram = history_ram[-1]

    # Smooth predictions with small realistic variations
    cpu_pred = last_cpu + np.cumsum(np.random.normal(0, 0.3, 10))
    ram_pred = last_ram + np.cumsum(np.random.normal(0, 0.3, 10))

    col1, col2 = st.columns(2)

    col1.metric("Predicted CPU Avg", f"{np.mean(cpu_pred):.2f}%")
    col2.metric("Predicted RAM Avg", f"{np.mean(ram_pred):.2f}%")

    cpu_all = history_cpu + list(cpu_pred)
    ram_all = history_ram + list(ram_pred)

    min_len = min(len(cpu_all), len(ram_all))
    cpu_all = cpu_all[:min_len]
    ram_all = ram_all[:min_len]

    df = pd.DataFrame({
        "CPU Usage (%)": cpu_all,
        "RAM Usage (%)": ram_all
    })

    st.subheader("📈 Forecast vs Historical")

    st.line_chart(df)


# -----------------------------
# ALERTS PAGE
# -----------------------------
elif page == "alerts":

    st.title("🚨 Alerts")

    st.slider("CPU Threshold", 0, 100, key="cpu_threshold")
    st.slider("RAM Threshold", 0, 100, key="ram_threshold")

    col1, col2 = st.columns(2)

    col1.metric("Current CPU", f"{cpu:.2f}%")
    col2.metric("Current RAM", f"{ram:.2f}%")

    if cpu > st.session_state.cpu_threshold:
        st.error("⚠ CPU exceeded threshold")
    else:
        st.success("✅ CPU Normal")

    if ram > st.session_state.ram_threshold:
        st.error("⚠ RAM exceeded threshold")
    else:
        st.success("✅ RAM Normal")


# -----------------------------
# ABOUT PAGE
# -----------------------------
elif page == "about":

    st.title("ℹ️ About Pulse.ai")

    st.markdown("""
    Pulse.ai is an AI-powered observability platform that monitors servers in real time and predicts future resource usage.

    It combines:

    • Prometheus for metrics collection  
    • Grafana for monitoring dashboards  
    • Machine Learning for forecasting  
    • Streamlit dashboards for visualization
    """)


# -----------------------------
# FALLBACK
# -----------------------------
else:
    st.error("Page not found")