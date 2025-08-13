#!/usr/bin/env python3
"""
Script para migrar datos de SQLite local a Supabase
Migra usuarios, puestos de comida y reseñas
"""

import sys
import os
import sqlite3

# Agregar el directorio de la aplicación al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def migrate_data():
    """Migra datos de SQLite a Supabase"""
    try:
        # Configuración de bases de datos
        sqlite_db_path = 'app/instance/quadra.db'
        
        print("🔄 Verificando base de datos SQLite local...")
        
        # Verificar si existe la base de datos SQLite
        if not os.path.exists(sqlite_db_path):
            print("❌ No se encontró la base de datos SQLite local.")
            print("🔍 Buscando en ubicaciones alternativas...")
            
            # Buscar en ubicaciones alternativas
            possible_paths = [
                'quadra.db',
                'instance/quadra.db',
                'app/quadra.db'
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    sqlite_db_path = path
                    print(f"✅ Encontrada base de datos en: {path}")
                    break
            else:
                print("❌ No se encontró ninguna base de datos SQLite.")
                return False
        
        # Conectar a SQLite
        print(f"🔄 Conectando a SQLite: {sqlite_db_path}")
        sqlite_conn = sqlite3.connect(sqlite_db_path)
        sqlite_cursor = sqlite_conn.cursor()
        
        # Verificar qué tablas existen en SQLite
        sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = sqlite_cursor.fetchall()
        print(f"📊 Tablas encontradas en SQLite: {[table[0] for table in tables]}")
        
        # Conectar a Supabase usando Flask
        from app import create_app, db
        from app.models.user import User
        from app.models.food_stand import FoodStand
        from app.models.review import Review
        
        print("🔄 Conectando a Supabase...")
        app = create_app()
        
        with app.app_context():
            # Migrar usuarios
            print("\n👥 Migrando usuarios...")
            try:
                sqlite_cursor.execute("SELECT * FROM users")
                users_data = sqlite_cursor.fetchall()
                
                if users_data:
                    # Obtener nombres de columnas
                    sqlite_cursor.execute("PRAGMA table_info(users)")
                    columns = [column[1] for column in sqlite_cursor.fetchall()]
                    print(f"📋 Columnas de usuarios: {columns}")
                    
                    migrated_users = 0
                    for user_row in users_data:
                        user_dict = dict(zip(columns, user_row))
                        
                        # Verificar si el usuario ya existe en Supabase
                        existing_user = User.query.filter_by(email=user_dict.get('email')).first()
                        if existing_user:
                            print(f"⚠️  Usuario {user_dict.get('username')} ya existe, saltando...")
                            continue
                        
                        # Crear nuevo usuario en Supabase
                        new_user = User(
                            username=user_dict.get('username'),
                            email=user_dict.get('email'),
                            password_hash=user_dict.get('password_hash'),
                            created_at=user_dict.get('created_at'),
                            is_active=user_dict.get('is_active', True)
                        )
                        
                        db.session.add(new_user)
                        migrated_users += 1
                        print(f"✅ Usuario migrado: {user_dict.get('username')}")
                    
                    db.session.commit()
                    print(f"🎉 {migrated_users} usuarios migrados exitosamente!")
                else:
                    print("ℹ️  No hay usuarios para migrar.")
                    
            except sqlite3.OperationalError as e:
                if "no such table: users" in str(e):
                    print("ℹ️  Tabla 'users' no existe en SQLite.")
                else:
                    print(f"❌ Error al migrar usuarios: {e}")
            
            # Migrar puestos de comida
            print("\n🍕 Migrando puestos de comida...")
            try:
                sqlite_cursor.execute("SELECT * FROM food_stands")
                food_stands_data = sqlite_cursor.fetchall()
                
                if food_stands_data:
                    sqlite_cursor.execute("PRAGMA table_info(food_stands)")
                    columns = [column[1] for column in sqlite_cursor.fetchall()]
                    print(f"📋 Columnas de food_stands: {columns}")
                    
                    migrated_stands = 0
                    for stand_row in food_stands_data:
                        stand_dict = dict(zip(columns, stand_row))
                        
                        # Verificar si el puesto ya existe
                        existing_stand = FoodStand.query.filter_by(name=stand_dict.get('name')).first()
                        if existing_stand:
                            print(f"⚠️  Puesto {stand_dict.get('name')} ya existe, saltando...")
                            continue
                        
                        # Crear nuevo puesto
                        new_stand = FoodStand(
                            name=stand_dict.get('name'),
                            description=stand_dict.get('description'),
                            latitude=stand_dict.get('latitude'),
                            longitude=stand_dict.get('longitude'),
                            address=stand_dict.get('address'),
                            phone=stand_dict.get('phone'),
                            owner_id=stand_dict.get('owner_id'),
                            created_at=stand_dict.get('created_at'),
                            is_active=stand_dict.get('is_active', True)
                        )
                        
                        db.session.add(new_stand)
                        migrated_stands += 1
                        print(f"✅ Puesto migrado: {stand_dict.get('name')}")
                    
                    db.session.commit()
                    print(f"🎉 {migrated_stands} puestos de comida migrados exitosamente!")
                else:
                    print("ℹ️  No hay puestos de comida para migrar.")
                    
            except sqlite3.OperationalError as e:
                if "no such table: food_stands" in str(e):
                    print("ℹ️  Tabla 'food_stands' no existe en SQLite.")
                else:
                    print(f"❌ Error al migrar puestos: {e}")
            
            # Migrar reseñas
            print("\n⭐ Migrando reseñas...")
            try:
                sqlite_cursor.execute("SELECT * FROM reviews")
                reviews_data = sqlite_cursor.fetchall()
                
                if reviews_data:
                    sqlite_cursor.execute("PRAGMA table_info(reviews)")
                    columns = [column[1] for column in sqlite_cursor.fetchall()]
                    print(f"📋 Columnas de reviews: {columns}")
                    
                    migrated_reviews = 0
                    for review_row in reviews_data:
                        review_dict = dict(zip(columns, review_row))
                        
                        # Crear nueva reseña
                        new_review = Review(
                            rating=review_dict.get('rating'),
                            comment=review_dict.get('comment'),
                            user_id=review_dict.get('user_id'),
                            food_stand_id=review_dict.get('food_stand_id'),
                            created_at=review_dict.get('created_at')
                        )
                        
                        db.session.add(new_review)
                        migrated_reviews += 1
                        print(f"✅ Reseña migrada (Rating: {review_dict.get('rating')})")
                    
                    db.session.commit()
                    print(f"🎉 {migrated_reviews} reseñas migradas exitosamente!")
                else:
                    print("ℹ️  No hay reseñas para migrar.")
                    
            except sqlite3.OperationalError as e:
                if "no such table: reviews" in str(e):
                    print("ℹ️  Tabla 'reviews' no existe en SQLite.")
                else:
                    print(f"❌ Error al migrar reseñas: {e}")
        
        # Cerrar conexión SQLite
        sqlite_conn.close()
        
        print("\n🎉 ¡Migración completada exitosamente!")
        print("📊 Datos transferidos de SQLite a Supabase.")
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante la migración: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("🚀 Iniciando migración de datos a Supabase...")
    success = migrate_data()
    
    if success:
        print("\n✅ ¡Migración completada! Tus datos ya están en Supabase.")
    else:
        print("\n💥 Hubo problemas durante la migración.")
        sys.exit(1)
