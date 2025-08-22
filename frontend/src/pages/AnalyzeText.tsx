import { useState } from 'react'
import { Search, Sparkles, BookOpen } from 'lucide-react'

const AnalyzeText = () => {
  const [artworkName, setArtworkName] = useState('')
  const [isAnalyzing, setIsAnalyzing] = useState(false)

  const handleAnalyze = async () => {
    if (!artworkName.trim()) return
    
    setIsAnalyzing(true)
    // TODO: Implementar chamada para API
    setTimeout(() => setIsAnalyzing(false), 3000)
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Pesquisar Obra de Arte
          </h1>
          <p className="text-xl text-gray-600">
            Digite o nome da obra para descobrir seu significado e história
          </p>
        </div>

        <div className="card max-w-2xl mx-auto">
          <div className="space-y-6">
            <div>
              <label htmlFor="artwork-name" className="block text-sm font-medium text-gray-700 mb-2">
                Nome da Obra de Arte
              </label>
              <input
                type="text"
                id="artwork-name"
                value={artworkName}
                onChange={(e) => setArtworkName(e.target.value)}
                placeholder="Ex: Mona Lisa, A Noite Estrelada, O Grito..."
                className="input-field"
              />
            </div>

            <button
              onClick={handleAnalyze}
              disabled={!artworkName.trim() || isAnalyzing}
              className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isAnalyzing ? (
                <>
                  <Sparkles className="w-5 h-5 mr-2 animate-pulse" />
                  Pesquisando...
                </>
              ) : (
                <>
                  <Search className="w-5 h-5 mr-2" />
                  Pesquisar e Analisar
                </>
              )}
            </button>
          </div>

          <div className="mt-8 p-4 bg-blue-50 rounded-lg">
            <h3 className="font-medium text-blue-900 mb-2">💡 Exemplos de obras famosas:</h3>
            <ul className="text-sm text-blue-800 space-y-1">
              <li>• Mona Lisa - Leonardo da Vinci</li>
              <li>• A Noite Estrelada - Vincent van Gogh</li>
              <li>• O Grito - Edvard Munch</li>
              <li>• Guernica - Pablo Picasso</li>
              <li>• A Persistência da Memória - Salvador Dalí</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}

export default AnalyzeText
