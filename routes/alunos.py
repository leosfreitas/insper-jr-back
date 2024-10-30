from schemas.alunos import AlunoCreate, AlunoResponse, AlunoEdit, NotaAdd, NotaRemove
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from database import user_collection
from utils.token import verify_token
from utils.hash import hash_password
from utils.mail import send_email

router = APIRouter()

@router.post("/create", response_model=dict)
async def create_aluno(aluno: AlunoCreate, user: dict = Depends(verify_token)):
    """
    Cria um novo aluno no sistema.

    Parâmetros:
    - aluno: Dados do aluno a serem criados, deve ser do tipo AlunoCreate.
    - user: Usuário autenticado que faz a requisição.

    Retorno:
    - Mensagem de sucesso e ID do aluno criado.

    Exceções:
    - HTTPException(401): Usuário não encontrado ou permissão negada.
    - HTTPException(400): CPF ou email já registrados.
    - HTTPException(500): Erro interno ao criar o aluno.
    """
    try:
        email = user['email']
        user_data = await user_collection.find_one({'email': email})
        
        if user_data is None:
            raise HTTPException(status_code=401, detail="Usuário não encontrado")
        
        permission = user_data['permissao']
        
        if permission != "GESTAO":
            raise HTTPException(status_code=401, detail="Permissão negada")

        existing_aluno = await user_collection.find_one({'cpf': aluno.cpf})
        if existing_aluno:
            raise HTTPException(status_code=400, detail="CPF já está registrado")

        aluno_dict = aluno.dict()  
        aluno_dict["permissao"] = "ALUNO"
        aluno_dict["notas"] = {}
        if await user_collection.find_one({"email": aluno_dict["email"]}):
            raise HTTPException(status_code=400, detail="Email já registrado")

        send_email(aluno_dict["password"], aluno_dict["email"])

        aluno_dict["password"] = hash_password(aluno_dict["password"])
        
        result = await user_collection.insert_one(aluno_dict)

        return JSONResponse(content={"message": "Aluno criado com sucesso", "id": str(result.inserted_id)}, status_code=201)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.put("/update/{cpf}", response_model=dict)
