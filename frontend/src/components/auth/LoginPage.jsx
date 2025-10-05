import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../services/api";
import { useAuth } from "../../context/AuthContext";
import { toast } from "react-toastify";

export default function LoginPage() {
  const navigate = useNavigate();
  const { login } = useAuth();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [busy, setBusy] = useState(false);

  const handleLogin = async (e) => {
    e.preventDefault();
    setBusy(true);
    try {
      const res = await api.post(
        "/auth/login",
        { username: username.trim(), password },
        { headers: { "Content-Type": "application/json" } }
      );

      if (res.data.access_token) {
        login(res.data.access_token);
        toast.success("Logged in successfully");
        navigate("/");
      } else {
        throw new Error("Invalid login response");
      }
    } catch (err) {
      toast.error(err.response?.data?.message || "Login failed");
    } finally {
      setBusy(false);
    }
  };

  const handleRegister = async () => {
    if (!username || !password) return toast.warn("Enter username and password");
    setBusy(true);
    try {
      await api.post(
        "/auth/register",
        { username: username.trim(), password },
        { headers: { "Content-Type": "application/json" } }
      );

      toast.success("Registered successfully! Logging in...");
      const res = await api.post(
        "/auth/login",
        { username: username.trim(), password },
        { headers: { "Content-Type": "application/json" } }
      );

      login(res.data.access_token);
      navigate("/");
    } catch (err) {
      toast.error(err.response?.data?.message || "Registration failed");
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="max-w-md mx-auto bg-white p-6 rounded-lg shadow">
      <h2 className="text-2xl font-semibold mb-4 text-center">
        Welcome to Lifestyle Hub
      </h2>

      <form onSubmit={handleLogin} className="space-y-4">
        <input
          className="w-full border px-3 py-2 rounded"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <input
          className="w-full border px-3 py-2 rounded"
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <div className="flex gap-3">
          <button
            className="flex-1 bg-green-600 text-white py-2 rounded"
            disabled={busy}
          >
            {busy ? "Working..." : "Login"}
          </button>
          <button
            type="button"
            onClick={handleRegister}
            className="flex-1 bg-blue-600 text-white py-2 rounded"
            disabled={busy}
          >
            {busy ? "..." : "Register"}
          </button>
        </div>
      </form>
    </div>
  );
}
