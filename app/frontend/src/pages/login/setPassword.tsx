import { useState } from "react";
import TextField from "../../components/fields/textField";
import AsyncButton from "../../components/buttons/asyncButton";


const SetPassword = () => {
  const [message, setMessage] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const handleSubmit = async () => {
    console.log(password, confirmPassword);
  };

  // Password input field component
  const passwordField = (
    <div className="input input-m">
      <TextField
        id="password"
        placeholder="New password"
        onKeyup={setPassword}
        value={password}
        type={"password"}
      ></TextField>
    </div>
  )

  // Password input field component
  const confirmPasswordField = (
    <div className="input input-m">
      <TextField
        id="confirm-password"
        placeholder="Confirm password"
        onKeyup={setConfirmPassword}
        value={confirmPassword}
        type={"password"}
      ></TextField>
    </div>
  )

  // Login button component with Async handling
  const submitButton = (
    <div className="justify-center">
      <AsyncButton
        children={<span>Set Password</span>}
        type="primary"
        onClick={handleSubmit}
        size={"large"}
      ></AsyncButton>
    </div>
  );

  return (
    <div className="align-center column card shadow w300">
      <div className="mb2">
        <span>Please enter a new password</span>
      </div>
      <div className={message ? "mb1" : "mb2"}>
        <div className="mb1">
          {passwordField}
        </div>
        <div>
          {confirmPasswordField}
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
};


export default SetPassword;
