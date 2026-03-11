import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import Layout from "./components/Layout";
import LandingPage from "./LandingPage";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Dashboard from "./pages/Dashboard";
import Forecast from "./pages/Forecast";
import Alerts from "./pages/Alerts";
import About from "./pages/About";

/* ---------------- PROTECTED ROUTE ---------------- */

function PrivateRoute({ children }) {

  const isLoggedIn = localStorage.getItem("auth");

  return isLoggedIn ? children : <Navigate to="/login" />;

}

/* ---------------- APP ROUTER ---------------- */

function App() {

  return (

    <BrowserRouter>

      <Routes>

        <Route element={<Layout />}>

          {/* Landing Page */}

          <Route path="/" element={<LandingPage />} />

          {/* Signup */}

          <Route path="/signup" element={<Signup />} />

          {/* Login */}

          <Route path="/login" element={<Login />} />

          {/* Dashboard (Protected) */}

          <Route
            path="/dashboard"
            element={
              <PrivateRoute>
                <Dashboard />
              </PrivateRoute>
            }
          />

          {/* Forecast */}

          <Route
            path="/forecast"
            element={
              <PrivateRoute>
                <Forecast />
              </PrivateRoute>
            }
          />

          {/* Alerts */}

          <Route
            path="/alerts"
            element={
              <PrivateRoute>
                <Alerts />
              </PrivateRoute>
            }
          />

          {/* About */}

          <Route path="/about" element={<About />} />

        </Route>

      </Routes>

    </BrowserRouter>

  );

}

export default App;