<button onClick={handleGenerateHash}>
  Generate Blockchain Hash
</button>


const handleGenerateHash = async () => {
  const formData = new FormData();
  formData.append("file", selectedFile);

  const res = await fetch("http://localhost:8000/api/generate-hash", {
    method: "POST",
    body: formData,
  });

  const data = await res.json();
  setHashValue(data.sha256);
};
