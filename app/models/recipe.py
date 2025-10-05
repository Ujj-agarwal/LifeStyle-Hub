import enum
from app import db

class CuisineType(enum.Enum):
    ITALIAN = "Italian"
    INDIAN = "Indian"
    MEXICAN = "Mexican"
    CHINESE = "Chinese"
    OTHER = "Other"

class Recipe(db.Model):
    """
    Recipe model for storing recipe details.
    """
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    recipe_name = db.Column(db.String(150), nullable=False)
    cuisine_type = db.Column(db.Enum(CuisineType), nullable=False)
    is_vegetarian = db.Column(db.Boolean, default=False, nullable=False)
    prep_time_minutes = db.Column(db.Integer, nullable=False)
    cook_time_minutes = db.Column(db.Integer, nullable=False)
    ingredients = db.Column(db.Text, nullable=False) # For the AI feature

    # Foreign key to link a recipe to a user
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @property
    def total_cooking_time(self):
        """Calculated field: total time is prep time + cook time."""
        return self.prep_time_minutes + self.cook_time_minutes

    def to_dict(self):
        """Helper function to serialize the object to a dictionary."""
        return {
            'id': self.id,
            'recipe_name': self.recipe_name,
            'cuisine_type': self.cuisine_type.value,
            'is_vegetarian': self.is_vegetarian,
            'prep_time_minutes': self.prep_time_minutes,
            'cook_time_minutes': self.cook_time_minutes,
            'ingredients': self.ingredients,
            'total_cooking_time': self.total_cooking_time,
            'user_id': self.user_id
        }
