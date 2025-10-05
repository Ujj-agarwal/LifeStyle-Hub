from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.recipe import Recipe, CuisineType

recipes_bp = Blueprint('recipes', __name__)

@recipes_bp.route('', methods=['POST'])
@jwt_required()
def create_recipe():
    """Create a new recipe for the logged-in user."""
    # --- THE FIX IS HERE ---
    # Convert the string identity from the token back to an integer
    current_user_id = int(get_jwt_identity())
    # -----------------------
    data = request.get_json()

    required_fields = ['recipe_name', 'cuisine_type', 'prep_time_minutes', 'cook_time_minutes', 'ingredients']
    if not all(field in data for field in required_fields):
        return jsonify({"msg": "Missing required fields"}), 400

    try:
        cuisine_type_enum = CuisineType[data['cuisine_type'].upper()]
    except KeyError:
        return jsonify({"msg": f"Invalid cuisine_type. Must be one of: {[t.name for t in CuisineType]}"}), 400

    new_recipe = Recipe(
        user_id=current_user_id,
        recipe_name=data['recipe_name'],
        cuisine_type=cuisine_type_enum,
        is_vegetarian=data.get('is_vegetarian', False),
        prep_time_minutes=data['prep_time_minutes'],
        cook_time_minutes=data['cook_time_minutes'],
        ingredients=data['ingredients']
    )
    db.session.add(new_recipe)
    db.session.commit()
    return jsonify(new_recipe.to_dict()), 201

@recipes_bp.route('', methods=['GET'])
@jwt_required()
def get_recipes():
    """Get a paginated and filtered list of recipes for the logged-in user."""
    current_user_id = int(get_jwt_identity())
    query = Recipe.query.filter_by(user_id=current_user_id)

    # Filtering by cuisine type
    cuisine_filter = request.args.get('cuisine_type')
    if cuisine_filter:
        try:
            query = query.filter_by(cuisine_type=CuisineType[cuisine_filter.upper()])
        except KeyError:
            pass

    # Filtering by vegetarian status
    veg_filter = request.args.get('is_vegetarian')
    if veg_filter is not None:
        if veg_filter.lower() == 'true':
            query = query.filter_by(is_vegetarian=True)
        elif veg_filter.lower() == 'false':
            query = query.filter_by(is_vegetarian=False)
            
    # Pagination
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    paginated_recipes = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "recipes": [r.to_dict() for r in paginated_recipes.items],
        "total": paginated_recipes.total,
        "pages": paginated_recipes.pages,
        "current_page": paginated_recipes.page
    }), 200

@recipes_bp.route('/<int:recipe_id>', methods=['GET'])
@jwt_required()
def get_recipe(recipe_id):
    """Get a single recipe by its ID."""
    current_user_id = int(get_jwt_identity())
    recipe = Recipe.query.filter_by(id=recipe_id, user_id=current_user_id).first_or_404()
    return jsonify(recipe.to_dict()), 200

@recipes_bp.route('/<int:recipe_id>', methods=['PUT'])
@jwt_required()
def update_recipe(recipe_id):
    """Update an existing recipe."""
    current_user_id = int(get_jwt_identity())
    recipe = Recipe.query.filter_by(id=recipe_id, user_id=current_user_id).first_or_404()
    data = request.get_json()

    # Fully implemented update logic
    recipe.recipe_name = data.get('recipe_name', recipe.recipe_name)
    recipe.is_vegetarian = data.get('is_vegetarian', recipe.is_vegetarian)
    recipe.prep_time_minutes = data.get('prep_time_minutes', recipe.prep_time_minutes)
    recipe.cook_time_minutes = data.get('cook_time_minutes', recipe.cook_time_minutes)
    recipe.ingredients = data.get('ingredients', recipe.ingredients)
    
    if 'cuisine_type' in data:
        try:
            recipe.cuisine_type = CuisineType[data['cuisine_type'].upper()]
        except KeyError:
            return jsonify({"msg": "Invalid cuisine_type"}), 400

    db.session.commit()
    return jsonify(recipe.to_dict()), 200

@recipes_bp.route('/<int:recipe_id>', methods=['DELETE'])
@jwt_required()
def delete_recipe(recipe_id):
    """Delete a recipe."""
    current_user_id = int(get_jwt_identity())
    recipe = Recipe.query.filter_by(id=recipe_id, user_id=current_user_id).first_or_404()
    
    db.session.delete(recipe)
    db.session.commit()
    return jsonify({"msg": "Recipe deleted successfully"}), 200

