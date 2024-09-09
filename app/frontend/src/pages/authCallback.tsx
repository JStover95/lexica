import React, { useContext, useEffect, useState } from "react";
import AuthContext from "../context/authContext";
import { Navigate } from "react-router-dom";


const AuthCallback = () => {
  const { handleAuthCallback } = useContext(AuthContext);
  const [code, setCode] = useState<string | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);

  useEffect(() => {
    const asyncHandleAuthCallback = async () => {
      const params = new URLSearchParams(window.location.search);
      const codeParam = params.get("code");
      if (codeParam) {
        setCode(codeParam);
      } else {
        setIsAuthenticated(false);
      }
    }
    asyncHandleAuthCallback();
  }, []);

  useEffect(() => {
    if (code) {
      handleAuthCallback(code)
        .then(() => setIsAuthenticated(true))
        .catch(() => setIsAuthenticated(false));
      setCode(null);
    }
  }, [code])

  if (isAuthenticated === null) {
    return <React.Fragment />
  }

  return isAuthenticated ? <Navigate to="/" /> : <Navigate to="/login" />;
};


export default AuthCallback;
