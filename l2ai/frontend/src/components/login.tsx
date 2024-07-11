import { Buffer } from "buffer";
import React, { useContext, useState } from "react";
import { makeRequest } from "../utils";
import { IResponseBody } from "../interfaces";
import AsyncButton from "./buttons/asyncButton";
import TextField from "./fields/textField";
import { AuthContext } from "../authContext";

interface ILoginProps {
  onLogin: () => null;
}


const login = async (email: string, password: string): Promise<IResponseBody> => {
  const auth = Buffer.from(`${email}:${password}`).toString("base64");
  const headers = { Authorization: "Basic " + auth };
  const opts = { method: "POST", headers: headers };
  const res = await makeRequest("/iam/login", opts);

  if (res.isAuthenticated) return res
  else throw res.message
}


const Login = () => {
  const { setAuthenticated } = useContext(AuthContext);
  const [message, setMessage] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const tryLogIn = async () => {
    try {
      const res = await login(email, password);
      if (!(res.AccessToken && res.RefreshToken)) throw Error("Failed login.");
      localStorage.setItem("accessToken", res.AccessToken);
      localStorage.setItem("refreshToken", res.RefreshToken);
      setAuthenticated(true);
    }

    catch (error) {
      if (typeof(error) == "string") setMessage(error);
      else console.error(error);
    }
  }

  const emailField = (
    <div className="login-field">
      <TextField
        id="login-email"
        placeholder="Email"
        onKeyup={setEmail}
        value={email}
      ></TextField>
    </div>
  )

  const passwordField = (
    <div className="login-field">
      <TextField
        id="login-password"
        placeholder="Password"
        onKeyup={setPassword}
        value={password}
      ></TextField>
    </div>
  )

  const submitButton = (
    <div className="login-buttons">
      <AsyncButton
        text="Log In"
        type="primary"
        onClick={tryLogIn}
      ></AsyncButton>
    </div>
  )

  return (
    <div className="login-container">
      <div className="login-menu">
        <div className="login-menu-content">
          <h1>MM</h1>
          <div className="login-message-container">
            <p>{message}</p>
          </div>
          {emailField}
          {passwordField}
          {submitButton}
        </div>
      </div>
    </div>
  )
}


export default Login;
