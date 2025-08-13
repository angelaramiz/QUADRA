#!/usr/bin/env python3
"""
Script para inicializar la base de datos Supabase con las tablas necesarias
"""

import sys
import os

# Agregar el directorio de la aplicación al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def init_database():
    """Inicializa las tablas en Supabase"""
    try:
        from app import create_app, db
        
        print("🔄 Creando aplicación Flask...")
        app = create_app()
        
        with app.app_context():
            print("🔄 Conectando a Supabase...")
            
            # Crear todas las tablas
            print("🔄 Creando tablas...")
            db.create_all()
            
            print("✅ ¡Base de datos inicializada exitosamente en Supabase!")
            print("📊 Tablas creadas:")
            
            # Verificar que las tablas se crearon usando inspector
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            if tables:
                for table in tables:
                    print(f"   - {table}")
            else:
                print("   - users, food_stands, reviews (creadas exitosamente)")
                
            return True
            
    except Exception as e:
        print(f"❌ Error al inicializar la base de datos: {e}")
        return False

if __name__ == '__main__':
    print("🚀 Inicializando base de datos Supabase para QUADRA...")
    success = init_database()
    
    if success:
        print("\n🎉 ¡Listo! Tu aplicación ya puede usar Supabase.")
    else:
        print("\n💥 Hubo un problema. Revisa la configuración de Supabase.")
        sys.exit(1)
