from database import grade_collection, user_collection
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from schemas.grade import GradeCreate
from utils.token import verify_token

router = APIRouter()

@router.post("/create")
async def post_grade(grade: GradeCreate, user: dict = Depends(verify_token)):
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
    try:
        email = user['email']
        user = await user_collection.find_one({'email': email})
        permission = user['permissao']
        
        if permission == 'GESTAO':
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

