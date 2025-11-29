import { useRef, useState } from 'react'

const FileUpload = ({ onFileSelect, isProcessing }) => {
  const fileInputRef = useRef(null)
  const [selectedFileName, setSelectedFileName] = useState('')
  const [isDragging, setIsDragging] = useState(false)

  const handleFile = (file) => {
    if (file && file.type === 'application/pdf') {
      setSelectedFileName(file.name)
      onFileSelect(file)
    } else {
      alert('Please select a PDF file')
    }
  }

  const handleFileChange = (e) => {
    const file = e.target.files[0]
    handleFile(file)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setIsDragging(false)
    const file = e.dataTransfer.files[0]
    handleFile(file)
  }

  const handleDragOver = (e) => {
    e.preventDefault()
    if (!isProcessing) setIsDragging(true)
  }

  const handleDragLeave = (e) => {
    e.preventDefault()
    setIsDragging(false)
  }

  return (
    <div
      className="w-full max-w-3xl mx-auto"
      onDrop={handleDrop}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
    >
      <div
        className={`relative overflow-hidden rounded-2xl p-[1px] transition-all duration-300 ${
          isProcessing
            ? 'bg-gradient-to-r from-gray-200 via-gray-100 to-gray-200'
            : isDragging
            ? 'bg-gradient-to-r from-blue-500 via-indigo-500 to-purple-500 shadow-2xl shadow-blue-300/40'
            : 'bg-gradient-to-r from-blue-400 via-indigo-500 to-purple-500 shadow-lg'
        }`}
      >
        <div
          className={`rounded-2xl bg-white/90 backdrop-blur-sm px-6 py-7 sm:px-10 sm:py-9 flex flex-col items-center text-center transition-all duration-300 ${
            isProcessing ? 'opacity-80 cursor-wait' : 'hover:bg-white'
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

          {/* Icon */}
          <div className="relative mb-4">
            <div className="absolute inset-0 bg-blue-100 rounded-full blur-2xl opacity-70" />
            <div className="relative flex items-center justify-center w-16 h-16 rounded-2xl bg-blue-50 text-blue-600 shadow-inner shadow-blue-100">
              <svg
                className="w-9 h-9"
                stroke="currentColor"
                fill="none"
                viewBox="0 0 48 48"
              >
                <path
                  d="M28 8H15a4 4 0 00-4 4v24a4 4 0 004 4h18a4 4 0 004-4V17.5L28 8z"
                  strokeWidth={2}
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
                <path
                  d="M28 8v8h9"
                  strokeWidth={2}
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
                <path
                  d="M18 28l4-4 4 4 4-4"
                  strokeWidth={2}
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
                <path
                  d="M20 32h8"
                  strokeWidth={2}
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
            </div>
          </div>

          {/* Text */}
          <div className="space-y-1 mb-4">
            <p className="text-xl font-semibold text-gray-900">
              {isProcessing ? 'Analyzing your certificate…' : 'Upload Certificate PDF'}
            </p>
            <p className="text-sm text-gray-500">
              Drag &amp; drop your PDF here, or{' '}
              <span className="font-semibold text-blue-600">click to browse</span>
            </p>
            {selectedFileName && !isProcessing && (
              <p className="text-xs text-gray-400 mt-1">
                Selected: <span className="font-medium text-gray-600">{selectedFileName}</span>
              </p>
            )}
          </div>

          {/* Button + Hint */}
          <div className="flex flex-col sm:flex-row items-center gap-3">
            <button
              onClick={() => !isProcessing && fileInputRef.current?.click()}
              disabled={isProcessing}
              className={`px-6 py-2.5 rounded-full font-medium text-sm shadow-md shadow-blue-200/70 transform transition-all duration-200 ${
                isProcessing
                  ? 'bg-gray-200 text-gray-500 cursor-not-allowed'
                  : 'bg-blue-600 text-white hover:bg-blue-700 hover:shadow-lg hover:-translate-y-0.5 active:translate-y-0'
              }`}
            >
              {isProcessing ? 'Processing…' : 'Select PDF'}
            </button>
            <span className="text-xs text-gray-400">
              Max size 10MB • PDF only • Secure local processing
            </span>
          </div>
        </div>
      </div>
    </div>
  )
}

export default FileUpload

