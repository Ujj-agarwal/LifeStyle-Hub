import React, { useState, useEffect } from "react";
import api from "../../services/api";
import { toast } from "react-toastify";

export default function WorkoutsPage() {
    const [workouts, setWorkouts] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [isAdding, setIsAdding] = useState(false);

    // State for the new workout form fields
    const [newNotes, setNewNotes] = useState("");
    const [newWorkoutType, setNewWorkoutType] = useState("STRENGTH");
    const [newGoalAchieved, setNewGoalAchieved] = useState(false);
    const [newDuration, setNewDuration] = useState("");
    const [newIntensity, setNewIntensity] = useState("");

    // Function to fetch workouts from the backend
    const fetchWorkouts = async () => {
        setIsLoading(true);
        try {
            const response = await api.get("/workouts");
            setWorkouts(response.data.workouts || []);
        } catch (error) {
            toast.error(error.response?.data?.msg || "Failed to fetch workouts.");
        } finally {
            setIsLoading(false);
        }
    };

    // Fetch workouts when the component first loads
    useEffect(() => {
        fetchWorkouts();
    }, []);

    // Handler for the "Add Workout" form submission
    const handleAddWorkout = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        try {
            await api.post("/workouts", {
                notes: newNotes,
                workout_type: newWorkoutType,
                goal_achieved: newGoalAchieved,
                duration_minutes: parseInt(newDuration, 10),
                intensity: parseInt(newIntensity, 10),
            });
            toast.success("Workout added successfully!");
            
            // Reset form fields and hide the form
            setNewNotes("");
            setNewWorkoutType("STRENGTH");
            setNewGoalAchieved(false);
            setNewDuration("");
            setNewIntensity("");
            setIsAdding(false);

            // Refresh the list with the new workout
            fetchWorkouts();
        } catch (error) {
            toast.error(error.response?.data?.msg || "Failed to add workout.");
        } finally {
            setIsLoading(false);
        }
    };

    // Handler for deleting a workout
    const handleDeleteWorkout = async (workoutId) => {
        if (window.confirm("Are you sure you want to delete this workout?")) {
            try {
                await api.delete(`/workouts/${workoutId}`);
                toast.success("Workout deleted successfully!");
                fetchWorkouts(); // Refresh the list
            } catch (error) {
                toast.error(error.response?.data?.msg || "Failed to delete workout.");
            }
        }
    };

    return (
        <div className="max-w-4xl mx-auto">
            <div className="bg-white p-6 rounded-lg shadow">
                <div className="flex justify-between items-center mb-6">
                    <h1 className="text-2xl font-bold">My Workouts</h1>
                    <button
                        onClick={() => setIsAdding(!isAdding)}
                        className={`px-4 py-2 rounded text-white font-semibold transition-colors ${isAdding ? 'bg-gray-500 hover:bg-gray-600' : 'bg-blue-600 hover:bg-blue-700'}`}
                    >
                        {isAdding ? 'Cancel' : 'Log New Workout'}
                    </button>
                </div>

                {/* Collapsible "Add Workout" Form */}
                {isAdding && (
                    <form onSubmit={handleAddWorkout} className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8 p-4 border rounded-lg bg-gray-50">
                        {/* Column 1 */}
                        <div className="space-y-4">
                            <textarea placeholder="Workout Notes (e.g., Felt strong on squats)" value={newNotes} onChange={(e) => setNewNotes(e.target.value)} required className="w-full border px-3 py-2 rounded" rows="8"></textarea>
                        </div>
                        {/* Column 2 */}
                        <div className="space-y-4">
                            <select value={newWorkoutType} onChange={(e) => setNewWorkoutType(e.target.value)} className="w-full border px-3 py-2 rounded">
                                <option value="STRENGTH">Strength</option>
                                <option value="CARDIO">Cardio</option>
                                <option value="YOGA">Yoga</option>
                            </select>
                            <input type="number" placeholder="Duration (mins)" value={newDuration} onChange={(e) => setNewDuration(e.target.value)} required className="w-full border px-3 py-2 rounded" />
                            <input type="number" placeholder="Intensity (1-5)" value={newIntensity} onChange={(e) => setNewIntensity(e.target.value)} required min="1" max="5" className="w-full border px-3 py-2 rounded" />
                            <div className="flex items-center gap-2 py-1">
                                <input type="checkbox" id="goal-achieved" checked={newGoalAchieved} onChange={(e) => setNewGoalAchieved(e.target.checked)} className="h-4 w-4 rounded" />
                                <label htmlFor="goal-achieved">Goal Achieved?</label>
                            </div>
                        </div>
                        <div className="md:col-span-2">
                            <button type="submit" disabled={isLoading} className="w-full bg-green-600 text-white py-2 rounded disabled:bg-green-300 hover:bg-green-700 transition-colors">
                                {isLoading ? 'Saving...' : 'Save Workout'}
                            </button>
                        </div>
                    </form>
                )}

                {/* List of Existing Workouts */}
                {isLoading && workouts.length === 0 ? (
                    <p className="text-center text-gray-500">Loading workouts...</p>
                ) : workouts.length > 0 ? (
                    <div className="space-y-4">
                        {workouts.map((workout) => (
                            <div key={workout.id} className="p-4 border rounded-lg flex justify-between items-start">
                                <div>
                                    <h3 className="text-lg font-semibold">{workout.workout_type} Session</h3>
                                    <p className="text-sm text-gray-700 mt-1">{workout.notes}</p>
                                    <p className="text-sm text-gray-500 mt-2">
                                        Duration: {workout.duration_minutes} mins | Intensity: {workout.intensity}/5
                                    </p>
                                    <p className="text-sm font-medium text-blue-600">
                                        Est. Calories Burned: {workout.calories_burned}
                                    </p>
                                </div>
                                <button
                                    onClick={() => handleDeleteWorkout(workout.id)}
                                    className="text-sm text-red-500 hover:text-red-700 font-semibold"
                                >
                                    Delete
                                </button>
                            </div>
                        ))}
                    </div>
                ) : (
                    <p className="text-center text-gray-500">You haven't logged any workouts yet. Click "Log New Workout" to get started!</p>
                )}
            </div>
        </div>
    );
}

