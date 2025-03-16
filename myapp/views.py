from django.shortcuts import render, redirect
from .models import HistorialBebidas, Ingrediente, CustomUser  # ✅ Importar los modelos
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login


def home(request):
    return render(request, 'myapp/home.html')

def register(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        usuario = request.POST['usuario']
        contrasena = request.POST['contrasena']
        correo = request.POST['correo']

        user = CustomUser.objects.create_user(
            usuario=usuario,
            contrasena=contrasena,
            nombre=nombre,
            correo=correo,
        )

        return redirect('login')
    return render(request, 'myapp/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST["usuario"]
        password = request.POST["contrasena"]
        print("como lo mueve ${username}")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            print("si sale")
            return redirect('myapp/home')
        else:
            print("no sale")
            return render(request, 'myapp/login.html')
    return render(request, 'myapp/login.html')

def logout_view(request):
    return render(request, 'myapp/logout.html')  # Si no tienes logout.html, usa Django auth.logout

def historial_bebidas(request):
    historial = HistorialBebidas.objects.order_by('-fecha')[:5] if request.user.is_authenticated else []
    return render(request, 'myapp/historial.html', {'historial': historial})

def gestion_ingredientes(request):
    ingredientes = Ingrediente.objects.all()[:2] if request.user.is_authenticated else []
    
    if request.method == 'POST' and request.user.is_authenticated:
        for i, ingrediente in enumerate(ingredientes, start=1):
            ingrediente.nombre = request.POST.get(f'nombre_{i}', ingrediente.nombre)
            ingrediente.cantidad = request.POST.get(f'cantidad_{i}', ingrediente.cantidad)
            ingrediente.save()

    return render(request, 'myapp/gestion.html', {'ingredientes': ingredientes})