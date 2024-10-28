from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.users import router as user_router
from routes.auth import router as auth_router 
from routes.avisos import router as avisos_router
from routes.alunos import router as alunos_router
from routes.grade import router as grade_router
from routes.info import router as info_router

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])  
app.include_router(alunos_router, prefix="/alunos", tags=["alunos"])
app.include_router(avisos_router, prefix="/avisos", tags=["avisos"])
app.include_router(grade_router, prefix="/grade", tags=["grade"])
app.include_router(info_router, prefix="/info", tags=["info"])

@app.get("/")


async def root():
    return {"message": "API is running!"}
