from bson import ObjectId
from pydantic import BaseModel, EmailStr
from typing import Optional

class Aluno(BaseModel):
    id: Optional[str]
    email: EmailStr
    cpf: str
    nome: str
    notas: dict 
    sala: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
