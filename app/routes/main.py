from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app.models.food_stand import FoodStand
from app.models.review import Review
from app import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Página principal - mapa público con todos los puestos"""
    # Obtener todos los puestos activos para mostrar en el mapa
    food_stands = FoodStand.query.filter_by(is_active=True).order_by(FoodStand.created_at.desc()).all()
    
    # Preparar datos para el mapa
    stands_data = []
    for stand in food_stands:
        stands_data.append({
            'id': stand.id,
            'name': stand.name,
            'description': stand.description[:100] + '...' if len(stand.description) > 100 else stand.description,
            'latitude': stand.latitude,
            'longitude': stand.longitude,
            'address': stand.address,
            'image_filename': stand.image_filename,
            'average_rating': round(stand.average_rating, 1),
            'total_reviews': stand.total_reviews,
            'owner': stand.owner.username,
            'created_at': stand.created_at.strftime('%d/%m/%Y')
        })
    
    return render_template('index.html', food_stands=stands_data)

@main_bp.route('/landing')
def landing():
    """Landing page tradicional con información de la aplicación"""
    return render_template('landing.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard principal para usuarios autenticados"""
    # Obtener puestos recientes
    recent_stands = FoodStand.query.filter_by(is_active=True).order_by(FoodStand.created_at.desc()).limit(6).all()
    
    # Obtener puestos mejor calificados
    top_rated_stands = FoodStand.query.filter_by(is_active=True).all()
    top_rated_stands.sort(key=lambda x: x.average_rating, reverse=True)
    top_rated_stands = top_rated_stands[:6]
    
    # Mis puestos
    my_stands = FoodStand.query.filter_by(user_id=current_user.id, is_active=True).limit(3).all()
    
    return render_template('dashboard.html', 
                         recent_stands=recent_stands,
                         top_rated_stands=top_rated_stands,
                         my_stands=my_stands)

@main_bp.route('/api/stands/nearby')
@login_required
def nearby_stands():
    """API para obtener puestos cercanos basado en coordenadas"""
    lat = request.args.get('lat', type=float)
    lng = request.args.get('lng', type=float)
    radius = request.args.get('radius', 5, type=float)  # radio en km
    
    if not lat or not lng:
        return jsonify({'error': 'Coordenadas requeridas'}), 400
    
    # TODO: Implementar búsqueda por proximidad geográfica
    # Por ahora, devolver todos los puestos activos
    stands = FoodStand.query.filter_by(is_active=True).all()
    
    stands_data = []
    for stand in stands:
        stands_data.append({
            'id': stand.id,
            'name': stand.name,
            'description': stand.description,
            'latitude': stand.latitude,
            'longitude': stand.longitude,
            'address': stand.address,
            'image_filename': stand.image_filename,
            'average_rating': stand.average_rating,
            'total_reviews': stand.total_reviews,
            'owner': stand.owner.username
        })
    
    return jsonify({'stands': stands_data})
