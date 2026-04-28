from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('public.urls')),      # Página pública
    path('cuenta/', include('core.urls')), # Área autenticada
]
