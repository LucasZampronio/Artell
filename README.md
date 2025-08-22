# Artell 🎨

Uma aplicação web que funciona como um "Songtell" para obras de arte, permitindo aos utilizadores descobrir o significado e sentimentos por trás de obras de arte através de fotos ou pesquisa por nome.

## ✨ Funcionalidades

- **Análise por Nome**: Pesquisa obras de arte pelo nome e recebe análises detalhadas
- **Análise por Imagem**: Envia fotos de obras de arte para análise visual
- **Cache Inteligente**: Sistema de cache MongoDB para otimizar respostas e reduzir custos
- **Histórico de Análises**: Galeria com todas as análises realizadas
- **API RESTful**: Interface completa para integração com outras aplicações

## 🛠️ Stack Tecnológica

### Frontend
- **React 18** com TypeScript
- **Vite** para build e desenvolvimento
- **Tailwind CSS** para estilização
- **React Router** para navegação
- **Axios** para comunicação com API
- **Lucide React** para ícones

### Backend
- **Python 3.11+** com FastAPI
- **Pydantic** para validação de dados
- **Uvicorn** como servidor ASGI
- **Motor** para MongoDB assíncrono
- **Groq API** para inteligência artificial (gratuito!)
- **Python-dotenv** para gestão de configurações

### Base de Dados
- **MongoDB** para cache e persistência de análises
- **Docker** para orquestração

### DevOps
- **Docker Compose** para desenvolvimento local
- **Scripts de setup** para Windows e Linux/Mac

## 📁 Estrutura do Projeto

```
Artell/
├── frontend/          # Aplicação React
├── backend/           # API FastAPI
├── docs/             # Documentação
├── scripts/          # Scripts de setup e deploy
└── docker-compose.yml # Orquestração de serviços
```

## 🚀 Pré-requisitos

- **Python 3.11+**
- **Node.js 18+**
- **Docker** e **Docker Compose**
- **Git**

## ⚡ Execução Rápida

### 1. Clone o Repositório
```bash
git clone <repository-url>
cd Artell
```

### 2. Configure as Variáveis de Ambiente
```bash
cd backend
cp env.example .env
# Edite .env com sua GROQ_API_KEY (já incluída no exemplo)
```

### 3. Execute com Docker
```bash
docker-compose up -d
```

### 4. Acesse a Aplicação
- **Backend API**: http://localhost:8000
- **Documentação**: http://localhost:8000/docs
- **Frontend**: http://localhost:3000 (quando implementado)
- **MongoDB Express**: http://localhost:8081

## 🔧 Configuração Manual

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## 📚 API Endpoints

### Análise de Obras de Arte
- `POST /analise-por-nome` - Analisa obra por nome
- `GET /analises-recentes` - Lista análises recentes
- `GET /estatisticas` - Estatísticas das análises

### Sistema
- `GET /` - Informações da API
- `GET /health` - Verificação de saúde
- `GET /docs` - Documentação interativa

## 🎯 Por que Groq?

- **Gratuito**: Sem custos de API
- **Alta Qualidade**: Modelo Llama 4 Scout de 17B parâmetros
- **Velocidade**: Respostas rápidas e eficientes
- **Compatibilidade**: API compatível com OpenAI

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🆘 Suporte

Se encontrar algum problema ou tiver dúvidas:
1. Verifique a documentação em `/docs`
2. Consulte os logs da aplicação
3. Abra uma issue no repositório

---

**Artell** - Descubra o significado das obras de arte através da inteligência artificial! 🎨✨
