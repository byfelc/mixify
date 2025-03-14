from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='myapp\.env')
MONGODB_URI = os.environ.get('MONGODB_URI')
client = MongoClient(MONGODB_URI)
db = client['mixifydb']

class CustomUsermanager(BaseUserManager):

    def create_user(self, usuario, nombre, correo, telefono, estatus, contrasena):
        if not usuario:
            raise ValueError("Ingrese nombre de usuario")
        
        user = self.model(
            usuario=usuario,
            nombre=nombre,
            correo=correo,
            estatus=estatus
            )
        if contrasena:
            user.set_password(contrasena)
        user.save(using=self._db)
        return user
        
class CustomUser(AbstractBaseUser):
    nombre = models.CharField(max_length=50, unique=True)
    usuario = models.CharField(max_length=100, unique=True)
    correo = models.EmailField(max_length=100)
    contrasena = models.CharField(max_length=100)
    estatus = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'usuario'
    REQUIRED_FIELDS = ['contrasena']

    objects = CustomUsermanager()

    def __str__(self):
        return self.usuario

    def save(self, *args, **kwargs):
        if self.contrasena:
            self.set_password(self.contrasena) 
        super().save(*args, **kwargs)
        collection = db['usuarios']
        
        user_data = {
            'nombre': self.nombre,
            'usuario': self.usuario,
            'contrasena': self.contrasena,
            'correo': self.correo,
            'estatus': self.estatus,
            'fecha_registro': self.fecha_registro
        }
        collection.insert_one(user_data)

class Ingrediente(models.Model):
    nombre = models.CharField(max_length=100)
    cantidad = models.IntegerField(default=100)  # Porcentaje del ingrediente

    def __str__(self):
        return f"{self.nombre} ({self.cantidad}%)"

class HistorialBebidas(models.Model):
    nombre = models.CharField(max_length=200)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.fecha}"
