import axios from "axios";

// This logic uses the environment variable on the live Vercel site,
// but falls back to your specific Render URL for local development.
// IMPORTANT: Replace the placeholder with your actual live backend URL from Render.
const BASE_URL = import.meta.env.VITE_API_URL || "https://lifestyle-hub-api.onrender.com";

const api = axios.create({
  baseURL: BASE_URL,
  headers: { "Content-Type": "application/json" },
});

// This "interceptor" automatically attaches the JWT token to every request
// if it exists in local storage.
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;

