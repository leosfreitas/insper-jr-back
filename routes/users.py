from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from database import user_collection, tokens_collection , alunos_collection
from schemas.user import UserCreate, UserResponse  
from utils.hash import hash_password

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate):
    try:
        user_dict = user.dict()
        user_dict["password"] = hash_password(user_dict["password"])
        user_dict["permissao"] = user_dict["permissao"].upper()
        user_dict["nome"] = user_dict["nome"].capitalize()

        if await user_collection.find_one({"email": user_dict["email"]}):
            raise HTTPException(status_code=400, detail="Email já registrado")
        
        new_user = await user_collection.insert_one(user_dict)
        created_user = await user_collection.find_one({"_id": new_user.inserted_id})
        created_user["id"] = str(created_user["_id"])
        del created_user["_id"]
        
        return UserResponse(**created_user)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/permission")
async def get_user_permission(token: str = Depends(oauth2_scheme)):
    try:
        user_token = await tokens_collection.find_one({"token": token})
        if not user_token:
            return JSONResponse(content={"permissao": None}, status_code=200)

        email = user_token["email"]
        user = await user_collection.find_one({"email": email})
        if not user:
            return JSONResponse(content={"permissao": None}, status_code=200)

        permissao = user["permissao"]
        return JSONResponse(content={"permissao": permissao}, status_code=200)

    except Exception as e:
        return JSONResponse(content={"permissao": None}, status_code=500)
