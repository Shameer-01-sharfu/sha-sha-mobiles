from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Namma puthu code oda IMPORTS-ah inga add pannidunga
from django.contrib.auth.models import User
from django.http import HttpResponse

# Namma puthu USER CREATION function
def create_free_admin(request):
    if not User.objects.filter(username='Shameer_Admin').exists():
        User.objects.create_superuser('Shameer_Admin', 'admin@example.com', 'MyNewPassword@123')
        return HttpResponse("Sema! Admin Account Successfully Created!")
    return HttpResponse("Account already exists!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
    
    # Namma puthu SECRET URL routing line-ah inga thaan serukanum
    path('make-me-admin/', create_free_admin),
]

# Ithu thaan media folder-la iruka pictures-ah browser-ku anupum
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)