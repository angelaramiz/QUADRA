from app import db
from datetime import datetime
import math

class FoodStand(db.Model):
    __tablename__ = 'food_stands'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(200), nullable=True)
    # Nuevos campos para ubicación detallada
    municipality = db.Column(db.String(100), nullable=True)  # Municipio/Alcaldía
    state = db.Column(db.String(100), nullable=True)         # Estado
    neighborhood = db.Column(db.String(100), nullable=True)  # Colonia/Barrio
    postal_code = db.Column(db.String(10), nullable=True)    # Código postal
    
    image_filename = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Clave foránea
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relaciones
    reviews = db.relationship('Review', backref='food_stand', lazy=True, cascade='all, delete-orphan')
    
    @property
    def average_rating(self):
        """Calcula el promedio de calificaciones"""
        if not self.reviews:
            return 0
        return sum(review.rating for review in self.reviews) / len(self.reviews)
    
    def distance_to(self, lat, lng):
        """Calcula la distancia en kilómetros a una coordenada dada usando la fórmula de Haversine"""
        R = 6371  # Radio de la Tierra en kilómetros
        
        lat1_rad = math.radians(self.latitude)
        lon1_rad = math.radians(self.longitude)
        lat2_rad = math.radians(lat)
        lon2_rad = math.radians(lng)
        
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        
        a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        return R * c
    
    @classmethod
    def find_within_radius(cls, lat, lng, radius_km=5):
        """Encuentra puestos dentro de un radio específico"""
        stands = cls.query.filter_by(is_active=True).all()
        return [stand for stand in stands if stand.distance_to(lat, lng) <= radius_km]
    
    @classmethod
    def find_by_location(cls, municipality=None, state=None):
        """Encuentra puestos por municipio o estado"""
        query = cls.query.filter_by(is_active=True)
        
        if municipality:
            query = query.filter(cls.municipality.ilike(f'%{municipality}%'))
        if state:
            query = query.filter(cls.state.ilike(f'%{state}%'))
            
        return query.all()
    
    @property
    def total_reviews(self):
        """Cuenta el total de reseñas"""
        return len(self.reviews)
    
    def __repr__(self):
        return f'<FoodStand {self.name}>'
