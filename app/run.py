#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Punto de entrada para ejecutar la aplicación QUADRA
Ejecutar desde la carpeta app/ o desde la raíz con: python -m app.run
"""

import os

try:
    # Cuando se ejecuta desde la carpeta app/
    from __init__ import create_app, db
except ImportError:
    # Cuando se ejecuta como módulo desde la raíz
    from . import create_app, db

def main():
    app = create_app()
    
    with app.app_context():
        # Crear todas las tablas si no existen
        db.create_all()
        print("✅ Base de datos inicializada")
    
    print("🚀 Iniciando aplicación QUADRA...")
    print("📍 URL: http://localhost:5000")
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)

if __name__ == '__main__':
    main()
