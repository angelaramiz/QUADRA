from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.urls import url_parse
try:
    from ..models.user import User
    from .. import db
except ImportError:
    from app.models.user import User
    from app import db
import time

auth_bp = Blueprint('auth', __name__)

def check_rate_limit(key, max_attempts=5, window=300):
    """Verificar rate limiting simple"""
    now = time.time()
    attempts_key = f'attempts_{key}'
    timestamp_key = f'timestamp_{key}'
    
    if attempts_key not in session:
        session[attempts_key] = 0
        session[timestamp_key] = now
    
    # Resetear si ha pasado el tiempo de ventana
    if now - session.get(timestamp_key, 0) > window:
        session[attempts_key] = 0
        session[timestamp_key] = now
    
    session[attempts_key] += 1
    
    return session[attempts_key] <= max_attempts

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Página de inicio de sesión"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        # Rate limiting
        client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR', 'unknown'))
        if not check_rate_limit(f'login_{client_ip}'):
            flash('Demasiados intentos de inicio de sesión. Inténtalo más tarde.', 'error')
            return render_template('auth/login.html')
        
        username = request.form.get('username')
        password = request.form.get('password')
        remember = bool(request.form.get('remember'))
        
        if not username or not password:
            flash('Por favor, completa todos los campos.', 'error')
            return render_template('auth/login.html')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user, remember=remember)
            
            # Resetear contador de intentos en login exitoso
            session.pop(f'attempts_login_{client_ip}', None)
            
            # Redirigir a la página que intentaba acceder o al dashboard
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('main.dashboard')
            
            flash(f'¡Bienvenido, {user.username}!', 'success')
            return redirect(next_page)
        else:
            flash('Usuario o contraseña incorrectos.', 'error')
    
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Página de registro de nuevos usuarios"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validaciones
        if not all([username, email, password, confirm_password]):
            flash('Por favor, completa todos los campos.', 'error')
            return render_template('auth/register.html')
        
        # Validar formato de email
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            flash('Por favor, ingresa un email válido.', 'error')
            return render_template('auth/register.html')
        
        if password != confirm_password:
            flash('Las contraseñas no coinciden.', 'error')
            return render_template('auth/register.html')
        
        if len(password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres.', 'error')
            return render_template('auth/register.html')
        
        # Validar entrada para prevenir inyección
        username = username.strip()
        email = email.strip().lower()
        
        # Validar longitud de campos
        if len(username) < 3 or len(username) > 50:
            flash('El nombre de usuario debe tener entre 3 y 50 caracteres.', 'error')
            return render_template('auth/register.html')
        
        if len(email) > 120:
            flash('El email es demasiado largo.', 'error')
            return render_template('auth/register.html')
        
        # Validar caracteres permitidos en username
        import re
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            flash('El nombre de usuario solo puede contener letras, números y guiones bajos.', 'error')
            return render_template('auth/register.html')
        
        # Verificar si el usuario ya existe
        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()
        
        if existing_user:
            if existing_user.username == username:
                flash('El nombre de usuario ya está en uso.', 'error')
            else:
                flash('El email ya está registrado.', 'error')
            return render_template('auth/register.html')
        
        # Crear nuevo usuario
        try:
            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            
            flash('¡Registro exitoso! Ya puedes iniciar sesión.', 'success')
            return redirect(url_for('auth.login'))
        
        except Exception as e:
            db.session.rollback()
            flash('Error al registrar usuario. Inténtalo de nuevo.', 'error')
            return render_template('auth/register.html')
    
    return render_template('auth/register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """Cerrar sesión del usuario"""
    logout_user()
    flash('Has cerrado sesión exitosamente.', 'info')
    return redirect(url_for('main.index'))
