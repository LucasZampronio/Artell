// frontend/src/hooks/useArtImageAnalysis.ts

import { useState, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'

// A interface de resposta é a mesma da análise por texto, o que é ótimo!
interface AnalysisResponse {
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

interface UseArtImageAnalysisReturn {
  isLoading: boolean
  error: string | null
  analysis: AnalysisResponse | null
  analyzeImage: (file: File) => Promise<void>
  clearError: () => void
}

export const useArtImageAnalysis = (): UseArtImageAnalysisReturn => {
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [analysis, setAnalysis] = useState<AnalysisResponse | null>(null)
  const navigate = useNavigate()

  const clearError = useCallback(() => {
    setError(null)
  }, [])

  const analyzeImage = useCallback(async (file: File) => {
    setIsLoading(true)
    setError(null)

    // Usamos FormData para enviar ficheiros
    const formData = new FormData()
    formData.append('file', file)

    try {
      // O endpoint é 'analise-por-imagem' e o método é POST
      const response = await fetch('http://localhost:8001/analise-por-imagem', {
        method: 'POST',
        // Nota: Não definimos 'Content-Type'. O browser faz isso
        // automaticamente quando se usa FormData, incluindo o 'boundary' necessário.
        body: formData,
      })

      if (!response.ok) {
        const errorData = await response.json()
        // Tratamento de erros detalhado do backend
        throw new Error(errorData.detail || 'Erro ao analisar a imagem.')
      }

      const result: AnalysisResponse = await response.json()
      setAnalysis(result)
      
      // Navega para a página de resultados com o ID da análise
      if (result.id) {
        navigate(`/analysis/${result.id}`)
      } else {
        throw new Error("A resposta da API não continha um ID de análise.")
      }
      
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Ocorreu um erro desconhecido.'
      setError(errorMessage)
      console.error('Erro na análise da imagem:', err)
    } finally {
      setIsLoading(false)
    }
  }, [navigate])

  return {
    isLoading,
    error,
    analysis,
    analyzeImage,
    clearError,
  }
}