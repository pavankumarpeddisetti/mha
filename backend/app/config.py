"""
Configuration settings for the EduCred backend application.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).parent.parent

# API Configuration
API_PREFIX = os.getenv("API_PREFIX", "/api")
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")

# File Upload Configuration
MAX_UPLOAD_SIZE = int(os.getenv("MAX_UPLOAD_SIZE", 10485760))  # 10MB default
UPLOAD_DIR = BASE_DIR / os.getenv("UPLOAD_DIR", "uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# OCR Configuration
TESSERACT_CMD = os.getenv("TESSERACT_CMD", "/usr/bin/tesseract")

# Logo Detection Configuration
LOGOS_DIR = BASE_DIR / "app" / "assets" / "logos"
LOGOS_DIR.mkdir(parents=True, exist_ok=True)
LOGO_MATCH_THRESHOLD = float(os.getenv("LOGO_MATCH_THRESHOLD", "0.50"))

# Trust Scoring Weights
TRUST_WEIGHTS = {
    "ocr": float(os.getenv("WEIGHT_OCR", "0.20")),
    "metadata": float(os.getenv("WEIGHT_METADATA", "0.15")),
    "qr": float(os.getenv("WEIGHT_QR", "0.20")),
    "logo": float(os.getenv("WEIGHT_LOGO", "0.20")),
    "tamper": float(os.getenv("WEIGHT_TAMPER", "0.25")),
}

# Environment
ENV = os.getenv("ENV", "development")

