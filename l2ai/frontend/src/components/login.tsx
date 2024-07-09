import { Buffer } from "buffer";
import React, { useState } from "react";
import { makeRequest } from "../utils";
import { IResponseBody } from "../interfaces";
import AsyncButton from "./buttons/asyncButton";
import TextField from "./fields/textField";

interface IMessage {
  id: number;
  element: React.ReactElement;
}


const login = (email: string, password: string): Promise<IResponseBody> => {
  const auth = Buffer.from(`${email}:${password}`).toString("base64");
  const headers = { Authorization: "Basic " + auth };
  const opts = { method: "POST", headers: headers };
  return makeRequest("/iam/login", opts);
}


const handleLogin = (res: IResponseBody) => {}


const handleFailure = (res: IResponseBody) => {}


const pushMessage = (message: IMessage) => {}


const popMessage = (id: number) => {}


const Login = () => {
  const [messages, setMessages] = useState<IMessage[]>([]);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const tryLogIn = async () => {
    await login(email, password).then(handleLogin, handleFailure)
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
    <div className="login-container bg-light">
      <div className="login-menu bg-white">
        <div className="login-menu-content">
          <h1>MM</h1>
          <div className="login-flash-message-container">
            {messages.map((m) => m.element)}
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
