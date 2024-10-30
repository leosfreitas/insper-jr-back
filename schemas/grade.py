# Importação da classe BaseModel da biblioteca Pydantic para validação de dados
from pydantic import BaseModel  # BaseModel para criar schemas de validação

class GradeCreate(BaseModel):
    """
    Schema para a criação de uma nova entrada na grade horária.

    Atributos:
        data (str): A data da aula, deve ser uma string representando a data (formato sugerido: YYYY-MM-DD).
        horario (str): O horário da aula, deve ser uma string representando o horário (formato sugerido: HH:MM).
        materia (str): O nome da matéria da aula.
        local (str): O local onde a aula será realizada.
        topico (str): O tópico a ser abordado na aula.
        professor (str): O nome do professor responsável pela aula.
        sala (str): O número ou nome da sala onde a aula será ministrada.
    """
    data: str  # Data da aula
    horario: str  # Horário da aula
    materia: str  # Matéria da aula
    local: str  # Local da aula
    topico: str  # Tópico da aula
    professor: str  # Nome do professor
    sala: str  # Sala onde a aula será realizada
