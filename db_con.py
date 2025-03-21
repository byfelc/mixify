from pymongo import MongoClient

# 🔹 Usa tus credenciales reales aquí
MONGODB_URI = "mongodb+srv://1234:1234@mixify.4va0z.mongodb.net/?retryWrites=true&w=majority&appName=mixifypip"

try:
    client = MongoClient(MONGODB_URI)
    db = client["mixifydb"]  # Nombre de la base de datos
    print("✅ Conexión exitosa a MongoDB")
    
    # Verificar colecciones
    collections = db.list_collection_names()
    print("📂 Colecciones en la BD:", collections)

except Exception as e:
    print("❌ Error de conexión:", e)
