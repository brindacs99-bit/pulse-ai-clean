import React from "react";
import { useNavigate } from "react-router-dom";

function Header() {

  const navigate = useNavigate();

  return (

    <nav className="navbar">

      <div className="logo-section" onClick={() => navigate("/")}>
        <img src="/logo.png" alt="Pulse AI Logo" className="logo"/>
        <h2>Pulse.ai</h2>
      </div>

      <div className="nav-links">

        <button onClick={() => navigate("/")}>
          Features
        </button>

        <button onClick={() => navigate("/dashboard?page=monitoring")}>
          Monitoring
        </button>

        <button onClick={() => navigate("/dashboard?page=forecast")}>
          Forecast
        </button>

        <button onClick={() => navigate("/dashboard?page=alerts")}>
          Alerts
        </button>

        <button onClick={() => navigate("/dashboard?page=about")}>
          About
        </button>

        <button onClick={() => navigate("/login")}>
          Login
        </button>

      </div>

    </nav>

  );

}

export default Header;