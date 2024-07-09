import React, { useContext } from "react";
import "./App.css";
import { AuthContext } from "./authContext";
import Login from "./components/login";
import Dashboard from "./components/dashboard";

const App = () => {
  const { isAuthenticated, loading } = useContext(AuthContext);

  const loadingPage = <p>Loading...</p>;
  if (loading) return loadingPage;

  return isAuthenticated ? Dashboard : Login
}

export default App;
