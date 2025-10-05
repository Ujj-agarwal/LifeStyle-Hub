// src/App.js
import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import LoginPage from "./components/auth/LoginPage";
import Dashboard from "./components/Dashboard";
import RecipesPage from "./components/recipes/RecipesPage";
import WorkoutsPage from "./components/workouts/WorkoutsPage";
import ProtectedRoute from "./components/ProtectedRoute";
import Navbar from "./components/layout/Navbar";

export default function App() {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <main className="flex-1 container mx-auto px-4 py-8">
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="/recipes"
            element={
              <ProtectedRoute>
                <RecipesPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/workouts"
            element={
              <ProtectedRoute>
                <WorkoutsPage />
              </ProtectedRoute>
            }
          />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
    </div>
  );
}
