const HeatmapVisualization = ({ heatmapImage, tamperScore }) => {
  if (!heatmapImage) return null

  const getScoreColor = (score) => {
    if (score > 0.7) return 'text-red-600 bg-red-50 border-red-300'
    if (score > 0.4) return 'text-yellow-600 bg-yellow-50 border-yellow-300'
    return 'text-green-600 bg-green-50 border-green-300'
  }

  const getScoreLabel = (score) => {
    if (score > 0.7) return 'High Risk'
    if (score > 0.4) return 'Moderate Risk'
    return 'Low Risk'
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6 transform transition-all duration-300 hover:shadow-xl">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-800">
          Tamper Detection Heatmap
        </h3>
        {tamperScore !== null && tamperScore !== undefined && (
          <div
            className={`px-4 py-2 rounded-lg border-2 font-semibold ${getScoreColor(
              tamperScore
            )}`}
          >
            {getScoreLabel(tamperScore)}: {(tamperScore * 100).toFixed(1)}%
          </div>
        )}
      </div>

      <div className="space-y-4">
        {/* Heatmap Image with Overlay */}
        <div className="relative border-2 border-gray-200 rounded-lg overflow-hidden group">
          <img
            src={`data:image/png;base64,${heatmapImage}`}
            alt="Tamper detection heatmap"
            className="w-full h-auto transition-transform duration-300 group-hover:scale-105"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent pointer-events-none"></div>
        </div>

        {/* Legend */}
        <div className="flex items-center justify-between text-sm">
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 bg-blue-500 rounded"></div>
            <span className="text-gray-600">Low Tamper Risk</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 bg-yellow-500 rounded"></div>
            <span className="text-gray-600">Moderate Risk</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 bg-red-500 rounded"></div>
            <span className="text-gray-600">High Tamper Risk</span>
          </div>
        </div>

        {/* Explanation */}
        <div className="bg-gray-50 rounded-lg p-4 border-l-4 border-blue-500">
          <p className="text-sm text-gray-700">
            <strong>Heatmap Analysis:</strong> This visualization shows areas of potential
            tampering detected through compression artifact analysis, noise pattern detection,
            and edge consistency checks. Red areas indicate higher suspicion of manipulation.
          </p>
        </div>
      </div>
    </div>
  )
}

export default HeatmapVisualization
