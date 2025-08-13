#!/usr/bin/env python3
"""
🗄️ Script para migrar la base de datos con nuevos campos de ubicación
Ejecuta la migración add_location_fields en Supabase
"""

import os
import sys
import psycopg2
from urllib.parse import urlparse

def run_migration():
    """Ejecuta la migración de ubicación en Supabase"""
    
    # URL de conexión a Supabase (usar variable de entorno)
    database_url = "postgresql://postgres.dfouootxfxsvvpxoerth:CuentaHasta22@aws-0-us-east-2.pooler.supabase.com:5432/postgres"
    
    try:
        # Conectar a la base de datos
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        print("🔗 Conectado a Supabase PostgreSQL")
        
        # Verificar si las columnas ya existen
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'food_stands' 
            AND column_name IN ('municipality', 'state', 'neighborhood', 'postal_code')
        """)
        
        existing_columns = [row[0] for row in cursor.fetchall()]
        
        if len(existing_columns) == 4:
            print("✅ Las columnas de ubicación ya existen en la tabla food_stands")
            return True
        
        print(f"📝 Columnas existentes: {existing_columns}")
        print("🔄 Ejecutando migración de ubicación...")
        
        # Ejecutar migración
        migration_sql = """
        ALTER TABLE food_stands 
        ADD COLUMN IF NOT EXISTS municipality VARCHAR(100),
        ADD COLUMN IF NOT EXISTS state VARCHAR(100),
        ADD COLUMN IF NOT EXISTS neighborhood VARCHAR(100),
        ADD COLUMN IF NOT EXISTS postal_code VARCHAR(10);
        """
        
        cursor.execute(migration_sql)
        conn.commit()
        
        print("✅ Migración ejecutada exitosamente")
        
        # Verificar las nuevas columnas
        cursor.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_name = 'food_stands' 
            AND column_name IN ('municipality', 'state', 'neighborhood', 'postal_code')
            ORDER BY column_name
        """)
        
        new_columns = cursor.fetchall()
        print("\n📊 Nuevas columnas agregadas:")
        for col_name, data_type, nullable in new_columns:
            print(f"  • {col_name}: {data_type} ({'NULL' if nullable == 'YES' else 'NOT NULL'})")
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante la migración: {e}")
        return False
        
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
        print("🔌 Conexión cerrada")

def main():
    print("🚀 MIGRACIÓN DE UBICACIÓN - QUADRA")
    print("=" * 50)
    
    success = run_migration()
    
    if success:
        print("\n🎉 Migración completada exitosamente!")
        print("📍 Nuevos campos disponibles:")
        print("  • municipality - Para filtrar por municipio/alcaldía")
        print("  • state - Para filtrar por estado")
        print("  • neighborhood - Para organizar por colonia/barrio")
        print("  • postal_code - Para futuras funcionalidades")
        return 0
    else:
        print("\n❌ La migración falló. Revisa los errores arriba.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
