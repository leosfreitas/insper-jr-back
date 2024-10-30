# Importação da classe BaseModel e EmailStr da biblioteca Pydantic para validação de dados
from pydantic import BaseModel, EmailStr  # BaseModel para criar schemas de validação, EmailStr para validação de e-mails

class UserCreate(BaseModel):
    """
    Schema para criação de um novo usuário.

    Atributos:
        nome (str): O nome completo do usuário.
        cpf (str): O CPF do usuário, deve ser uma string representando o número.
        email (EmailStr): O e-mail do usuário, deve ser um e-mail válido.
        permissao (str): O nível de permissão do usuário (ex: aluno, gestao, professor).
        password (str): A senha do usuário, deve ser armazenada de forma segura.
    """
    nome: str
    cpf: str
    email: EmailStr
    permissao: str
    password: str


class UserResponse(BaseModel):
    """
    Schema para a resposta ao consultar um usuário.

    Atributos:
        id (str): O identificador único do usuário.
        nome (str): O nome completo do usuário.
        cpf (str): O CPF do usuário, deve ser uma string representando o número.
        email (EmailStr): O e-mail do usuário, deve ser um e-mail válido.
        permissao (str): O nível de permissão do usuário (ex: aluno, gestao, professor).
    """
    id: str
    nome: str
    cpf: str
    email: EmailStr
    permissao: str


class UserEdit(BaseModel):
    """
    Schema para edição de um usuário existente.

    Atributos:
        nome (str): O nome completo do usuário.
        cpf (str): O CPF do usuário, deve ser uma string representando o número.
        email (EmailStr): O e-mail do usuário, deve ser um e-mail válido.
        permissao (str): O nível de permissão do usuário (ex: aluno, gestao, professor).
    """
    nome: str
    cpf: str
    email: EmailStr
    permissao: str
