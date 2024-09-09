import { useContext, useEffect, useState } from "react";
import { Navigate, Outlet } from "react-router-dom";
import AuthContext from "../context/authContext";

const ProtectedRoute = () => {
  const { checkAuth } = useContext(AuthContext);
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(true);
  
  useEffect(() => {
    const asyncCheckAuth = async () => {
      setIsAuthenticated(await checkAuth());
      setLoading(false);
    }
    asyncCheckAuth();
  }, []);

  if (loading) {
    return (
      <main className="wrapper">
        <div className="container">
          <div className="column p2 grow align-center">
            <div className="mb2">
              <h1>Lexica</h1>
            </div>
            <div>Loading...</div>
          </div>
        </div>
      </main>
    );
  }

  return isAuthenticated ? <Outlet /> : <Navigate to="/login" />;
};

export default ProtectedRoute;
