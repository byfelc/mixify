from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required  # Para proteger rutas
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages  # Para mostrar mensajes de error/éxito
from .models import HistorialBebidas, Ingrediente, CustomUser  # Importamos modelos


# 🔹 Home (protegido)
@login_required(login_url='login')
def home(request):
    return render(request, 'myapp/home.html')


# 🔹 Registro de usuarios
def register(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        usuario = request.POST['usuario']
        contrasena = request.POST['contrasena']
        correo = request.POST['correo']

        # Verificar si el usuario ya existe
        if CustomUser.objects.filter(username=usuario).exists():
            messages.error(request, "❌ El usuario ya está registrado.")
            return redirect('register')

        # Crear usuario con contraseña encriptada
        user = CustomUser(
            username=usuario,
            nombre=nombre,
            correo=correo,
        )
        user.set_password(contrasena)  # 🔐 Encripta la contraseña
        user.save()

        messages.success(request, "✅ Registro exitoso. ¡Ahora puedes iniciar sesión!")
        return redirect('login')

    return render(request, 'myapp/register.html')


# 🔹 Login de usuario
def login_view(request):
    if request.method == 'POST':
        username = request.POST["usuario"]
        password = request.POST["contrasena"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, f"✅ Bienvenido, {user.username}!")
            return redirect('home')
        else:
            messages.error(request, "❌ Usuario o contraseña incorrectos.")
            return redirect('login')

    return render(request, 'myapp/login.html')


# 🔹 Logout
def logout_view(request):
    logout(request)
    messages.success(request, "✅ Has cerrado sesión correctamente.")
    return redirect('login')


# 🔹 Historial de bebidas (protegido)
@login_required(login_url='login')
def historial_bebidas(request):
    historial = HistorialBebidas.objects.order_by('-fecha')[:5]  
    return render(request, 'myapp/historial.html', {'historial': historial})


# 🔹 Gestión de ingredientes (protegido)
@login_required(login_url='login')
def gestion_ingredientes(request):
    ingredientes = Ingrediente.objects.all()[:2]  # Solo mostrar 2 ingredientes

    if request.method == 'POST':
        for i, ingrediente in enumerate(ingredientes, start=1):
            nombre_nuevo = request.POST.get(f'nombre_{i}')
            cantidad_nueva = request.POST.get(f'cantidad_{i}')

            if nombre_nuevo and cantidad_nueva:  # Evitar errores si no hay valores
                ingrediente.nombre = nombre_nuevo
                ingrediente.cantidad = cantidad_nueva
                ingrediente.save()

        messages.success(request, "✅ Ingredientes actualizados correctamente.")

    return render(request, 'myapp/gestion.html', {'ingredientes': ingredientes})
 