import { createContext } from "react";

interface IAuthContext {
  isAuthenticated: boolean;
  loading: boolean;
  handleAuthRedirect: (code: string) => Promise<void>;
  checkAuth: () => Promise<boolean>;
  login: () => void;
  logout: () => void;
}

const AuthContext = createContext<IAuthContext>({
  isAuthenticated: false,
  loading: true,
  handleAuthRedirect: async (code: string) => {},
  checkAuth: async () => true,
  login: () => {},
  logout: () => {},
});

export default AuthContext;
