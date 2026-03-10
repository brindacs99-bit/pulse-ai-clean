"""
Shared config for Pulse.ai Python scripts.
Read from environment; fallbacks match docker-compose defaults.
"""
import os
from pathlib import Path

# InfluxDB (align with docker-compose and Telegraf)
INFLUX_URL = os.getenv("INFLUX_URL", "http://localhost:8086")
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN", "pulse-ai-secure-token")
INFLUX_ORG = os.getenv("INFLUX_ORG", "pulse-ai")
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET", "metrics")

# Prometheus
PROMETHEUS_URL = os.getenv("PROMETHEUS_URL", "http://localhost:9090")

# Paths (project root = parent of src/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODELS_DIR = PROJECT_ROOT / "models"
DATA_RAW_DIR = PROJECT_ROOT / "data" / "raw"
DATA_PREPROCESSED_DIR = PROJECT_ROOT / "data" / "preprocessed"
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"

# Model files used by model_predict.py and model_train.py
CPU_MODEL_PATH = MODELS_DIR / "cpu_model.pkl"
RAM_MODEL_PATH = MODELS_DIR / "ram_model.pkl"
