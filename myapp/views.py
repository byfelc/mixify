from django.shortcuts import render, redirect
from .models import HistorialBebidas, CustomUser, Contenedores
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.http import JsonResponse 

def home(request):
    return render(request, 'myapp/home.html')

def register(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre','')
        usuario = request.POST['usuario']
        contrasena = request.POST.get('contrasena','')
        correo = request.POST.get('correo','')
        estatus = True

        user = CustomUser.objects.create_user(
            usuario=usuario,
            contrasena=contrasena,
            nombre=nombre,
            correo=correo,
            estatus = estatus
        )

        return redirect('login')
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST["usuario"]
        password = request.POST["contrasena"]
        print("como lo mueve ${username}")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            print("si sale")
            return redirect('home')
        else:
            print("no sale")
            return render(request, 'myapp/login.html')
    return render(request, 'myapp/login.html')

def logout_view(request):
    return render(request, 'myapp/logout.html')  # Si no tienes logout.html, usa Django auth.logout

def historial_bebidas(request):
    historial = HistorialBebidas() if request.user.is_authenticated else []
    return JsonResponse({'historial': historial})

def gestion_ingredientes(request):
    ingredientes = Contenedores() if request.user.is_authenticated else []
    return JsonResponse({'ingredientes': ingredientes})