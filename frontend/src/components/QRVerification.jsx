const QRVerification = ({ qrData }) => {
  if (!qrData) return null

  const getStatusColor = (validation) => {
    switch (validation) {
      case 'valid':
        return 'bg-green-100 text-green-800 border-green-300'
      case 'invalid':
        return 'bg-red-100 text-red-800 border-red-300'
      case 'unverifiable':
        return 'bg-yellow-100 text-yellow-800 border-yellow-300'
      default:
        return 'bg-gray-100 text-gray-800 border-gray-300'
    }
  }

  const getStatusIcon = (validation) => {
    switch (validation) {
      case 'valid':
        return '✓'
      case 'invalid':
        return '✗'
      case 'unverifiable':
        return '?'
      default:
        return '—'
    }
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6 transform transition-all duration-300 hover:shadow-xl">
      <h3 className="text-lg font-semibold mb-4 text-gray-800">
        QR Code Verification
      </h3>
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <span className="text-sm font-medium text-gray-700">
            QR Code Found:
          </span>
          <span
            className={`px-3 py-1 rounded-full text-sm font-medium ${
              qrData.found
                ? 'bg-green-100 text-green-800'
                : 'bg-gray-100 text-gray-800'
            }`}
          >
            {qrData.found ? 'Yes' : 'No'}
          </span>
        </div>
        {qrData.found && (
          <>
            <div>
              <label className="text-sm font-medium text-gray-700">
                QR Content:
              </label>
              <p className="mt-1 text-sm text-gray-900 bg-gray-50 p-2 rounded break-all">
                {qrData.content || 'N/A'}
              </p>
            </div>
            <div>
              <label className="text-sm font-medium text-gray-700">
                Validation Status:
              </label>
              <div
                className={`mt-2 px-4 py-2 rounded-lg border-2 flex items-center justify-between ${getStatusColor(
                  qrData.validation
                )}`}
              >
                <span className="font-medium capitalize">
                  {qrData.validation || 'Unknown'}
                </span>
                <span className="text-xl font-bold">
                  {getStatusIcon(qrData.validation)}
                </span>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  )
}

export default QRVerification

