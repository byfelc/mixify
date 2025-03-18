from pymongo import MongoClient

MONGO_URI = "mongodb+srv://iracheta602:Mixify1234@mixify.4va0z.mongodb.net/?retryWrites=true&w=majority&appName=mixify"

client = MongoClient(MONGO_URI)
db = client['mixify']  # Aquí debes poner el nombre de tu base (¿se llama también mixify o diferente?)
usuarios_collection = db['usuarios']  # Ajusta si tu colección se llama diferente
