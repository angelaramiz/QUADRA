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
        
        app = create_app()
        with app.app_context():
            # Intentar conectar
            db.engine.execute('SELECT 1')
            print("✅ Conexión a PostgreSQL exitosa")
            
            # Verificar si hay tablas
            tables = db.engine.table_names()
            if tables:
                print(f"📋 Tablas existentes: {', '.join(tables)}")
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
