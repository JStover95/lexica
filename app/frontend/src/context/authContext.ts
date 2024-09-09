import { createContext } from "react";

interface IAuthContext {
  handleAuthCallback: (code: string) => Promise<boolean>;
  checkAuth: () => Promise<boolean>;
  login: () => void;
  logout: () => void;
}

const AuthContext = createContext<IAuthContext>({
  handleAuthCallback: async (code: string) => true,
  checkAuth: async () => true,
  login: () => {},
  logout: () => {},
});

export default AuthContext;
