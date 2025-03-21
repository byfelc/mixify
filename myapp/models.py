from pymongo import MongoClient
import os
from dotenv import load_dotenv
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Cargar las variables de entorno
load_dotenv(dotenv_path='myapp/.env')

# Conexión a MongoDB
MONGODB_URI = os.environ.get('MONGODB_URI')
client = MongoClient(MONGODB_URI)
db = client.get_database("mixifydb")  # Conectar a la base de datos "mixifydb"

class CustomUserManager(BaseUserManager):
    def create_user(self, usuario, nombre, correo, estatus, contrasena):
        if not usuario:
            raise ValueError("El nombre de usuario es obligatorio.")
        
        # Crear el usuario en MongoDB
        user_data = {
            'usuario': usuario,
            'nombre': nombre,
            'correo': correo,
            'estatus': estatus,
            'contrasena': contrasena
        }
        
        # Cifrar la contraseña antes de guardar
        if contrasena:
            user_data['contrasena'] = self.make_random_password()  # Cifra la contraseña

        # Guardar el usuario en MongoDB
        collection = db['usuarios']
        collection.insert_one(user_data)
        return user_data


class CustomUser(AbstractBaseUser):
    usuario = models.CharField(max_length=100, unique=True)  # Campo de usuario
    nombre = models.CharField(max_length=50, unique=True)
    correo = models.EmailField(max_length=100)
    contrasena = models.CharField(max_length=100)
    estatus = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'usuario'
    REQUIRED_FIELDS = ['contrasena']
    
    objects = CustomUserManager()

    def __str__(self):
        return self.usuario

    def save(self, *args, **kwargs):
        if self.contrasena:
            self.set_password(self.contrasena)
        
        # Guardamos el usuario en MongoDB
        user_data = {
            'nombre': self.nombre,
            'usuario': self.usuario,
            'correo': self.correo,
            'estatus': self.estatus,
            'fecha_registro': self.fecha_registro,
            'contrasena': self.contrasena,
        }
        collection = db['usuarios']
        collection.insert_one(user_data)

# Función para obtener el historial de bebidas
def HistorialBebidas():
    historial = db["historial_bebidas"]
    historial_bebidas = list(historial.find({}, {"_id": 0}))
    return historial_bebidas

# Función para obtener los contenedores de estado
def Contenedores():
    contenedores = db["estado-contenedores"]
    estado_contenedores = list(contenedores.find({}, {"_id": 0}))
    return estado_contenedores
