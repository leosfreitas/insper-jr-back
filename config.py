import pymongo
import certifi
import datetime

class CONFIG:
    JWT_SECRET_KEY = 'ps-insper-jr'
    JWT_VERIFY_EXPIRATION = True
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=10)
    MONGO_URI = 'mongodb+srv://admin:admin@cluster0.jko03zk.mongodb.net/'

client_mongo = pymongo.MongoClient(CONFIG.MONGO_URI, tlsCAFile=certifi.where())
users = client_mongo.insperjr.users
alunos = client_mongo.insperjr.alunos
tokens = client_mongo.insperjr.tokens
avisos = client_mongo.insperjr.avisos