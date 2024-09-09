import { createBrowserRouter, RouterProvider } from "react-router-dom";

import Dashboard from "./pages/dashboard/dashboard";
import Login from "./pages/login/login";
import LoginLayout from "./pages/login/loginLayout";
import AuthContext from "./context/authContext";
import useAuth from "./hooks/useAuth";

import "./styleSheets/App.css";
import DashboardLayout from "./pages/dashboard/dashboardLayout";
import ProtectedRoute from "./pages/protected";


const App = () => {
  const { isAuthenticated, loading, handleAuthRedirect, checkAuth, login, logout } = useAuth();

  const router = createBrowserRouter([
    {
      path: "/",
      element: <ProtectedRoute />,
      children: [
        {
          element: <DashboardLayout />,
          children: [
            {
              index: true,
              element: <Dashboard />
            },
          ],
        },
      ]
    },
    {
      path: "/login",
      element: <LoginLayout />,
      children: [
        {
          index: true,
          element: <Login />,
        }
      ]
    },
  ]);

  return (
    <AuthContext.Provider value={{ isAuthenticated, loading, handleAuthRedirect, checkAuth, login, logout }}>
      <RouterProvider router={router} />
    </AuthContext.Provider>
  );
};


export default App;
