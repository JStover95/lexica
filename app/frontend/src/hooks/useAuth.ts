import { useEffect, useState } from "react";
import { COGNITO_REDIRECT_URI } from "../environment.d";

const authConfig = {
  domain: process.env.REACT_APP_COGNITO_DOMAIN,
  clientId: process.env.REACT_APP_COGNITO_APP_CLIENT_ID,
  redirectUri: COGNITO_REDIRECT_URI,
};

const useAuth = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  const checkAuth = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_API_ENDPOINT}/verify-token`, {
        method: "POST",
        credentials: "include",
      });

      if (!response.ok) {
        throw new Error("Token invalid or expired");
      }

      setIsAuthenticated(true);
      setLoading(false);

      return true;
    } catch (error) {

      // Try refreshing the token
      try {
        const response = await fetch(`${process.env.REACT_APP_API_ENDPOINT}/refresh-token`, {
          method: "POST",
          credentials: "include",
        });
  
        if (!response.ok) {
          throw new Error("Token expired");
        }
  
        setIsAuthenticated(true);
        setLoading(false);
  
        return true;
      } catch (error) {
        setLoading(false);
        console.error("Authentication check failed:", error);
        return false;
      }
    }
  };

  const handleAuthRedirect = async (code: string) => {
    try {
      const response = await fetch(`${process.env.REACT_APP_API_ENDPOINT}/token-exchange`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ code }),
        credentials: "include",
      });

      if (response.ok) {
        setIsAuthenticated(true);
        setLoading(false);
      } else {
        console.error("Failed to authenticate.");
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

  const login = () => {
    window.location.href = `https://${authConfig.domain}/login?client_id=${authConfig.clientId}&scope=email&response_type=code&redirect_uri=${authConfig.redirectUri}`;
  };

  const logout = () => {
    setIsAuthenticated(false);
    window.location.href = `https://${authConfig.domain}/logout?client_id=${authConfig.clientId}&logout_uri=${authConfig.redirectUri}`;
  };

  return { isAuthenticated, loading, handleAuthRedirect, checkAuth, login, logout };
};


export default useAuth;
