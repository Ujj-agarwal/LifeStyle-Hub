import React, { useState, useEffect } from "react";
import api from "../../services/api";
import { toast } from "react-toastify";

export default function RecipesPage() {
    const [recipes, setRecipes] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [isAdding, setIsAdding] = useState(false);
    
    const [newName, setNewName] = useState("");
    const [newCuisine, setNewCuisine] = useState("ITALIAN");
    const [newIsVegetarian, setNewIsVegetarian] = useState(false);
    const [newPrepTime, setNewPrepTime] = useState("");
    const [newCookTime, setNewCookTime] = useState("");
    const [newIngredients, setNewIngredients] = useState("");

    const fetchRecipes = async () => {
        setIsLoading(true);
        try {
            const response = await api.get("/recipes");
            setRecipes(response.data.recipes || []);
        } catch (error) {
            toast.error(error.response?.data?.msg || "Failed to fetch recipes.");
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        fetchRecipes();
    }, []);

    const handleAddRecipe = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        try {
            await api.post("/recipes", {
                recipe_name: newName,
                cuisine_type: newCuisine,
                is_vegetarian: newIsVegetarian,
                prep_time_minutes: parseInt(newPrepTime, 10),
                cook_time_minutes: parseInt(newCookTime, 10),
                ingredients: newIngredients,
            });
            toast.success("Recipe added successfully!");
            setNewName("");
            setNewCuisine("ITALIAN");
            setNewIsVegetarian(false);
            setNewPrepTime("");
            setNewCookTime("");
            setNewIngredients("");
            setIsAdding(false);
            fetchRecipes();
        } catch (error) {
            toast.error(error.response?.data?.msg || "Failed to add recipe.");
        } finally {
            setIsLoading(false);
        }
    };
    
    const handleDeleteRecipe = async (recipeId) => {
        if (window.confirm("Are you sure you want to delete this recipe?")) {
            try {
                await api.delete(`/recipes/${recipeId}`);
                toast.success("Recipe deleted successfully!");
                fetchRecipes();
            } catch (error) {
                toast.error(error.response?.data?.msg || "Failed to delete recipe.");
            }
        }
    };

    return (
        <div className="max-w-4xl mx-auto">
            <div className="bg-white p-6 rounded-lg shadow">
                <div className="flex justify-between items-center mb-6">
                    <h1 className="text-2xl font-bold">My Recipes</h1>
                    <button 
                        onClick={() => setIsAdding(!isAdding)}
                        className={`px-4 py-2 rounded text-white font-semibold transition-colors ${isAdding ? 'bg-gray-500 hover:bg-gray-600' : 'bg-green-600 hover:bg-green-700'}`}
                    >
                        {isAdding ? 'Cancel' : 'Add New Recipe'}
                    </button>
                </div>
                
                {isAdding && (
                    <form onSubmit={handleAddRecipe} className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8 p-4 border rounded-lg bg-gray-50">
                        <div className="space-y-4">
                            <input type="text" placeholder="Recipe Name" value={newName} onChange={(e) => setNewName(e.target.value)} required className="w-full border px-3 py-2 rounded" />
                            <select value={newCuisine} onChange={(e) => setNewCuisine(e.target.value)} className="w-full border px-3 py-2 rounded">
                                <option value="ITALIAN">Italian</option>
                                <option value="INDIAN">Indian</option>
                                <option value="MEXICAN">Mexican</option>
                            </select>
                            <div className="flex items-center gap-2 py-1">
                                <input type="checkbox" id="is-veg" checked={newIsVegetarian} onChange={(e) => setNewIsVegetarian(e.target.checked)} className="h-4 w-4 rounded" />
                                <label htmlFor="is-veg">Is Vegetarian?</label>
                            </div>
                        </div>
                        <div className="space-y-4">
                             <input type="number" placeholder="Prep Time (mins)" value={newPrepTime} onChange={(e) => setNewPrepTime(e.target.value)} required className="w-full border px-3 py-2 rounded" />
                             <input type="number" placeholder="Cook Time (mins)" value={newCookTime} onChange={(e) => setNewCookTime(e.target.value)} required className="w-full border px-3 py-2 rounded" />
                             <textarea placeholder="Ingredients..." value={newIngredients} onChange={(e) => setNewIngredients(e.target.value)} required className="w-full border px-3 py-2 rounded" rows="3"></textarea>
                        </div>
                        <div className="md:col-span-2">
                            <button type="submit" disabled={isLoading} className="w-full bg-blue-600 text-white py-2 rounded disabled:bg-blue-300 hover:bg-blue-700 transition-colors">
                                {isLoading ? 'Saving...' : 'Save Recipe'}
                            </button>
                        </div>
                    </form>
                )}

                {isLoading && recipes.length === 0 ? (
                    <p className="text-center text-gray-500">Loading recipes...</p>
                ) : recipes.length > 0 ? (
                    <div className="space-y-4">
                        {recipes.map((recipe) => (
                            <div key={recipe.id} className="p-4 border rounded-lg flex justify-between items-start">
                                <div>
                                    <h3 className="text-lg font-semibold">{recipe.recipe_name}</h3>
                                    <p className="text-sm text-gray-600">Cuisine: {recipe.cuisine_type}</p>
                                    <p className="text-sm text-gray-600">
                                        Vegetarian: {recipe.is_vegetarian ? "Yes" : "No"}
                                    </p>
                                    <p className="text-sm text-gray-500">
                                        Total Time: {recipe.total_cooking_time} minutes
                                    </p>
                                </div>
                                <button
                                    onClick={() => handleDeleteRecipe(recipe.id)}
                                    className="text-sm text-red-500 hover:text-red-700 font-semibold"
                                >
                                    Delete
                                </button>
                            </div>
                        ))}
                    </div>
                ) : (
                    <p className="text-center text-gray-500">You haven't added any recipes yet. Click "Add New Recipe" to get started!</p>
                )}
            </div>
        </div>
    );
}
