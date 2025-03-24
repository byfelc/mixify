from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('historial/', views.historial_bebidas, name='historial'),
    path('gestion/', views.gestion_ingredientes, name='gestion'),
]