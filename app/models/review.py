from app import db
from datetime import datetime

class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 estrellas
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Claves foráneas
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    food_stand_id = db.Column(db.Integer, db.ForeignKey('food_stands.id'), nullable=False)
    
    # Restricción única: un usuario solo puede revisar un puesto una vez
    __table_args__ = (db.UniqueConstraint('user_id', 'food_stand_id', name='unique_user_food_stand_review'),)
    
    def __repr__(self):
        return f'<Review {self.rating} stars for FoodStand {self.food_stand_id}>'
