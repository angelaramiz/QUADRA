#!/usr/bin/env python3
"""
WSGI entry point para QUADRA
Usado por Gunicorn en producción (Fly.io)
"""

import os
import sys

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from app import create_app
    
    # Crear la aplicación Flask
    app = create_app()
    
    if __name__ == "__main__":
        # Para desarrollo local
        app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
        
except Exception as e:
    print(f"Error al inicializar la aplicación: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
