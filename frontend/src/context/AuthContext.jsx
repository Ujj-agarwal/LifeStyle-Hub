// src/context/AuthContext.jsx
import React, { createContext, useState, useEffect, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode"; // fixed import

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(null);
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const storedToken = localStorage.getItem("token");
    if (storedToken) {
      setToken(storedToken);
      try {
        const decoded = jwtDecode(storedToken);
        setUser(decoded);
      } catch (err) {
        console.error("Invalid token", err);
        localStorage.removeItem("token");
      }
    }
  }, []);

  const login = (token) => {
    setToken(token);
    localStorage.setItem("token", token);
    try {
      const decoded = jwtDecode(token);
      setUser(decoded);
    } catch (err) {
      console.error("Invalid token", err);
    }
    navigate("/");
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem("token");
    navigate("/login");
  };

  const value = {
    token,
    user,
    login,
    logout,
    isAuthenticated: !!token,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => useContext(AuthContext);
