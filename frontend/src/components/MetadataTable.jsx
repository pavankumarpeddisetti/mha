const MetadataTable = ({ metadata }) => {
  if (!metadata) return null

  const getFlagColor = (flag) => {
    if (flag.toLowerCase().includes('suspicious') || flag.toLowerCase().includes('modified')) {
      return 'text-red-600 bg-red-50'
    }
    return 'text-gray-600 bg-gray-50'
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6 transform transition-all duration-300 hover:shadow-xl">
      <h3 className="text-lg font-semibold mb-4 text-gray-800">
        PDF Metadata
      </h3>
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <tbody className="bg-white divide-y divide-gray-200">
            <tr>
              <td className="px-4 py-3 text-sm font-medium text-gray-700 bg-gray-50">
                Created Date
              </td>
              <td className="px-4 py-3 text-sm text-gray-900">
                {metadata.created_date || 'N/A'}
              </td>
            </tr>
            <tr>
              <td className="px-4 py-3 text-sm font-medium text-gray-700 bg-gray-50">
                Modified Date
              </td>
              <td className="px-4 py-3 text-sm text-gray-900">
                {metadata.modified_date || 'N/A'}
              </td>
            </tr>
            <tr>
              <td className="px-4 py-3 text-sm font-medium text-gray-700 bg-gray-50">
                Author
              </td>
              <td className="px-4 py-3 text-sm text-gray-900">
                {metadata.author || 'N/A'}
              </td>
            </tr>
            <tr>
              <td className="px-4 py-3 text-sm font-medium text-gray-700 bg-gray-50">
                Software
              </td>
              <td className="px-4 py-3 text-sm text-gray-900">
                {metadata.software || 'N/A'}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      {metadata.flags && metadata.flags.length > 0 && (
        <div className="mt-4">
          <h4 className="text-sm font-medium text-gray-700 mb-2">Flags</h4>
          <div className="space-y-2">
            {metadata.flags.map((flag, index) => (
              <div
                key={index}
                className={`px-3 py-2 rounded text-sm ${getFlagColor(flag)}`}
              >
                {flag}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default MetadataTable

