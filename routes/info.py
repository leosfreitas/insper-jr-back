from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from utils.token import verify_token
from database import user_collection
from bson import ObjectId

router = APIRouter()

@router.get("/getNumeroAlunosPresencial")
async def get_numero_alunos_presencial(user: dict = Depends(verify_token)):
    """
    Obtém o número de alunos matriculados na modalidade presencial.

    - **Requisitos**: O usuário deve ter permissão de 'GESTAO'.
    - **Parâmetros**:
        - user (dict): Dicionário contendo informações do usuário autenticado.
    - **Retorno**:
        - JSONResponse: Retorna o número total de alunos presenciais como JSON.
    - **Exceções**:
        - HTTPException: Lança uma exceção 401 se o usuário não tiver permissão, ou uma exceção 400 em caso de erro.
    """
    try:
        email = user['email']
        user = await user_collection.find_one({'email': email})
        permission = user['permissao']
        if permission == 'GESTAO':
            lista_alunos = await user_collection.find({'permissao': 'ALUNO', 'sala': 'Presencial'}).to_list(length=1000)
            numero_alunos = len(lista_alunos)
            return JSONResponse(content=numero_alunos, status_code=200)
        else:
            raise HTTPException(status_code=401, detail='Não é possível fazer a requisição')
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/getNumeroAlunosOnline")
async def get_numero_alunos_online(user: dict = Depends(verify_token)):
    """
    Obtém o número de alunos matriculados na modalidade online.

    - **Requisitos**: O usuário deve ter permissão de 'GESTAO'.
    - **Parâmetros**:
        - user (dict): Dicionário contendo informações do usuário autenticado.
    - **Retorno**:
        - JSONResponse: Retorna o número total de alunos online como JSON.
    - **Exceções**:
        - HTTPException: Lança uma exceção 401 se o usuário não tiver permissão, ou uma exceção 400 em caso de erro.
    """
    try:
        email = user['email']
        user = await user_collection.find_one({'email': email})
        permission = user['permissao']
        if permission == 'GESTAO':
            lista_alunos = await user_collection.find({'permissao': 'ALUNO', 'sala': 'Online'}).to_list(length=1000)
            numero_alunos = len(lista_alunos)
            return JSONResponse(content=numero_alunos, status_code=200)
        else:
            raise HTTPException(status_code=401, detail='Não é possível fazer a requisição')
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/getNumeroProfessores")
async def get_numero_professores(user: dict = Depends(verify_token)):
    """
    Obtém o número total de professores cadastrados.

    - **Requisitos**: O usuário deve ter permissão de 'GESTAO'.
    - **Parâmetros**:
        - user (dict): Dicionário contendo informações do usuário autenticado.
    - **Retorno**:
        - JSONResponse: Retorna o número total de professores como JSON.
    - **Exceções**:
        - HTTPException: Lança uma exceção 401 se o usuário não tiver permissão, ou uma exceção 400 em caso de erro.
    """
    try:
        email = user['email']
        user = await user_collection.find_one({'email': email})
        permission = user['permissao']
        if permission == 'GESTAO':
            lista_professores = await user_collection.find({'permissao': 'PROFESSOR'}).to_list(length=1000)
            numero_professores = len(lista_professores)
            return JSONResponse(content=numero_professores, status_code=200)
        else:
            raise HTTPException(status_code=401, detail='Não é possível fazer a requisição')
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/getNumeroGestao")
async def get_numero_gestao(user: dict = Depends(verify_token)):
    """
    Obtém o número total de usuários com permissão de gestão.

    - **Requisitos**: O usuário deve ter permissão de 'GESTAO'.
    - **Parâmetros**:
        - user (dict): Dicionário contendo informações do usuário autenticado.
    - **Retorno**:
        - JSONResponse: Retorna o número total de usuários de gestão como JSON.
    - **Exceções**:
        - HTTPException: Lança uma exceção 401 se o usuário não tiver permissão, ou uma exceção 400 em caso de erro.
    """
    try:
        email = user['email']
        user = await user_collection.find_one({'email': email})
        permission = user['permissao']
        if permission == 'GESTAO':
            lista_gestao = await user_collection.find({'permissao': 'GESTAO'}).to_list(length=1000)
            numero_gestao = len(lista_gestao)
            return JSONResponse(content=numero_gestao, status_code=200)
        else:
            raise HTTPException(status_code=401, detail='Não é possível fazer a requisição')
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/getNotasPresencial")
async def get_notas_presencial(user: dict = Depends(verify_token)):
    """
    Obtém as notas dos alunos matriculados na modalidade presencial.

    - **Requisitos**: O usuário deve ter permissão de 'GESTAO'.
    - **Parâmetros**:
        - user (dict): Dicionário contendo informações do usuário autenticado.
    - **Retorno**:
        - JSONResponse: Retorna as notas dos alunos presenciais como JSON.
    - **Exceções**:
        - HTTPException: Lança uma exceção 401 se o usuário não tiver permissão, ou uma exceção 400 em caso de erro.
    """
    try:
        email = user['email']
        user = await user_collection.find_one({'email': email})
        permission = user.get('permissao')
        
        if permission == 'GESTAO':
            lista_presencial = await user_collection.find({'permissao': 'ALUNO', 'sala': 'Presencial'}).to_list(length=1000)
            notas_presencial = [aluno.get('notas', {}) for aluno in lista_presencial]
            
            return JSONResponse(content=notas_presencial, status_code=200)
        else:
            raise HTTPException(status_code=401, detail='Não é possível fazer a requisição')
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/getNotasOnline")
async def get_notas_online(user: dict = Depends(verify_token)):
    """
    Obtém as notas dos alunos matriculados na modalidade online.

    - **Requisitos**: O usuário deve ter permissão de 'GESTAO'.
    - **Parâmetros**:
        - user (dict): Dicionário contendo informações do usuário autenticado.
    - **Retorno**:
        - JSONResponse: Retorna as notas dos alunos online como JSON.
    - **Exceções**:
        - HTTPException: Lança uma exceção 401 se o usuário não tiver permissão, ou uma exceção 400 em caso de erro.
    """
    try:
        email = user['email']
        user = await user_collection.find_one({'email': email})
        permission = user.get('permissao')
        
        if permission == 'GESTAO':
            lista_online = await user_collection.find({'permissao': 'ALUNO', 'sala': 'Online'}).to_list(length=1000)
            notas_online = [aluno.get('notas', {}) for aluno in lista_online]
            
            return JSONResponse(content=notas_online, status_code=200)
        else:
            raise HTTPException(status_code=401, detail='Não é possível fazer a requisição')
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/getNotasGerais")
async def get_notas_gerais(user: dict = Depends(verify_token)):
    """
    Obtém as notas de todos os alunos cadastrados.

    - **Requisitos**: O usuário deve ter permissão de 'GESTAO'.
    - **Parâmetros**:
        - user (dict): Dicionário contendo informações do usuário autenticado.
    - **Retorno**:
        - JSONResponse: Retorna as notas de todos os alunos como JSON.
    - **Exceções**:
        - HTTPException: Lança uma exceção 401 se o usuário não tiver permissão, ou uma exceção 400 em caso de erro.
    """
    try:
        email = user['email']
        user = await user_collection.find_one({'email': email})
        permission = user.get('permissao')
        
        if permission == 'GESTAO':
            lista_geral = await user_collection.find({'permissao': 'ALUNO'}).to_list(length=1000)
            notas_geral = [aluno.get('notas', {}) for aluno in lista_geral]
            
            return JSONResponse(content=notas_geral, status_code=200)
        else:
            raise HTTPException(status_code=401, detail='Não é possível fazer a requisição')
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
