import React from "react";
import { useNavigate } from "react-router-dom";

function Header() {

  const navigate = useNavigate();

  const isLoggedIn = localStorage.getItem("auth");
  const user = localStorage.getItem("user");
  const server = localStorage.getItem("server"); // ✅ get server

  const handleLogout = () => {
    localStorage.clear();
    navigate("/login");
  };

  return (

    <nav className="navbar">

      {/* LOGO */}
      <div
        className="logo-section"
        onClick={() => isLoggedIn
          ? navigate(`/dashboard?page=home`)
          : navigate("/")
        }
      >
        <img src="/logo.png" alt="Pulse AI Logo" className="logo"/>
        <h2>Pulse.ai</h2>
      </div>

      {/* NAVIGATION */}
      <div className="nav-links">

        {/* ✅ HOME */}
        <button onClick={() => navigate("/dashboard?page=home")}>
          Home
        </button>

        {/* ✅ ALL ROUTES FIXED */}
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

        {/* ✅ LOGIN / LOGOUT */}
        {isLoggedIn ? (
          <button onClick={handleLogout}>
            Logout ({user})
          </button>
        ) : (
          <button onClick={() => navigate("/login")}>
            Login
          </button>
        )}

      </div>

    </nav>

  );

}

export default Header;