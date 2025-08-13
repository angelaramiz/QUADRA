#!/usr/bin/env python3
"""
Script para actualizar la base de datos Supabase con los nuevos campos para recuperación de contraseña
"""

import sys
import os

# Agregar el directorio de la aplicación al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def update_database():
    """Actualiza la base de datos con los nuevos campos"""
    try:
        from app import create_app, db
        from app.models.user import User
        
        print("🔄 Conectando a Supabase...")
        app = create_app()
        
        with app.app_context():
            print("🔄 Verificando estructura actual de la tabla users...")
            
            # Verificar si los campos ya existen
            from sqlalchemy import inspect, text
            inspector = inspect(db.engine)
            columns = inspector.get_columns('users')
            column_names = [col['name'] for col in columns]
            
            print(f"📋 Columnas actuales: {column_names}")
            
            # Verificar si necesitamos agregar las nuevas columnas
            needs_reset_token = 'reset_token' not in column_names
            needs_reset_expires = 'reset_token_expires' not in column_names
            
            if needs_reset_token or needs_reset_expires:
                print("🔄 Agregando nuevas columnas para recuperación de contraseña...")
                
                with db.engine.connect() as conn:
                    if needs_reset_token:
                        print("   - Agregando columna 'reset_token'")
                        conn.execute(text("ALTER TABLE users ADD COLUMN reset_token VARCHAR(128)"))
                        conn.commit()
                    
                    if needs_reset_expires:
                        print("   - Agregando columna 'reset_token_expires'")
                        conn.execute(text("ALTER TABLE users ADD COLUMN reset_token_expires TIMESTAMP"))
                        conn.commit()
                
                print("✅ Columnas agregadas exitosamente!")
            else:
                print("✅ Las columnas ya existen. No se necesitan cambios.")
            
            # Verificar la estructura final
            inspector = inspect(db.engine)
            columns = inspector.get_columns('users')
            column_names = [col['name'] for col in columns]
            
            print(f"📊 Estructura final de la tabla users:")
            for col in columns:
                print(f"   - {col['name']}: {col['type']}")
            
            print("\n✅ ¡Base de datos actualizada exitosamente!")
            return True
            
    except Exception as e:
        print(f"❌ Error al actualizar la base de datos: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("🚀 Actualizando base de datos para recuperación de contraseñas...")
    success = update_database()
    
    if success:
        print("\n🎉 ¡Listo! Tu base de datos ya soporta recuperación de contraseñas.")
    else:
        print("\n💥 Hubo un problema al actualizar la base de datos.")
        sys.exit(1)
