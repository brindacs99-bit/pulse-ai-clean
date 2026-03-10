import time
import requests
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

from src.config import (
    PROMETHEUS_URL,
    INFLUX_URL,
    INFLUX_TOKEN,
    INFLUX_ORG,
    INFLUX_BUCKET,
)

# ---------------------------
# InfluxDB Client
# ---------------------------
client = InfluxDBClient(
    url=INFLUX_URL,
    token=INFLUX_TOKEN,
    org=INFLUX_ORG,
)

write_api = client.write_api(write_options=SYNCHRONOUS)

# ---------------------------
# Prometheus Queries
# ---------------------------
CPU_QUERY = (
    "100 - (avg by (instance) "
    "(rate(node_cpu_seconds_total{mode='idle'}[1m])) * 100)"
)

RAM_QUERY = (
    "(1 - (node_memory_MemAvailable_bytes "
    "/ node_memory_MemTotal_bytes)) * 100"
)

# ---------------------------
# Helper function
# ---------------------------
def query_prometheus(query):
    response = requests.get(
        f"{PROMETHEUS_URL}/api/v1/query",
        params={"query": query}
    )
    result = response.json()["data"]["result"]
    return float(result[0]["value"][1]) if result else None

# ---------------------------
# Main Loop
# ---------------------------
print("🚀 Pulse.ai Collector Started")

while True:
    try:
        cpu = query_prometheus(CPU_QUERY)
        ram = query_prometheus(RAM_QUERY)

        if cpu is not None and ram is not None:
            point = (
                Point("system_metrics")
                .field("cpu_usage", cpu)
                .field("ram_usage", ram)
            )

            write_api.write(bucket=INFLUX_BUCKET, record=point)

            print(f"✅ Stored → CPU: {cpu:.2f}% | RAM: {ram:.2f}%")

        time.sleep(10)

    except Exception as e:
        print("❌ Error:", e)
        time.sleep(10)