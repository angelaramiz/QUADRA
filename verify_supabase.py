#!/usr/bin/env python3
"""
Script para verificar los datos migrados en Supabase
"""

import sys
import os

# Agregar el directorio de la aplicación al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def verify_supabase_data():
    """Verifica que los datos estén correctamente en Supabase"""
    try:
        from app import create_app, db
        from app.models.user import User
        from app.models.food_stand import FoodStand
        from app.models.review import Review
        
        print("🔄 Conectando a Supabase...")
        app = create_app()
        
        with app.app_context():
            print("\n📊 Verificando datos en Supabase:")
            
            # Verificar usuarios
            users = User.query.all()
            print(f"👥 Usuarios encontrados: {len(users)}")
            for user in users:
                print(f"   - {user.username} ({user.email}) - Creado: {user.created_at}")
            
            # Verificar puestos de comida
            food_stands = FoodStand.query.all()
            print(f"🍕 Puestos de comida: {len(food_stands)}")
            for stand in food_stands:
                print(f"   - {stand.name} - Propietario: {stand.owner.username if stand.owner else 'N/A'}")
            
            # Verificar reseñas
            reviews = Review.query.all()
            print(f"⭐ Reseñas: {len(reviews)}")
            for review in reviews:
                print(f"   - Rating: {review.rating}/5 - Autor: {review.author.username if review.author else 'N/A'}")
            
            print(f"\n✅ Conexión a Supabase verificada exitosamente!")
            print(f"🗄️  Base de datos: {db.engine.url}")
            
            return True
            
    except Exception as e:
        print(f"❌ Error al verificar datos: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("🔍 Verificando datos en Supabase...")
    success = verify_supabase_data()
    
    if success:
        print("\n🎉 ¡Todo funcionando correctamente con Supabase!")
    else:
        print("\n💥 Hubo un problema al acceder a Supabase.")
        sys.exit(1)
