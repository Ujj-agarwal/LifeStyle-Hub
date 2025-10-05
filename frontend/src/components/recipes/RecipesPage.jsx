import React, { useEffect, useState } from 'react';
import { apiFetch } from '../../services/api';
import { toast } from 'react-toastify';

const CUISINES = ['Italian', 'Indian', 'Mexican', 'Chinese', 'Other'];

function RecipeCard({ r, onDelete }) {
  return (
    <div className="bg-white p-4 rounded border">
      <div className="flex justify-between items-start">
        <div>
          <h4 className="font-semibold">{r.recipe_name}</h4>
          <div className="text-sm text-gray-600">{r.cuisine_type} • {r.total_cooking_time} min</div>
        </div>
        <div>
          <button onClick={() => onDelete(r.id)} className="text-sm bg-red-500 text-white px-2 py-1 rounded">Delete</button>
        </div>
      </div>
      <p className="mt-3 text-sm">{r.ingredients}</p>
    </div>
  );
}

export default function RecipesPage() {
  const [recipes, setRecipes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState({
    recipe_name: '', cuisine_type: 'Indian', is_vegetarian: false,
    prep_time_minutes: 10, cook_time_minutes: 10, ingredients: ''
  });

  const load = async () => {
    setLoading(true);
    try {
      const res = await apiFetch('/recipes');
      setRecipes(res.recipes || []);
    } catch (err) {
      toast.error(err.message || 'Could not load recipes');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  const create = async (e) => {
    e.preventDefault();
    try {
      await apiFetch('/recipes', { method: 'POST', body: form });
      toast.success('Recipe created');
      setForm({ recipe_name: '', cuisine_type: 'Indian', is_vegetarian: false, prep_time_minutes: 10, cook_time_minutes: 10, ingredients: '' });
      await load();
    } catch (err) {
      toast.error(err.message || 'Create failed');
    }
  };

  const del = async (id) => {
    if (!window.confirm('Delete recipe?')) return;
    try {
      await apiFetch(`/recipes/${id}`, { method: 'DELETE' });
      toast.success('Deleted');
      await load();
    } catch (err) {
      toast.error(err.message || 'Delete failed');
    }
  };

  return (
    <div className="max-w-4xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div className="lg:col-span-1 bg-white p-4 rounded shadow">
        <h3 className="font-semibold">Create Recipe</h3>
        <form onSubmit={create} className="space-y-3 mt-3">
          <input placeholder="Recipe name" required value={form.recipe_name} onChange={e => setForm(f => ({...f, recipe_name: e.target.value}))} className="w-full border px-2 py-1 rounded" />
          <select value={form.cuisine_type} onChange={e => setForm(f => ({...f, cuisine_type: e.target.value}))} className="w-full border px-2 py-1 rounded">
            {CUISINES.map(c => <option key={c} value={c}>{c}</option>)}
          </select>
          <div className="flex gap-2">
            <input type="number" min="0" value={form.prep_time_minutes} onChange={e => setForm(f => ({...f, prep_time_minutes: Number(e.target.value)}))} className="w-1/2 border px-2 py-1 rounded" />
            <input type="number" min="0" value={form.cook_time_minutes} onChange={e => setForm(f => ({...f, cook_time_minutes: Number(e.target.value)}))} className="w-1/2 border px-2 py-1 rounded" />
          </div>
          <textarea placeholder="Ingredients" value={form.ingredients} onChange={e => setForm(f => ({...f, ingredients: e.target.value}))} className="w-full border px-2 py-1 rounded" />
          <label className="flex items-center gap-2">
            <input type="checkbox" checked={form.is_vegetarian} onChange={e => setForm(f => ({...f, is_vegetarian: e.target.checked}))} />
            Vegetarian
          </label>
          <button className="w-full bg-green-600 text-white py-2 rounded">Create</button>
        </form>
      </div>

      <div className="lg:col-span-2">
        <h3 className="mb-3">Your Recipes</h3>
        {loading ? <div>Loading...</div> : (
          <div className="grid gap-4">
            {recipes.length === 0 && <div className="text-gray-600">No recipes yet</div>}
            {recipes.map(r => <RecipeCard key={r.id} r={r} onDelete={del} />)}
          </div>
        )}
      </div>
    </div>
  );
}
