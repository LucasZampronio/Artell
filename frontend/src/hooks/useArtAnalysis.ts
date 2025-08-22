import { useState, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'

interface AnalysisRequest {
  artwork_name: string
}

interface AnalysisResponse {
  artwork: string
  analysis: string
  artist?: string
  year?: string
  style?: string
  emotions: string[]
  processing_time: number
  cached: boolean
}

interface UseArtAnalysisReturn {
  isLoading: boolean
  error: string | null
  analysis: AnalysisResponse | null
  analyzeArtwork: (artworkName: string) => Promise<void>
  clearError: () => void
  resetAnalysis: () => void
}

export const useArtAnalysis = (): UseArtAnalysisReturn => {
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [analysis, setAnalysis] = useState<AnalysisResponse | null>(null)
  const navigate = useNavigate()

  const clearError = useCallback(() => {
    setError(null)
  }, [])

  const resetAnalysis = useCallback(() => {
    setAnalysis(null)
    setError(null)
  }, [])

  const analyzeArtwork = useCallback(async (artworkName: string) => {
    if (!artworkName.trim()) {
      setError('Nome da obra de arte é obrigatório')
      return
    }

    setIsLoading(true)
    setError(null)

    try {
      const response = await fetch('http://localhost:8001/analise-por-nome', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ artwork_name: artworkName } as AnalysisRequest),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Erro na análise da obra de arte')
      }

      const result: AnalysisResponse = await response.json()
      setAnalysis(result)
      
      // Redirecionar para página de resultado
      navigate(`/analysis/${Date.now()}`) // Usar timestamp como ID temporário
      
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Erro desconhecido na análise'
      setError(errorMessage)
      console.error('Erro na análise:', err)
    } finally {
      setIsLoading(false)
    }
  }, [navigate])

  return {
    isLoading,
    error,
    analysis,
    analyzeArtwork,
    clearError,
    resetAnalysis,
  }
}
