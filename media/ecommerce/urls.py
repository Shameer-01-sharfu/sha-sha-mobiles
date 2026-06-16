"""
URL configuration for Ecommerce_Project project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 1. Main Django Admin Portal (Typo fixed here from admin.site.split -> urls)
    path('admin/', admin.site.urls),
    
    # 2. Connecting your App routing system
    path('', include('store.urls')), 
]

# 3. Serving Media Images (Mobiles photos fetch aagurathuku idhu romba mukkiyam)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)