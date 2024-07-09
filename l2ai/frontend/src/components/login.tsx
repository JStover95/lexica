import * as React from "react";
import { Component } from "react";
import TextField from "./fields/textField";
import Dashboard from "./dashboard";
import { Buffer } from "buffer";
import { makeRequest } from "../utils";
import { IResponseBody } from "../interfaces";
import AsyncButton from "./buttons/asyncButton";
import "./login.css";

/**
 * flashMessages: messages to show above the login form fields
 * email: input in the email login field
 * password: input in the password login field
 * firstLogin: whether the user is logging in for the first time
 * loggedIn: whether the user is logged in
 * loading: whether to show the loading screen
 * loadingDb: whether the database is starting up
 * setPassword: input in the set password field during a user's first login
 * confirmPassword: input in the confirm password field during a user's first login
 * fading: whether to show the loading screen's 0.5 second fade-out
 */
interface LoginState {
  flashMessages: { id: number; element: React.ReactElement }[];
  email: string;
  password: string;
  setPassword: string;
  confirmPassword: string;
}

class Login extends React.Component<any, LoginState> {
  state = {
    flashMessages: [] as { id: number; element: React.ReactElement }[],
    email: "",
    password: "",
    setPassword: "",
    confirmPassword: "",
  };

  /**
   * Log the user in
   * @returns - A response from the login endpoint
   */
  logIn = (): Promise<IResponseBody> => {
    const { email, password } = this.state;
    const auth = Buffer.from(email + ":" + password).toString("base64");
    const headers = { Authorization: "Basic " + auth };
    const opts = { method: "POST", headers: headers };
    return makeRequest("/iam/login", opts);
  };

  tryLogIn = async (): Promise<void> => {
    await this.logIn().then(this.handleLogin, this.handleFailure);
  };

  /**
   * Set a user's password during their first login
   * @returns - A response from the set password endpoint
   */
  setPassword = (): Promise<IResponseBody> => {
    const { setPassword, confirmPassword } = this.state;

    // if the user's password doesn't match the confirm password field
    if (!(setPassword == confirmPassword)) throw "Passwords do not match.";
    const body = JSON.stringify({ password: setPassword });
    const opts = { method: "POST", body: body };
    return makeRequest("/iam/set-password", opts);
  };

  trySetPassword = (): void => {
    this.setPassword().then(this.handleLogin, this.handleFailure);
  };

  /**
   * Handle the response after logging the user in
   * @param res - The response from the login endpoint
   */
  handleLogin = (res: IResponseBody): void => {};

  /**
   * Handle an error after logging the user in
   * @param res - The response from the login endpoint
   */
  handleFailure = (res: IResponseBody) => {

    // flash the message from the server or "Internal server error"
    const msg = <span>{res.Message ? res.Message : "Internal server error"}</span>;
    this.flashMessage(msg, "danger");
  };

  /**
   * Show a message above the login fields
   * @param msg - The content of the message
   * @param type - The type of message (success, info, danger, etc.)
   */
  flashMessage = (msg: React.ReactElement, type: string): void => {
    const { flashMessages } = this.state;

    // set the element's key to 0 or the last message's key + 1
    const id = flashMessages.length
      ? flashMessages[flashMessages.length - 1].id + 1
      : 0;

    const element = (
      <div key={id} className={"shadow flash-message flash-message-" + type}>
        <div className="flash-message-content">
          <span>{msg}</span>
        </div>
        <div
          className="flash-message-close"
          onClick={() => this.popMessage(id)}
        >
          <span>x</span>
        </div>
      </div>
    );

    // add the message to the page
    flashMessages.push({ id, element });
    this.setState({ flashMessages });
  };

  /**
   * Remove a message from the page
   * @param id - The id of the message to remove
   */
  popMessage = (id: number): void => {
    let { flashMessages } = this.state;
    flashMessages = flashMessages.filter((fm) => fm.id != id);
    this.setState({ flashMessages });
  };

  render() {
    const {
      flashMessages,
      email,
      password,
      setPassword,
      confirmPassword
    } = this.state;

    const loginFields = (
      <React.Fragment>
        <div className="login-field">
          <TextField
            id="login-email"
            placeholder="Email"
            onKeyup={(text: string) => this.setState({ email: text })}
            value={email}
          ></TextField>
        </div>
        <div className="login-field">
          <TextField
            id="login-password"
            type="password"
            placeholder="Password"
            onKeyup={(text: string) => this.setState({ password: text })}
            value={password}
          ></TextField>
        </div>
        <div className="login-buttons">
          <AsyncButton text="Sign In" type="primary" onClick={this.tryLogIn} />
        </div>
      </React.Fragment>
    );

    // the login page
    const page = (
      <div className="login-container bg-light">
        <div className="login-menu bg-white">
          <div className="login-menu-content">
            <h1>MM</h1>
            <div className="login-flash-message-container">
              {flashMessages.map((fm) => fm.element)}
            </div>
            {loginFields}
          </div>
        </div>
      </div>
    );

    return <div>{page}</div>;
  }
}

export default Login;
