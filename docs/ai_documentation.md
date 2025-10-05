# AI Documentation

This file lists the AI prompts I used while building the Workout and Recipe Manager project for the assignment.

---

### Prompt 1
**Context:** Browser routing error between `index.js` and `App.js`.  
**Prompt:** "Why am I getting a browser routing error between index.js and App.js in React?"  
**AI Used:** ChatGPT  
**How I used it:** AI explained that duplicate BrowserRouter wrappers were causing the issue. I kept only one `<BrowserRouter>` in `index.js` and removed it from `App.js`. This fixed the routing and page refresh problems.

---

### Prompt 2
**Context:** JWT token creation error in Flask.  
**Prompt:** "JWT create_access_token(identity=1) error: subject must be a string — how to fix?"  
**AI Used:** ChatGPT  
**How I used it:** AI explained that the JWT library now enforces the `sub` (subject) claim to be a string. I updated the code to `create_access_token(identity=str(user.id))`, which fixed the issue and allowed login tokens to validate properly.

---

### Prompt 3
**Context:** Tailwind CSS version mismatch error.  
**Prompt:** "Tailwind not compiling — PostCSS version error or plugin load failed. How to fix?"  
**AI Used:** ChatGPT  
**How I used it:** AI found that my Tailwind version was incompatible with the installed PostCSS. I reinstalled the matching versions using:  
npm install -D tailwindcss@latest postcss@latest autoprefixer@latest
npx tailwindcss init -p

yaml
Copy code
After that, Tailwind compiled correctly and the styles started rendering.

---

### Prompt 4
**Context:** JWT decode token error on frontend.  
**Prompt:** "How to decode JWT token in React for authentication and redirect handling?"  
**AI Used:** ChatGPT  
**How I used it:** AI suggested using the `jwt-decode` library to extract user info from the token. I added:
npm install jwt-decode
and then decoded tokens in the AuthContext to manage login state. This fixed the protected route handling.

### Prompt 5
**Context**: Protecting routes and verifying authentication.
**Prompt**: "How to restrict direct URL access in React Router and redirect unauthorized users to login page?"
**AI Used**: ChatGPT
**How I used it**: Implemented a ProtectedRoute component that checks for the token using context. If no token is found, the user is redirected to /login. This ensures no private route is accessible without login.

### Prompt 6
**Context**: AI-based features for Recipes and Workouts.
**Prompt: "How to integrate Google AI Studio API into a Flask backend to generate AI responses for recipes or workout plans?"
**AI Used**: Gemini (Google AI Studio)
**How I used it**: Planned to use the Gemini API for two features:

Recipes: “Create Shopping List & Calorie Calculator” — send ingredients to Gemini and return structured ingredient lists and estimated calories per serving.

Workout: “Plan Today’s Workout” — send previous workouts and workout type to Gemini to get a 3–4 exercise plan for the day.

