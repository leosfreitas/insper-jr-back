from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from database import user_collection, tokens_collection
from schemas.login import UserLogin 
from fastapi import Header
from utils.hash import verify_password 
from utils.token import create_access_token
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler

router = APIRouter()
scheduler = AsyncIOScheduler()
scheduler_running = False  

async def remove_expired_tokens():
    """
    Remove tokens de acesso expirados.

    Esta função é responsável por deletar tokens armazenados na coleção de tokens que
    já expiraram. A verificação é realizada comparando a data atual com a data de
    expiração dos tokens.

    Retorna:
    - None: Apenas remove os tokens expirados do banco de dados.
    """
    try:
        now = datetime.utcnow()
        result = await tokens_collection.delete_many({"expira_em": {"$lt": now}})
        print(f"Removed {result.deleted_count} expired tokens.")
    except Exception as e:
        print(f"Error removing expired tokens: {str(e)}")

@router.on_event("startup")
async def startup_event():
    """
    Evento de inicialização da aplicação.

    Esta função é chamada quando a aplicação inicia. Ela verifica se o
    agendador de tarefas já está em execução; se não estiver, adiciona
    uma tarefa que executa a função remove_expired_tokens a cada hora.

    Retorna:
    - None: Apenas inicializa o agendador.
    """
    global scheduler_running
    if not scheduler_running: 
        scheduler.add_job(remove_expired_tokens, "interval", hours=1)
        scheduler.start()
        scheduler_running = True  

@router.post("/login")
async def login(user: UserLogin):
    """
    Realiza o login do usuário.

    Esta função autentica o usuário verificando suas credenciais (email e senha).
    Se as credenciais forem válidas, um token de acesso é gerado e armazenado no banco de dados.

    Parâmetros:
    - user: Um objeto do tipo UserLogin que contém as credenciais do usuário.

    Retorna:
    - dict: Um dicionário contendo o token de acesso gerado.
    - HTTPException: Lança uma exceção se o email ou a senha forem inválidos.
    """
    try:
        db_user = await user_collection.find_one({"email": user.email})
        if not db_user:
            raise HTTPException(status_code=401, detail="Invalid email or password")

        password_match = verify_password(user.password, db_user["password"])

        if password_match:
            expires = timedelta(days=10)
            access_token = create_access_token(data={"sub": str(db_user["_id"])}, expires_delta=expires)

            expira_em = datetime.utcnow() + expires
            await tokens_collection.insert_one({
                "email": user.email,
                "token": access_token,
                "permissao": db_user["permissao"],
                "expira_em": expira_em
            })

            return {"token": access_token}
        else:
            raise HTTPException(status_code=401, detail="Invalid email or password")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/logout")
async def logout(authorization: str = Header(...)): 
    """
    Realiza o logout do usuário.

    Esta função remove o token de acesso da coleção de tokens, efetivamente
    desconectando o usuário. O token é passado no cabeçalho de autorização.

    Parâmetros:
    - authorization: O cabeçalho de autorização que contém o token Bearer.

    Retorna:
    - JSONResponse: Uma resposta JSON confirmando que o logout foi realizado.
    - HTTPException: Lança uma exceção se o token for inválido ou não estiver presente.
    """
    try:
        token = authorization.split(" ")[1]  
        
        user = await tokens_collection.find_one({"token": token})
        if user:
            await tokens_collection.delete_one({"token": token})
            return JSONResponse(content={"message": "Logout successfully"}, status_code=200)
        else:
            raise HTTPException(status_code=401, detail="Invalid token")
    except IndexError:
        raise HTTPException(status_code=400, detail="Authorization header must be Bearer token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/verify-token")
async def verify_token(authorization: str = Header(...)):
    """
    Verifica a validade do token de acesso.

    Esta função verifica se o token passado no cabeçalho de autorização está presente na coleção
    de tokens. Se o token for encontrado, significa que o usuário está autenticado.

    Parâmetros:
    - authorization: O cabeçalho de autorização que contém o token Bearer.

    Retorna:
    - JSONResponse: Uma resposta JSON confirmando que o usuário foi encontrado ou não.
    - HTTPException: Lança uma exceção se o token não estiver presente ou houver um erro de cabeçalho.
    """
    try:
        token = authorization.split(" ")[1]  
        user = await tokens_collection.find_one({'token': token })
        if user:
            return JSONResponse(content={"message": "Usuário encontrado"}, status_code=200)
        else:
            return JSONResponse(content={"message": "Usuário não encontrado"}, status_code=404)
    except IndexError:
        raise HTTPException(status_code=400, detail="Authorization header must be Bearer token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
