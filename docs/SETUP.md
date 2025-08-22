Artell: Analisador de Arte com IA
Artell é uma aplicação web que utiliza inteligência artificial para realizar análises detalhadas de obras de arte. Os usuários podem submeter imagens ou descrições textuais de obras e receber insights sobre estilo, contexto histórico, técnica e possíveis interpretações.

![Imagem de uma galeria de arte digital]

✨ Funcionalidades
Análise por Imagem: Envie uma imagem de uma obra de arte para receber uma análise completa.

Análise por Texto: Descreva uma obra de arte para que a IA gere uma análise baseada na sua descrição.

Galeria de Análises: Navegue por todas as análises já realizadas e salvas na plataforma.

Interface Responsiva: Acesse a aplicação de forma otimizada em desktops, tablets e dispositivos móveis.

🛠️ Tecnologias Utilizadas
A aplicação é construída com uma arquitetura moderna, separando o frontend do backend.

Backend:

Framework: FastAPI (Python)

Inteligência Artificial: API da Groq

Banco de Dados: MongoDB

Frontend:

Framework: React (com TypeScript)

Build Tool: Vite

Estilização: Tailwind CSS

Containerização:

Docker e Docker Compose

🚀 Como Executar o Projeto
Siga os passos abaixo para configurar e executar o ambiente de desenvolvimento localmente.

Pré-requisitos
Docker

Docker Compose

1. Variáveis de Ambiente
Antes de iniciar, crie um arquivo chamado .env na raiz do projeto. Copie o conteúdo abaixo e preencha com suas chaves e credenciais.

# Chave da API do Groq para o serviço de IA
GROQ_API_KEY=sua_chave_api_aqui

# Credenciais para o banco de dados MongoDB
MONGO_INITDB_ROOT_USERNAME=root
MONGO_INITDB_ROOT_PASSWORD=example
MONGO_INITDB_DATABASE=artell
MONGODB_URI=mongodb://root:example@mongo:27017/

2. Script de Setup
O projeto inclui um script que automatiza a construção dos containers Docker e a instalação de dependências.

No Windows:

.\scripts\setup.bat

No Linux ou macOS:

chmod +x ./scripts/setup.sh
./scripts/setup.sh

Este comando irá iniciar todos os serviços necessários (frontend, backend e banco de dados) usando o Docker Compose.

3. Acessando a Aplicação
Após a execução do script, a aplicação estará disponível nos seguintes endereços:

Frontend: http://localhost:5173

Documentação da API (Swagger): http://localhost:8000/docs

📁 Estrutura do Projeto
artell/
├── backend/         # Contém a API em FastAPI (Python)
│   ├── app/
│   │   ├── core/      # Configuração, banco de dados
│   │   ├── models/    # Modelos de dados (Pydantic)
│   │   ├── routers/   # Endpoints da API (rotas)
│   │   └── services/  # Lógica de negócio
│   ├── main.py      # Ponto de entrada da API
│   └── Dockerfile
├── frontend/        # Contém a aplicação em React (TypeScript)
│   ├── src/
│   │   ├── components/
│   │   ├── hooks/
│   │   └── pages/
│   └── Dockerfile
├── docs/            # Documentação adicional
├── scripts/         # Scripts de inicialização e setup
└── docker-compose.yml # Orquestração dos containers

🔌 Endpoints da API
A API do backend oferece os seguintes endpoints principais:

POST /api/analyze/image: Submete uma imagem para análise.

POST /api/analyze/text: Submete uma descrição textual para análise.

GET /api/analyses/: Retorna a lista de todas as análises salvas.

GET /api/analyses/{id}: Retorna uma análise específica pelo seu ID.

Para mais detalhes, acesse a documentação interativa do Swagger após iniciar o projeto.