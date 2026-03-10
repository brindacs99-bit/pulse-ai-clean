require("dotenv").config();
const express = require("express");
const axios = require("axios");
const cors = require("cors");
const path = require("path");
const { exec } = require("child_process");

const app = express();
app.use(cors());
app.use(express.json());

const PORT = process.env.PORT || 5000;
const isProduction = process.env.NODE_ENV === "production";
const PROM_URL = process.env.PROM_URL || "http://localhost:9090/api/v1/query";

/* ---------------- CPU ---------------- */

app.get("/cpu", async (req, res) => {
  try {
    const response = await axios.get(PROM_URL, {
      params: {
        query:
          "100 - (avg(irate(node_cpu_seconds_total{mode='idle'}[5m])) * 100)",
      },
    });

    let value = response.data.data.result[0]?.value[1] || 0;
    value = Math.max(0, parseFloat(value)).toFixed(2);

    res.json({ cpu: value });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

/* ---------------- MEMORY ---------------- */

app.get("/memory", async (req, res) => {
  try {
    const response = await axios.get(PROM_URL, {
      params: {
        query:
          "(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100",
      },
    });

    let value = response.data.data.result[0]?.value[1] || 0;
    value = parseFloat(value).toFixed(2);

    res.json({ memory: value });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

/* ---------------- DISK ---------------- */

app.get("/disk", async (req, res) => {
  try {
    const response = await axios.get(PROM_URL, {
      params: {
        query:
          "(node_filesystem_size_bytes - node_filesystem_free_bytes) / node_filesystem_size_bytes * 100",
      },
    });

    let value = response.data.data.result[0]?.value[1] || 0;
    value = parseFloat(value).toFixed(2);

    res.json({ disk: value });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

/* ---------------- NETWORK ---------------- */

app.get("/network", async (req, res) => {
  try {
    const response = await axios.get(PROM_URL, {
      params: {
        query: "rate(node_network_receive_bytes_total[5m])",
      },
    });

    let value = response.data.data.result[0]?.value[1] || 0;
    value = parseFloat(value).toFixed(2);

    res.json({ network: value });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

/* ---------------- FORECAST ---------------- */

const PYTHON_CMD =
  process.env.PYTHON_CMD || (process.platform === "win32" ? "python" : "python3");
const PROJECT_ROOT = __dirname;

app.get("/forecast", (req, res) => {
  exec(
    `${PYTHON_CMD} model_predict.py`,
    { cwd: PROJECT_ROOT, maxBuffer: 1024 * 1024 },
    (error, stdout, stderr) => {
      const output = (stdout || "").trim();
      const errOutput = (stderr || "").trim();

      // Python may exit(1) but still print JSON like {"error": "..."}
      if (output) {
        try {
          const result = JSON.parse(output);
          if (result.error) {
            return res.status(503).json({ error: result.error });
          }
          return res.json(result);
        } catch {
          // not JSON – fall through to generic error
        }
      }

      if (error) {
        const message = errOutput || error.message || "Forecast failed.";
        return res.status(500).json({ error: message });
      }

      res
        .status(500)
        .json({ error: "Invalid forecast output", raw: output || errOutput });
    }
  );
});

/* ---------------- SERVE REACT BUILD (FULL STACK) ---------------- */

// Always serve the built React app
app.use(express.static(path.join(__dirname, "frontend", "build")));

app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "frontend", "build", "index.html"));
});

// SPA fallback (Express 5 path-to-regexp syntax)
app.get("/{*path}", (req, res) => {
  res.sendFile(path.join(__dirname, "frontend", "build", "index.html"));
});

/* ---------------- START SERVER ---------------- */

app.listen(PORT, () => {
  console.log(
    `Server running on port ${PORT}${
      isProduction ? " (serving full-stack app)" : ""
    }`
  );
});