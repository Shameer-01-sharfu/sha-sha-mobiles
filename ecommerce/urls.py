from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# BACKGROUND AUTO RUN CODE
from django.contrib.auth.models import User
try:
    # Inga 'Shameer_Admin' nu username, 'MyNewPassword@123' nu password kuduthurken
    if not User.objects.filter(username='Shameer_Admin').exists():
        User.objects.create_superuser('Shameer_Admin', 'admin@example.com', 'MyNewPassword@123')
        print("--- SUPERUSER CREATED SUCCESSFULLY IN BACKGROUND ---")
except Exception as e:
    pass

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)