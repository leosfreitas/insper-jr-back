from database import grade_collection, user_collection
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from schemas.grade import GradeCreate
from utils.token import verify_token
from bson import ObjectId

router = APIRouter()

@router.get("/get")
async def get_grades(user: dict = Depends(verify_token)):
    """
    Obtém todas as grades disponíveis.

    Essa função busca grades na coleção `grade_collection`. O acesso é permitido
    apenas a usuários com permissão de 'GESTAO' ou 'PROFESSOR'.

    Args:
        user (dict): O dicionário do usuário, obtido através da verificação do token.

    Returns:
        JSONResponse: Um JSON contendo uma lista de grades ou uma mensagem de erro.
    """
    try:
        email = user['email']
        user = await user_collection.find_one({'email': email})
        permission = user['permissao']
        if permission == 'GESTAO' or permission == 'PROFESSOR':
            grades = await grade_collection.find().to_list(length=1000)
            grades = [{**grade, "_id": str(grade["_id"])} for grade in grades]  
            if not grades:
                return JSONResponse(content={'message': 'Grade não encontrada'}, status_code=200)
            return JSONResponse(content={'grades': grades}, status_code=200)
        else:
            raise HTTPException(status_code=401, detail='Não é possível fazer a requisição')
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.delete("/delete/{id}")
async def delete_grade(id: str, user: dict = Depends(verify_token)):
    """
    Remove uma grade específica pelo ID.

    Essa função exclui uma grade da coleção `grade_collection` com base no ID
    fornecido. O acesso é permitido apenas a usuários com permissão de 'GESTAO'.

    Args:
        id (str): O ID da grade a ser excluída.
        user (dict): O dicionário do usuário, obtido através da verificação do token.

    Returns:
        JSONResponse: Um JSON confirmando a exclusão ou uma mensagem de erro.
    """
    try:
        email = user['email']
        user = await user_collection.find_one({'email': email})
        permission = user['permissao']

        if permission == 'GESTAO':
            await grade_collection.delete_one({'_id': ObjectId(id)})
            return JSONResponse(content={'message': 'Grade deletada com sucesso'}, status_code=200)
        else:
            raise HTTPException(status_code=401, detail='Não é possível fazer a requisição')
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/create")
async def post_grade(grade: GradeCreate, user: dict = Depends(verify_token)):
    """
    Cria uma nova grade.

    Essa função insere uma nova grade na coleção `grade_collection` utilizando
    os dados fornecidos no corpo da requisição. O acesso é permitido apenas a
    usuários com permissão de 'GESTAO'.

    Args:
        grade (GradeCreate): Os dados da grade a serem criados.
        user (dict): O dicionário do usuário, obtido através da verificação do token.

    Returns:
        JSONResponse: Um JSON confirmando a criação da grade ou uma mensagem de erro.
    """
    try:
        email = user['email']
        user = await user_collection.find_one({'email': email})
        permission = user['permissao']
        if permission == 'GESTAO':
            await grade_collection.insert_one({
                'data': grade.data,
                'horario': grade.horario,
                'materia': grade.materia,
                'local': grade.local,
                'topico': grade.topico,
                'professor': grade.professor,    
                'sala': grade.sala,            
            })
            return JSONResponse(content={'message': 'Grade criada com sucesso'}, status_code=200)
        else:
            raise HTTPException(status_code=401, detail='Não é possível fazer a requisição')
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{data}")
async def get_grade(data: str, user: dict = Depends(verify_token)):
    """
    Obtém grades filtradas por data e sala.

    Essa função busca grades na coleção `grade_collection` filtradas pela data
    fornecida e pela sala do usuário. O acesso é permitido apenas a usuários com
    permissão de 'GESTAO' ou 'PROFESSOR'. Caso contrário, o acesso é limitado
    aos alunos que pertencem à sala do usuário.

    Args:
        data (str): A data das grades a serem buscadas.
        user (dict): O dicionário do usuário, obtido através da verificação do token.

    Returns:
        JSONResponse: Um JSON contendo as grades filtradas ou uma mensagem de erro.
    """
    try:
        email = user['email']
        user = await user_collection.find_one({'email': email})
        permission = user['permissao']
        
        if permission == 'GESTAO' or permission == 'PROFESSOR':
            grades = await grade_collection.find().to_list(length=1000)
            grades = [{**grade, "_id": str(grade["_id"])} for grade in grades]  
            if not grades:
                return JSONResponse(content={'message': 'Grade não encontrada'}, status_code=200)
            
            return JSONResponse(content=grades, status_code=200)
        
        sala = user['sala']
        grades = await grade_collection.find({'data': data, 'sala': sala}).to_list(length=1000)  
        grades = [{**grade, "_id": str(grade["_id"])} for grade in grades]  

        if not grades:
            return JSONResponse(content={'message': 'Grade não encontrada'}, status_code=200)

        return JSONResponse(content=grades, status_code=200)
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
