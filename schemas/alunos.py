from pydantic import BaseModel, EmailStr

class AlunoCreate(BaseModel):
    email: EmailStr
    cpf: str
    nome: str
    password : str
    sala: str

class AlunoResponse(BaseModel):
    id: str
    email: EmailStr
    cpf: str
    nome: str
    password : str
    sala: str