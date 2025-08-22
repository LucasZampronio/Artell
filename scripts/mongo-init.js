// Script de inicialização do MongoDB para o projeto Artell
print('🎨 Inicializando banco de dados Artell...');

// Conectar ao banco artell
db = db.getSiblingDB('artell');

// Cria a coleção de análises de obras de arte
db.createCollection('artwork_analyses');

// Cria índices para otimização
db.artwork_analyses.createIndex({ "artwork_name": 1 });
db.artwork_analyses.createIndex({ "created_at": 1 });
db.artwork_analyses.createIndex({ "artist": 1 });

print('✅ Banco de dados Artell inicializado com sucesso!');
print('📊 Índices criados para otimização de consultas:');
print('   - artwork_name (busca por nome da obra)');
print('   - created_at (ordenação por data)');
print('   - artist (busca por artista)');
print('');
print('🚀 Pronto para receber análises de obras de arte!');
