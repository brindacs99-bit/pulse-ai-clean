import React from "react";

function Forecast() {

  return (

    <div style={{
      height:"100vh",
      width:"100%",
      background:"#020b1f"
    }}>

      <iframe
        src="http://localhost:8501/?page=forecast"
        title="AI Forecast"
        width="100%"
        height="100%"
        style={{border:"none"}}
      />

    </div>

  );

}

export default Forecast;