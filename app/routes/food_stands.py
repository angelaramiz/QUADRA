from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
try:
    from ..models.food_stand import FoodStand
    from ..models.review import Review
    from .. import db
except ImportError:
    from app.models.food_stand import FoodStand
    from app.models.review import Review
    from app import db
import os
from PIL import Image

food_stands_bp = Blueprint('food_stands', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def resize_image(image_path, max_size=(800, 600)):
    """Redimensiona imagen para optimizar almacenamiento"""
    with Image.open(image_path) as img:
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        img.save(image_path, optimize=True, quality=85)

@food_stands_bp.route('/')
@login_required
def list_stands():
    """Lista todos los puestos de comida activos"""
    page = request.args.get('page', 1, type=int)
    stands = FoodStand.query.filter_by(is_active=True)\
                          .order_by(FoodStand.created_at.desc())\
                          .paginate(page=page, per_page=12, error_out=False)
    
    return render_template('food_stands/list.html', stands=stands)

@food_stands_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_stand():
    """Crear un nuevo puesto de comida"""
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        latitude = request.form.get('latitude', type=float)
        longitude = request.form.get('longitude', type=float)
        address = request.form.get('address')
        
        # Validaciones
        if not all([name, description, latitude, longitude]):
            flash('Por favor, completa todos los campos requeridos.', 'error')
            return render_template('food_stands/create.html')
        
        # Validar coordenadas
        if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
            flash('Coordenadas geográficas inválidas.', 'error')
            return render_template('food_stands/create.html')
        
        # Manejar archivo de imagen
        image_filename = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '' and allowed_file(file.filename):
                try:
                    # Crear directorio de uploads si no existe
                    upload_dir = os.path.join(current_app.root_path, 'static', 'uploads')
                    if not os.path.exists(upload_dir):
                        os.makedirs(upload_dir)
                    
                    filename = secure_filename(file.filename)
                    # Agregar timestamp para evitar conflictos
                    import time
                    timestamp = str(int(time.time()))
                    name_part, ext = os.path.splitext(filename)
                    image_filename = f"{name_part}_{timestamp}{ext}"
                    
                    file_path = os.path.join(upload_dir, image_filename)
                    
                    # Verificar tamaño del archivo
                    file.seek(0, 2)  # Ir al final del archivo
                    file_size = file.tell()
                    file.seek(0)  # Volver al inicio
                    
                    if file_size > current_app.config['MAX_CONTENT_LENGTH']:
                        flash('La imagen es demasiado grande. Máximo 16MB.', 'error')
                        return render_template('food_stands/create.html')
                    
                    file.save(file_path)
                    
                    # Redimensionar imagen
                    resize_image(file_path)
                    
                except Exception as e:
                    flash(f'Error al procesar la imagen: {str(e)}', 'error')
                    return render_template('food_stands/create.html')
            elif 'image' in request.files and request.files['image'].filename != '':
                flash('Formato de imagen no válido. Usa PNG, JPG, JPEG o GIF.', 'error')
                return render_template('food_stands/create.html')
        
        # Crear nuevo puesto
        try:
            # Obtener campos adicionales de ubicación
            municipality = request.form.get('municipality', '').strip()
            state = request.form.get('state', '').strip()
            neighborhood = request.form.get('neighborhood', '').strip()
            
            stand = FoodStand(
                name=name,
                description=description,
                latitude=latitude,
                longitude=longitude,
                address=address,
                municipality=municipality if municipality else None,
                state=state if state else None,
                neighborhood=neighborhood if neighborhood else None,
                image_filename=image_filename,
                user_id=current_user.id
            )
            
            db.session.add(stand)
            db.session.commit()
            
            flash('¡Puesto de comida creado exitosamente!', 'success')
            return redirect(url_for('food_stands.view_stand', id=stand.id))
        
        except Exception as e:
            db.session.rollback()
            flash('Error al crear el puesto. Inténtalo de nuevo.', 'error')
    
    return render_template('food_stands/create.html')

@food_stands_bp.route('/<int:id>')
@login_required
def view_stand(id):
    """Ver detalles de un puesto específico"""
    stand = FoodStand.query.get_or_404(id)
    
    if not stand.is_active:
        flash('Este puesto no está disponible.', 'error')
        return redirect(url_for('food_stands.list_stands'))
    
    # Obtener reseñas del puesto
    reviews = Review.query.filter_by(food_stand_id=id)\
                         .order_by(Review.created_at.desc()).all()
    
    # Verificar si el usuario actual ya ha reseñado este puesto
    user_review = None
    if current_user.is_authenticated:
        user_review = Review.query.filter_by(
            user_id=current_user.id, 
            food_stand_id=id
        ).first()
    
    return render_template('food_stands/detail.html', 
                         stand=stand, 
                         reviews=reviews, 
                         user_review=user_review)

@food_stands_bp.route('/<int:id>/review', methods=['POST'])
@login_required
def add_review(id):
    """Agregar una reseña a un puesto"""
    stand = FoodStand.query.get_or_404(id)
    
    # Verificar que el usuario no sea el dueño del puesto
    if stand.user_id == current_user.id:
        flash('No puedes reseñar tu propio puesto.', 'error')
        return redirect(url_for('food_stands.view_stand', id=id))
    
    # Verificar si ya tiene una reseña
    existing_review = Review.query.filter_by(
        user_id=current_user.id, 
        food_stand_id=id
    ).first()
    
    if existing_review:
        flash('Ya has reseñado este puesto.', 'error')
        return redirect(url_for('food_stands.view_stand', id=id))
    
    rating = request.form.get('rating', type=int)
    comment = request.form.get('comment', '')
    
    if not rating or rating < 1 or rating > 5:
        flash('Debes seleccionar una calificación válida (1-5 estrellas).', 'error')
        return redirect(url_for('food_stands.view_stand', id=id))
    
    try:
        review = Review(
            rating=rating,
            comment=comment,
            user_id=current_user.id,
            food_stand_id=id
        )
        
        db.session.add(review)
        db.session.commit()
        
        flash('¡Reseña agregada exitosamente!', 'success')
    
    except Exception as e:
        db.session.rollback()
        flash('Error al agregar la reseña.', 'error')
    
    return redirect(url_for('food_stands.view_stand', id=id))

@food_stands_bp.route('/my-stands')
@login_required
def my_stands():
    """Ver los puestos creados por el usuario actual"""
    stands = FoodStand.query.filter_by(user_id=current_user.id, is_active=True)\
                          .order_by(FoodStand.created_at.desc()).all()
    
    return render_template('food_stands/my_stands.html', stands=stands)
