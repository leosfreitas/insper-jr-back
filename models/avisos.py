from pydantic import BaseModel

class Aviso(BaseModel):
    titulo: str
    mensagem: str
    tipo: str