async def update_aluno(cpf: str, aluno: AlunoEdit, user: dict = Depends(verify_token)):
    """
    Atualiza os dados de um aluno existente.

    Parâmetros:
    - cpf: CPF do aluno a ser atualizado.
    - aluno: Novos dados do aluno, deve ser do tipo AlunoEdit.
    - user: Usuário autenticado que faz a requisição.

    Retorno:
    - Mensagem de sucesso indicando que o aluno foi atualizado.

    Exceções:
    - HTTPException(401): Permissão negada.
    - HTTPException(400): Email já registrado ou nenhuma alteração encontrada.
    - HTTPException(404): Aluno não encontrado.
    - HTTPException(500): Erro interno ao atualizar o aluno.
    """
    try:
        email = user['email']
        user_data = await user_collection.find_one({'email': email})
        permission = user_data['permissao']
        existing_aluno = await user_collection.find_one({'cpf': cpf})

        if permission != "GESTAO":
            raise HTTPException(status_code=401, detail="Permissão negada")

        if aluno.email != existing_aluno['email'] and await user_collection.find_one({"email": aluno.email}):
            raise HTTPException(status_code=400, detail="Email já registrado")
        
        if existing_aluno is None:
            raise HTTPException(status_code=404, detail="Aluno não encontrado")
        
        updated_fields = {}

        if aluno.nome and aluno.nome != existing_aluno['nome']:
            updated_fields["nome"] = aluno.nome

        if aluno.email and aluno.email != existing_aluno['email']:
            updated_fields["email"] = aluno.email 

        if aluno.sala and aluno.sala != existing_aluno['sala']:
            updated_fields["sala"] = aluno.sala

        if not updated_fields:
            raise HTTPException(status_code=400, detail="Nenhuma alteração encontrada")

        await user_collection.update_one({'cpf': cpf}, {"$set": updated_fields})

        return {"detail": "Aluno atualizado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    
@router.delete("/delete/{cpf}", response_model=dict)
async def delete_aluno(cpf: str, user: dict = Depends(verify_token)):
    """
    Remove um aluno do sistema.

    Parâmetros:
    - cpf: CPF do aluno a ser deletado.
    - user: Usuário autenticado que faz a requisição.

    Retorno:
    - Mensagem de sucesso indicando que o aluno foi deletado.

    Exceções:
    - HTTPException(401): Permissão negada.
    - HTTPException(404): Aluno não encontrado.
    - HTTPException(500): Erro interno ao deletar o aluno.
    """
    try:
        email = user['email']
        user_data = await user_collection.find_one({'email': email})
        permission = user_data['permissao']

        if permission != "GESTAO":
            raise HTTPException(status_code=401, detail="Permissão negada")
        
        aluno = await user_collection.find_one({'cpf': cpf})

        if aluno is None:
            raise HTTPException(status_code=404, detail="Aluno não encontrado")
        
        await user_collection.delete_one({'cpf': cpf})
        return JSONResponse(content={"message": "Aluno deletado com sucesso"}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get")
async def get_alunos(user: dict = Depends(verify_token)):
    """
    Retorna a lista de todos os alunos no sistema.

    Parâmetros:
    - user: Usuário autenticado que faz a requisição.

    Retorno:
    - Lista de alunos.

    Exceções:
    - HTTPException(401): Usuário não encontrado ou permissão negada.
    - HTTPException(500): Erro interno ao recuperar os alunos.
    """
    try:
        email = user['email']
        user_data = await user_collection.find_one({'email': email})

        if user_data is None:
            raise HTTPException(status_code=401, detail="Usuário não encontrado")
        
        permission = user_data['permissao']
        
        if permission != "GESTAO" and permission != "PROFESSOR":
            raise HTTPException(status_code=401, detail="Permissão negada")

        lista_alunos = []
        async for aluno in user_collection.find({'permissao': 'ALUNO'}):
            aluno['_id'] = str(aluno['_id'])
            lista_alunos.append(aluno)

        return JSONResponse(content={'alunos': lista_alunos}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get/{cpf}", response_model=AlunoResponse)  
async def get_aluno(cpf: str, user: dict = Depends(verify_token)):
    """
    Retorna os dados de um aluno específico pelo CPF.

    Parâmetros:
    - cpf: CPF do aluno a ser buscado.
    - user: Usuário autenticado que faz a requisição.

    Retorno:
    - Dados do aluno.

    Exceções:
    - HTTPException(401): Permissão negada.
    - HTTPException(404): Aluno não encontrado.
    - HTTPException(500): Erro interno ao recuperar o aluno.
    """
    
    try:
        email = user['email']
        user_data = await user_collection.find_one({'email': email})
        permission = user_data['permissao']
        
        if permission != "GESTAO" and permission != "PROFESSOR":
            raise HTTPException(status_code=401, detail="Permissão negada")
        
        aluno = await user_collection.find_one({'cpf': cpf})
        
        if aluno is None:
            raise HTTPException(status_code=404, detail="Aluno não encontrado")

        aluno['id'] = str(aluno['_id'])
        del aluno['_id']  

        return AlunoResponse(**aluno)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
    
@router.get("/getNotas")
async def get_notas(user: dict = Depends(verify_token)):
    """
    Retorna as notas do usuário autenticado.

    Parâmetros:
    - user: Usuário autenticado que faz a requisição.

    Retorno:
    - Notas do usuário.

    Exceções:
    - HTTPException(401): Usuário não encontrado.
    - HTTPException(500): Erro interno ao recuperar as notas.
    """
    try:
        email = user['email']
        user = await user_collection.find_one({'email': email})
        notas = user['notas']
        return JSONResponse(content=notas, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/addNota/{cpf}", response_model=dict)
async def add_nota(cpf: str, nota: NotaAdd, user: dict = Depends(verify_token)):
    """
    Adiciona uma nova nota a um aluno.

    Parâmetros:
    - cpf: CPF do aluno ao qual a nota será adicionada.
    - nota: Dados da nota a ser adicionada, deve ser do tipo NotaAdd.
    - user: Usuário autenticado que faz a requisição.

    Retorno:
    - Mensagem de sucesso indicando que a nota foi adicionada.

    Exceções:
    - HTTPException(401): Permissão negada.
    - HTTPException(404): Aluno não encontrado.
    - HTTPException(400): Avaliação ou nota não podem ser vazias.
    - HTTPException(500): Erro interno ao adicionar a nota.
    """
        
    try:
        email = user['email']
        user_data = await user_collection.find_one({'email': email})
        permission = user_data['permissao']

        if permission != "GESTAO":
            raise HTTPException(status_code=401, detail="Permissão negada")
        
        aluno = await user_collection.find_one({'cpf': cpf})
        
        if aluno is None:
            raise HTTPException(status_code=404, detail="Aluno não encontrado")
        
        aluno_notas = aluno['notas']
        aluno_notas[nota.avaliacao] = nota.nota
        
        if nota.avaliacao == "" or nota.nota == "":
            raise HTTPException(status_code=400, detail="Avaliação ou nota não podem ser vazias")

        await user_collection.update_one({'cpf': cpf}, {"$set": {'notas': aluno_notas}})
        return JSONResponse(content={"message": "Nota adicionada com sucesso"}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
@router.delete("/removeNota/{cpf}", response_model=dict)
async def remove_nota(cpf: str, nota: NotaRemove, user: dict = Depends(verify_token)):
    """
    Remove uma nota de um aluno.

    Parâmetros:
    - cpf: CPF do aluno ao qual a nota será removida.
    - nota: Dados da nota a ser removida, deve ser do tipo NotaRemove.
    - user: Usuário autenticado que faz a requisição.

    Retorno:
    - Mensagem de sucesso indicando que a nota foi removida.

    Exceções:
    - HTTPException(401): Permissão negada.
    - HTTPException(404): Aluno não encontrado ou avaliação não encontrada.
    - HTTPException(500): Erro interno ao remover a nota.
    """
    try:
        email = user['email']
        user_data = await user_collection.find_one({'email': email})
        permission = user_data['permissao']

        if permission != "GESTAO":
            raise HTTPException(status_code=401, detail="Permissão negada")
        
        aluno = await user_collection.find_one({'cpf': cpf})

        if aluno is None:
            raise HTTPException(status_code=404, detail="Aluno não encontrado")
        
        aluno_notas = aluno['notas']
        if nota.avaliacao not in aluno_notas:
            raise HTTPException(status_code=404, detail="Avaliação não encontrada")
        
        del aluno_notas[nota.avaliacao]
        await user_collection.update_one({'cpf': cpf}, {"$set": {'notas': aluno_notas}})
        return JSONResponse(content={"message": "Nota removida com sucesso"}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



