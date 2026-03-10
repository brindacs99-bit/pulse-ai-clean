import numpy as np
import pandas as pd
import joblib
from influxdb_client import InfluxDBClient
from sklearn.linear_model import LinearRegression

from src.config import (
    INFLUX_URL,
    INFLUX_TOKEN,
    INFLUX_ORG,
    INFLUX_BUCKET,
    MODELS_DIR,
    CPU_MODEL_PATH,
    RAM_MODEL_PATH,
)

# ----------------------------
# Connect to InfluxDB
# ----------------------------
client = InfluxDBClient(
    url=INFLUX_URL,
    token=INFLUX_TOKEN,
    org=INFLUX_ORG,
)

query_api = client.query_api()

# ----------------------------
# Fetch last 10 minutes data
# ----------------------------
query = f'''
from(bucket: "{INFLUX_BUCKET}")
  |> range(start: -10m)
  |> filter(fn: (r) => r._measurement == "system_metrics")
  |> filter(fn: (r) => r._field == "cpu_usage" or r._field == "ram_usage")
'''

tables = query_api.query(query)

records = []
for table in tables:
    for row in table.records:
        records.append({
            "time": row.get_time(),
            "field": row.get_field(),
            "value": row.get_value()
        })

df = pd.DataFrame(records)

print("DEBUG → Total records fetched:", len(df))

if df.empty:
    raise Exception("No data found in InfluxDB")

# ----------------------------
# Prepare Dataset
# ----------------------------
cpu_df = df[df["field"] == "cpu_usage"].sort_values("time")
ram_df = df[df["field"] == "ram_usage"].sort_values("time")

X = np.arange(len(cpu_df)).reshape(-1, 1)
y_cpu = cpu_df["value"].values
y_ram = ram_df["value"].values

# ----------------------------
# Train Models
# ----------------------------
cpu_model = LinearRegression()
ram_model = LinearRegression()

cpu_model.fit(X, y_cpu)
ram_model.fit(X, y_ram)

# ----------------------------
# Save Models
# ----------------------------
MODELS_DIR.mkdir(parents=True, exist_ok=True)
joblib.dump(cpu_model, str(CPU_MODEL_PATH))
joblib.dump(ram_model, str(RAM_MODEL_PATH))

print("✅ AI models trained and saved successfully")