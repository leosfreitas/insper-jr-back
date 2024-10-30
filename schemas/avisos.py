# Importação da classe BaseModel da biblioteca Pydantic para validação de dados
from pydantic import BaseModel  # BaseModel para criar schemas de validação

class AvisoCreate(BaseModel):
    """
    Schema para a criação de um novo aviso.

    Atributos:
        titulo (str): O título do aviso.
        mensagem (str): O conteúdo da mensagem do aviso.
        tipo (str): O tipo do aviso (ex: "informativo", "urgente").
    """
    titulo: str  # Título do aviso
    mensagem: str  # Mensagem do aviso
    tipo: str  # Tipo do aviso
