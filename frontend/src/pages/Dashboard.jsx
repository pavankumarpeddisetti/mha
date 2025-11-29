import { useState } from 'react'
import FileUpload from '../components/FileUpload'
import CertificatePreview from '../components/CertificatePreview'
import OCRResults from '../components/OCRResults'
import MetadataTable from '../components/MetadataTable'
import QRVerification from '../components/QRVerification'
import LogoDetection from '../components/LogoDetection'
import HeatmapVisualization from '../components/HeatmapVisualization'
import TrustScore from '../components/TrustScore'
import VerdictBadge from '../components/VerdictBadge'
import LoadingSpinner from '../components/LoadingSpinner'
import { analyzeCertificate } from '../services/api'

const Dashboard = () => {
  const [isProcessing, setIsProcessing] = useState(false)
  const [analysisResult, setAnalysisResult] = useState(null)
  const [error, setError] = useState(null)
  const [progress, setProgress] = useState(null)

  const handleFileSelect = async (file) => {
    setIsProcessing(true)
    setError(null)
    setAnalysisResult(null)
    setProgress(0)

    // Simulate progress updates
    const progressInterval = setInterval(() => {
      setProgress((prev) => {
        if (prev === null) return 10
        if (prev >= 90) return prev
        return prev + Math.random() * 15
      })
    }, 500)

    try {
      const result = await analyzeCertificate(file)
      setProgress(100)
      setTimeout(() => {
        setAnalysisResult(result)
        setIsProcessing(false)
        setProgress(null)
        clearInterval(progressInterval)
      }, 300)
    } catch (err) {
      clearInterval(progressInterval)
      setError(
        err.response?.data?.detail || err.message || 'Failed to analyze certificate'
      )
      console.error('Analysis error:', err)
      setIsProcessing(false)
      setProgress(null)
    }
  }

  const handleDownloadReport = () => {
    if (!analysisResult) return

    const report = {
      timestamp: new Date().toISOString(),
      analysis: analysisResult,
    }

    const blob = new Blob([JSON.stringify(report, null, 2)], {
      type: 'application/json',
    })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `certificate-analysis-${Date.now()}.json`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      {/* Header */}
      <header className="bg-white shadow-md sticky top-0 z-40 backdrop-blur-sm bg-opacity-95">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
            EduCred — Certificate Authenticity Analyzer
          </h1>
          <p className="text-sm text-gray-600 mt-1">
            AI-Powered Certificate Verification Platform
          </p>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Upload Section */}
        <div className="mb-8 transform transition-all duration-300">
          <FileUpload onFileSelect={handleFileSelect} isProcessing={isProcessing} />
        </div>

        {/* Error Display */}
        {error && (
          <div className="mb-6 bg-red-50 border-l-4 border-red-400 rounded-lg p-4 animate-slideInLeft shadow-md">
            <div className="flex items-center">
              <span className="text-red-600 mr-2 text-xl">⚠️</span>
              <p className="text-red-800 font-medium">{error}</p>
            </div>
          </div>
        )}

        {/* Results Section with Animations */}
        {analysisResult && (
          <div className="space-y-6 animate-fadeInUp">
            {/* Top Row: Trust Score and Verdict */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="animate-slideInLeft delay-100">
                <TrustScore trustScore={analysisResult.trust_evaluation?.trust_score} />
              </div>
              <div className="animate-slideInRight delay-100">
                <VerdictBadge
                  verdict={analysisResult.trust_evaluation?.verdict}
                  reasons={analysisResult.trust_evaluation?.reasons}
                />
              </div>
            </div>

            {/* Certificate Preview */}
            {analysisResult.certificate_preview && (
              <div className="animate-fadeIn delay-200">
                <CertificatePreview
                  previewImage={analysisResult.certificate_preview}
                />
              </div>
            )}

            {/* Analysis Results Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="animate-slideInLeft delay-300">
                <OCRResults ocrData={analysisResult.ocr} />
              </div>
              <div className="animate-slideInRight delay-300">
                <MetadataTable metadata={analysisResult.metadata} />
              </div>
              <div className="animate-slideInLeft delay-400">
                <QRVerification qrData={analysisResult.qr} />
              </div>
              <div className="animate-slideInRight delay-400">
                <LogoDetection logoData={analysisResult.logo_detection} />
              </div>
            </div>

            {/* Heatmap */}
            {analysisResult.tamper_report && (
              <div className="animate-fadeIn delay-500">
                <HeatmapVisualization
                  heatmapImage={analysisResult.tamper_report.heatmap}
                  tamperScore={analysisResult.tamper_report.score}
                />
              </div>
            )}

            {/* Download Report Button */}
            <div className="flex justify-center animate-fadeIn delay-600">
              <button
                onClick={handleDownloadReport}
                className="px-8 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-medium rounded-lg hover:from-blue-700 hover:to-indigo-700 transition-all duration-300 shadow-lg hover:shadow-xl transform hover:scale-105"
              >
                📥 Download Analysis Report
              </button>
            </div>
          </div>
        )}

        {/* Empty State */}
        {!analysisResult && !isProcessing && !error && (
          <div className="text-center py-12 animate-fadeIn">
            <div className="inline-block p-4 bg-white rounded-full shadow-lg mb-4">
              <svg
                className="w-16 h-16 text-blue-500"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                />
              </svg>
            </div>
            <p className="text-gray-600 text-lg font-medium">
              Upload a PDF certificate to begin analysis
            </p>
            <p className="text-gray-500 text-sm mt-2">
              Our AI will analyze the certificate for authenticity
            </p>
          </div>
        )}
      </main>

      {/* Loading Overlay */}
      {isProcessing && <LoadingSpinner progress={progress} />}
    </div>
  )
}

export default Dashboard
