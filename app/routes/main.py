from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
try:
    from ..models.food_stand import FoodStand
    from ..models.review import Review
    from .. import db
except ImportError:
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
    """Dashboard principal para usuarios autenticados con filtros"""
    # Obtener parámetros de filtro
    search_query = request.args.get('search', '').strip()
    municipality_filter = request.args.get('municipality', '').strip()
    state_filter = request.args.get('state', '').strip()
    radius_filter = request.args.get('radius', type=float)
    user_lat = request.args.get('lat', type=float)
    user_lng = request.args.get('lng', type=float)
    
    # Construir query base
    stands_query = FoodStand.query.filter_by(is_active=True)
    
    # Aplicar filtro de búsqueda por nombre
    if search_query:
        stands_query = stands_query.filter(FoodStand.name.ilike(f'%{search_query}%'))
    
    # Aplicar filtro por municipio
    if municipality_filter:
        stands_query = stands_query.filter(FoodStand.municipality.ilike(f'%{municipality_filter}%'))
    
    # Aplicar filtro por estado
    if state_filter:
        stands_query = stands_query.filter(FoodStand.state.ilike(f'%{state_filter}%'))
    
    # Obtener resultados
    filtered_stands = stands_query.all()
    
    # Aplicar filtro de radio si hay coordenadas
    if radius_filter and user_lat and user_lng:
        filtered_stands = [stand for stand in filtered_stands 
                          if stand.distance_to(user_lat, user_lng) <= radius_filter]
    
    # Puestos recientes (sin filtros para mostrar actividad general)
    recent_stands = FoodStand.query.filter_by(is_active=True).order_by(FoodStand.created_at.desc()).limit(6).all()
    
    # Puestos mejor calificados (aplicar filtros)
    top_rated_stands = sorted(filtered_stands, key=lambda x: x.average_rating, reverse=True)[:6]
    
    # Mis puestos
    my_stands = FoodStand.query.filter_by(user_id=current_user.id, is_active=True).limit(3).all()
    
    # Obtener listas únicas para filtros
    municipalities = db.session.query(FoodStand.municipality).filter(
        FoodStand.municipality.isnot(None), 
        FoodStand.is_active == True
    ).distinct().all()
    municipalities = [m[0] for m in municipalities if m[0]]
    
    states = db.session.query(FoodStand.state).filter(
        FoodStand.state.isnot(None), 
        FoodStand.is_active == True
    ).distinct().all()
    states = [s[0] for s in states if s[0]]
    
    return render_template('dashboard.html', 
                         recent_stands=recent_stands,
                         top_rated_stands=top_rated_stands,
                         my_stands=my_stands,
                         filtered_stands=filtered_stands,
                         municipalities=municipalities,
                         states=states,
                         current_filters={
                             'search': search_query,
                             'municipality': municipality_filter,
                             'state': state_filter,
                             'radius': radius_filter,
                             'lat': user_lat,
                             'lng': user_lng
                         })

@main_bp.route('/api/stands/nearby')
@login_required
def nearby_stands():
    """API para obtener puestos cercanos basado en coordenadas"""
    lat = request.args.get('lat', type=float)
    lng = request.args.get('lng', type=float)
    radius = request.args.get('radius', 5, type=float)  # radio en km
    
    if not lat or not lng:
        return jsonify({'error': 'Coordenadas requeridas'}), 400
    
    # Usar el nuevo método de búsqueda por radio
    stands = FoodStand.find_within_radius(lat, lng, int(radius))
    
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
