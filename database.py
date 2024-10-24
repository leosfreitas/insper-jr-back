from motor.motor_asyncio import AsyncIOMotorClient
from bson.objectid import ObjectId
import os

MONGO_DETAILS = os.getenv("MONGO_DETAILS", "mongodb+srv://admin:admin@cluster0.jko03zk.mongodb.net/") 

client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.insperjr  
user_collection = database.get_collection("users") 
tokens_collection = database.get_collection("tokens")
avisos_collection = database.get_collection("avisos")
alunos_collection = database.get_collection("alunos")

async def connect_to_mongo():
    try:
        client.admin.command('ping')
        print("Conexão com o MongoDB estabelecida com sucesso!")
    except Exception as e:
        print(f"Erro ao conectar ao MongoDB: {e}")