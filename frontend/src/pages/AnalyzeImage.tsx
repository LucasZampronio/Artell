// frontend/src/pages/AnalyzeImage.tsx

import { useState } from 'react'
import { Camera, Sparkles, AlertTriangle } from 'lucide-react'
// ✨ 1. Importar o nosso novo hook
import { useArtImageAnalysis } from '../hooks/useArtImageAnalysis'

const AnalyzeImage = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [preview, setPreview] = useState<string | null>(null)
  
  // ✨ 2. Instanciar o hook para obter as suas funções e estados
  const { isLoading, error, analyzeImage, clearError } = useArtImageAnalysis()

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    // Limpar erros anteriores ao selecionar um novo ficheiro
    if (error) clearError()

    const file = event.target.files?.[0]
    if (file) {
      // Validação simples do tamanho do ficheiro no frontend
      if (file.size > 10 * 1024 * 1024) { // 10MB
        alert("O ficheiro é muito grande. O tamanho máximo é 10MB.")
        return;
      }
      setSelectedFile(file)
      const reader = new FileReader()
      reader.onload = (e) => setPreview(e.target?.result as string)
      reader.readAsDataURL(file)
    }
  }

  const handleAnalyze = async () => {
    if (!selectedFile) return
    
    // ✨ 3. Chamar a função do hook para iniciar a análise
    await analyzeImage(selectedFile)
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4 font-serif">
            Analisar por Imagem
          </h1>
          <p className="text-xl text-gray-600">
            Envie uma imagem e deixe a nossa IA desvendar a sua história.
          </p>
        </div>

        <div className="bg-white rounded-2xl p-8 shadow-lg border border-gray-100 max-w-2xl mx-auto">
          {/* Upload Area */}
          <div className="mb-8">
            <label htmlFor="image-upload" className="cursor-pointer block border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-primary-400 transition-colors duration-200">
              <input
                type="file"
                accept="image/jpeg, image/png, image/webp"
                onChange={handleFileSelect}
                className="hidden"
                id="image-upload"
              />
              {preview ? (
                <div className="space-y-4">
                  <img
                    src={preview}
                    alt="Preview"
                    className="max-h-64 object-contain rounded-lg mx-auto"
                  />
                  <p className="text-sm text-gray-500">
                    {selectedFile?.name} ({Math.round(selectedFile?.size / 1024)} KB)
                  </p>
                  <span className="font-semibold text-primary-600">Clique para alterar a imagem</span>
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
                      ou arraste e solte o ficheiro aqui
                    </p>
                  </div>
                  <p className="text-xs text-gray-400">
                    PNG, JPG, ou WebP até 10MB
                  </p>
                </div>
              )}
            </label>
          </div>

          {/* Error Display */}
          {error && (
            <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-xl text-red-700 text-sm">
              <div className="flex items-center">
                <AlertTriangle className="w-5 h-5 mr-3" />
                <span>{error}</span>
              </div>
            </div>
          )}

          {/* Analyze Button */}
          <button
            onClick={handleAnalyze}
            disabled={!selectedFile || isLoading}
            className="w-full bg-gradient-to-r from-primary-600 to-primary-700 text-white px-8 py-4 rounded-xl font-semibold hover:from-primary-700 hover:to-primary-800 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 shadow-lg hover:shadow-xl text-lg inline-flex items-center justify-center"
          >
            {isLoading ? (
              <>
                <Sparkles className="w-5 h-5 mr-2 animate-pulse" />
                A analisar... (isto pode demorar um pouco)
              </>
            ) : (
              <>
                <Sparkles className="w-5 h-5 mr-2" />
                Analisar com IA
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  )
}

export default AnalyzeImage