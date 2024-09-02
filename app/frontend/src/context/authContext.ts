import { createContext } from "react";
import { IUser } from "../interfaces";

interface IAuthContext {
  user: IUser | null;
  setUser: (user: IUser | null) => void;
  isAuthenticated: boolean;
  setIsAuthenticated: (isAuthenticated: boolean) => void;
  accessToken: string;
  setAccessToken: (accessToken: string) => void;
  refreshToken: string;
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
