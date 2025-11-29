const CertificatePreview = ({ previewImage }) => {
  if (!previewImage) return null

  return (
    <div className="bg-white rounded-lg shadow-md p-4 transform transition-all duration-300 hover:shadow-xl">
      <h3 className="text-lg font-semibold mb-4 text-gray-800">
        Certificate Preview
      </h3>
      <div className="border-2 border-gray-200 rounded-lg overflow-hidden group">
        <img
          src={`data:image/png;base64,${previewImage}`}
          alt="Certificate preview"
          className="w-full h-auto transition-transform duration-300 group-hover:scale-[1.02]"
        />
      </div>
    </div>
  )
}

export default CertificatePreview

