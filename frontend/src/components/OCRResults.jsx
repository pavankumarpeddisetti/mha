const OCRResults = ({ ocrData }) => {
  if (!ocrData) return null

  return (
    <div className="bg-white rounded-lg shadow-md p-6 transform transition-all duration-300 hover:shadow-xl">
      <h3 className="text-lg font-semibold mb-4 text-gray-800">
        Extracted Information
      </h3>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="text-sm font-medium text-gray-600">Name</label>
          <p className="mt-1 text-gray-900 bg-gray-50 p-2 rounded">
            {ocrData.name || 'Not found'}
          </p>
        </div>
        <div>
          <label className="text-sm font-medium text-gray-600">Course</label>
          <p className="mt-1 text-gray-900 bg-gray-50 p-2 rounded">
            {ocrData.course || 'Not found'}
          </p>
        </div>
        <div>
          <label className="text-sm font-medium text-gray-600">Issuer</label>
          <p className="mt-1 text-gray-900 bg-gray-50 p-2 rounded">
            {ocrData.issuer || 'Not found'}
          </p>
        </div>
        <div>
          <label className="text-sm font-medium text-gray-600">Date</label>
          <p className="mt-1 text-gray-900 bg-gray-50 p-2 rounded">
            {ocrData.date || 'Not found'}
          </p>
        </div>
        <div className="md:col-span-2">
          <label className="text-sm font-medium text-gray-600">
            Certificate ID
          </label>
          <p className="mt-1 text-gray-900 bg-gray-50 p-2 rounded">
            {ocrData.certificate_id || 'Not found'}
          </p>
        </div>
        <div className="md:col-span-2">
          <label className="text-sm font-medium text-gray-600">Raw Text</label>
          <div className="mt-1 text-sm text-gray-700 bg-gray-50 p-3 rounded max-h-40 overflow-y-auto">
            {ocrData.raw_text || 'No text extracted'}
          </div>
        </div>
      </div>
    </div>
  )
}

export default OCRResults

