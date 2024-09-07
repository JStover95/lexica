import { createBrowserRouter, RouterProvider } from "react-router-dom";

import Dashboard from "./pages/dashboard/dashboard";
import Login from "./pages/login/login";
import LoginLayout from "./pages/login/loginLayout";
import AuthContext from "./context/authContext";
import useAuth from "./hooks/useAuth";

import "./styleSheets/App.css";
import DashboardLayout from "./pages/dashboard/dashboardLayout";
import ProtectedRoute from "./pages/protected";
import SetPassword from "./pages/login/setPassword";


const App = () => {
  const {
    user,
    setUser,
    isAuthenticated,
    setIsAuthenticated,
    accessToken,
    setAccessToken,
    refreshToken,
    setRefreshToken
  } = useAuth();

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
        },
        {
          path: "/login/set-password",
          element: <SetPassword />
        }
      ]
    },
  ]);

  return (
    <AuthContext.Provider value={{
      user,
      setUser,
      isAuthenticated,
      setIsAuthenticated,
      accessToken,
      setAccessToken,
      refreshToken,
      setRefreshToken
    }}
    >
      <RouterProvider router={router} />
    </AuthContext.Provider>
  );
};


export default App;
