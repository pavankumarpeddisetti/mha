# EduCred Frontend

React + Vite frontend for the EduCred Certificate Authenticity Analyzer.

## Features

- Modern React 18 with Vite
- TailwindCSS for styling
- Responsive dashboard design
- Real-time certificate analysis visualization
- Component-based architecture

## Installation

```bash
npm install
```

## Development

```bash
npm run dev
```

## Build

```bash
npm run build
```

## Preview Production Build

```bash
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── components/     # Reusable UI components
│   ├── pages/          # Page components
│   ├── services/       # API services
│   ├── App.jsx         # Main app component
│   ├── main.jsx        # Entry point
│   └── index.css       # Global styles
├── index.html
├── package.json
└── vite.config.js
```

## Components

- **FileUpload**: PDF file upload with drag & drop
- **CertificatePreview**: Displays certificate image
- **OCRResults**: Shows extracted text fields
- **MetadataTable**: PDF metadata information
- **QRVerification**: QR code validation status
- **LogoDetection**: Logo matching results
- **HeatmapVisualization**: Tamper detection heatmap
- **TrustScore**: Circular gauge showing trust score
- **VerdictBadge**: Final verdict with reasons
- **LoadingSpinner**: Loading overlay

## Environment Variables

Create a `.env` file:

```
VITE_API_URL=http://localhost:8000
```

