# Importação de dependências necessárias para a conexão com o MongoDB
from motor.motor_asyncio import AsyncIOMotorClient  # Cliente assíncrono para conexão com o MongoDB
from bson.objectid import ObjectId  # Classe para manipulação de ObjectId (identificadores únicos do MongoDB)
import os  # Biblioteca para acessar variáveis de ambiente

# Define a URL de conexão com o MongoDB
# A URL padrão é obtida a partir de uma variável de ambiente, ou usa o valor fornecido como fallback
MONGO_DETAILS = os.getenv("MONGO_DETAILS", "mongodb+srv://admin:admin@cluster0.jko03zk.mongodb.net/")

# Criação do cliente de conexão assíncrona com o MongoDB
client = AsyncIOMotorClient(MONGO_DETAILS)

# Referência ao banco de dados utilizado (neste caso, 'insperjr')
database = client.insperjr

# Criação de referências para as coleções dentro do banco de dados 'insperjr'
user_collection = database.get_collection("users")  # Coleção que armazena dados de usuários
tokens_collection = database.get_collection("tokens")  # Coleção para armazenar tokens de autenticação
avisos_collection = database.get_collection("avisos")  # Coleção para armazenar avisos
grade_collection = database.get_collection("grade")  # Coleção para armazenar dados relacionados à grade

async def connect_to_mongo():
    """
    Função assíncrona para testar a conexão com o MongoDB.
    Envia um comando 'ping' para o servidor do MongoDB e imprime o status da conexão.
    
    Em caso de sucesso, exibe uma mensagem indicando que a conexão foi bem-sucedida.
    Em caso de erro, exibe uma mensagem de erro com os detalhes da exceção.
    """
    try:
        client.admin.command('ping')  # Envia um comando 'ping' para verificar a conectividade
        print("Conexão com o MongoDB estabelecida com sucesso!")
    except Exception as e:
        print(f"Erro ao conectar ao MongoDB: {e}")  # Exibe o erro em caso de falha
