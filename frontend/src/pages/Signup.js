import React, {useState} from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function Signup(){

  const navigate = useNavigate();

  const [email,setEmail] = useState("");
  const [password,setPassword] = useState("");

  const signup = async () => {

    try{

      await axios.post("http://localhost:5001/signup",{
        email,
        password
      });

      alert("Signup successful");

      navigate("/login");

    }
    catch(err){

      alert("User already exists");

    }

  };

  return(

    <div style={{textAlign:"center",marginTop:"100px"}}>

      <h2>Create Account</h2>

      <input
      placeholder="Email"
      onChange={(e)=>setEmail(e.target.value)}
      />

      <br/><br/>

      <input
      type="password"
      placeholder="Password"
      onChange={(e)=>setPassword(e.target.value)}
      />

      <br/><br/>

      <button onClick={signup}>
        Sign Up
      </button>

    </div>

  );

}

export default Signup;