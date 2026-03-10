# Pulse.ai – How Everything Is Linked

This doc explains how the pieces connect and how to run the full stack.

## One config to rule them all

- **`.env`** – Copy from `.env.example`, fill in if needed. Used by:
  - **Express** (`server.js`) via `dotenv`: `PORT`, `PROM_URL`, `NODE_ENV`
  - **Python** (optional): set `INFLUX_URL`, `INFLUX_TOKEN`, `INFLUX_ORG`, `INFLUX_BUCKET`, `PROMETHEUS_URL` so all scripts and Streamlit use the same values
- **`src/config.py`** – Single source of truth for Python: Influx, Prometheus, and paths. Used by:
  - `src/collector.py` – Prometheus → InfluxDB (writes `system_metrics`)
  - `src/model_train.py` – Reads from Influx, saves `models/cpu_model.pkl`, `models/ram_model.pkl`
  - `src/ingestion.py` – Reads from Influx (with Docker env fallback)
  - `model_predict.py` – Loads models from `config` paths, used by Express `/forecast` and Streamlit
- **Telegraf** (`telegraf/telegraf.conf`) – Same Influx org/bucket/token as Docker and Python (`pulse-ai` / `metrics` / `pulse-ai-secure-token`).

## Data flow

```
Node Exporter → Prometheus (scrape)
                     ↓
    ┌────────────────┴────────────────┐
    │                                  │
    ▼                                  ▼
Express (server.js)              src/collector.py
 /cpu, /memory, /disk, /network        ↓
    │                          InfluxDB (metrics bucket)
    │                                  │
    │                                  ▼
    │                          model_train.py → models/*.pkl
    │                                  │
    ▼                                  ▼
React (frontend)              model_predict.py ← used by Express /forecast
    │                          and by Streamlit AI Forecasting page
    └───────────────────────────────
```

- **Live metrics**: React and Streamlit both get CPU/RAM/disk/network. React gets them only via **Express** (Prometheus). Streamlit can use **Prometheus** directly (same data source, different client).
- **Forecast**: One implementation (`model_predict.py`). Called by Express (`/forecast`) for React, and imported by Streamlit for its “AI Forecasting” page. Models come from `models/` (trained by `model_train.py` from Influx `system_metrics`).

## Two UIs (both linked to the same backend data)

| UI | How it gets data | When to use |
|----|------------------|-------------|
| **React (Express)** | Only via Express API (`/cpu`, `/memory`, `/disk`, `/network`, `/forecast`) | Full-stack app: one server serves API + React build. |
| **Streamlit** | Prometheus directly + `model_predict.predict_future` in-process | Docker stack: Grafana embed, same metrics + forecast. |

For a single “source of truth” API, use the **Express** backend; React already uses it. Streamlit can later be switched to call Express instead of Prometheus/model_predict if you want one gateway.

## How to run

### Option A: Full stack locally (React + Express + Python forecast)

```bash
# 1. Config (optional)
cp .env.example .env
# Edit .env if you need different ports or Prometheus URL

# 2. Backend + frontend together
npm install
cd frontend && npm install && cd ..
npm run dev
```

- Backend: http://localhost:5000  
- Frontend: http://localhost:3000 (proxies API to 5000)

Prometheus must be running (e.g. `docker-compose up -d prometheus node-exporter`) for live metrics. For **forecast** you need trained models:

- **Quick demo (no InfluxDB):** `python scripts/train_demo_models.py` – creates `models/cpu_model.pkl` and `models/ram_model.pkl` from synthetic data.
- **Real training:** Run the collector (so InfluxDB has `system_metrics`), then `python -m src.model_train` (see README).

### Option B: Production build (one server)

```bash
npm run build
npm start
```

Serves API + React at http://localhost:5000. Set `PORT` and `PROM_URL` in `.env` if needed.

### Option C: Docker (entire stack including React + Express)

```bash
docker-compose up -d
```

- **Web (Express + React)**: http://localhost:5000  
- **Streamlit**: http://localhost:8501  
- **Grafana**: http://localhost:3000  
- **Prometheus**: http://localhost:9090  
- **InfluxDB**: http://localhost:8086  
- **MLflow**: http://localhost:5050  

The `web` service uses `PROM_URL=http://prometheus:9090/api/v1/query`. Mount `./models` so forecast works (run training first or copy existing `models/`).

### Option D: Docker (Streamlit-only UI)

Same as above; use http://localhost:8501. Streamlit uses `PROMETHEUS_URL` (default `http://prometheus:9090` in Docker).

## Port summary

| Port | Service |
|------|--------|
| 3000 | Grafana |
| 5000 | Express + React (web) |
| 5050 | MLflow (host) |
| 8086 | InfluxDB |
| 8501 | Streamlit |
| 9090 | Prometheus |

## Optional next improvements

1. **Single API for Streamlit** – Point Streamlit at Express for metrics and forecast so one backend serves both UIs.
2. **Wire MLflow to training** – Log runs/artifacts from `model_train.py` so experiments are tracked.
3. **Unify Influx schemas** – Collector writes `system_metrics`; ingestion uses `cpu`/`mem` (Telegraf). Either train from one schema or align both.
