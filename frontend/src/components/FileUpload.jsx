import { useRef } from 'react'

const FileUpload = ({ onFileSelect, isProcessing }) => {
  const fileInputRef = useRef(null)

  const handleFileChange = (e) => {
    const file = e.target.files[0]
    if (file && file.type === 'application/pdf') {
      onFileSelect(file)
    } else {
      alert('Please select a PDF file')
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    const file = e.dataTransfer.files[0]
    if (file && file.type === 'application/pdf') {
      onFileSelect(file)
    } else {
      alert('Please drop a PDF file')
    }
  }

  const handleDragOver = (e) => {
    e.preventDefault()
  }

  return (
    <div
      className="w-full max-w-2xl mx-auto"
      onDrop={handleDrop}
      onDragOver={handleDragOver}
    >
      <div
        className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
          isProcessing
            ? 'border-gray-300 bg-gray-50'
            : 'border-blue-400 hover:border-blue-500 bg-blue-50'
        }`}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf"
          onChange={handleFileChange}
          className="hidden"
          disabled={isProcessing}
        />
        <div className="space-y-4">
          <svg
            className="mx-auto h-12 w-12 text-blue-500"
            stroke="currentColor"
            fill="none"
            viewBox="0 0 48 48"
          >
            <path
              d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
              strokeWidth={2}
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
          <div>
            <p className="text-lg font-semibold text-gray-700">
              {isProcessing ? 'Processing...' : 'Upload Certificate PDF'}
            </p>
            <p className="text-sm text-gray-500 mt-2">
              Drag and drop your PDF here, or click to browse
            </p>
          </div>
          <button
            onClick={() => fileInputRef.current?.click()}
            disabled={isProcessing}
            className={`px-6 py-2 rounded-md font-medium transition-colors ${
              isProcessing
                ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                : 'bg-blue-600 text-white hover:bg-blue-700'
            }`}
          >
            Select File
          </button>
        </div>
      </div>
    </div>
  )
}

export default FileUpload

