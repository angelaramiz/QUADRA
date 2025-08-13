#!/usr/bin/env python3
"""
Script simplificado para agregar campos de ubicación usando psycopg2 directamente
"""

import os

def migrate_with_psycopg2():
    """Migra usando psycopg2 directamente"""
    try:
        import psycopg2
        
        # Conexión directa a Supabase
        conn = psycopg2.connect(
            "postgresql://postgres.dfouootxfxsvvpxoerth:CuentaHasta22@aws-0-us-east-2.pooler.supabase.com:5432/postgres"
        )
        
        cursor = conn.cursor()
        
        print("🔗 Conectado a Supabase PostgreSQL")
        
        # Verificar si las columnas ya existen
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'food_stands'
        """)
        
        existing_columns = [row[0] for row in cursor.fetchall()]
        print(f"📋 Columnas existentes: {existing_columns}")
        
        # Agregar columnas que no existen
        new_columns = [
            ('municipality', 'VARCHAR(100)'),
            ('state', 'VARCHAR(100)'),
            ('neighborhood', 'VARCHAR(100)'),
            ('postal_code', 'VARCHAR(10)')
        ]
        
        for col_name, col_type in new_columns:
            if col_name not in existing_columns:
                sql = f"ALTER TABLE food_stands ADD COLUMN {col_name} {col_type}"
                print(f"➕ Ejecutando: {sql}")
                cursor.execute(sql)
                print(f"✅ Columna '{col_name}' agregada")
            else:
                print(f"⏭️ Columna '{col_name}' ya existe")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("🎉 Migración completada exitosamente!")
        return True
        
    except ImportError:
        print("❌ psycopg2 no está instalado")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 QUADRA - Migración directa con psycopg2")
    print("=" * 50)
    
    if migrate_with_psycopg2():
        print("\n✅ ¡Campos de ubicación agregados exitosamente!")
        print("🎯 Ahora puedes usar los filtros de búsqueda por municipio, estado y radio")
    else:
        print("\n❌ No se pudo ejecutar la migración automática")
        print("💡 Puedes agregar los campos manualmente en Supabase:")
        print("   ALTER TABLE food_stands ADD COLUMN municipality VARCHAR(100);")
        print("   ALTER TABLE food_stands ADD COLUMN state VARCHAR(100);")
        print("   ALTER TABLE food_stands ADD COLUMN neighborhood VARCHAR(100);")
        print("   ALTER TABLE food_stands ADD COLUMN postal_code VARCHAR(10);")
