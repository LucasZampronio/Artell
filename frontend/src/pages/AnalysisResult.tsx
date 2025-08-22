import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { Heart, Eye, Palette, Calendar, Clock, ArrowLeft, Share2, Bookmark, Star } from 'lucide-react'

interface AnalysisData {
  artwork: string
  analysis: string
  artist?: string
  year?: string
  style?: string
  emotions: string[]
  processing_time: number
  cached: boolean
}

const AnalysisResult = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const [analysis, setAnalysis] = useState<AnalysisData | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    // Simular dados de análise (em produção, buscar da API)
    const mockAnalysis: AnalysisData = {
      artwork: "A Noite Estrelada",
      analysis: "A Noite Estrelada, pintada por Vincent van Gogh em 188 9, é uma das obras mais icônicas do pós-impressionismo. Esta pintura representa a vista noturna da janela do sanatório de Saint-Paul-de-Mausole, onde o artista estava internado. Van Gogh criou esta obra durante um período de intensa criatividade, apesar de sua instabilidade mental. A composição é dominada por um céu noturno turbulento, onde as nuvens e estrelas parecem girar em espirais cósmicas, criando um movimento dinâmico que reflete a agitação interior do artista. As pinceladas espessas e expressivas, características do estilo de Van Gogh, transmitem uma sensação de energia e emoção intensa. A paleta de cores vibrantes, com azuis profundos, amarelos brilhantes e brancos luminosos, cria um contraste dramático que evoca tanto a beleza quanto a melancolia da noite. A vila ao fundo, com suas casas simples e a torre da igreja, representa a estabilidade e a humanidade em contraste com o caos cósmico do céu. Esta obra transcende a representação literal para se tornar uma expressão dos sentimentos mais profundos de Van Gogh sobre a vida, a morte e a eternidade. A Noite Estrelada continua a fascinar e inspirar, sendo considerada uma das maiores obras-primas da história da arte.",
      artist: "Vincent van Gogh",
      year: "1889",
      style: "Pós-impressionismo",
      emotions: ["awe", "melancholy", "wonder", "tranquility", "mystery"],
      processing_time: 2.34,
      cached: false
    }

    // Simular carregamento
    setTimeout(() => {
      setAnalysis(mockAnalysis)
      setIsLoading(false)
    }, 1000)
  }, [id])

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
          <p className="text-gray-600">Analisando obra de arte...</p>
        </div>
      </div>
    )
  }

  if (error || !analysis) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-600 mb-4">Erro ao carregar análise</p>
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
                {analysis.artwork}
              </h1>
              
              {analysis.artist && (
                <p className="text-2xl text-gray-600 mb-4">
                  por <span className="font-semibold text-primary-600">{analysis.artist}</span>
                </p>
              )}
              
              <div className="flex flex-wrap justify-center items-center gap-6 text-sm text-gray-500">
                {analysis.year && (
                  <div className="flex items-center">
                    <Calendar className="w-4 h-4 mr-2" />
                    {analysis.year}
                  </div>
                )}
                
                {analysis.style && (
                  <div className="flex items-center">
                    <Palette className="w-4 h-4 mr-2" />
                    {analysis.style}
                  </div>
                )}
                
                <div className="flex items-center">
                  <Clock className="w-4 h-4 mr-2" />
                  {analysis.processing_time.toFixed(2)}s
                </div>
                
                {analysis.cached && (
                  <div className="flex items-center text-green-600">
                    <Star className="w-4 h-4 mr-2" />
                    Cache
                  </div>
                )}
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex flex-wrap justify-center gap-4 mb-8">
              <button className="inline-flex items-center px-6 py-3 bg-primary-600 text-white rounded-xl font-semibold hover:bg-primary-700 transition-colors duration-200">
                <Bookmark className="w-5 h-5 mr-2" />
                Salvar Análise
              </button>
              
              <button className="inline-flex items-center px-6 py-3 bg-gray-100 text-gray-700 rounded-xl font-semibold hover:bg-gray-200 transition-colors duration-200">
                <Share2 className="w-5 h-5 mr-2" />
                Compartilhar
              </button>
            </div>
          </div>
        </div>

        {/* Analysis Content */}
        <div className="grid lg:grid-cols-3 gap-8">
          {/* Main Analysis */}
          <div className="lg:col-span-2 space-y-8">
            {/* Meaning Section */}
            <div className="bg-white rounded-2xl p-8 shadow-lg border border-gray-100">
              <h2 className="text-2xl font-semibold text-gray-900 mb-6 flex items-center">
                <Eye className="w-6 h-6 mr-3 text-primary-600" />
                Significado da Obra
              </h2>
              <div className="prose prose-lg max-w-none">
                <p className="text-gray-700 leading-relaxed whitespace-pre-line">
                  {analysis.analysis}
                </p>
              </div>
            </div>

            {/* Artist Intention */}
            <div className="bg-white rounded-2xl p-8 shadow-lg border border-gray-100">
              <h2 className="text-2xl font-semibold text-gray-900 mb-6 flex items-center">
                <Palette className="w-6 h-6 mr-3 text-primary-600" />
                Contexto e Intenção
              </h2>
              <p className="text-gray-700 leading-relaxed">
                Esta obra foi criada durante um período significativo da vida do artista, 
                refletindo suas experiências pessoais, estado emocional e visão artística única. 
                A técnica e o estilo demonstram a evolução do artista e sua contribuição 
                para o movimento artístico da época.
              </p>
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Emotions */}
            <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100">
              <h3 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
                <Heart className="w-5 h-5 mr-2 text-primary-600" />
                Emoções Evocadas
              </h3>
              <div className="space-y-3">
                {analysis.emotions.map((emotion) => (
                  <div
                    key={emotion}
                    className={`inline-block px-3 py-2 rounded-full text-sm font-medium ${getEmotionColor(emotion)}`}
                  >
                    {emotionLabels[emotion] || emotion}
                  </div>
                ))}
              </div>
            </div>

            {/* Technical Details */}
            <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">
                Detalhes Técnicos
              </h3>
              <div className="space-y-3 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-600">Estilo:</span>
                  <span className="font-medium">{analysis.style || "Não especificado"}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Período:</span>
                  <span className="font-medium">{analysis.year || "Não especificado"}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Tempo de análise:</span>
                  <span className="font-medium">{analysis.processing_time.toFixed(2)}s</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Fonte:</span>
                  <span className="font-medium text-primary-600">Groq AI</span>
                </div>
              </div>
            </div>

            {/* Related Works */}
            <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">
                Obras Relacionadas
              </h3>
              <div className="space-y-2">
                <button className="text-left text-primary-600 hover:text-primary-700 text-sm">
                  • Girassóis (Van Gogh)
                </button>
                <button className="text-left text-primary-600 hover:text-primary-700 text-sm">
                  • O Quarto (Van Gogh)
                </button>
                <button className="text-left text-primary-600 hover:text-primary-700 text-sm">
                  • Campo de Trigo (Van Gogh)
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Bottom CTA */}
        <div className="mt-12 text-center">
          <div className="bg-gradient-to-r from-primary-600 to-primary-700 rounded-2xl p-8 text-white">
            <h3 className="text-2xl font-bold mb-4">
              Analise outra obra de arte
            </h3>
            <p className="text-primary-100 mb-6">
              Continue explorando o mundo da arte com nossa IA
            </p>
            <button
              onClick={() => navigate('/')}
              className="inline-flex items-center px-8 py-4 bg-white text-primary-700 rounded-xl font-semibold hover:bg-gray-50 transition-colors duration-200"
            >
              <Palette className="w-5 h-5 mr-2" />
              Analisar Nova Obra
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default AnalysisResult   
