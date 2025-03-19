from pymongo import MongoClient
import os
from dotenv import load_dotenv

# 🔹 Cargar variables de entorno
load_dotenv()
MONGODB_URI = os.environ.get('MONGO_URI')  # Recuerda que en tu .env es MONGO_URI
client = MongoClient(MONGODB_URI)
db = client['mixifydb']  # Cambia al nombre real de tu base en Atlas

# 🔹 Colecciones principales
usuarios_collection = db['usuarios']
ingredientes_collection = db['ingredientes']
historial_collection = db['historial_bebidas']

# 🔹 Helper para registrar usuario
def insert_usuario(data):
    return usuarios_collection.insert_one(data)

# 🔹 Helper para buscar usuario por nombre de usuario
def buscar_usuario(usuario):
    return usuarios_collection.find_one({"usuario": usuario})

# 🔹 Helper para insertar una bebida al historial
def insertar_bebida_historial(data):
    return historial_collection.insert_one(data)

# 🔹 Helper para actualizar un ingrediente
def actualizar_ingrediente(nombre, cantidad):
    return ingredientes_collection.update_one(
        {"nombre": nombre},
        {"$set": {"cantidad": cantidad}}
    )

# 🔹 Helper para obtener todos los ingredientes
def obtener_ingredientes():
    return list(ingredientes_collection.find())
