# Back-End Processo Seletivo Insper Jr - CComp Segunda Fase

Plataforma para o Cursinho Insper que visa aproximar alunos da equipe dos gestores e professores. A plataforma conta com funcionalidades como: visualizar avisos, notas, grade horária, criar alunos e usuários, entre outras.

## Tecnologias Utilizadas

### FastAPI

FastAPI é um framework moderno e rápido para construir APIs com Python. Ele é baseado em Starlette e Pydantic e oferece uma série de benefícios:

- **Desempenho Alto**: FastAPI é um dos frameworks mais rápidos disponíveis para construção de APIs, aproveitando o desempenho do Starlette.
- **Validação Automática**: A validação de dados é feita automaticamente usando Pydantic, garantindo que os dados recebidos e enviados sejam válidos.
- **Documentação Automática**: FastAPI gera automaticamente a documentação da API com Swagger UI e ReDoc, facilitando a exploração da API.

## Por que usar FastAPI?

- **Desenvolvimento Rápido**: Com a validação de dados e a documentação automática, você pode desenvolver suas APIs de forma mais rápida e eficiente.
- **Tipagem Estática**: A tipagem do Python é aproveitada para validar dados, o que ajuda a prevenir erros e a melhorar a qualidade do código.
- **Suporte a Assincronismo**: FastAPI suporta rotas assíncronas, permitindo o desenvolvimento de APIs de alta performance e escaláveis.

## Instalação

Para iniciar o projeto, siga os passos abaixo:

### Pré-requisitos

Certifique-se de ter o Python 3.7 ou superior instalado. Você pode baixar em [python.org](https://www.python.org/downloads/).

### Passos para Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/leosfreitas/insper-jr-back

2. Crie um ambiente virtual:
   ```bash
    python -m venv venv
    venv\Scripts\activate # No Mac, use: source venv/bin/activate 

3. Instale as dependências:
    ```bash
    pip install -r requirements.txt

4. Inicie o servidor:
    ```bash
    uvicorn main:app --reload