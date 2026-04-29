from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registro/', views.registro_docente, name='registro_docente'),
    path('registro-maia/', views.registro_maia, name='registro_maia'),
    path('dashboard/', views.dashboard_docente, name='dashboard_docente'),
]