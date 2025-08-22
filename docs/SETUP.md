# 🎨 Setup do Projeto Artell

Este guia irá ajudá-lo a configurar e executar o projeto Artell em sua máquina local.

## 📋 Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- **Python 3.11+** - [Download Python](https://www.python.org/downloads/)
- **Node.js 18+** - [Download Node.js](https://nodejs.org/)
- **Docker** - [Download Docker](https://www.docker.com/products/docker-desktop/)
- **Git** - [Download Git](https://git-scm.com/)

## 🚀 Configuração Rápida

### 1. Clone o Repositório
```bash
git clone <repository-url>
cd Artell
```

### 2. Execute o Script de Setup

**Linux/Mac:**
```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

**Windows:**
```cmd
scripts\setup.bat
```

O script irá:
- ✅ Verificar dependências
- 🐍 Configurar ambiente Python
- ⚛️ Instalar dependências React
- 🗄️ Iniciar MongoDB com Docker
- 📝 Criar arquivo de configuração

## 🔧 Configuração Manual

Se preferir configurar manualmente ou se o script automático falhar:

### Backend Python

1. **Crie ambiente virtual:**
```bash
cd backend
python -m venv venv
```

2. **Ative o ambiente:**
```bash
# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

3. **Instale dependências:**
```bash
pip install -r requirements.txt
```

4. **Configure variáveis de ambiente:**
```bash
cp env.example .env
# Edite .env com suas configurações
```

### Frontend React

1. **Instale dependências:**
```bash
cd frontend
npm install
```

### MongoDB

1. **Inicie com Docker:**
```bash
docker-compose up -d mongodb
```

## ⚙️ Configuração das Variáveis de Ambiente

Edite o arquivo `backend/.env`:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017/artell

# Security
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# App Configuration
APP_NAME=Artell
APP_VERSION=1.0.0
DEBUG=True

# CORS
ALLOWED_ORIGINS=["http://localhost:3000", "http://localhost:5173"]
```

### 🔑 Obter OpenAI API Key

1. Acesse [OpenAI Platform](https://platform.openai.com/)
2. Faça login ou crie uma conta
3. Vá para "API Keys"
4. Crie uma nova chave
5. Copie a chave para `OPENAI_API_KEY`

## 🚀 Executando o Projeto

### 1. Inicie o Backend
```bash
cd backend
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

uvicorn main:app --reload
```

O backend estará disponível em: http://localhost:8000
Documentação da API: http://localhost:8000/docs

### 2. Inicie o Frontend
```bash
cd frontend
npm run dev
```

O frontend estará disponível em: http://localhost:3000

### 3. MongoDB
```bash
# Verificar status
docker-compose ps

# Acessar logs
docker-compose logs mongodb

# Interface web (opcional)
# http://localhost:8081 (admin/password123)
```

## 🧪 Testando a Aplicação

1. **Acesse** http://localhost:5173
2. **Teste análise por imagem:**
   - Vá para "Analisar Imagem"
   - Faça upload de uma imagem de obra de arte
   - Clique em "Analisar com IA"
3. **Teste análise por texto:**
   - Vá para "Pesquisar Obra"
   - Digite "Mona Lisa"
   - Clique em "Pesquisar e Analisar"

## 📁 Estrutura do Projeto

```
Artell/
├── backend/                 # API FastAPI
│   ├── app/
│   │   ├── core/           # Configuração e base de dados
│   │   ├── models/         # Modelos Pydantic
│   │   ├── routers/        # Endpoints da API
│   │   └── services/       # Lógica de negócio
│   ├── main.py             # Aplicação principal
│   ├── requirements.txt    # Dependências Python
│   └── env.example         # Variáveis de ambiente
├── frontend/               # Aplicação React
│   ├── src/
│   │   ├── components/     # Componentes reutilizáveis
│   │   ├── pages/          # Páginas da aplicação
│   │   ├── App.tsx         # Componente principal
│   │   └── main.tsx        # Ponto de entrada
│   ├── package.json        # Dependências Node.js
│   └── tailwind.config.js  # Configuração Tailwind
├── scripts/                # Scripts de setup
├── docs/                   # Documentação
├── docker-compose.yml      # Orquestração Docker
└── README.md               # Documentação principal
```

## 🔍 Endpoints da API

- `POST /api/analyze/image` - Analisa obra por imagem
- `POST /api/analyze/text` - Analisa obra por nome
- `GET /api/analyses` - Lista análises
- `GET /api/analyses/{id}` - Obtém análise específica
- `GET /api/analyses/stats/summary` - Estatísticas

## 🐛 Solução de Problemas

### Erro de Conexão com MongoDB
```bash
# Verificar se o container está rodando
docker-compose ps

# Reiniciar MongoDB
docker-compose restart mongodb

# Ver logs
docker-compose logs mongodb
```

### Erro de Dependências Python
```bash
cd backend
rm -rf venv
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
pip install -r requirements.txt
```

### Erro de Dependências Node.js
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Porta já em uso
```bash
# Verificar processos nas portas
lsof -i :8000  # Linux/Mac
netstat -ano | findstr :8000  # Windows

# Matar processo
kill -9 <PID>  # Linux/Mac
taskkill /PID <PID> /F  # Windows
```

## 📚 Recursos Adicionais

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- [MongoDB Documentation](https://docs.mongodb.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs)

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT.

---

**Boa sorte com o seu projeto Artell! 🎨✨**
