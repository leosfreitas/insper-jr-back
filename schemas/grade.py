from pydantic import BaseModel

class GradeCreate(BaseModel):
    data: str
    horario: str
    materia: str
    local: str
    topico: str
    professor: str 
    sala: str

