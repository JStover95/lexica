import { useContext, useEffect } from "react";
import { IUser } from "../interfaces";
import AuthContext from "../context/authContext";


const useAuth = () => {
  const {
    user,
    setUser,
    isAuthenticated,
    setIsAuthenticated,
    accessToken,
    setAccessToken,
    refreshToken,
    setRefreshToken
  } = useContext(AuthContext);

  const login = (user: IUser) => {
    setUser(user);
    setIsAuthenticated(true);
    setAccessToken(user.accessToken);
    setRefreshToken(user.refreshToken);
    localStorage.setItem("user", JSON.stringify(user));
  };

  const logout = () => {
    setUser(null);
    setIsAuthenticated(false);
    setAccessToken("");
    setRefreshToken("");
    localStorage.setItem("user", "");
  };

  useEffect(() => {
    const user = localStorage.getItem("user");
    if (user) login(JSON.parse(user));
  });

  return {
    user,
    setUser,
    isAuthenticated,
    setIsAuthenticated,
    accessToken,
    setAccessToken,
    refreshToken,
    setRefreshToken,
    login,
    logout,
  };
};


export default useAuth;
