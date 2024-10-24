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
    try:
        now = datetime.utcnow()
        result = await tokens_collection.delete_many({"expira_em": {"$lt": now}})
        print(f"Removed {result.deleted_count} expired tokens.")
    except Exception as e:
        print(f"Error removing expired tokens: {str(e)}")

@router.on_event("startup")
async def startup_event():
    global scheduler_running
    if not scheduler_running: 
        scheduler.add_job(remove_expired_tokens, "interval", hours=1)
        scheduler.start()
        scheduler_running = True  

@router.post("/login")
async def login(user: UserLogin):
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