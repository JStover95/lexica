import { createContext, ReactNode, useEffect, useState } from "react";
import { getCurrentAuthenticatedUser } from "./utils";

interface IAuthContext {
  isAuthenticated: boolean;
  loading: boolean;
}

interface IAuthProvider {
  children: ReactNode;
}

export const AuthContext = createContext<IAuthContext>({
  isAuthenticated: false,
  loading: true,
});


export const AuthProvider= (children: ReactNode) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkAuth = async () => {
      try {
        await getCurrentAuthenticatedUser();
        setIsAuthenticated(true);
      } catch {
        setIsAuthenticated(false);
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, []);

  return (
    <AuthContext.Provider value={{ isAuthenticated, loading }}>
      {children}
    </AuthContext.Provider>
  );
};
