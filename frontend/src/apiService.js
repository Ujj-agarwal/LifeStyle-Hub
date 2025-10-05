// The base URL of your Flask API.
const API_URL = 'http://127.0.0.1:5000';

/**
 * A reusable helper function to make authenticated API calls to the Flask backend.
 */
export async function apiFetch(endpoint, options = {}) {
    const token = localStorage.getItem('token');

    const headers = {
        'Content-Type': 'application/json',
        ...options.headers,
    };

    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const url = `${API_URL}${endpoint}`;
    console.log('apiFetch ->', options.method || 'GET', url, options.body);

    try {
        const response = await fetch(url, {
            ...options,
            headers,
            body: options.body ? JSON.stringify(options.body) : null,
        });

        console.log('apiFetch response status:', response.status, response.statusText);

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({ msg: "An unknown server error occurred." }));
            throw new Error(errorData.msg || `HTTP Error: ${response.status}`);
        }

        const contentType = response.headers.get("content-type");
        if (contentType && contentType.includes("application/json")) {
            return response.json();
        }

        return {};
    } catch (error) {
        console.error('API Fetch Error:', error);
        throw error;
    }
}
