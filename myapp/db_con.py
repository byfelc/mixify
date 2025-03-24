from pymongo import MongoClient

MONGO_URI = "mongodb+srv://iracheta602:Mixify1234@mixify.4va0z.mongodb.net/?retryWrites=true&w=majority&appName=mixify"

client = MongoClient(MONGO_URI)
db = client['mixifydb']  # ✅ Aquí ya es "mixifydb"

usuarios_collection = db['usuarios']
historial_collection = db['historial_bebidas']  # si ya tienes esta colección
ingredientes_collection = db['estado_contenedores']
