#!/bin/bash

echo "🎨 Configurando o projeto Artell..."

# Verifica se o Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não está instalado. Por favor, instale o Python 3.11+ primeiro."
    exit 1
fi

# Verifica se o Node.js está instalado
if ! command -v node &> /dev/null; then
    echo "❌ Node.js não está instalado. Por favor, instale o Node.js 18+ primeiro."
    exit 1
fi

# Verifica se o Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não está instalado. Por favor, instale o Docker primeiro."
    exit 1
fi

echo "✅ Dependências básicas verificadas!"

# Configuração do Backend
echo "🐍 Configurando o backend Python..."
cd backend

# Cria ambiente virtual
python3 -m venv venv

# Ativa o ambiente virtual
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Instala dependências
pip install --upgrade pip
pip install -r requirements.txt

# Copia arquivo de ambiente
if [ ! -f .env ]; then
    cp env.example .env
    echo "📝 Arquivo .env criado. Por favor, configure suas variáveis de ambiente."
fi

cd ..

# Configuração do Frontend
echo "⚛️  Configurando o frontend React..."
cd frontend

# Instala dependências
npm install

cd ..

# Inicia MongoDB com Docker
echo "🗄️  Iniciando MongoDB..."
docker-compose up -d mongodb

echo "⏳ Aguardando MongoDB inicializar..."
sleep 10

echo ""
echo "🎉 Configuração concluída!"
echo ""
echo "📋 Próximos passos:"
echo "1. Configure suas variáveis de ambiente em backend/.env"
echo "2. Inicie o backend: cd backend && source venv/bin/activate && uvicorn main:app --reload"
echo "3. Inicie o frontend: cd frontend && npm run dev"
echo "4. Acesse http://localhost:3000 no seu navegador"
echo ""
echo "🔧 MongoDB está rodando em localhost:27017"
echo "🌐 MongoDB Express está disponível em http://localhost:8081"
echo ""
echo "Boa sorte com o seu projeto Artell! 🎨"
