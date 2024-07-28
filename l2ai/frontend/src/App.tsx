import Dashboard from "./components/dashboard";
import Login from "./components/login";
import AuthContext from "./context/authContext";
import useAuth from "./hooks/useAuth";


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
      {isAuthenticated ? <Dashboard /> : <Login />}
    </AuthContext.Provider>
  );
};


export default App;
