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

@main_bp.route('/init-sample-data')
def init_sample_data():
    """Crear datos de ejemplo para desarrollo (solo para desarrollo)"""
    from app.models.user import User
    from app.models.food_stand import FoodStand
    from app.models.review import Review
    import random
    
    # Verificar si ya existen datos
    if User.query.count() > 0:
        return "Los datos de ejemplo ya existen"
    
    try:
        # Crear usuarios de ejemplo (solo si no existen)
        if User.query.count() == 0:
            import secrets
            import string
            
            def generate_secure_password():
                """Genera una contraseña segura aleatoria"""
                alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
                return ''.join(secrets.choice(alphabet) for _ in range(12))
            
            users_data = [
                {'username': 'juan_tacos', 'email': 'juan@example.com'},
                {'username': 'maria_quesadillas', 'email': 'maria@example.com'},
                {'username': 'carlos_tortas', 'email': 'carlos@example.com'},
                {'username': 'ana_elotes', 'email': 'ana@example.com'},
            ]
            
            users = []
            for user_data in users_data:
                user = User(username=user_data['username'], email=user_data['email'])
                # Usar contraseña segura aleatoria para datos de prueba
                secure_password = generate_secure_password()
                user.set_password(secure_password)
                db.session.add(user)
                users.append(user)
                
                # Log para desarrollo (remover en producción)
                print(f"Usuario creado: {user.username} - Contraseña: {secure_password}")
        else:
            users = User.query.limit(4).all()
        
        db.session.commit()
        
        # Crear puestos de ejemplo en Ciudad de México
        stands_data = [
            {
                'name': 'Tacos El Güero',
                'description': 'Los mejores tacos al pastor de la colonia. Preparados con carne de primera calidad y tortillas hechas a mano.',
                'latitude': 19.4326,
                'longitude': -99.1332,
                'address': 'Av. Insurgentes Sur 1234, Roma Norte',
                'user': users[0]
            },
            {
                'name': 'Quesadillas Doña María',
                'description': 'Quesadillas de flor de calabaza, huitlacoche y queso oaxaca. Tradición familiar de más de 20 años.',
                'latitude': 19.4285,
                'longitude': -99.1277,
                'address': 'Calle Orizaba 123, Roma Sur',
                'user': users[1]
            },
            {
                'name': 'Tortas Ahogadas El Poblano',
                'description': 'Auténticas tortas ahogadas estilo Guadalajara. Salsa roja y verde, ingredientes frescos diariamente.',
                'latitude': 19.4204,
                'longitude': -99.1374,
                'address': 'Av. Álvaro Obregón 456, Condesa',
                'user': users[2]
            },
            {
                'name': 'Elotes y Esquites La Michoacana',
                'description': 'Elotes y esquites con todos los ingredientes: mayonesa, queso, chile piquín y limón. ¡Deliciosos!',
                'latitude': 19.4150,
                'longitude': -99.1300,
                'address': 'Parque México, Condesa',
                'user': users[3]
            },
            {
                'name': 'Tamales Oaxaqueños',
                'description': 'Tamales de mole, rajas con queso y dulces. Receta tradicional oaxaqueña con ingredientes auténticos.',
                'latitude': 19.4390,
                'longitude': -99.1290,
                'address': 'Mercado Medellín, Doctores',
                'user': users[0]
            },
            {
                'name': 'Sopes y Huaraches La Capital',
                'description': 'Sopes y huaraches con frijoles, lechuga, crema, queso y salsa verde. Masa hecha en casa diariamente.',
                'latitude': 19.4247,
                'longitude': -99.1435,
                'address': 'Av. Chapultepec 789, Juárez',
                'user': users[1]
            }
        ]
        
        stands = []
        for stand_data in stands_data:
            stand = FoodStand(
                name=stand_data['name'],
                description=stand_data['description'],
                latitude=stand_data['latitude'],
                longitude=stand_data['longitude'],
                address=stand_data['address'],
                user_id=stand_data['user'].id
            )
            db.session.add(stand)
            stands.append(stand)
        
        db.session.commit()
        
        # Crear reseñas de ejemplo
        review_comments = [
            "¡Excelente! Los tacos están buenísimos.",
            "Muy rico, definitivamente regresaré.",
            "Buena calidad y precio justo.",
            "Me encanta venir aquí, siempre está fresco.",
            "Recomendado al 100%, sabor auténtico.",
            "Rico pero podrían mejorar la atención.",
            "Está bien, nada extraordinario.",
            "Delicioso y muy buena porción.",
            "Lugar tradicional con buen sazón.",
            "Precios accesibles y buen sabor."
        ]
        
        for stand in stands:
            # Cada puesto tendrá entre 2 y 5 reseñas
            num_reviews = random.randint(2, 5)
            reviewed_users = random.sample(users, min(num_reviews, len(users)))
            
            for user in reviewed_users:
                if user.id != stand.user_id:  # El dueño no puede reseñar su propio puesto
                    review = Review(
                        rating=random.randint(3, 5),  # Calificaciones entre 3 y 5
                        comment=random.choice(review_comments),
                        user_id=user.id,
                        food_stand_id=stand.id
                    )
                    db.session.add(review)
        
        db.session.commit()
        
        return f"Datos de ejemplo creados: {len(users)} usuarios, {len(stands)} puestos, y reseñas aleatorias"
        
    except Exception as e:
        db.session.rollback()
        return f"Error al crear datos de ejemplo: {str(e)}"

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
