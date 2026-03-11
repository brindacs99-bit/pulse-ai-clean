import React from "react";
import { useLocation } from "react-router-dom";

function Dashboard() {

  const location = useLocation();

  const params = new URLSearchParams(location.search);

  const page = params.get("page") || "home";

  return (

    <div style={{
      height: "100vh",
      width: "100%"
    }}>

      <iframe
        src={`http://localhost:8501/?page=${page}`}
        title="Pulse AI Dashboard"
        width="100%"
        height="100%"
        style={{ border: "none" }}
      />

    </div>

  );

}

export default Dashboard;