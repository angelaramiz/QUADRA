# Importar todas las rutas
from .main import main_bp
from .auth import auth_bp
from .food_stands import food_stands_bp

__all__ = ['main_bp', 'auth_bp', 'food_stands_bp']
