from django.shortcuts import render, redirect
from django.http import HttpResponse
from .db_con import usuarios_collection, historial_collection, ingredientes_collection
import bcrypt
import requests
from datetime import datetime
from bson import ObjectId


def editar_perfil(request):
    if not request.session.get('is_authenticated'):
        return redirect('login')

    user_id = request.session.get('usuario_id')
    user = usuarios_collection.find_one({'_id': ObjectId(user_id)})

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        usuario = request.POST.get('usuario')
        correo = request.POST.get('correo')

        usuarios_collection.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': {
                'nombre': nombre,
                'usuario': usuario,
                'correo': correo
            }}
        )

        # 🔄 Actualiza también la sesión
        request.session['nombre'] = nombre
        request.session['usuario'] = usuario

        return redirect('perfil')

    return render(request, 'myapp/perfil.html', {'user': user})


# ✅ HOME
def home(request):
    return render(request, 'myapp/home.html')

# ✅ REGISTER
def register(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        usuario = request.POST.get('usuario', '').strip()
        correo = request.POST.get('correo', '').strip()
        contrasena = request.POST.get('contrasena', '').strip()
        confirm = request.POST.get('confirm_password', '').strip()

        if contrasena != confirm:
            return HttpResponse("Las contraseñas no coinciden", status=400)

        existing_user = usuarios_collection.find_one({"usuario": usuario})
        if existing_user:
            return HttpResponse("Este usuario ya existe", status=400)

        # ✅ Hashear y convertir a string
        hashed = bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        usuarios_collection.insert_one({
            "nombre": nombre,
            "usuario": usuario,
            "correo": correo,
            "password": hashed,
            "estado": "activo"
        })

        return redirect('login')
    return render(request, 'myapp/register.html')

# ✅ LOGIN
def login_view(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario', '').strip()
        contrasena = request.POST.get('contrasena', '').strip()

        user = usuarios_collection.find_one({"usuario": usuario})

        if user and bcrypt.checkpw(contrasena.encode('utf-8'), user['password'].encode('utf-8')):
            request.session['usuario'] = user['usuario']
            request.session['nombre'] = user['nombre']
            request.session['usuario_id'] = str(user['_id'])
            request.session['is_authenticated'] = True
            return redirect('home')
        else:
            return HttpResponse("Usuario o contraseña incorrectos", status=401)

    return render(request, 'myapp/login.html')

# ✅ LOGOUT
def logout_view(request):
    request.session.flush()
    return redirect('login')

# ✅ Perfil de Usuario
def perfil(request):
    if not request.session.get('is_authenticated'):
        return redirect('login')

    user_data = usuarios_collection.find_one({'_id': ObjectId(request.session['usuario_id'])})
    return render(request, 'myapp/perfil.html', {'user': user_data})

# ✅ HISTORIAL DE BEBIDAS GLOBAL
def historial_bebidas(request):
    if not request.session.get('is_authenticated'):
        return redirect('login')
    
    # Ordena por fecha descendente (el más nuevo primero)
    historial = list(historial_collection.find().sort('fecha', -1))

    for registro in historial:
        try:
            registro["fecha_formateada"] = datetime.strptime(
                registro["fecha"], "%Y-%m-%dT%H:%M:%S"
            ).strftime("%d/%m/%Y %H:%M")
        except Exception:
            registro["fecha_formateada"] = registro["fecha"]

    return render(request, 'myapp/historial.html', {'historial': historial})

def gestion_ingredientes(request):
    if not request.session.get('is_authenticated'):
        return redirect('login')

    ingredientes = list(ingredientes_collection.find({}))

    if request.method == 'POST':
        for i in range(1, len(ingredientes) + 1):
            original_nombre = request.POST.get(f'original_nombre_{i}')
            nuevo_nombre = request.POST.get(f'nombre_{i}')
            tipo = request.POST.get(f'tipo_{i}')
            cantidad = request.POST.get(f'cantidad_{i}')

            if original_nombre and nuevo_nombre and tipo and cantidad:
                ingredientes_collection.update_one(
                    {'nombre': original_nombre},
                    {'$set': {
                        'nombre': nuevo_nombre,
                        'tipo': tipo,
                        'Cant_rest': int(cantidad)
                    }}
                )
        return redirect('gestion')

    return render(request, 'myapp/gestion.html', {'ingredientes': ingredientes})