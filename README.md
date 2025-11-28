# EduCred — AI-Powered Certificate Authenticity Analyzer

A full-stack web application that analyzes PDF certificates using AI and computer vision to determine authenticity and generate trust scores.

## 🎯 Features

- **PDF Processing**: Converts PDF certificates to images for analysis
- **OCR Extraction**: Extracts text fields (name, course, issuer, date, etc.)
- **Metadata Analysis**: Checks PDF creation/modification timestamps
- **QR Verification**: Detects and validates QR codes
- **Logo Detection**: Matches logos against known issuer databases
- **Tamper Detection**: Identifies image manipulation and anomalies
- **Trust Scoring**: Generates weighted trust scores with detailed explanations

## 🏗️ Project Structure

```
/educred
 ├── backend/          # FastAPI backend
 ├── frontend/         # React + Vite frontend
 ├── docker-compose.yml
 └── README.md
```

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)
- Node.js 18+ (for local development)

### Using Docker

1. Clone the repository
2. Copy `.env.example` to `.env`
3. Run `docker-compose up`

### Local Development

#### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

## 📝 Environment Variables

See `.env.example` for configuration options.

## 🔧 Tech Stack

- **Backend**: Python, FastAPI
- **Frontend**: React, Vite, TailwindCSS
- **AI/CV**: OpenCV, Tesseract OCR, EasyOCR, PyMuPDF

## 📄 License

MIT

