"""
OCR text extraction service using PaddleOCR.
Extracts text fields from certificate image using PaddleOCR with field extraction.
"""
import re
from PIL import Image
import io
from app.models.schemas import OCRData
from app.ocr_utils import run_ocr


def extract_ocr_data(image: Image.Image) -> OCRData:
    """
    Extract text data from certificate image using PaddleOCR.
    
    Args:
        image: PIL Image object
        
    Returns:
        OCRData object with extracted fields
    """
    try:
        # Convert PIL Image to bytes for OCR
        img_buffer = io.BytesIO()
        image.save(img_buffer, format='PNG')
        image_bytes = img_buffer.getvalue()
        
        # Run PaddleOCR
        raw_text = run_ocr(image_bytes)
        
        # Extract structured fields using regex patterns
        name = extract_name(raw_text)
        course = extract_course(raw_text)
        issuer = extract_issuer(raw_text)
        date = extract_date(raw_text)
        certificate_id = extract_certificate_id(raw_text)
        
        return OCRData(
            name=name,
            course=course,
            issuer=issuer,
            date=date,
            certificate_id=certificate_id,
            raw_text=raw_text.strip()
        )
        
    except Exception as e:
        print(f"Error in OCR extraction: {str(e)}")
        return OCRData(raw_text="")


def extract_name(text: str) -> str:
    """Extract name from OCR text."""
    patterns = [
        r'(?:certify|certificate|awarded to|presented to|this is to certify that)[\s:]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
        r'(?:name|student|participant)[\s:]+([A-Z][a-z]+\s+[A-Z][a-z]+)',
        r'\b([A-Z][a-z]+\s+[A-Z][a-z]+)\b',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            name = match.group(1).strip()
            if name.lower() not in ['certificate', 'course', 'program', 'certification', 'this is']:
                if len(name.split()) >= 2:
                    return name
    return ""


def extract_course(text: str) -> str:
    """Extract course name from OCR text."""
    patterns = [
        r'(?:course|program|certification in|for|completed)[\s:]+([A-Z][A-Za-z\s&]+?)(?:has|successfully|completed|certificate|program)',
        r'(?:successfully completed|completed)[\s:]+([A-Z][A-Za-z\s&]+?)(?:course|program|certification)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            course = match.group(1).strip()
            if 3 < len(course) < 100 and not course.lower().startswith('has'):
                return course
    return ""


def extract_issuer(text: str) -> str:
    """Extract issuer/organization name from OCR text."""
    patterns = [
        r'(?:issued by|by|from|organization|certified by|awarded by)[\s:]+([A-Z][A-Za-z\s&.,-]+?)(?:on|date|$)',
        r'([A-Z][A-Z\s&.,-]+(?:University|College|Institute|Academy|Organization|Corporation|Inc|Ltd|Foundation))',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            issuer = match.group(1).strip()
            if len(issuer) > 3:
                return issuer
    return ""


def extract_date(text: str) -> str:
    """Extract date from OCR text."""
    patterns = [
        r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b',
        r'\b(\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4})\b',
        r'\b((?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4})\b',
        r'\b(?:date|on)[\s:]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return ""


def extract_certificate_id(text: str) -> str:
    """Extract certificate ID from OCR text."""
    patterns = [
        r'(?:certificate|cert|id|number|serial)[\s#:]+([A-Z0-9-]{5,})',
        r'(?:ID|No\.?|Number|Serial)[\s:]+([A-Z0-9-]{5,})',
        r'([A-Z]{2,}\d{4,})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            cert_id = match.group(1).strip()
            if len(cert_id) >= 5:
                return cert_id
    return ""
