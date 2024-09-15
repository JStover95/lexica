import React, { useContext, useEffect, useState } from "react";
import AuthContext from "../context/authContext";
import { Navigate } from "react-router-dom";


/**
 * The functional component for callback redirects from the AWS Cognito hosted
 * UI.
 */
const AuthCallback = () => {
  const { handleAuthCallback } = useContext(AuthContext);
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);

  // Attempt exchange the id code from Cognito for access token after redirect
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const code = params.get("code");
    if (code) {
      // Attempt exchanging the code for access and refresh tokens
      handleAuthCallback(code)
        .then(() => setIsAuthenticated(true))
        .catch(() => setIsAuthenticated(false));
    } else {
      // Set the user as not authenticated if a code is not present
      setIsAuthenticated(false);
    }
  }, []);

  // Show an empty page until authentication succeeds or fails
  if (isAuthenticated === null) {
    return <React.Fragment />
  }

  // Redirect to login if the user is unauthenticated
  return isAuthenticated ? <Navigate to="/" /> : <Navigate to="/login" />;
};


export default AuthCallback;
