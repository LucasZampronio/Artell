import { useState } from 'react'
import { Search, Filter, Calendar, Palette, Heart } from 'lucide-react'

const Gallery = () => {
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedStyle, setSelectedStyle] = useState('')

  // Mock data - em produção viria da API
  const analyses = [
    {
      id: '1',
      artwork_name: 'Mona Lisa',
      artist_name: 'Leonardo da Vinci',
      year_created: '1503-1519',
      style: 'Renaissance',
      emotions: ['awe', 'mystery', 'peace'],
      created_at: '2024-01-15T10:30:00Z',
      analysis_type: 'image'
    },
    {
      id: '2',
      artwork_name: 'A Noite Estrelada',
      artist_name: 'Vincent van Gogh',
      year_created: '1889',
      style: 'Post-Impressionism',
      emotions: ['excitement', 'melancholy', 'awe'],
      created_at: '2024-01-14T15:45:00Z',
      analysis_type: 'text'
    },
    {
      id: '3',
      artwork_name: 'O Grito',
      artist_name: 'Edvard Munch',
      year_created: '1893',
      style: 'Expressionism',
      emotions: ['fear', 'anxiety', 'despair'],
      created_at: '2024-01-13T09:20:00Z',
      analysis_type: 'image'
    }
  ]

  const styles = ['Renaissance', 'Post-Impressionism', 'Expressionism', 'Cubism', 'Surrealism']

  const filteredAnalyses = analyses.filter(analysis => {
    const matchesSearch = analysis.artwork_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         analysis.artist_name?.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesStyle = !selectedStyle || analysis.style === selectedStyle
    return matchesSearch && matchesStyle
  })

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('pt-BR')
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Galeria de Análises
          </h1>
          <p className="text-xl text-gray-600">
            Explore todas as análises de obras de arte realizadas
          </p>
        </div>

        {/* Filters */}
        <div className="card mb-8">
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <label htmlFor="search" className="block text-sm font-medium text-gray-700 mb-2">
                Pesquisar
              </label>
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                <input
                  type="text"
                  id="search"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  placeholder="Nome da obra ou artista..."
                  className="input-field pl-10"
                />
              </div>
            </div>
            <div>
              <label htmlFor="style" className="block text-sm font-medium text-gray-700 mb-2">
                Estilo Artístico
              </label>
              <select
                id="style"
                value={selectedStyle}
                onChange={(e) => setSelectedStyle(e.target.value)}
                className="input-field"
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

        {/* Results */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredAnalyses.map((analysis) => (
            <div key={analysis.id} className="card hover:shadow-lg transition-shadow duration-300">
              <div className="space-y-4">
                <div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-1">
                    {analysis.artwork_name}
                  </h3>
                  {analysis.artist_name && (
                    <p className="text-gray-600">
                      por {analysis.artist_name}
                    </p>
                  )}
                </div>

                <div className="flex items-center space-x-4 text-sm text-gray-500">
                  {analysis.year_created && (
                    <div className="flex items-center">
                      <Calendar className="w-4 h-4 mr-1" />
                      {analysis.year_created}
                    </div>
                  )}
                  {analysis.style && (
                    <div className="flex items-center">
                      <Palette className="w-4 h-4 mr-1" />
                      {analysis.style}
                    </div>
                  )}
                </div>

                <div>
                  <div className="flex flex-wrap gap-2 mb-3">
                    {analysis.emotions.map((emotion) => (
                      <span
                        key={emotion}
                        className="px-2 py-1 bg-primary-100 text-primary-800 rounded-full text-xs font-medium"
                      >
                        {emotion}
                      </span>
                    ))}
                  </div>
                </div>

                <div className="flex items-center justify-between pt-4 border-t border-gray-200">
                  <span className="text-sm text-gray-500">
                    {formatDate(analysis.created_at)}
                  </span>
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                    analysis.analysis_type === 'image' 
                      ? 'bg-blue-100 text-blue-800' 
                      : 'bg-green-100 text-green-800'
                  }`}>
                    {analysis.analysis_type === 'image' ? 'Imagem' : 'Texto'}
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>

        {filteredAnalyses.length === 0 && (
          <div className="text-center py-12">
            <Heart className="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              Nenhuma análise encontrada
            </h3>
            <p className="text-gray-500">
              Tente ajustar os filtros ou faça sua primeira análise!
            </p>
          </div>
        )}
      </div>
    </div>
  )
}

export default Gallery
