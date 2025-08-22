// frontend/src/hooks/useGallery.ts

import { useState, useEffect, useCallback } from 'react';

// A interface de resposta deve corresponder à que o backend envia
export interface Analysis {
  id: string;
  artwork_name: string;
  artist: string | null;
  year: string | null;
  style: string | null;
  emotions: string[];
  created_at?: string; // Adicionado para consistência, se o backend o enviar
}

interface UseGalleryReturn {
  analyses: Analysis[];
  isLoading: boolean;
  error: string | null;
  fetchAnalyses: () => void;
}

export const useGallery = (): UseGalleryReturn => {
  const [analyses, setAnalyses] = useState<Analysis[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchAnalyses = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      // Chamada ao endpoint GET /analyses que já existe no seu backend
      const response = await fetch('http://localhost:8001/analyses/?page=1&limit=50');

      if (!response.ok) {
        throw new Error('Não foi possível carregar as análises da galeria.');
      }

      const data: Analysis[] = await response.json();
      setAnalyses(data);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Ocorreu um erro desconhecido.';
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Efeito para carregar os dados quando o hook é usado pela primeira vez
  useEffect(() => {
    fetchAnalyses();
  }, [fetchAnalyses]);

  return { analyses, isLoading, error, fetchAnalyses };
};