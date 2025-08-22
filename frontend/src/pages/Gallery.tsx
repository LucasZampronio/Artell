// frontend/src/pages/Gallery.tsx

import { useState, useMemo } from 'react';
import { Search, Calendar, Palette, Heart, Loader, AlertTriangle } from 'lucide-react';
import { Link } from 'react-router-dom';

// ✨ 1. Importar o nosso novo hook
import { useGallery } from '../hooks/useGallery';

const Gallery = () => {
  // ✨ 2. Usar o hook para obter os dados e estados
  const { analyses, isLoading, error } = useGallery();

  const [searchTerm, setSearchTerm] = useState('');
  const [selectedStyle, setSelectedStyle] = useState('');

  // Lógica de filtragem agora usa os dados da API
  const filteredAnalyses = useMemo(() => {
    return analyses.filter(analysis => {
      const matchesSearch = 
        analysis.artwork_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        analysis.artist?.toLowerCase().includes(searchTerm.toLowerCase());
      const matchesStyle = !selectedStyle || analysis.style === selectedStyle;
      return matchesSearch && matchesStyle;
    });
  }, [analyses, searchTerm, selectedStyle]);
  
  // Extrair estilos únicos a partir dos dados recebidos
  const styles = useMemo(() => {
      const allStyles = analyses.map(a => a.style).filter(Boolean);
      return [...new Set(allStyles)] as string[];
  }, [analyses]);


  // ✨ 3. Lidar com os estados de carregamento e erro
  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-96">
        <Loader className="w-12 h-12 animate-spin text-primary-600" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <AlertTriangle className="w-16 h-16 text-red-400 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-red-700 mb-2">
          Ocorreu um erro
        </h3>
        <p className="text-gray-500">{error}</p>
      </div>
    );
  }

  // ✨ 4. Renderizar a galeria com os dados reais
  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4 font-serif">
            Galeria de Análises
          </h1>
          <p className="text-xl text-gray-600">
            Explore todas as análises de obras de arte realizadas
          </p>
        </div>

        {/* Filters */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-8">
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <label htmlFor="search" className="block text-sm font-medium text-gray-700 mb-2">
                Pesquisar por Obra ou Artista
              </label>
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                <input
                  type="text"
                  id="search"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  placeholder="Ex: Mona Lisa..."
                  className="w-full pl-10 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                />
              </div>
            </div>
            <div>
              <label htmlFor="style" className="block text-sm font-medium text-gray-700 mb-2">
                Filtrar por Estilo Artístico
              </label>
              <select
                id="style"
                value={selectedStyle}
                onChange={(e) => setSelectedStyle(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              >
                <option value="">Todos os estilos</option>
                {styles.map((style) => (
                  <option key={style} value={style}>
                    {style}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {/* Results Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredAnalyses.map((analysis) => (
            <Link to={`/analysis/${analysis.id}`} key={analysis.id} className="block bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-lg hover:border-primary-300 transition-all duration-300">
              <div className="space-y-4">
                <div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-1">
                    {analysis.artwork_name}
                  </h3>
                  {analysis.artist && (
                    <p className="text-gray-600">
                      por {analysis.artist}
                    </p>
                  )}
                </div>

                <div className="flex items-center space-x-4 text-sm text-gray-500">
                  {analysis.year && (
                    <div className="flex items-center">
                      <Calendar className="w-4 h-4 mr-1.5" />
                      {analysis.year}
                    </div>
                  )}
                  {analysis.style && (
                    <div className="flex items-center">
                      <Palette className="w-4 h-4 mr-1.5" />
                      {analysis.style}
                    </div>
                  )}
                </div>

                <div className="flex flex-wrap gap-2 pt-2">
                  {analysis.emotions.slice(0, 3).map((emotion) => (
                    <span
                      key={emotion}
                      className="px-2 py-1 bg-primary-50 text-primary-700 rounded-full text-xs font-medium"
                    >
                      {emotion}
                    </span>
                  ))}
                </div>
              </div>
            </Link>
          ))}
        </div>

        {/* Mensagem de "Nenhum resultado" */}
        {analyses.length > 0 && filteredAnalyses.length === 0 && (
          <div className="text-center py-12">
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              Nenhuma análise encontrada
            </h3>
            <p className="text-gray-500">
              Tente ajustar os seus filtros de pesquisa.
            </p>
          </div>
        )}

        {/* Mensagem de "Galeria Vazia" */}
        {analyses.length === 0 && !isLoading && (
           <div className="text-center py-12">
             <Heart className="w-16 h-16 text-gray-300 mx-auto mb-4" />
             <h3 className="text-lg font-medium text-gray-900 mb-2">
               A sua galeria está vazia
             </h3>
             <p className="text-gray-500">
               Comece por fazer a sua primeira análise de uma obra de arte!
             </p>
           </div>
        )}
      </div>
    </div>
  );
};

export default Gallery;