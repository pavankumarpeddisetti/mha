const LogoDetection = ({ logoData }) => {
  if (!logoData) return null

  return (
    <div className="bg-white rounded-lg shadow-md p-6 transform transition-all duration-300 hover:shadow-xl">
      <h3 className="text-lg font-semibold mb-4 text-gray-800">
        Logo Detection
      </h3>
      {logoData.matches && logoData.matches.length > 0 ? (
        <div className="space-y-3">
          {logoData.matches.map((match, index) => (
            <div
              key={index}
              className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
            >
              <span className="text-sm font-medium text-gray-700">
                {match.name}
              </span>
              <div className="flex items-center space-x-2">
                <div className="w-32 bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-blue-600 h-2 rounded-full transition-all"
                    style={{ width: `${match.confidence * 100}%` }}
                  ></div>
                </div>
                <span className="text-sm font-semibold text-gray-900 w-12 text-right">
                  {(match.confidence * 100).toFixed(1)}%
                </span>
              </div>
            </div>
          ))}
          {logoData.flag && (
            <div className="mt-3 px-3 py-2 bg-yellow-50 border border-yellow-200 rounded text-sm text-yellow-800">
              ⚠️ Low confidence match detected
            </div>
          )}
        </div>
      ) : (
        <p className="text-sm text-gray-500">No logos detected</p>
      )}
    </div>
  )
}

export default LogoDetection

