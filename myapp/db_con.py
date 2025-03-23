import os
from pymongo import MongoClient

# ⚠️ Primero revisa si existe la variable de entorno y usa la que pasaremos en Render
MONGO_URI = os.environ.get(
    "MONGO_URI",
    "mongodb+srv://iracheta602:Mixify1234@mixify.4va0z.mongodb.net/?retryWrites=true&w=majority&appName=mixify"
)

client = MongoClient(MONGO_URI)
db = client['mixifydb']

usuarios_collection = db['usuarios']
historial_collection = db['historial_bebidas']
ingredientes_collection = db['estado_contenedores']
