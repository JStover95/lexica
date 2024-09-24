import React, { useContext } from "react";
import AuthContext from "../../context/authContext";
import "../../styleSheets/styles.css";


/**
 * The login component for directing users to the AWS Cognito hosted UI.
 */
const Login: React.FC = () => {
  const { login } = useContext(AuthContext);

  return (
    <div className="flex flex-col items-center justify-center p-16 shadow-lg rounded-4xl">
      <div className="mb-8">
        <span>Log in to continue</span>
      </div>
      <button className="btn btn-primary btn-lg" onClick={login}>
        Continue to login
      </button>
    </div>
  );
}

export default Login;
