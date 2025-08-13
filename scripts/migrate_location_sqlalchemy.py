#!/usr/bin/env python3
"""
🗄️ Script para migrar la base de datos usando SQLAlchemy
Ejecuta la migración add_location_fields en Supabase
"""

import os
import sys

def run_migration():
    """Ejecuta la migración usando SQLAlchemy"""
    
    try:
        # Configurar variables de entorno
        os.environ['DATABASE_URL'] = "postgresql://postgres.dfouootxfxsvvpxoerth:CuentaHasta22@aws-0-us-east-2.pooler.supabase.com:5432/postgres"
        
        # Importar después de configurar env
        sys.path.append('.')
        from app import create_app, db
        
        app = create_app()
        
        with app.app_context():
            print("🔗 Conectado a Supabase PostgreSQL")
            
            # Ejecutar SQL directamente
            migration_sql = """
            ALTER TABLE food_stands 
            ADD COLUMN IF NOT EXISTS municipality VARCHAR(100),
            ADD COLUMN IF NOT EXISTS state VARCHAR(100),
            ADD COLUMN IF NOT EXISTS neighborhood VARCHAR(100),
            ADD COLUMN IF NOT EXISTS postal_code VARCHAR(10);
            """
            
            db.engine.execute(migration_sql)
            
            print("✅ Migración ejecutada exitosamente")
            print("📍 Nuevos campos agregados:")
            print("  • municipality - Para filtrar por municipio/alcaldía")
            print("  • state - Para filtrar por estado")  
            print("  • neighborhood - Para organizar por colonia/barrio")
            print("  • postal_code - Para futuras funcionalidades")
            
            return True
            
    except Exception as e:
        print(f"❌ Error durante la migración: {e}")
        
        # Intentar método alternativo
        try:
            print("🔄 Intentando método alternativo...")
            db.session.execute(migration_sql)
            db.session.commit()
            print("✅ Migración exitosa con método alternativo")
            return True
        except Exception as e2:
            print(f"❌ Error en método alternativo: {e2}")
            return False

def main():
    print("🚀 MIGRACIÓN DE UBICACIÓN - QUADRA")
    print("=" * 50)
    
    success = run_migration()
    
    if success:
        print("\n🎉 Migración completada!")
        print("🔄 Reinicia la aplicación para usar los nuevos filtros")
        return 0
    else:
        print("\n❌ La migración falló.")
        print("💡 Tip: Los filtros funcionarán cuando se agreguen los campos manualmente")
        return 1

if __name__ == "__main__":
    sys.exit(main())
