"""
Pydantic models for request/response schemas.
"""
from pydantic import BaseModel
from typing import List, Optional


class OCRData(BaseModel):
    """OCR extracted data model."""
    name: str = ""
    course: str = ""
    issuer: str = ""
    date: str = ""
    certificate_id: str = ""
    raw_text: str = ""


class MetadataData(BaseModel):
    """PDF metadata model."""
    created_date: str = ""
    modified_date: str = ""
    author: str = ""
    software: str = ""
    flags: List[str] = []


class QRData(BaseModel):
    """QR code verification model."""
    found: bool = False
    content: str = ""
    validation: str = "unverifiable"  # valid | invalid | unverifiable


class LogoMatch(BaseModel):
    """Logo match result model."""
    name: str
    confidence: float


class LogoDetectionData(BaseModel):
    """Logo detection results model."""
    matches: List[LogoMatch] = []
    flag: bool = False


class TamperReport(BaseModel):
    """Tamper detection report model."""
    score: float = 0.0
    heatmap: str = ""  # base64 encoded image


class TrustEvaluation(BaseModel):
    """Trust evaluation results model."""
    trust_score: int = 0
    verdict: str = "Unknown"  # Valid | Suspicious | Fake
    reasons: List[str] = []


class CertificateAnalysisResponse(BaseModel):
    """Complete certificate analysis response model."""
    certificate_preview: str = ""  # base64 encoded PNG
    ocr: OCRData
    metadata: MetadataData
    qr: QRData
    logo_detection: LogoDetectionData
    tamper_report: TamperReport
    trust_evaluation: TrustEvaluation

