"""
Train minimal CPU/RAM models on synthetic data so forecasting works without InfluxDB.
Run from project root: python scripts/train_demo_models.py
"""
import sys
from pathlib import Path

# Add project root so "from src.config" works
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np
import joblib
from sklearn.linear_model import LinearRegression

from src.config import MODELS_DIR, CPU_MODEL_PATH, RAM_MODEL_PATH

def main():
    # Synthetic time-series: slight trend + noise (similar to real CPU/RAM)
    n = 60
    X = np.arange(n).reshape(-1, 1)
    np.random.seed(42)
    y_cpu = 20 + 0.3 * np.arange(n) + np.random.randn(n) * 5
    y_ram = 50 + 0.1 * np.arange(n) + np.random.randn(n) * 3

    cpu_model = LinearRegression()
    ram_model = LinearRegression()
    cpu_model.fit(X, y_cpu)
    ram_model.fit(X, y_ram)

    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(cpu_model, str(CPU_MODEL_PATH))
    joblib.dump(ram_model, str(RAM_MODEL_PATH))

    print("Demo models saved to models/cpu_model.pkl and models/ram_model.pkl")
    print("You can now use 'Run forecast' in the app.")


if __name__ == "__main__":
    main()
