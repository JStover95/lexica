import { Buffer } from "buffer";
import React, { useContext, useState } from "react";
import { makeRequest } from "../../utils/utils";
import AsyncButton from "../../components/buttons/asyncButton";
import TextField from "../../components/fields/textField";
import AuthContext from "../../context/authContext";
import "../../styleSheets/styles.css";
import { redirect } from "react-router-dom";

/**
 * Login Component
 * 
 * This component provides a login form for users to authenticate. It uses
 * React's Context API to manage authentication state. Upon a successful login,
 * the access and refresh tokens are stored in the local storage, and the
 * authentication state is updated.
 */
const Login: React.FC = () => {
  // Get authentication-related context values
  const { accessToken, setIsAuthenticated } = useContext(AuthContext);
  
  // Local component state to manage form input and messages
  const [message, setMessage] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  /**
   * Handles the login process
   * 
   * This function is triggered when the user clicks the login button. It sends
   * an HTTP POST request with the user's email and password encoded in base64
   * for Basic Authentication. If the login is successful, the access and
   * refresh tokens are stored in local storage, and the authentication state is
   * updated.
   */
  const handleLogin = async () => {
    try {
      // Encode email and password in base64
      const auth = Buffer.from(`${email}:${password}`).toString("base64");
      const headers = { Authorization: "Basic " + auth };
      const options = { headers: headers };
      
      // Send the login request
      const [status, res] = await makeRequest(
        { url: "/login", accessToken, options }
      );

      // Check if login is successful
      if (!(status === 200 && res.AccessToken && res.RefreshToken)) {
        // If the server is requesting a challenge
        if (res.Message == "Challenge requested by server.") {
          redirect("/login/set-password");
        } else {
          setMessage(res.Message ? res.Message : "Login failed.");
        }
        return;
      }

      // Store tokens in local storage and update authentication state
      localStorage.setItem("accessToken", res.AccessToken);
      localStorage.setItem("refreshToken", res.RefreshToken);
      setIsAuthenticated(true);
    } catch (error) {
      if (typeof(error) == "string") setMessage(error);
      else console.error(error);
    }
  }

  // Email input field component
  const emailField = (
    <div className="input input-m">
      <TextField
        id="login-email"
        placeholder="Email"
        onKeyup={setEmail}
        value={email}
        type={"email"}
      ></TextField>
    </div>
  )

  // Password input field component
  const passwordField = (
    <div className="input input-m">
      <TextField
        id="login-password"
        placeholder="Password"
        onKeyup={setPassword}
        value={password}
        type={"password"}
      ></TextField>
    </div>
  )

  // Login button component with Async handling
  const submitButton = (
    <div className="justify-center">
      <AsyncButton
        children={<span>Log In</span>}
        type="primary"
        onClick={handleLogin}
        size={"large"}
      ></AsyncButton>
    </div>
  )

  return (
    <div className="align-center column card shadow w300">
      <div className="mb2">
        <span>Please log in to continue</span>
      </div>
      <div className={message ? "mb1" : "mb2"}>
        <div className="mb1">
          {emailField}
        </div>
        <div>
          {passwordField}
        </div>
      </div>
      {message &&
        <div className="mb2 font-s font-red">
          <span>{message}</span>
        </div>
      }
      {submitButton}
    </div>
  )
}

export default Login;
