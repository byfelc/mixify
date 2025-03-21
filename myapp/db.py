from pymongo import MongoClient
import os
from dotenv import load_dotenv

# 🔹 Cargar credenciales desde .env
load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")

# 🔹 Conexión a MongoDB
client = MongoClient(MONGODB_URI)
db = client["mixifydb"]  # Nombre de la BD

print("✅ Conectado a MongoDB desde Django")
