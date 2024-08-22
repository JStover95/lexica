import { Buffer } from "buffer";
import { useContext, useState } from "react";
import { makeRequest } from "../utils";
import AsyncButton from "./buttons/asyncButton";
import TextField from "./fields/textField";
import AuthContext from "../context/authContext";

import "../styles.css";


const Login = () => {
  const { accessToken, setIsAuthenticated } = useContext(AuthContext);
  const [message, setMessage] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");


  const handleLogin = async () => {
    try {
      const auth = Buffer.from(`${email}:${password}`).toString("base64");
      const headers = { Authorization: "Basic " + auth };
      const options = { method: "POST", headers: headers };
      const [status, res] = await makeRequest(
        { url: "/iam/login", accessToken, options }
      );

      if (!(status === 200 && res.AccessToken && res.RefreshToken)) {
        setMessage(res.message ? res.message : "Login failed.");
        return;
      }

      localStorage.setItem("accessToken", res.AccessToken);
      localStorage.setItem("refreshToken", res.RefreshToken);
      setIsAuthenticated(true);
    }

    catch (error) {
      if (typeof(error) == "string") setMessage(error);
      else console.error(error);
    }
  }

  const emailField = (
    <div className="mb1">
      <TextField
        id="login-email"
        placeholder="Email"
        onKeyup={setEmail}
        value={email}
        type={"email"}
      ></TextField>
    </div>
  )

  const passwordField = (
    <div className="mb1">
      <TextField
        id="login-password"
        placeholder="Password"
        onKeyup={setPassword}
        value={password}
        type={"password"}
      ></TextField>
    </div>
  )

  const submitButton = (
    <div className="mb1">
      <AsyncButton
        children={<span>Log In</span>}
        type="primary"
        onClick={handleLogin}
      ></AsyncButton>
    </div>
  )

  return (
    <div className="p1">
      <h1>MM</h1>
      <div className="mb0-5 font-s">
        <span>{message}</span>
      </div>
      {emailField}
      {passwordField}
      {submitButton}
    </div>
  )
}


export default Login;
