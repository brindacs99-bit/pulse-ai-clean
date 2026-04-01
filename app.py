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

PROMETHEUS_URL = "http://localhost:9090"

# -----------------------------
# GET SERVER + PAGE FROM URL
# -----------------------------
query_params = st.query_params

page = query_params.get("page", "home")
server = query_params.get("server", "mac-host")

if isinstance(page, list):
    page = page[0]

if isinstance(server, list):
    server = server[0]

# -----------------------------
# MAP SERVERS (ONLY FOR LABEL DISPLAY)
# -----------------------------
SERVER_MAP = {
    "mac-host": "Mac",
    "server-2": "Docker",
    "server-3": "Test"
}

# -----------------------------
# PROMETHEUS QUERY
# -----------------------------
def query_prometheus(query):
    url = f"{PROMETHEUS_URL}/api/v1/query"

    try:
        response = requests.get(url, params={"query": query}, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get("data", {}).get("result", [])
    except:
        return []

    return []

# -----------------------------
# CPU USAGE (FIXED)
# -----------------------------
def get_cpu_usage():
    query = '''
    100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[1m])) * 100)
    '''

    result = query_prometheus(query)

    if result:
        return float(result[0]["value"][1])

    return 0


# -----------------------------
# RAM USAGE (FIXED)
# -----------------------------
def get_ram_usage():
    query = '''
    (1 - (
        node_memory_MemAvailable_bytes
        /
        node_memory_MemTotal_bytes
    )) * 100
    '''

    result = query_prometheus(query)

    if result:
        return float(result[0]["value"][1])

    return 0


# -----------------------------
# HISTORY CPU (FIXED)
# -----------------------------
def get_cpu_history():
    query = '''
    100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[1m])) * 100)
    '''

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
        response = requests.get(url, params=params, timeout=5)
        data = response.json()

        if data["data"]["result"]:
            values = data["data"]["result"][0]["values"]
            return [float(v[1]) for v in values]

    except:
        return []

    return []


# -----------------------------
# HISTORY RAM (FIXED)
# -----------------------------
def get_ram_history():
    query = '''
    (1 - (
        node_memory_MemAvailable_bytes
        /
        node_memory_MemTotal_bytes
    )) * 100
    '''

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
        response = requests.get(url, params=params, timeout=5)
        data = response.json()

        if data["data"]["result"]:
            values = data["data"]["result"][0]["values"]
            return [float(v[1]) for v in values]

    except:
        return []

    return []


# -----------------------------
# CURRENT METRICS
# -----------------------------
cpu = get_cpu_usage()
ram = get_ram_usage()

# -----------------------------
# HOME
# -----------------------------
if page == "home":

    st.title(f"🚀 Pulse.ai ({server})")

    col1, col2 = st.columns(2)
    col1.metric("CPU Usage", f"{cpu:.2f}%")
    col2.metric("RAM Usage", f"{ram:.2f}%")


# -----------------------------
# MONITORING
# -----------------------------
elif page == "monitoring":

    st.title(f"📊 Monitoring ({server})")

    grafana_url = (
        f"http://localhost:3000/d/rYdddlPWk"
        f"?refresh=5s&kiosk"
    )

    st.components.v1.iframe(grafana_url, height=900)


# -----------------------------
# FORECAST
# -----------------------------
elif page == "forecast":

    st.title(f"🤖 Forecast ({server})")

    history_cpu = get_cpu_history()
    history_ram = get_ram_history()

    if len(history_cpu) == 0:
        history_cpu = list(np.random.normal(40, 10, 20))

    if len(history_ram) == 0:
        history_ram = list(np.random.normal(50, 10, 20))

    cpu_pred, ram_pred = predict_future(steps=10)

    col1, col2 = st.columns(2)
    col1.metric("Predicted CPU Avg", f"{np.mean(cpu_pred):.2f}%")
    col2.metric("Predicted RAM Avg", f"{np.mean(ram_pred):.2f}%")

    df = pd.DataFrame({
        "CPU": history_cpu + list(cpu_pred),
        "RAM": history_ram + list(ram_pred)
    })

    st.line_chart(df)


# -----------------------------
# ALERTS
# -----------------------------
elif page == "alerts":

    st.title(f"🚨 Alerts ({server})")

    cpu_threshold = st.slider("CPU Threshold", 0, 100, 80)
    ram_threshold = st.slider("RAM Threshold", 0, 100, 80)

    if cpu > cpu_threshold:
        st.error("⚠ CPU High")
    else:
        st.success("✅ CPU Normal")

    if ram > ram_threshold:
        st.error("⚠ RAM High")
    else:
        st.success("✅ RAM Normal")


# -----------------------------
# ABOUT
# -----------------------------
elif page == "about":

    st.title("ℹ️ About Pulse.ai")

    st.markdown("""
### 🚀 What is Pulse.ai?

Pulse.ai is an AI-powered observability platform that monitors servers in real time and predicts future resource usage.

---

### 🧠 What it does:

- 📊 Real-time monitoring using **Prometheus**
- 📈 Visualization dashboards via **Grafana**
- 🤖 AI-based forecasting using machine learning
- 🚨 Smart alert system based on thresholds
- ⚡ Interactive dashboards powered by **Streamlit**

---

### 🏗️ Architecture:

- Prometheus → Collects metrics  
- Grafana → Visualizes system performance  
- Node Exporter → Provides server metrics  
- ML Model → Predicts future CPU & RAM usage  
- Streamlit → Displays intelligent dashboards  

---

### 🎯 Goal:

To help system administrators:
- Detect issues early  
- Predict future load  
- Avoid downtime  
- Optimize performance  

---

💡 Built as a full-stack AI-powered monitoring system.
""")


# -----------------------------
# FALLBACK
# -----------------------------
else:
    st.error("Page not found")