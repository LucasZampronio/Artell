import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { Heart, Eye, Palette, Calendar, Clock, ArrowLeft, Share2, Bookmark, Star } from 'lucide-react'

// Interface atualizada para corresponder à resposta da API
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
  const { id } = useParams<{ id: string }>() // Obtém o ID da URL
  const navigate = useNavigate()
  const [analysis, setAnalysis] = useState<AnalysisData | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // ✨ LÓGICA CORRIGIDA: Este useEffect agora busca os dados reais da API ✨
  useEffect(() => {
    if (!id) {
      setError("ID da análise não encontrado na URL.")
      setIsLoading(false)
      return
    }

    const fetchAnalysisData = async () => {
      setIsLoading(true)
      try {
        // A URL agora aponta para o endpoint que busca pelo ID
        const response = await fetch(`http://localhost:8001/analyses/${id}`)
        
        if (!response.ok) {
          throw new Error('Não foi possível carregar a análise. Tente novamente mais tarde.')
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
  }, [id]) // A busca é refeita sempre que o ID na URL muda

  // O resto do seu componente (lógica de emoções, renderização, etc.) pode ser mantido,
  // mas vamos ajustar para usar 'artwork_name'

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
  }

  const getEmotionColor = (emotion: string) => {
    const colors = {
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
    return colors[emotion as keyof typeof colors] || "bg-gray-100 text-gray-800"
  }

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
        <div className="text-center">
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

  // O seu JSX de renderização estava ótimo, só precisa de usar 'artwork_name'
  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <button
            onClick={() => navigate('/')}
            className="inline-flex items-center text-primary-600 hover:text-primary-700 mb-4 transition-colors duration-200"
          >
            <ArrowLeft className="w-5 h-5 mr-2" />
            Voltar ao Início
          </button>
          
          <div className="bg-white rounded-2xl p-8 shadow-lg border border-gray-100">
            <div className="text-center mb-8">
              <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
                {analysis.artwork_name} 
              </h1>
              
              {analysis.artist && (
                <p className="text-2xl text-gray-600 mb-4">
                  por <span className="font-semibold text-primary-600">{analysis.artist}</span>
                </p>
              )}
              
             {/* ... O resto do seu código JSX continua aqui, sem alterações ... */}
             
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default AnalysisResult