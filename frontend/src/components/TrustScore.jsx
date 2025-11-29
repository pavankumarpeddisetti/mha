const TrustScore = ({ trustScore }) => {
  if (trustScore === null || trustScore === undefined) return null

  const getColor = (score) => {
    if (score >= 80) return 'text-green-600'
    if (score >= 60) return 'text-yellow-600'
    return 'text-red-600'
  }

  const getBgColor = (score) => {
    if (score >= 80) return 'bg-green-100'
    if (score >= 60) return 'bg-yellow-100'
    return 'bg-red-100'
  }

  const getStrokeColor = (score) => {
    if (score >= 80) return 'stroke-green-600'
    if (score >= 60) return 'stroke-yellow-600'
    return 'stroke-red-600'
  }

  // Calculate circumference for SVG circle (2 * π * r)
  const radius = 80
  const circumference = 2 * Math.PI * radius
  const offset = circumference - (trustScore / 100) * circumference

  return (
    <div className="bg-white rounded-lg shadow-md p-6 transform transition-all duration-300 hover:shadow-xl">
      <h3 className="text-lg font-semibold mb-4 text-gray-800 text-center">
        Trust Score
      </h3>
      <div className="flex flex-col items-center justify-center">
        <div className="relative w-48 h-48">
          <svg className="transform -rotate-90 w-48 h-48">
            {/* Background circle */}
            <circle
              cx="96"
              cy="96"
              r={radius}
              stroke="currentColor"
              strokeWidth="12"
              fill="none"
              className="text-gray-200"
            />
            {/* Progress circle */}
            <circle
              cx="96"
              cy="96"
              r={radius}
              stroke="currentColor"
              strokeWidth="12"
              fill="none"
              strokeDasharray={circumference}
              strokeDashoffset={offset}
              strokeLinecap="round"
              className={`transition-all duration-500 ${getStrokeColor(trustScore)}`}
            />
          </svg>
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="text-center">
              <div
                className={`text-4xl font-bold ${getColor(trustScore)}`}
              >
                {trustScore}
              </div>
              <div className="text-sm text-gray-500 mt-1">out of 100</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default TrustScore

