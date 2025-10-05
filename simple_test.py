from flask import Flask, jsonify
from flask_jwt_extended import create_access_token, jwt_required, JWTManager

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "this-is-a-super-secret-key-for-testing"
jwt = JWTManager(app)

@app.route("/login", methods=["POST"])
def login():
    # --- THE FIX IS HERE ---
    # Convert the identity from an integer (1) to a string ('1')
    access_token = create_access_token(identity=str(1))
    # -----------------------
    
    print("\n--- NEW ACCESS TOKEN ---")
    print(access_token)
    print("------------------------\n")

    return jsonify(access_token=access_token)

@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    return jsonify(message="Success! Your token is valid.")

if __name__ == "__main__":
    app.run(port=5001, debug=True)

### Your Action Plan to Victory


# Change this:
access_token = create_access_token(identity=user.id)

# To this:
access_token = create_access_token(identity=str(user.id))

