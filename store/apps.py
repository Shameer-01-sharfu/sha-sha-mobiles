from django.apps import AppConfig
from django.db.models.signals import post_migrate

def create_superuser_auto(sender, **kwargs):
    from django.contrib.auth.models import User
    try:
        if not User.objects.filter(username='Shameer_Live').exists():
            User.objects.create_superuser('Shameer_Live', 'admin@example.com', 'Shameer@12345')
            print("--- SUPERUSER CREATED IN LIVE DATABASE ---")
    except Exception as e:
        print(f"Error creating superuser: {e}")

class StoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store'

    def ready(self):
        post_migrate.connect(create_superuser_auto, sender=self)