# Importação das bibliotecas necessárias
from datetime import datetime, timedelta  # Para manipulação de datas e horas
from fastapi import HTTPException, Header  # Exceções HTTP e manipulação de headers no FastAPI
from database import tokens_collection  # Importação da coleção de tokens do banco de dados
from jose import JWTError, jwt  # Biblioteca para criação e verificação de JSON Web Tokens (JWT)

# Definições de constantes para o token
SECRET_KEY = "ps-insper-jr"  # Chave secreta utilizada para codificação do JWT
ALGORITHM = "HS256"  # Algoritmo de codificação do JWT
ACCESS_TOKEN_EXPIRE_MINUTES = 14400  # Duração do token de acesso em minutos (10 dias)

def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Cria um token de acesso JWT.

    Args:
        data (dict): Dados que serão codificados no token.
        expires_delta (timedelta, optional): Duração adicional para a expiração do token.

    Returns:
        str: O token de acesso codificado em formato JWT.
    """
    to_encode = data.copy()  # Cria uma cópia dos dados fornecidos
    if expires_delta:
        expire = datetime.utcnow() + expires_delta  # Define a expiração com base no delta fornecido
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)  # Define a expiração padrão
    to_encode.update({"exp": expire})  # Adiciona a data de expiração ao payload do token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # Codifica o token
    return encoded_jwt  # Retorna o token codificado


async def verify_token(authorization: str = Header(...)):
    """
    Verifica a validade de um token de acesso.

    Args:
        authorization (str): O header de autorização contendo o token.

    Raises:
        HTTPException: Se o token é inválido ou não encontrado, ou se o formato do header está incorreto.

    Returns:
        dict: Os dados do usuário associados ao token, se válido.
    """
    try:
        token = authorization.split(" ")[1]  # Extrai o token do header de autorização
        user = await tokens_collection.find_one({'token': token})  # Busca o token na coleção
        if not user:
            raise HTTPException(status_code=401, detail='Token inválido ou não encontrado')  # Token não encontrado
        return user  # Retorna os dados do usuário associado ao token
    except IndexError:
        # Lança uma exceção se o header de autorização não contiver um token Bearer
        raise HTTPException(status_code=400, detail='Authorization header must be Bearer token')
