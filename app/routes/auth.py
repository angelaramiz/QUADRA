from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from urllib.parse import urlparse
try:
    from ..models.user import User
    from .. import db
except ImportError:
    from app.models.user import User
    from app import db
import time
import os
import re

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

        # Asegurar que los valores sean strings (no None) antes de operaciones
        username = (request.form.get('username') or '').strip()
        password = request.form.get('password') or ''
        remember = bool(request.form.get('remember'))

        if not username or not password:
            flash('Por favor, completa todos los campos.', 'error')
            return render_template('auth/login.html')

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user, remember=remember)

            # Resetear contador de intentos en login exitoso
            session.pop(f'attempts_login_{client_ip}', None)
            session.pop(f'timestamp_login_{client_ip}', None)

            # Redirigir a la página que intentaba acceder o al dashboard
            next_page = request.args.get('next')
            if not next_page or urlparse(next_page).netloc != '':
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
        username = (request.form.get('username') or '').strip()
        email = (request.form.get('email') or '').strip().lower()
        password = request.form.get('password') or ''
        confirm_password = request.form.get('confirm_password') or ''

        # Validaciones básicas
        if not all([username, email, password, confirm_password]):
            flash('Por favor, completa todos los campos.', 'error')
            return render_template('auth/register.html')

        # Validar formato de email
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

        # Validar longitud de campos
        if len(username) < 3 or len(username) > 50:
            flash('El nombre de usuario debe tener entre 3 y 50 caracteres.', 'error')
            return render_template('auth/register.html')

        if len(email) > 120:
            flash('El email es demasiado largo.', 'error')
            return render_template('auth/register.html')

        # Validar caracteres permitidos en username
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
            # Crear usuario asignando atributos (evita problemas de tipos en análisis estático)
            user = User()
            user.username = username
            user.email = email
            user.set_password(password)
            db.session.add(user)
            db.session.commit()

            flash('¡Registro exitoso! Ya puedes iniciar sesión.', 'success')
            return redirect(url_for('auth.login'))

        except Exception:
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


def send_reset_email(user, token):
    """Envía email de recuperación de contraseña"""
    try:
        # Por ahora, simularemos el envío de email
        # En producción, aquí usarías un servicio de email real
        reset_url = url_for('auth.reset_password', token=token, _external=True)

        # Para desarrollo, simplemente mostraremos el enlace en consola
        print(f"\n🔗 ENLACE DE RECUPERACIÓN PARA {user.email}:")
        print(f"   {reset_url}")
        print(f"⏰ Válido por 1 hora\n")

        # TODO: Implementar envío real de email usando SMTP o servicio de email
        # smtp_server = "smtp.gmail.com"
        # smtp_port = 587
        # sender_email = os.getenv('EMAIL_USER')
        # sender_password = os.getenv('EMAIL_PASSWORD')

        return True

    except Exception as e:
        print(f"Error al enviar email: {e}")
        return False


@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Página para solicitar recuperación de contraseña"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        email = (request.form.get('email') or '').strip().lower()

        if not email:
            flash('Por favor, ingresa tu email.', 'error')
            return render_template('auth/forgot_password.html')

        # Rate limiting
        client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR', 'unknown'))
        if not check_rate_limit(f'reset_{client_ip}', max_attempts=3, window=300):
            flash('Demasiados intentos. Inténtalo más tarde.', 'error')
            return render_template('auth/forgot_password.html')

        user = User.query.filter_by(email=email).first()

        if user:
            # Generar token de recuperación
            token = user.generate_reset_token()
            db.session.commit()

            # Enviar email
            if send_reset_email(user, token):
                flash('Te hemos enviado un enlace de recuperación a tu email.', 'success')
            else:
                flash('Error al enviar el email. Inténtalo más tarde.', 'error')
        else:
            # Por seguridad, siempre mostramos el mismo mensaje
            flash('Te hemos enviado un enlace de recuperación a tu email.', 'success')

        return redirect(url_for('auth.login'))

    return render_template('auth/forgot_password.html')


@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Página para restablecer contraseña con token"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    user = User.query.filter_by(reset_token=token).first()

    if not user or not user.verify_reset_token(token):
        flash('El enlace de recuperación es inválido o ha expirado.', 'error')
        return redirect(url_for('auth.forgot_password'))

    if request.method == 'POST':
        password = request.form.get('password') or ''
        confirm_password = request.form.get('confirm_password') or ''

        if not password or not confirm_password:
            flash('Por favor, completa todos los campos.', 'error')
            return render_template('auth/reset_password.html', token=token)

        if password != confirm_password:
            flash('Las contraseñas no coinciden.', 'error')
            return render_template('auth/reset_password.html', token=token)

        if len(password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres.', 'error')
            return render_template('auth/reset_password.html', token=token)

        try:
            # Cambiar contraseña
            user.set_password(password)
            user.clear_reset_token()
            db.session.commit()

            flash('Tu contraseña ha sido restablecida exitosamente.', 'success')
            return redirect(url_for('auth.login'))

        except Exception:
            db.session.rollback()
            flash('Error al restablecer la contraseña. Inténtalo de nuevo.', 'error')

    return render_template('auth/reset_password.html', token=token)


@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Página para cambiar contraseña (usuario logueado)"""
    if request.method == 'POST':
        current_password = request.form.get('current_password') or ''
        new_password = request.form.get('new_password') or ''
        confirm_password = request.form.get('confirm_password') or ''

        if not all([current_password, new_password, confirm_password]):
            flash('Por favor, completa todos los campos.', 'error')
            return render_template('auth/change_password.html')

        # Verificar contraseña actual
        if not current_user.check_password(current_password):
            flash('La contraseña actual es incorrecta.', 'error')
            return render_template('auth/change_password.html')

        if new_password != confirm_password:
            flash('Las contraseñas nuevas no coinciden.', 'error')
            return render_template('auth/change_password.html')

        if len(new_password) < 6:
            flash('La nueva contraseña debe tener al menos 6 caracteres.', 'error')
            return render_template('auth/change_password.html')

        if current_password == new_password:
            flash('La nueva contraseña debe ser diferente a la actual.', 'error')
            return render_template('auth/change_password.html')

        try:
            # Cambiar contraseña
            current_user.set_password(new_password)
            db.session.commit()

            flash('Tu contraseña ha sido cambiada exitosamente.', 'success')
            return redirect(url_for('main.dashboard'))

        except Exception:
            db.session.rollback()
            flash('Error al cambiar la contraseña. Inténtalo de nuevo.', 'error')

    return render_template('auth/change_password.html')
