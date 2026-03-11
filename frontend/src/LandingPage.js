import React from "react";
import { Link } from "react-router-dom";
import "./LandingPage.css";

function LandingPage() {

  return (

    <div>

      {/* HERO SECTION */}

      <div className="hero">

        <div className="hero-left">

          <h1>
            AI Powered Server Monitoring & Forecasting
          </h1>

          <p>
            Pulse.ai provides real-time infrastructure monitoring using
            Prometheus and Grafana while predicting future server load
            using machine learning models.
          </p>

          <div className="features">
            <span>Real Time Monitoring</span>
            <span>AI Forecasting</span>
            <span>Alert System</span>
            <span>Infrastructure Insights</span>
          </div>

        </div>


        {/* SIGNUP CARD */}

        <div className="hero-right">

          <div className="signup-card">

            <h2>Start Monitoring Your Servers</h2>

            <input type="email" placeholder="Email" />

            <input type="password" placeholder="Password" />

            {/* GET STARTED BUTTON */}

            <Link to="/signup">
              <button>
                GET STARTED
              </button>
            </Link>

          </div>

        </div>

      </div>

    </div>

  );

}

export default LandingPage;