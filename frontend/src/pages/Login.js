import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

function Login() {

  const navigate = useNavigate();

  const [email,setEmail] = useState("");
  const [password,setPassword] = useState("");

  const handleLogin = (e) => {

    e.preventDefault();

    if(email === "admin@gmail.com" && password === "admin123"){

      localStorage.setItem("auth","true");

      navigate("/dashboard");

    }
    else{

      alert("Invalid credentials");

    }

  };

  return(

    <div style={{
      background:"#020b1f",
      height:"100vh",
      display:"flex",
      justifyContent:"center",
      alignItems:"center"
    }}>

      <form
        onSubmit={handleLogin}
        style={{
          background:"#1b223c",
          padding:"40px",
          borderRadius:"10px",
          width:"350px"
        }}
      >

        <h2 style={{color:"white"}}>Login to Pulse.ai</h2>

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e)=>setEmail(e.target.value)}
          style={{
            width:"100%",
            padding:"12px",
            marginTop:"20px"
          }}
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e)=>setPassword(e.target.value)}
          style={{
            width:"100%",
            padding:"12px",
            marginTop:"10px"
          }}
        />

        <button
          type="submit"
          style={{
            width:"100%",
            padding:"12px",
            marginTop:"20px",
            background:"#ff7a00",
            color:"white",
            border:"none"
          }}
        >
          Login
        </button>

      </form>

    </div>

  );

}

export default Login;