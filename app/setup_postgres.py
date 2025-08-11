#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para configurar PostgreSQL para Quadra
Ejecutar después de instalar PostgreSQL y crear la base de datos
"""

import os
import sys
from dotenv import load_dotenv

def main():
    print("🐘 CONFIGURACIÓN DE POSTGRESQL PARA QUADRA")
    print("=" * 50)
    
    # Cargar variables de entorno
    load_dotenv()
    
    # Verificar si ya está configurado PostgreSQL
    database_url = os.environ.get('DATABASE_URL', '')
    
    if database_url.startswith('postgresql://'):
        print("✅ PostgreSQL ya está configurado en .env")
        print(f"📊 Database URL: {database_url}")
    else:
        print("⚠️  PostgreSQL no está configurado. Usando SQLite por defecto.")
        print("📝 Para configurar PostgreSQL:")
        print()
        print("1. Instala PostgreSQL: https://www.postgresql.org/download/")
        print("2. Crea la base de datos:")
        print("   psql -U postgres")
        print("   CREATE DATABASE quadra_db;")
        print("   CREATE USER quadra_user WITH PASSWORD 'tu_contraseña';")
        print("   GRANT ALL PRIVILEGES ON DATABASE quadra_db TO quadra_user;")
        print("   \\q")
        print()
        print("3. Edita el archivo .env y cambia:")
        print("   DATABASE_URL=postgresql://quadra_user:tu_contraseña@localhost:5432/quadra_db")
        print()
        return
    
    # Verificar conexión
    try:
        from app import create_app, db
        from sqlalchemy import inspect, text
        
        app = create_app()
        with app.app_context():
            # Intentar conectar
            result = db.session.execute(text('SELECT 1')).fetchone()
            print("✅ Conexión a PostgreSQL exitosa")
            print(f"🔧 Motor de BD: {db.engine.name}")
            
            # Verificar si hay tablas
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            if tables:
                print(f"📋 Tablas existentes ({len(tables)}): {', '.join(tables)}")
                
                # Verificar datos
                from app.models.user import User
                from app.models.food_stand import FoodStand
                from app.models.review import Review
                
                print(f"📊 Datos actuales:")
                print(f"   👤 Usuarios: {User.query.count()}")
                print(f"   🏪 Puestos: {FoodStand.query.count()}")
                print(f"   ⭐ Reseñas: {Review.query.count()}")
            else:
                print("⚠️  No hay tablas. Ejecuta las migraciones:")
                print("   flask db init")
                print("   flask db migrate -m 'Initial migration'")
                print("   flask db upgrade")
                
    except Exception as e:
        print(f"❌ Error conectando a PostgreSQL: {e}")
        print("🔧 Verifica:")
        print("   - PostgreSQL está ejecutándose")
        print("   - La base de datos existe")
        print("   - Las credenciales son correctas")
        print("   - El puerto 5432 está disponible")

if __name__ == '__main__':
    main()
