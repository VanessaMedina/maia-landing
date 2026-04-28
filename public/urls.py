from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('sobre/', views.about, name='about'),
    path('articulos/', views.articles, name='articles'),
    path('preguntas-frecuentes/', views.faq, name='faq'),
    path('recursos/', views.articles_list, name='articles_list'),
    path('recursos/<slug:slug>/', views.article_detail, name='article_detail'),
]