from schemas.user import UserCreate, UserResponse, UserEdit 
from database import user_collection, tokens_collection
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from utils.hash import hash_password
from utils.token import verify_token
from bson import ObjectId
import resend

resend.api_key = "re_BCc8xFut_GGA9FjBGEwojKF6SsLHBYdCp"

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  

@router.post("/register", response_model=UserResponse)
async def register(user_create: UserCreate, user: dict = Depends(verify_token)):
    try:
        email = user["email"]
        user_data = await user_collection.find_one({"email": email})
        permission = user_data["permissao"]

        if permission != "GESTAO":
            raise HTTPException(status_code=401, detail="Permissão negada")
        
        user_dict = user_create.dict()
        if await user_collection.find_one({"email": user_dict["email"]}):
            raise HTTPException(status_code=400, detail="Email já registrado")
        
        email = {
                "from": "Cursinho Insper <gerenciamento@cursinho.insper.com>",
                "to": user_dict["email"],
                "subject": "Confirmação de cadastro",
                "text": f"Você está recebendo esse email porque você foi cadastrado na plataforma do Cursinho Insper! Aqui está a sua senha: {user_dict['password']}"
            }
        
        resend.Emails.send(email)

        user_dict["password"] = hash_password(user_dict["password"])
        result = await user_collection.insert_one(user_dict)
        user_dict["_id"] = str(result.inserted_id)
        return JSONResponse(content={"message": "Usuário criado com sucesso", "user": user_dict}, status_code=201)
    
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

@router.get("/get")
async def get_users(user: dict = Depends(verify_token)):
    try: 
        email = user["email"]
        user = await user_collection.find_one({"email": email})
        permission = user["permissao"]

        if permission == "GESTAO":
            users = await user_collection.find({"permissao": {"$in": ["GESTAO", "PROFESSOR"]}}).to_list(length=1000)
            users = [{**user, "_id": str(user["_id"])} for user in users]
            return JSONResponse(content={"users": users}, status_code=200)
        else:
            raise HTTPException(status_code=401, detail="Não é possível fazer a requisição")
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.get("/get/{user_id}")
async def get_user(user_id: str, user: dict = Depends(verify_token)):
    try:
        email = user["email"]
        user_data = await user_collection.find_one({"email": email})
        permission = user_data["permissao"]

        if permission != "GESTAO":
            raise HTTPException(status_code=401, detail="Permissão negada")

        user_id_object = ObjectId(user_id)
        user = await user_collection.find_one({"_id": user_id_object})

        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        user["_id"] = str(user["_id"])
        return JSONResponse(content=user, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete/{user_id}")
async def delete_user(user_id: str, user: dict = Depends(verify_token)):
    try:
        email = user["email"]
        user_data = await user_collection.find_one({"email": email})
        permission = user_data["permissao"]

        if permission != "GESTAO":
            raise HTTPException(status_code=401, detail="Permissão negada")

        user_id_object = ObjectId(user_id)
        user = await user_collection.find_one({"_id": user_id_object})  

        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        await user_collection.delete_one({"_id": user_id_object})
        return JSONResponse(content={"message": "Usuário deletado com sucesso"}, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/update/{user_id}", response_model=dict)
async def update_aluno(user_id: str, user_edit: UserEdit, user: dict = Depends(verify_token)):
    try:
        email = user['email']
        user_data = await user_collection.find_one({'email': email})
        permission = user_data['permissao']

        user_id_object = ObjectId(user_id)
        existing_user = await user_collection.find_one({'_id': user_id_object})

        if permission != "GESTAO":
            raise HTTPException(status_code=401, detail="Permissão negada")

        if user_edit.email != existing_user['email'] and await user_collection.find_one({"email": user_edit.email}):
            raise HTTPException(status_code=400, detail="Email já registrado")
        
        if existing_user is None:
            raise HTTPException(status_code=404, detail="Aluno não encontrado")
        
        updated_fields = {}

        if user_edit.nome and user_edit.nome != existing_user['nome']:
            updated_fields["nome"] = user_edit.nome

        if user_edit.email and user_edit.email != existing_user['email']:
            updated_fields["email"] = user_edit.email 

        if user_edit.permissao and user_edit.permissao != existing_user['permissao']:
            updated_fields["permissao"] = user_edit.permissao

        if not updated_fields:
            raise HTTPException(status_code=400, detail="Nenhuma alteração encontrada")

        await user_collection.update_one({'_id': user_id_object}, {"$set": updated_fields})

        return {"detail": "Aluno atualizado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))