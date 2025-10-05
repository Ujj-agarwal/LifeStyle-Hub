import React from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";

export default function Navbar() {
  const { token, logout } = useAuth();

  return (
    <nav className="bg-white border-b">
      <div className="container mx-auto px-4 py-3 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Link to="/" className="text-xl font-semibold text-green-600">
            Lifestyle Hub
          </Link>
          {token && (
            <>
              <Link to="/recipes" className="text-sm text-gray-700 hover:text-gray-900">
                Recipes
              </Link>
              <Link to="/workouts" className="text-sm text-gray-700 hover:text-gray-900">
                Workouts
              </Link>
            </>
          )}
        </div>

        <div>
          {!token ? (
            <Link to="/login" className="text-sm bg-green-600 text-white px-3 py-1 rounded">
              Login
            </Link>
          ) : (
            <button onClick={logout} className="text-sm bg-red-500 text-white px-3 py-1 rounded">
              Logout
            </button>
          )}
        </div>
      </div>
    </nav>
  );
}
