# Importação da biblioteca bcrypt para hashing de senhas
import bcrypt  # Para criptografia de senhas

def hash_password(password: str) -> str:
    """
    Criptografa uma senha usando o algoritmo bcrypt.

    Args:
        password (str): A senha a ser criptografada.

    Returns:
        str: A senha criptografada em formato de string.
    """
    salt = bcrypt.gensalt()  # Gera um salt aleatório para a criptografia
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)  # Criptografa a senha com o salt gerado
    return hashed_password.decode('utf-8')  # Retorna a senha criptografada como string


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se uma senha em texto plano corresponde a uma senha criptografada.

    Args:
        plain_password (str): A senha em texto plano a ser verificada.
        hashed_password (str): A senha criptografada para comparação.

    Returns:
        bool: True se a senha em texto plano corresponder à senha criptografada, False caso contrário.
    """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))  # Verifica a correspondência
