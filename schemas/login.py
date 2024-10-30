# Importação da classe BaseModel e EmailStr da biblioteca Pydantic para validação de dados
from pydantic import BaseModel, EmailStr  # BaseModel para criar schemas de validação, EmailStr para validação de e-mails

class UserLogin(BaseModel):
    """
    Schema para login de um usuário.

    Atributos:
        email (EmailStr): O e-mail do usuário, deve ser um e-mail válido.
        password (str): A senha do usuário, deve ser armazenada de forma segura.
    """
    email: EmailStr  # E-mail do usuário que está tentando fazer login
    password: str  # Senha do usuário que está tentando fazer login
