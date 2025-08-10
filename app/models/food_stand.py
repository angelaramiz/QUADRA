from app import db
from datetime import datetime

class FoodStand(db.Model):
    __tablename__ = 'food_stands'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(200), nullable=True)
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
    
    @property
    def total_reviews(self):
        """Cuenta el total de reseñas"""
        return len(self.reviews)
    
    def __repr__(self):
        return f'<FoodStand {self.name}>'
