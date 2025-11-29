import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 120000, // 2 minutes timeout for analysis
})

/**
 * Analyze a certificate PDF file
 * @param {File} file - The PDF file to analyze
 * @returns {Promise} Analysis results matching CertificateAnalysisResponse schema
 */
export const analyzeCertificate = async (file) => {
  const formData = new FormData()
  formData.append('file', file)

  try {
    const response = await api.post('/api/analyze-certificate', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  } catch (error) {
    console.error('Error analyzing certificate:', error)
    // Extract error message from FastAPI error response
    if (error.response?.data?.detail) {
      throw new Error(error.response.data.detail)
    }
    if (error.message) {
      throw error
    }
    throw new Error('Failed to analyze certificate. Please try again.')
  }
}

/**
 * Health check endpoint
 * @returns {Promise} Health status
 */
export const checkHealth = async () => {
  try {
    const response = await api.get('/health')
    return response.data
  } catch (error) {
    console.error('Health check failed:', error)
    throw error
  }
}

export default api

