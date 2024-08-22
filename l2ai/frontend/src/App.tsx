import Dashboard from "./components/dashboard";
import Login from "./components/login";
import AuthContext from "./context/authContext";
import useAuth from "./hooks/useAuth";

import "./styleSheets/App.css";


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
      <div className="wrapper">
        <div className="container">
          {!isAuthenticated ? <Dashboard /> : <Login />}
        </div>
      </div>
    </AuthContext.Provider>
  );
};


export default App;
