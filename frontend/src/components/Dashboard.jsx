import React from 'react';
import { Link } from 'react-router-dom';

export default function Dashboard() {
  return (
    <div className="max-w-4xl mx-auto">
      <section className="bg-white p-6 rounded shadow">
        <h1 className="text-2xl font-bold">Hello — welcome to Lifestyle Hub</h1>
        <p className="mt-2 text-gray-600">Track your recipes and workouts. Click a card below to get started.</p>

        <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4">
          <Link to="/recipes" className="p-6 bg-green-50 border rounded hover:shadow">
            <h3 className="text-lg font-semibold">Recipes</h3>
            <p className="mt-2 text-sm text-gray-600">Add, list and delete your recipes.</p>
          </Link>

          <Link to="/workouts" className="p-6 bg-blue-50 border rounded hover:shadow">
            <h3 className="text-lg font-semibold">Workouts</h3>
            <p className="mt-2 text-sm text-gray-600">Manage workouts and generate suggestions (AI coming soon).</p>
          </Link>
        </div>
      </section>
    </div>
  );
}
