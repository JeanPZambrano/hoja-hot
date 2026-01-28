import os
import django
from django.contrib.auth import get_user_model

# Asegúrate de que este nombre sea igual al de la carpeta que tiene el archivo settings.py
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hoja_de_vida.settings") 
django.setup()

User = get_user_model()
USERNAME = 'admin_render'
EMAIL = 'admin@example.com'
PASSWORD = 'ContrasenaSegura123'

if not User.objects.filter(username=USERNAME).exists():
    print(f"Creando superusuario {USERNAME}...")
    User.objects.create_superuser(USERNAME, EMAIL, PASSWORD)
    print("¡Superusuario creado exitosamente!")
else:
    print(f"El usuario {USERNAME} ya existe.")