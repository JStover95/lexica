import { createBrowserRouter, RouterProvider } from "react-router-dom";

import Dashboard from "./pages/dashboard/dashboard";
import Login from "./pages/login/login";
import LoginLayout from "./pages/login/loginLayout";
import AuthContext from "./context/authContext";
import useAuth from "./hooks/useAuth";

import "./styleSheets/App.css";
import DashboardLayout from "./pages/dashboard/dashboardLayout";
import ProtectedRoute from "./pages/protectedRoute";
import AuthCallback from "./pages/authCallback";


const App = () => {
  const { handleAuthCallback, checkAuth, login, logout } = useAuth();

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
    {
      path: "/auth/callback",
      element: <AuthCallback />
    }
  ]);

  return (
    <AuthContext.Provider value={{ handleAuthCallback, checkAuth, login, logout }}>
      <RouterProvider router={router} />
    </AuthContext.Provider>
  );
};


export default App;
