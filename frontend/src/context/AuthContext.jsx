import React, { createContext, useState, useEffect, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const storedToken = localStorage.getItem("token");
    if (storedToken) {
      const decoded = decodeToken(storedToken);
      if (decoded && decoded.exp * 1000 > Date.now()) {
        setToken(storedToken);
        scheduleLogout(decoded.exp);
      } else {
        logout();
      }
    }
  }, []);

  const decodeToken = (t) => {
    try {
      return jwtDecode(t);
    } catch (err) {
      console.error("Invalid token:", err);
      return null;
    }
  };

  const scheduleLogout = (exp) => {
    const timeout = exp * 1000 - Date.now();
    if (timeout > 0) {
      setTimeout(() => logout(), timeout);
    }
  };

  const login = (newToken) => {
    setToken(newToken);
    localStorage.setItem("token", newToken);
    const decoded = decodeToken(newToken);
    if (decoded?.exp) scheduleLogout(decoded.exp);
    navigate("/");
  };

  const logout = () => {
    setToken(null);
    localStorage.removeItem("token");
    navigate("/login");
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
