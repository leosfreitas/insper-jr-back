# Importação de dependências principais
from fastapi import FastAPI  # Importa o framework FastAPI para criar a aplicação web
from fastapi.middleware.cors import CORSMiddleware  # Middleware para configurar o CORS

# Importação de rotas de diferentes módulos da aplicação
from routes.users import router as user_router  # Roteamento relacionado aos usuários
from routes.auth import router as auth_router  # Roteamento de autenticação e autorização
from routes.avisos import router as avisos_router  # Roteamento para avisos
from routes.alunos import router as alunos_router  # Roteamento para operações de alunos
from routes.grade import router as grade_router  # Roteamento para informações de grade
from routes.info import router as info_router  # Roteamento para outras informações

# Instancia a aplicação FastAPI
app = FastAPI()

# Configura as origens permitidas para acesso (CORS) - neste caso, apenas localhost na porta 5173
origins = [
    "http://localhost:5173",
]

# Configura o middleware de CORS para permitir requisições de diferentes origens, credenciais e métodos HTTP
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Define as origens permitidas para a aplicação
    allow_credentials=True,  # Permite o envio de cookies e credenciais de sessão
    allow_methods=["*"],  # Permite todos os métodos HTTP (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permite todos os cabeçalhos HTTP
)

# Inclusão das rotas de diferentes módulos com respectivos prefixos e tags
app.include_router(user_router, prefix="/user", tags=["user"])  # Rotas relacionadas ao módulo de usuários
app.include_router(auth_router, prefix="/auth", tags=["auth"])  # Rotas de autenticação
app.include_router(alunos_router, prefix="/alunos", tags=["alunos"])  # Rotas para operações com alunos
app.include_router(avisos_router, prefix="/avisos", tags=["avisos"])  # Rotas para gerenciamento de avisos
app.include_router(grade_router, prefix="/grade", tags=["grade"])  # Rotas para informações de grade
app.include_router(info_router, prefix="/info", tags=["info"])  # Rotas para informações gerais

# Rota principal para verificar o status da API
@app.get("/")
async def root():
    """
    Rota raiz para verificar o status da API.
    Retorna uma mensagem indicando que a API está em execução.
    """
    return {"message": "API is running!"}
