import { useState } from 'react'
import { Link } from 'react-router-dom'
import { Camera, Search, Sparkles, Palette, Heart, Eye, ArrowRight, Star, Users, Zap, BookOpen } from 'lucide-react'
import { useArtAnalysis } from '../hooks/useArtAnalysis'

const Home = () => {
  const [searchQuery, setSearchQuery] = useState('')
  const { isLoading, error, analyzeArtwork, clearError } = useArtAnalysis()

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!searchQuery.trim()) return

    await analyzeArtwork(searchQuery)
  }

  const features = [
    {
      icon: <Camera className="w-6 h-6" />,
      title: "Analise por Imagem",
      description: "Tire uma foto ou envie uma imagem de uma obra de arte para análise instantânea"
    },
    {
      icon: <Search className="w-6 h-6" />,
      title: "Pesquise por Nome",
      description: "Digite o nome da obra e descubra seu significado e história"
    },
    {
      icon: <Sparkles className="w-6 h-6" />,
      title: "IA Avançada",
      description: "Análises detalhadas usando Groq com modelo Llama 4 Scout de 17B parâmetros"
    }
  ]

  const benefits = [
    {
      icon: <Heart className="w-6 h-6" />,
      title: "Descubra Emoções",
      description: "Entenda os sentimentos e emoções que cada obra de arte evoca"
    },
    {
      icon: <Eye className="w-6 h-6" />,
      title: "Significado Profundo",
      description: "Revele o significado oculto e a intenção do artista por trás de cada obra"
    },
    {
      icon: <Palette className="w-6 h-6" />,
      title: "Contexto Histórico",
      description: "Aprenda sobre o período, movimento artístico e influências culturais"
    }
  ]

  const stats = [
    { number: "1000+", label: "Obras Analisadas" },
    { number: "50+", label: "Estilos Artísticos" },
    { number: "24/7", label: "Disponibilidade" },
    { number: "0€", label: "Custo" }
  ]

  const popularArtworks = [
    "Mona Lisa",
    "A Noite Estrelada",
    "O Grito",
    "Guernica",
    "A Persistência da Memória",
    "O Nascimento de Vênus"
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-white">
      {/* Hero Section */}
      <section className="relative py-20 px-4 sm:px-6 lg:px-8 overflow-hidden">
        <div className="max-w-7xl mx-auto">
          {/* Background Pattern */}
          <div className="absolute inset-0 opacity-5">
            <div className="absolute inset-0" style={{
              backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%239C92AC' fill-opacity='0.4'%3E%3Ccircle cx='30' cy='30' r='2'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
            }} />
          </div>

          <div className="relative text-center">
            {/* Main Heading */}
            <h1 className="text-5xl md:text-7xl font-bold text-gray-900 mb-6 leading-tight">
              Descubra o
              <span className="block text-transparent bg-clip-text bg-gradient-to-r from-primary-600 to-primary-800">
                significado
              </span>
              das obras de arte
            </h1>

            {/* Subtitle */}
            <p className="text-xl md:text-2xl text-gray-600 mb-12 max-w-4xl mx-auto leading-relaxed">
              Artell utiliza inteligência artificial avançada para analisar obras de arte e revelar seus 
              <span className="font-semibold text-primary-700"> significados ocultos</span>, 
              <span className="font-semibold text-primary-700"> intenções do artista</span> e as 
              <span className="font-semibold text-primary-700"> emoções que evocam</span>.
            </p>

            {/* Search Bar */}
            <div className="max-w-2xl mx-auto mb-12">
              <form onSubmit={handleSearch} className="relative">
                <div className="relative">
                  <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 w-6 h-6 text-gray-400" />
                  <input
                    type="text"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    placeholder="Digite o nome de uma obra de arte..."
                    className="w-full pl-14 pr-32 py-4 text-lg border-2 border-gray-200 rounded-2xl focus:border-primary-500 focus:ring-4 focus:ring-primary-100 transition-all duration-200 shadow-lg"
                  />
                  <button
                    type="submit"
                    disabled={!searchQuery.trim() || isLoading}
                    className="absolute right-2 top-1/2 transform -translate-y-1/2 bg-gradient-to-r from-primary-600 to-primary-700 text-white px-8 py-3 rounded-xl font-semibold hover:from-primary-700 hover:to-primary-800 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 shadow-lg hover:shadow-xl"
                  >
                    {isLoading ? (
                      <div className="flex items-center">
                        <Sparkles className="w-5 h-5 mr-2 animate-pulse" />
                        Analisando...
                      </div>
                    ) : (
                      <div className="flex items-center">
                        <Sparkles className="w-5 h-5 mr-2" />
                        Analisar
                      </div>
                    )}
                  </button>
                </div>
              </form>

              {/* Error Display */}
              {error && (
                <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-xl text-red-700 text-sm">
                  <div className="flex items-center justify-between">
                    <span>{error}</span>
                    <button
                      onClick={clearError}
                      className="text-red-500 hover:text-red-700 font-medium"
                    >
                      ✕
                    </button>
                  </div>
                </div>
              )}
            </div>

            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
              <Link
                to="/analyze/image"
                className="inline-flex items-center px-8 py-4 bg-white border-2 border-primary-600 text-primary-700 rounded-2xl font-semibold hover:bg-primary-50 transition-all duration-200 shadow-lg hover:shadow-xl"
              >
                <Camera className="w-5 h-5 mr-2" />
                Analisar por Imagem
                <ArrowRight className="w-5 h-5 ml-2" />
              </Link>
              <Link
                to="/gallery"
                className="inline-flex items-center px-8 py-4 bg-gray-900 text-white rounded-2xl font-semibold hover:bg-gray-800 transition-all duration-200 shadow-lg hover:shadow-xl"
              >
                <BookOpen className="w-5 h-5 mr-2" />
                Ver Galeria
                <ArrowRight className="w-5 h-5 ml-2" />
              </Link>
            </div>

            {/* Popular Searches */}
            <div className="mt-12">
              <p className="text-gray-500 mb-4">Obras populares:</p>
              <div className="flex flex-wrap justify-center gap-2">
                {popularArtworks.map((artwork) => (
                  <button
                    key={artwork}
                    onClick={() => setSearchQuery(artwork)}
                    className="px-4 py-2 bg-white border border-gray-200 rounded-full text-gray-700 hover:border-primary-300 hover:text-primary-700 transition-all duration-200 text-sm"
                  >
                    {artwork}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-white">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
              Como funciona o Artell?
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Nossa tecnologia de IA analisa obras de arte em segundos, fornecendo insights 
              profundos sobre significado, contexto histórico e emoções evocadas.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <div
                key={index}
                className="text-center p-8 rounded-2xl bg-gradient-to-br from-gray-50 to-white border border-gray-100 hover:border-primary-200 hover:shadow-xl transition-all duration-300"
              >
                <div className="w-16 h-16 bg-gradient-to-br from-primary-500 to-primary-600 rounded-2xl flex items-center justify-center mx-auto mb-6 text-white">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-4">
                  {feature.title}
                </h3>
                <p className="text-gray-600 leading-relaxed">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-br from-primary-50 to-primary-100">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
              Por que escolher o Artell?
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Descubra as vantagens de usar nossa plataforma para entender melhor as obras de arte.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {benefits.map((benefit, index) => (
              <div
                key={index}
                className="text-center p-8 rounded-2xl bg-white border border-gray-100 hover:shadow-xl transition-all duration-300"
              >
                <div className="w-16 h-16 bg-gradient-to-br from-primary-500 to-primary-600 rounded-2xl flex items-center justify-center mx-auto mb-6 text-white">
                  {benefit.icon}
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-4">
                  {benefit.title}
                </h3>
                <p className="text-gray-600 leading-relaxed">
                  {benefit.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gray-900">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
              Números que impressionam
            </h2>
            <p className="text-xl text-gray-300 max-w-3xl mx-auto">
              Milhares de usuários já descobriram o poder do Artell para análise de arte.
            </p>
          </div>

          <div className="grid md:grid-cols-4 gap-8">
            {stats.map((stat, index) => (
              <div key={index} className="text-center">
                <div className="text-4xl md:text-5xl font-bold text-primary-400 mb-2">
                  {stat.number}
                </div>
                <div className="text-gray-300 text-lg">
                  {stat.label}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-r from-primary-600 to-primary-800">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
            Pronto para descobrir o significado das obras de arte?
          </h2>
          <p className="text-xl text-primary-100 mb-6">
            Junte-se a milhares de usuários que já transformaram sua experiência com arte através do Artell.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button
              onClick={() => setSearchQuery('Mona Lisa')}
              className="inline-flex items-center px-8 py-4 bg-white text-primary-700 rounded-2xl font-semibold hover:bg-gray-50 transition-all duration-200 shadow-lg hover:shadow-xl"
            >
              <Search className="w-5 h-5 mr-2" />
              Começar Agora
              <ArrowRight className="w-5 h-5 ml-2" />
            </button>
            <Link
              to="/gallery"
              className="inline-flex items-center px-8 py-4 border-2 border-white text-white rounded-2xl font-semibold hover:bg-white hover:text-primary-700 transition-all duration-200"
            >
              <BookOpen className="w-5 h-5 mr-2" />
              Ver Exemplos
            </Link>
          </div>
        </div>
      </section>
    </div>
  )
}

export default Home
