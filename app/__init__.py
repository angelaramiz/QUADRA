from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
# Import CSRFProtect lazily inside create_app to avoid import-time errors
# when Werkzeug/Flask-WTF version conflicts occur during release/build.
from flask_cors import CORS
from dotenv import load_dotenv
import os
from typing import cast

# Cargar variables de entorno desde app/.env si existe (más robusto que load_dotenv() a ciegas)
basedir = os.path.abspath(os.path.dirname(__file__))
env_path = os.path.join(basedir, '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)
else:
    # fallback: intentar cargar .env en el cwd u otros lugares
    load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
# csrf may be initialized inside create_app; keep a module-level placeholder
csrf = None

def create_app():
    app = Flask(__name__)
    
    # Configuración
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'dev-key-change-in-production'
    
    # Usar SQLite para desarrollo si no se especifica PostgreSQL
    database_url = os.environ.get('DATABASE_URL')
    if database_url and database_url.startswith('postgresql://'):
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        # SQLite para desarrollo
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quadra.db'
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Configurar rutas de uploads usando rutas absolutas para producción
    upload_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
    app.config['UPLOAD_FOLDER'] = upload_folder
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    
    # Asegurar que el directorio de uploads existe
    os.makedirs(upload_folder, exist_ok=True)
    
    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Inicializar CSRF de forma perezosa. Si la importación falla (por ejemplo
    # por incompatibilidades entre Flask-WTF y Werkzeug) continuamos sin CSRF
    # para permitir que el release_command (migraciones/creación de tablas)
    # se ejecute en entornos donde no se pueda resolver la dependencia.
    csrf_enabled = False
    try:
        from flask_wtf.csrf import CSRFProtect, generate_csrf
        global csrf
        if csrf is None:
            csrf = CSRFProtect()
        csrf.init_app(app)
        csrf_enabled = True
        
        # Hacer csrf_token disponible en todas las plantillas
        @app.context_processor
        def inject_csrf_token_enabled():
            return dict(csrf_token=generate_csrf)
            
    except Exception:
        # Si CSRF falla, proveer una función dummy para las plantillas
        @app.context_processor
        def inject_csrf_token_disabled():
            return dict(csrf_token=lambda: '')

    CORS(app)
    
    # Configurar login manager
    # Asignar usando setattr para evitar comprobaciones estáticas de tipos
    setattr(login_manager, 'login_view', 'auth.login')
    login_manager.login_message = 'Por favor, inicia sesión para acceder a esta página.'
    login_manager.login_message_category = 'info'
    
    # Registrar Blueprints con imports relativos
    try:
        # Cuando se ejecuta desde la carpeta app/
        from routes.main import main_bp
        from routes.auth import auth_bp
        from routes.food_stands import food_stands_bp
    except ImportError:
        # Cuando se ejecuta como módulo desde la raíz
        from app.routes.main import main_bp
        from app.routes.auth import auth_bp
        from app.routes.food_stands import food_stands_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(food_stands_bp, url_prefix='/stands')
    
    # Ruta para servir archivos de uploads desde el volumen persistente
    @app.route('/static/uploads/<filename>')
    def uploaded_file(filename):
        """Servir archivos de uploads desde el volumen persistente"""
        from flask import send_from_directory
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    
    # User loader para Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        try:
            from .models.user import User
        except ImportError:
            from app.models.user import User
        return User.query.get(int(user_id))
    
    return app
