const VerdictBadge = ({ verdict, reasons }) => {
  if (!verdict) return null

  const getVerdictConfig = (verdict) => {
    const lowerVerdict = verdict.toLowerCase()
    if (lowerVerdict.includes('valid') || lowerVerdict.includes('authentic')) {
      return {
        color: 'bg-green-100 text-green-800 border-green-300',
        icon: '🟢',
        label: 'Valid',
      }
    }
    if (lowerVerdict.includes('suspicious')) {
      return {
        color: 'bg-yellow-100 text-yellow-800 border-yellow-300',
        icon: '🟡',
        label: 'Suspicious',
      }
    }
    if (lowerVerdict.includes('fake') || lowerVerdict.includes('invalid')) {
      return {
        color: 'bg-red-100 text-red-800 border-red-300',
        icon: '🔴',
        label: 'Fake',
      }
    }
    return {
      color: 'bg-gray-100 text-gray-800 border-gray-300',
      icon: '⚪',
      label: verdict,
    }
  }

  const config = getVerdictConfig(verdict)

  return (
    <div className="bg-white rounded-lg shadow-md p-6 transform transition-all duration-300 hover:shadow-xl">
      <h3 className="text-lg font-semibold mb-4 text-gray-800">
        Final Verdict
      </h3>
      <div className="space-y-4">
        <div
          className={`px-6 py-4 rounded-lg border-2 flex items-center justify-center space-x-3 ${config.color}`}
        >
          <span className="text-2xl">{config.icon}</span>
          <span className="text-xl font-bold">{config.label}</span>
        </div>
        {reasons && reasons.length > 0 && (
          <div>
            <h4 className="text-sm font-medium text-gray-700 mb-2">
              Reasons:
            </h4>
            <ul className="space-y-2">
              {reasons.map((reason, index) => (
                <li
                  key={index}
                  className="text-sm text-gray-600 bg-gray-50 px-3 py-2 rounded flex items-start"
                >
                  <span className="mr-2">•</span>
                  <span>{reason}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  )
}

export default VerdictBadge

