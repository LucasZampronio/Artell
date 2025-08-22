FROM node:18-slim

WORKDIR /app

# Copiar apenas package.json (sem package-lock.json)
COPY package.json ./

# Instalar todas as dependências (Vite incluso)
RUN npm install

# Copiar todo o restante do código
COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

