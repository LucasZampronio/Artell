import { useState } from 'react'
import { Camera, Upload, Sparkles, ArrowRight } from 'lucide-react'

const AnalyzeImage = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [preview, setPreview] = useState<string | null>(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      setSelectedFile(file)
      const reader = new FileReader()
      reader.onload = (e) => setPreview(e.target?.result as string)
      reader.readAsDataURL(file)
    }
  }

  const handleAnalyze = async () => {
    if (!selectedFile) return
    
    setIsAnalyzing(true)
    // TODO: Implementar chamada para API
    setTimeout(() => setIsAnalyzing(false), 3000)
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Analisar Obra de Arte
          </h1>
          <p className="text-xl text-gray-600">
            Tire uma foto ou envie uma imagem para descobrir o significado da obra
          </p>
        </div>

        <div className="card max-w-2xl mx-auto">
          {/* Upload Area */}
          <div className="mb-8">
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-primary-400 transition-colors duration-200">
              <input
                type="file"
                accept="image/*"
                onChange={handleFileSelect}
                className="hidden"
                id="image-upload"
              />
              <label htmlFor="image-upload" className="cursor-pointer">
                {preview ? (
                  <div className="space-y-4">
                    <img
                      src={preview}
                      alt="Preview"
                      className="max-w-full h-64 object-cover rounded-lg mx-auto"
                    />
                    <p className="text-sm text-gray-500">
                      Clique para alterar a imagem
                    </p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    <div className="mx-auto w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center">
                      <Camera className="w-8 h-8 text-primary-600" />
                    </div>
                    <div>
                      <p className="text-lg font-medium text-gray-900">
                        Clique para selecionar uma imagem
                      </p>
                      <p className="text-sm text-gray-500 mt-1">
                        ou arraste e solte aqui
                      </p>
                    </div>
                    <p className="text-xs text-gray-400">
                      PNG, JPG, WebP até 10MB
                    </p>
                  </div>
                )}
              </label>
            </div>
          </div>

          {/* Analyze Button */}
          <button
            onClick={handleAnalyze}
            disabled={!selectedFile || isAnalyzing}
            className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isAnalyzing ? (
              <>
                <Sparkles className="w-5 h-5 mr-2 animate-pulse" />
                Analisando...
              </>
            ) : (
              <>
                <Sparkles className="w-5 h-5 mr-2" />
                Analisar com IA
              </>
            )}
          </button>

          {/* Instructions */}
          <div className="mt-8 p-4 bg-blue-50 rounded-lg">
            <h3 className="font-medium text-blue-900 mb-2">💡 Dicas para melhor análise:</h3>
            <ul className="text-sm text-blue-800 space-y-1">
              <li>• Certifique-se de que a imagem está bem iluminada</li>
              <li>• Capture a obra de arte completa</li>
              <li>• Evite reflexos e sombras excessivas</li>
              <li>• Para obras famosas, uma foto clara do rosto ou detalhes principais</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}

export default AnalyzeImage
