import { useContext, useEffect } from "react";
import { IUser } from "../interfaces";
import AuthContext from "../context/authContext";

// Custom hook to manage authentication state
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

  /**
   * Logs in the user by updating the context state and local storage with user
   * information and tokens.
   *
   * @param {IUser} user - The user object containing user information and
   *  tokens.
   */
  const login = (user: IUser) => {
    setUser(user);
    setIsAuthenticated(true);  // Set authenticated state to true
    setAccessToken(user.accessToken);  // Store access token
    setRefreshToken(user.refreshToken);  // Store refresh token
    localStorage.setItem("user", JSON.stringify(user));  // Save user info to local storage
  };

  /**
   * Logs out the user by resetting the context state and local storage.
   */
  const logout = () => {
    setUser(null);  // Clear user information
    setIsAuthenticated(false);  // Set authenticated state to false
    setAccessToken("");  // Clear access token
    setRefreshToken("");  // Clear refresh token
    localStorage.setItem("user", "");  // Remove user info from local storage
  };

  /**
   * useEffect hook to retrieve user information from local storage on
   * component mount and log in the user if found.
   */
  useEffect(() => {
    const user = localStorage.getItem("user");
    if (user) login(JSON.parse(user));  // Log in existing user
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
