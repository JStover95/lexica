import Dashboard from "./pages/dashboard";
import Login from "./pages/login";
import AuthContext from "./context/authContext";
import useAuth from "./hooks/useAuth";

import "./styleSheets/App.css";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Layout from "./pages/layout";


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
      element: <Layout />,
      children: [
        {
          index: true,
          element: <Dashboard />
        },
      ]
    },
    {
      path: "/login",
      element: <Login />
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
