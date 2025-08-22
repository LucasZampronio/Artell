@echo off
echo 🎨 Configurando o projeto Artell...

REM Verifica se o Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não está instalado. Por favor, instale o Python 3.11+ primeiro.
    pause
    exit /b 1
)

REM Verifica se o Node.js está instalado
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js não está instalado. Por favor, instale o Node.js 18+ primeiro.
    pause
    exit /b 1
)

REM Verifica se o Docker está instalado
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker não está instalado. Por favor, instale o Docker primeiro.
    pause
    exit /b 1
)

echo ✅ Dependências básicas verificadas!

REM Configuração do Backend
echo 🐍 Configurando o backend Python...
cd backend

REM Cria ambiente virtual
python -m venv venv

REM Ativa o ambiente virtual
call venv\Scripts\activate.bat

REM Instala dependências
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Copia arquivo de ambiente
if not exist .env (
    copy env.example .env
    echo 📝 Arquivo .env criado. Por favor, configure suas variáveis de ambiente.
)

cd ..

REM Configuração do Frontend
echo ⚛️  Configurando o frontend React...
cd frontend

REM Instala dependências
npm install

cd ..

REM Inicia MongoDB com Docker
echo 🗄️  Iniciando MongoDB...
docker-compose up -d mongodb

echo ⏳ Aguardando MongoDB inicializar...
timeout /t 10 /nobreak >nul

echo.
echo 🎉 Configuração concluída!
echo.
echo 📋 Próximos passos:
echo 1. Configure suas variáveis de ambiente em backend\.env
echo 2. Inicie o backend: cd backend ^&^& venv\Scripts\activate ^&^& uvicorn main:app --reload
echo 3. Inicie o frontend: cd frontend ^&^& npm run dev
echo 4. Acesse http://localhost:3000 no seu navegador
echo.
echo 🔧 MongoDB está rodando em localhost:27017
echo 🌐 MongoDB Express está disponível em http://localhost:8081
echo.
echo Boa sorte com o seu projeto Artell! 🎨
pause
