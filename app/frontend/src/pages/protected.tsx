import { useContext, useEffect } from "react";
import { Navigate, Outlet } from "react-router-dom";
import AuthContext from "../context/authContext";
import useAuth from "../hooks/useAuth";

const ProtectedRoute = () => {
  const { isAuthenticated, loading, handleAuthRedirect, checkAuth } = useContext(AuthContext);

  useEffect(() => {
    const asyncCheckAuth = async () => {
      await checkAuth();
    };
    asyncCheckAuth();
  }, []);

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const code = params.get("code");
    if (code && !isAuthenticated) handleAuthRedirect(code);
  }, [isAuthenticated]);

  if (loading) {
    return <div>Loading...</div>;
  }

  return isAuthenticated ? <Outlet /> : <Navigate to="/login" />;
};

export default ProtectedRoute;
