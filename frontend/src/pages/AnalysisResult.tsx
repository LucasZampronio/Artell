// frontend/src/pages/AnalysisResult.tsx

import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { Palette, Calendar, Clock, ArrowLeft, Share2, Bookmark, Star } from 'lucide-react'

// Interface para os dados da análise (continua correta)
interface AnalysisData {
  id: string;
  artwork_name: string;
  analysis: string;
  artist?: string;
  year?: string;
  style?: string;
  emotions: string[];
  processing_time: number;
  cached: boolean;
}

const AnalysisResult = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [analysis, setAnalysis] = useState<AnalysisData | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!id) {
      setError("ID da análise não encontrado na URL.")
      setIsLoading(false)
      return
    }

    const fetchAnalysisData = async () => {
      setIsLoading(true)
      try {
        const response = await fetch(`http://localhost:8001/analyses/${id}`)
        
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || 'Não foi possível carregar a análise.')
        }
        
        const data: AnalysisData = await response.json()
        setAnalysis(data)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Ocorreu um erro desconhecido')
      } finally {
        setIsLoading(false)
      }
    }

    fetchAnalysisData()
  }, [id])

  // Lógica para emoções
  const emotionLabels: Record<string, string> = {
    awe: "Deslumbramento",
    melancholy: "Melancolia",
    wonder: "Maravilhamento",
    tranquility: "Tranquilidade",
    mystery: "Mistério",
    joy: "Alegria",
    sadness: "Tristeza",
    excitement: "Excitação",
    peace: "Paz",
    curiosity: "Curiosidade"
    // Adicione mais se necessário
  }

  const getEmotionColor = (emotion: string) => {
    const colors: Record<string, string> = {
      awe: "bg-purple-100 text-purple-800",
      melancholy: "bg-blue-100 text-blue-800",
      wonder: "bg-yellow-100 text-yellow-800",
      tranquility: "bg-green-100 text-green-800",
      mystery: "bg-gray-100 text-gray-800",
      joy: "bg-pink-100 text-pink-800",
      sadness: "bg-indigo-100 text-indigo-800",
      excitement: "bg-red-100 text-red-800",
      peace: "bg-teal-100 text-teal-800",
      curiosity: "bg-orange-100 text-orange-800"
    }
    return colors[emotion] || "bg-gray-100 text-gray-800"
  }

  // Ecrãs de Loading e Erro
  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-primary-600 mx-auto mb-4"></div>
          <p className="text-gray-600">A carregar a análise...</p>
        </div>
      </div>
    )
  }

  if (error || !analysis) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center max-w-md mx-auto">
          <p className="text-red-600 mb-4">{error || "Não foi possível encontrar a análise."}</p>
          <button
            onClick={() => navigate('/')}
            className="btn-primary"
          >
            Voltar ao Início
          </button>
        </div>
      </div>
    )
  }

  // ✨ CÓDIGO ADICIONADO ABAIXO ✨
  // Componente principal com os dados
  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <button
            onClick={() => navigate('/')}
            className="inline-flex items-center text-primary-600 hover:text-primary-700 mb-4 transition-colors duration-200"
          >
            <ArrowLeft className="w-5 h-5 mr-2" />
            Voltar ao Início
          </button>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Coluna Principal da Análise */}
          <div className="lg:col-span-2 bg-white rounded-2xl p-8 shadow-lg border border-gray-100">
            <div className="text-center mb-8">
              <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4 font-serif">
                {analysis.artwork_name}
              </h1>
              {analysis.artist && (
                <p className="text-2xl text-gray-600">
                  por <span className="font-semibold text-primary-600">{analysis.artist}</span>
                </p>
              )}
            </div>

            {/* Conteúdo da Análise */}
            <div className="prose prose-lg max-w-none text-gray-700 leading-relaxed whitespace-pre-line">
              {analysis.analysis}
            </div>
          </div>

          {/* Coluna de Metadados */}
          <div className="space-y-6">
            <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100">
              <h3 className="text-xl font-bold mb-4 text-gray-800">Detalhes da Obra</h3>
              <ul className="space-y-3 text-gray-600">
                {analysis.artist && (
                  <li className="flex items-center">
                    <Palette className="w-5 h-5 mr-3 text-primary-500" />
                    <strong>Artista:</strong><span className="ml-2">{analysis.artist}</span>
                  </li>
                )}
                {analysis.year && (
                  <li className="flex items-center">
                    <Calendar className="w-5 h-5 mr-3 text-primary-500" />
                    <strong>Ano:</strong><span className="ml-2">{analysis.year}</span>
                  </li>
                )}
                {analysis.style && (
                  <li className="flex items-center">
                    <Palette className="w-5 h-5 mr-3 text-primary-500" />
                    <strong>Estilo:</strong><span className="ml-2">{analysis.style}</span>
                  </li>
                )}
              </ul>
            </div>
            
            <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100">
              <h3 className="text-xl font-bold mb-4 text-gray-800">Emoções Evocadas</h3>
              <div className="flex flex-wrap gap-2">
                {analysis.emotions.length > 0 ? analysis.emotions.map((emotion) => (
                  <span
                    key={emotion}
                    className={`px-3 py-1 rounded-full text-sm font-medium ${getEmotionColor(emotion)}`}
                  >
                    {emotionLabels[emotion] || emotion}
                  </span>
                )) : <p className="text-sm text-gray-500">Nenhuma emoção primária identificada.</p>}
              </div>
            </div>

            <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100">
                <h3 className="text-xl font-bold mb-4 text-gray-800">Ações</h3>
                <div className="flex space-x-2">
                    <button className="flex-1 btn-secondary inline-flex items-center justify-center"><Share2 className="w-4 h-4 mr-2"/> Partilhar</button>
                    <button className="flex-1 btn-secondary inline-flex items-center justify-center"><Bookmark className="w-4 h-4 mr-2"/> Salvar</button>
                </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default AnalysisResult