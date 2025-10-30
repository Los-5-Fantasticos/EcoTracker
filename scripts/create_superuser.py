import os
import sys
from pathlib import Path
import django
import secrets
import string

# Ensure project root is on sys.path so Django settings can be imported
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EcoTracker.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

username = 'eckotrakeradmin'
email = 'sebaziustf2@gmail.com'
# safe alphabet without $ to avoid shell interpolation issues
alphabet = string.ascii_letters + string.digits + '!@#%&*()-_=+'
password = ''.join(secrets.choice(alphabet) for _ in range(16))

user, created = User.objects.get_or_create(username=username, defaults={'email': email})
user.email = email
user.set_password(password)
user.is_staff = True
user.is_superuser = True
user.save()

print('SUPERUSER_CREATED' if created else 'SUPERUSER_UPDATED')
print('USERNAME:' + username)
print('PASSWORD:' + password)
