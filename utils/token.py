from datetime import datetime, timedelta
from fastapi import HTTPException, Header
from database import tokens_collection
from jose import JWTError, jwt

SECRET_KEY = "ps-insper-jr"  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 14400 # 10 days

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def verify_token(authorization: str = Header(...)):
    try:
        token = authorization.split(" ")[1]  
        user = await tokens_collection.find_one({'token': token})
        if not user:
            raise HTTPException(status_code=401, detail='Token inválido ou não encontrado')
        return user
    except IndexError:
        raise HTTPException(status_code=400, detail='Authorization header must be Bearer token')
