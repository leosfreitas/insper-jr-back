from pydantic import BaseModel

class AvisoCreate(BaseModel):
    titulo: str
    mensagem: str
    tipo: str