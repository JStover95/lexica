import { useContext, useEffect, useState } from "react";
import { Navigate, Outlet } from "react-router-dom";
import AuthContext from "../context/authContext";


/**
 * The Protected Route functional component to be used as the React Router
 * parent for all functional components that require authentication. A loading
 * screen is shown while a request is made to check whether the user is
 * authenticated. If the user is not authenticated, they are redirected to the
 * login screen.
 */
const ProtectedRoute = () => {
  const { checkAuth } = useContext(AuthContext);
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(true);

  // Check if the user is authenticated before accessing a protected route
  useEffect(() => {
    const asyncCheckAuth = async () => {
      setIsAuthenticated(await checkAuth());
      setLoading(false);
    }
    asyncCheckAuth();
  }, []);

  // Show a loading screen while checking whether the user is authenticated
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

  // Redirect to login if the user is not authenticated
  return isAuthenticated ? <Outlet /> : <Navigate to="/login" />;
};

export default ProtectedRoute;
