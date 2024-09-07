import { createContext } from "react";
import { IUser } from "../utils/interfaces";

interface IAuthContext {
  // The current authenticated user or null if not authenticated
  user: IUser | null;
  
  // Function to set the current authenticated user
  setUser: (user: IUser | null) => void;

  // Boolean indicating whether the user is authenticated
  isAuthenticated: boolean;

  // Function to set the authentication status
  setIsAuthenticated: (isAuthenticated: boolean) => void;

  // JWT access token for the authenticated session
  accessToken: string;

  // Function to set the access token
  setAccessToken: (accessToken: string) => void;

  // JWT refresh token for refreshing the access token
  refreshToken: string;

  // Function to set the refresh token
  setRefreshToken: (refreshToken: string) => void;
}


const AuthContext = createContext<IAuthContext>({
  user: null,
  setUser: () => {},
  isAuthenticated: false,
  setIsAuthenticated: () => {},
  accessToken: "",
  setAccessToken: () => {},
  refreshToken: "",
  setRefreshToken: () => {},
});


export default AuthContext;
