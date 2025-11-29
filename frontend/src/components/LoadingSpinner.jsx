const LoadingSpinner = ({ message = 'Analyzing certificate...', progress = null }) => {
  const steps = [
    'Converting PDF to image...',
    'Extracting text with OCR...',
    'Analyzing metadata...',
    'Detecting QR codes...',
    'Matching logos...',
    'Detecting tampering...',
    'Calculating trust score...',
  ]

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 animate-fadeIn">
      <div className="bg-white rounded-xl p-8 max-w-md w-full mx-4 shadow-2xl transform transition-all animate-slideUp">
        <div className="flex flex-col items-center space-y-6">
          {/* Animated Spinner */}
          <div className="relative">
            <div className="animate-spin rounded-full h-20 w-20 border-4 border-blue-200 border-t-blue-600"></div>
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="h-12 w-12 bg-blue-600 rounded-full animate-pulse"></div>
            </div>
          </div>

          {/* Progress Message */}
          <div className="text-center space-y-2">
            <p className="text-lg font-semibold text-gray-800">{message}</p>
            {progress !== null && (
              <div className="w-64 bg-gray-200 rounded-full h-2 overflow-hidden">
                <div
                  className="bg-blue-600 h-2 rounded-full transition-all duration-300 ease-out"
                  style={{ width: `${progress}%` }}
                ></div>
              </div>
            )}
            <p className="text-sm text-gray-500">
              {progress !== null ? `${Math.round(progress)}% complete` : 'This may take a few moments...'}
            </p>
          </div>

          {/* Processing Steps */}
          <div className="w-full space-y-2">
            {steps.map((step, index) => (
              <div
                key={index}
                className={`text-xs text-gray-600 px-3 py-1 rounded transition-all duration-300 ${
                  progress !== null && index < (progress / 100) * steps.length
                    ? 'bg-green-50 text-green-700'
                    : 'bg-gray-50'
                }`}
              >
                {step}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default LoadingSpinner
