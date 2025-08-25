# Importar todos los modelos para que Flask-Migrate los detecte
from .user import User
from .food_stand import FoodStand
from .review import Review

__all__ = ['User', 'FoodStand', 'Review']
