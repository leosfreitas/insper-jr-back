from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    nome: str
    cpf: str
    email: EmailStr
    permissao: str
    password: str

class UserResponse(BaseModel):
    id: str
    nome: str
    cpf: str
    email: EmailStr
    permissao: str

class UserEdit(BaseModel):
    nome: str
    cpf: str
    email: EmailStr
    permissao: str