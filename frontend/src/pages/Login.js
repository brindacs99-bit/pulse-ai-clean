import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

// ✅ USERS + SERVER MAPPING
const USERS = {
  "admin1@gmail.com": { password: "admin@123", server: "mac-host" },
  "admin2@gmail.com": { password: "admin@123", server: "server-2" },
  "admin3@gmail.com": { password: "admin@123", server: "server-3" }
};

function Login() {

  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  // ✅ AUTO REDIRECT IF ALREADY LOGGED IN
  useEffect(() => {
    const isLoggedIn = localStorage.getItem("auth");
    if (isLoggedIn) {
      navigate("/dashboard?page=home");
    }
  }, [navigate]);

  const handleLogin = (e) => {
    e.preventDefault();

    const user = USERS[email];

    if (user && user.password === password) {

      // ✅ SAVE LOGIN + SERVER
      localStorage.setItem("auth", "true");
      localStorage.setItem("user", email);
      localStorage.setItem("server", user.server);

      // ❌ remove alert (clean UI)
      // alert("Login successful");

      // ✅ GO TO DASHBOARD HOME WITH SERVER
      navigate(`/dashboard?page=home&server=${user.server}`);

    } else {
      alert("Invalid credentials");
    }
  };

  return (

    <div style={{
      background: "#020b1f",
      height: "100vh",
      display: "flex",
      justifyContent: "center",
      alignItems: "center"
    }}>

      <form
        onSubmit={handleLogin}
        style={{
          background: "#1b223c",
          padding: "40px",
          borderRadius: "10px",
          width: "350px"
        }}
      >

        <h2 style={{ color: "white" }}>Login to Pulse.ai</h2>

        {/* EMAIL */}
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          style={{
            width: "100%",
            padding: "12px",
            marginTop: "20px"
          }}
        />

        {/* PASSWORD */}
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          style={{
            width: "100%",
            padding: "12px",
            marginTop: "10px"
          }}
        />

        {/* LOGIN BUTTON */}
        <button
          type="submit"
          style={{
            width: "100%",
            padding: "12px",
            marginTop: "20px",
            background: "#ff7a00",
            color: "white",
            border: "none"
          }}
        >
          Login
        </button>

      </form>

    </div>
  );

}

export default Login;