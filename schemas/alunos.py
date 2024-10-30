# Importação da classe BaseModel e EmailStr da biblioteca Pydantic para validação de dados
from pydantic import BaseModel, EmailStr  # BaseModel para criar schemas de validação, EmailStr para validação de e-mails

class AlunoCreate(BaseModel):
    """
    Schema para a criação de um novo aluno.

    Atributos:
        email (EmailStr): O e-mail do aluno, deve ser um e-mail válido.
        cpf (str): O CPF do aluno, deve ser uma string representando o número.
        nome (str): O nome completo do aluno.
        password (str): A senha do aluno, deve ser armazenada de forma segura.
        sala (str): A sala onde o aluno está matriculado.
    """
    email: EmailStr  # E-mail do aluno
    cpf: str  # CPF do aluno
    nome: str  # Nome do aluno
    password: str  # Senha do aluno
    sala: str  # Sala do aluno


class AlunoEdit(BaseModel):
    """
    Schema para edição das informações de um aluno existente.

    Atributos:
        email (EmailStr): O e-mail do aluno, deve ser um e-mail válido.
        nome (str): O nome completo do aluno.
        sala (str): A sala onde o aluno está matriculado.
    """
    email: EmailStr  # E-mail do aluno
    nome: str  # Nome do aluno
    sala: str  # Sala do aluno


class AlunoResponse(BaseModel):
    """
    Schema para a resposta ao consultar um aluno.

    Atributos:
        id (str): O identificador único do aluno.
        email (EmailStr): O e-mail do aluno, deve ser um e-mail válido.
        cpf (str): O CPF do aluno, deve ser uma string representando o número.
        nome (str): O nome completo do aluno.
        sala (str): A sala onde o aluno está matriculado.
        notas (dict): Um dicionário contendo as notas do aluno.
    """
    id: str  # Identificador único do aluno
    email: EmailStr  # E-mail do aluno
    cpf: str  # CPF do aluno
    nome: str  # Nome do aluno
    sala: str  # Sala do aluno
    notas: dict  # Notas do aluno


class NotaAdd(BaseModel):
    """
    Schema para adicionar uma nota a um aluno.

    Atributos:
        avaliacao (str): O nome da avaliação.
        nota (str): A nota a ser adicionada.
    """
    avaliacao: str  # Nome da avaliação
    nota: str  # Nota a ser adicionada


class NotaRemove(BaseModel):
    """
    Schema para remover uma nota de um aluno.

    Atributos:
        avaliacao (str): O nome da avaliação que terá a nota removida.
    """
    avaliacao: str  # Nome da avaliação
