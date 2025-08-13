#!/usr/bin/env python3
"""
🔐 Generador de credenciales seguras para QUADRA
Este script genera claves secretas seguras para usar en producción.
"""

import secrets
import string
import sys

def generate_secret_key(length=64):
    """Genera una clave secreta segura para Flask"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*(-_=+)"
    secret_key = ''.join(secrets.choice(alphabet) for _ in range(length))
    return secret_key

def generate_jwt_secret(length=32):
    """Genera una clave para JWT tokens"""
    return secrets.token_hex(length)

def main():
    print("🔐 GENERADOR DE CREDENCIALES SEGURAS - QUADRA")
    print("=" * 50)
    
    # Generar claves
    flask_secret = generate_secret_key(64)
    jwt_secret = generate_jwt_secret(32)
    
    print("\n✅ Credenciales generadas exitosamente:")
    print("\n1. SECRET_KEY para Flask:")
    print(f"   {flask_secret}")
    
    print("\n2. JWT_SECRET_KEY (opcional):")
    print(f"   {jwt_secret}")
    
    print("\n🔒 INSTRUCCIONES DE SEGURIDAD:")
    print("• NUNCA compartas estas claves públicamente")
    print("• Usa estas claves solo en tu entorno de producción")
    print("• Guárdalas en un lugar seguro")
    print("• Configúralas con: flyctl secrets set SECRET_KEY=\"tu_clave_aqui\"")
    
    print("\n📋 Comando para Fly.io:")
    print(f'flyctl secrets set SECRET_KEY="{flask_secret}"')
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
