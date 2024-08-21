import { Buffer } from "buffer";
import { useContext, useState } from "react";
import { makeRequest } from "../utils";
import AsyncButton from "./buttons/asyncButton";
import TextField from "./fields/textField";
import AuthContext from "../context/authContext";


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
    <div className="login-field">
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
    <div className="login-field">
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
    <div className="login-buttons">
      <AsyncButton
        text="Log In"
        type="primary"
        onClick={handleLogin}
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
