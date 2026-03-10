import numpy as np
import pandas as pd
import joblib
from influxdb_client import InfluxDBClient

# ----------------------------
# InfluxDB Configuration
# ----------------------------
INFLUX_URL = "http://localhost:8086"
INFLUX_TOKEN = "pulse-ai-secure-token"
ORG = "pulse-ai"
BUCKET = "metrics"

# ----------------------------
# Load trained models
# ----------------------------
cpu_model = joblib.load("models/cpu_model.pkl")
ram_model = joblib.load("models/ram_model.pkl")

# ----------------------------
# Connect to InfluxDB
# ----------------------------
client = InfluxDBClient(
    url=INFLUX_URL,
    token=INFLUX_TOKEN,
    org=ORG
)

query_api = client.query_api()

# ----------------------------
# Fetch recent metrics
# ----------------------------
def fetch_recent_metrics():

    query = f'''
    from(bucket:"{BUCKET}")
      |> range(start: -10m)
      |> filter(fn:(r) => r["_measurement"] == "system")
      |> filter(fn:(r) => r["_field"] == "cpu_usage" or r["_field"] == "ram_usage")
      |> pivot(rowKey:["_time"], columnKey:["_field"], valueColumn:"_value")
      |> keep(columns: ["cpu_usage","ram_usage"])
    '''

    tables = query_api.query_data_frame(query)

    if isinstance(tables, list):
        df = pd.concat(tables)

    else:
        df = tables

    return df

# ----------------------------
# Prediction function
# ----------------------------
def predict_future(steps=10):

    try:

        df = fetch_recent_metrics()

        if df.empty:
            raise ValueError("No data")

        cpu_history = df["cpu_usage"].values[-steps:]
        ram_history = df["ram_usage"].values[-steps:]

    except:

        # fallback if DB not ready
        cpu_history = np.random.normal(30, 5, steps)
        ram_history = np.random.normal(40, 5, steps)

    X_future = np.arange(len(cpu_history), len(cpu_history) + steps).reshape(-1,1)

    cpu_pred = cpu_model.predict(X_future)
    ram_pred = ram_model.predict(X_future)

    cpu_pred = np.clip(cpu_pred, 0, 100)
    ram_pred = np.clip(ram_pred, 0, 100)

    return cpu_pred, ram_pred
