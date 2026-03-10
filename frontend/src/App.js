import React, { useEffect, useState } from "react";
import axios from "axios";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Line } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const API_BASE = process.env.REACT_APP_API_URL || "";

function App() {
  const [cpu, setCpu] = useState(0);
  const [memory, setMemory] = useState(0);
  const [disk, setDisk] = useState(0);
  const [network, setNetwork] = useState(0);
  const [forecast, setForecast] = useState(null);
  const [forecastLoading, setForecastLoading] = useState(false);
  const [forecastError, setForecastError] = useState(null);

  const getMetrics = async () => {
    try {
      const [cpuRes, memRes, diskRes, netRes] = await Promise.all([
        axios.get(`${API_BASE}/cpu`),
        axios.get(`${API_BASE}/memory`),
        axios.get(`${API_BASE}/disk`),
        axios.get(`${API_BASE}/network`),
      ]);
      setCpu(cpuRes.data.cpu);
      setMemory(memRes.data.memory);
      setDisk(diskRes.data.disk);
      setNetwork(netRes.data.network);
    } catch (err) {
      console.log("API error", err);
    }
  };

  const getForecast = async () => {
    setForecastLoading(true);
    setForecastError(null);
    try {
      const res = await axios.get(`${API_BASE}/forecast`);
      setForecast(res.data);
    } catch (err) {
      setForecastError(err.response?.data?.error || err.message);
    } finally {
      setForecastLoading(false);
    }
  };

  useEffect(() => {
    getMetrics();
    const interval = setInterval(getMetrics, 5000);
    return () => clearInterval(interval);
  }, []);

  const cardStyle = {
    background: "white",
    padding: "20px",
    margin: "15px",
    borderRadius: "10px",
    width: "200px",
    boxShadow: "0px 4px 10px rgba(0,0,0,0.1)",
  };

  const forecastChartOptions = {
    responsive: true,
    plugins: {
      legend: { position: "top" },
      title: { display: true, text: "AI Forecast – Next 10 steps" },
    },
    scales: {
      y: { beginAtZero: true, title: { display: true, text: "Usage %" } },
      x: { title: { display: true, text: "Step" } },
    },
  };

  const forecastChartData = forecast
    ? {
        labels: (forecast.cpu_forecast || []).map((_, i) => `Step ${i + 1}`),
        datasets: [
          {
            label: "CPU forecast %",
            data: forecast.cpu_forecast || [],
            borderColor: "rgb(75, 192, 192)",
            backgroundColor: "rgba(75, 192, 192, 0.1)",
            tension: 0.3,
          },
          {
            label: "RAM forecast %",
            data: forecast.ram_forecast || [],
            borderColor: "rgb(255, 99, 132)",
            backgroundColor: "rgba(255, 99, 132, 0.1)",
            tension: 0.3,
          },
        ],
      }
    : null;

  return (
    <div
      style={{
        textAlign: "center",
        fontFamily: "Arial",
        background: "#f4f6f9",
        minHeight: "100vh",
        paddingTop: "40px",
        paddingBottom: "40px",
      }}
    >
      <h1>🚀 Pulse AI Server Monitoring</h1>

      <div
        style={{
          display: "flex",
          justifyContent: "center",
          flexWrap: "wrap",
          marginTop: "30px",
        }}
      >
        <div style={cardStyle}>
          <h3>CPU Usage</h3>
          <h2>{cpu}%</h2>
        </div>
        <div style={cardStyle}>
          <h3>Memory Usage</h3>
          <h2>{memory}%</h2>
        </div>
        <div style={cardStyle}>
          <h3>Disk Usage</h3>
          <h2>{disk}%</h2>
        </div>
        <div style={cardStyle}>
          <h3>Network</h3>
          <h2>{network}</h2>
        </div>
      </div>

      <section
        style={{
          maxWidth: "800px",
          margin: "40px auto",
          background: "white",
          padding: "24px",
          borderRadius: "12px",
          boxShadow: "0px 4px 10px rgba(0,0,0,0.1)",
        }}
      >
        <h2>🤖 AI Forecasting</h2>
        <p style={{ color: "#666", marginBottom: "16px" }}>
          Predict CPU and RAM usage for the next 10 steps using trained ML models.
        </p>
        <button
          onClick={getForecast}
          disabled={forecastLoading}
          style={{
            padding: "10px 20px",
            fontSize: "16px",
            cursor: forecastLoading ? "not-allowed" : "pointer",
            borderRadius: "8px",
            border: "none",
            background: "#4a90d9",
            color: "white",
          }}
        >
          {forecastLoading ? "Running prediction…" : "Run forecast"}
        </button>
        {forecastError && (
          <div style={{ color: "#c00", marginTop: "12px", textAlign: "left", maxWidth: "560px", margin: "12px auto" }}>
            <p>{forecastError}</p>
            {forecastError.includes("not found") || forecastError.includes("Run training") ? (
              <p style={{ fontSize: "14px", color: "#666", marginTop: "8px" }}>
                Quick fix: run <code>python scripts/train_demo_models.py</code> from the project root to create demo models (no InfluxDB needed).
              </p>
            ) : null}
          </div>
        )}
        {forecastChartData && (
          <div style={{ marginTop: "24px", height: "300px" }}>
            <Line options={forecastChartOptions} data={forecastChartData} />
          </div>
        )}
      </section>
    </div>
  );
}

export default App;
