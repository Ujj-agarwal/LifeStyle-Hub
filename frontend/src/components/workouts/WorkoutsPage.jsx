import React, { useEffect, useState } from 'react';
import { apiFetch } from '../../services/api';
import { toast } from 'react-toastify';

const TYPES = ['Strength', 'Cardio', 'Yoga'];

function WorkoutCard({ w, onDelete }) {
  return (
    <div className="bg-white p-4 rounded border">
      <div className="flex justify-between">
        <div>
          <h4 className="font-semibold">{w.workout_type}</h4>
          <div className="text-sm text-gray-600">{w.duration_minutes} min — Intensity {w.intensity}</div>
        </div>
        <div>
          <button className="text-sm bg-red-500 text-white px-2 py-1 rounded" onClick={() => onDelete(w.id)}>Delete</button>
        </div>
      </div>
      {w.notes && <p className="mt-2 text-sm">{w.notes}</p>}
      <div className="mt-2 text-xs text-gray-500">Calories (est): {w.calories_burned}</div>
    </div>
  );
}

export default function WorkoutsPage() {
  const [workouts, setWorkouts] = useState([]);
  const [form, setForm] = useState({ workout_type: 'Cardio', duration_minutes: 30, intensity: 3, notes: '', goal_achieved: false });
  const [loading, setLoading] = useState(false);

  const load = async () => {
    setLoading(true);
    try {
      const res = await apiFetch('/workouts');
      setWorkouts(res.workouts || []);
    } catch (err) {
      toast.error(err.message || 'Could not load workouts');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  const create = async (e) => {
    e.preventDefault();
    try {
      await apiFetch('/workouts', { method: 'POST', body: form });
      toast.success('Workout created');
      setForm({ workout_type: 'Cardio', duration_minutes: 30, intensity: 3, notes: '', goal_achieved: false });
      await load();
    } catch (err) {
      toast.error(err.message || 'Create failed');
    }
  };

  const del = async (id) => {
    if (!window.confirm('Delete workout?')) return;
    try {
      await apiFetch(`/workouts/${id}`, { method: 'DELETE' });
      toast.success('Deleted');
      await load();
    } catch (err) {
      toast.error(err.message || 'Delete failed');
    }
  };

  return (
    <div className="max-w-4xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div className="lg:col-span-1 bg-white p-4 rounded shadow">
        <h3 className="font-semibold">Create Workout</h3>
        <form onSubmit={create} className="space-y-3 mt-3">
          <select value={form.workout_type} onChange={e => setForm(f => ({...f, workout_type: e.target.value}))} className="w-full border px-2 py-1 rounded">
            {TYPES.map(t => <option key={t} value={t}>{t}</option>)}
          </select>
          <input type="number" min="0" value={form.duration_minutes} onChange={e => setForm(f => ({...f, duration_minutes: Number(e.target.value)}))} className="w-full border px-2 py-1 rounded" />
          <input type="number" min="1" max="10" value={form.intensity} onChange={e => setForm(f => ({...f, intensity: Number(e.target.value)}))} className="w-full border px-2 py-1 rounded" />
          <textarea placeholder="Notes" value={form.notes} onChange={e => setForm(f => ({...f, notes: e.target.value}))} className="w-full border px-2 py-1 rounded" />
          <label className="flex items-center gap-2">
            <input type="checkbox" checked={form.goal_achieved} onChange={e => setForm(f => ({...f, goal_achieved: e.target.checked}))} />
            Goal achieved
          </label>
          <button className="w-full bg-blue-600 text-white py-2 rounded">Create</button>
        </form>
      </div>

      <div className="lg:col-span-2">
        <h3 className="mb-3">Your Workouts</h3>
        {loading ? <div>Loading...</div> : (
          <div className="grid gap-4">
            {workouts.length === 0 && <div className="text-gray-600">No workouts yet</div>}
            {workouts.map(w => <WorkoutCard key={w.id} w={w} onDelete={del} />)}
          </div>
        )}
      </div>
    </div>
  );
}
