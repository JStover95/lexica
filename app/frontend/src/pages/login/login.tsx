import React, { useContext } from "react";
import AuthContext from "../../context/authContext";
import "../../styleSheets/styles.css";


const Login: React.FC = () => {
  const { login } = useContext(AuthContext);

  return (
    <div className="align-center column card shadow w300">
      <div className="mb2">
        <span>Log in to continue</span>
      </div>
      <div>
        <button className="btn btn-primary btn-large" onClick={login}>
          Continue to login
        </button>
      </div>
    </div>
  );
}

export default Login;
