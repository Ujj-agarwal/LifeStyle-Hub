import React, {
  createContext,
  useState,
  useEffect,
  useContext,
  useCallback,
} from "react";
import { useNavigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(null);
  const navigate = useNavigate();

  // The 'logout' function is wrapped in useCallback to prevent it from being
  // recreated on every render, which stabilizes it for use in other hooks.
  const logout = useCallback(() => {
    setToken(null);
    localStorage.removeItem("token");
    navigate("/login");
  }, [navigate]);

  const decodeToken = (t) => {
    try {
      return jwtDecode(t);
    } catch (err) {
      console.error("Invalid token:", err);
      return null;
    }
  };

  // The 'scheduleLogout' function is also wrapped in useCallback.
  const scheduleLogout = useCallback(
    (exp) => {
      const timeout = exp * 1000 - Date.now();
      if (timeout > 0) {
        setTimeout(() => logout(), timeout);
      }
    },
    [logout]
  );

  // This useEffect hook runs once when the app loads to check for an existing token.
  // By adding 'logout' and 'scheduleLogout' to the dependency array, we satisfy the
  // exhaustive-deps rule and ensure the hook has access to the latest versions of these functions.
  useEffect(() => {
    const storedToken = localStorage.getItem("token");
    if (storedToken) {
      const decoded = decodeToken(storedToken);
      if (decoded && decoded.exp * 1000 > Date.now()) {
        setToken(storedToken);
        scheduleLogout(decoded.exp);
      } else {
        // Token is expired or invalid
        logout();
      }
    }
  }, [logout, scheduleLogout]);

  // The login function now also uses the stable 'scheduleLogout' function.
  const login = (newToken) => {
    setToken(newToken);
    localStorage.setItem("token", newToken);
    const decoded = decodeToken(newToken);
    if (decoded?.exp) scheduleLogout(decoded.exp);
    navigate("/");
  };

  const value = {
    token,
    login,
    logout,
    isAuthenticated: !!token,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => useContext(AuthContext);
