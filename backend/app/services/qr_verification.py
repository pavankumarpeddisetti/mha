"""
QR code detection and verification service using pyzbar.
Detects QR codes in certificate and validates their content.
"""
from PIL import Image
import io
import requests
from urllib.parse import urlparse
from app.models.schemas import QRData
from app.qr_utils import decode_qr_from_image


def verify_qr_code(image: Image.Image) -> QRData:
    """
    Detect and verify QR codes in certificate image using pyzbar.
    
    Args:
        image: PIL Image object
        
    Returns:
        QRData object with QR code information and validation status
    """
    try:
        # Convert PIL Image to bytes
        img_buffer = io.BytesIO()
        image.save(img_buffer, format='PNG')
        image_bytes = img_buffer.getvalue()
        
        # Decode QR codes using pyzbar
        qr_results = decode_qr_from_image(image_bytes)
        
        if qr_results and len(qr_results) > 0:
            # Get the first QR code found
            qr_data = qr_results[0]
            content = qr_data.get('data', '')
            
            # Validate QR code content
            validation = validate_qr_content(content)
            
            return QRData(
                found=True,
                content=content,
                validation=validation
            )
        else:
            return QRData(found=False, content="", validation="unverifiable")
        
    except Exception as e:
        print(f"Error in QR verification: {str(e)}")
        return QRData(found=False, content="", validation="unverifiable")


def validate_qr_content(content: str) -> str:
    """Validate QR code content."""
    if not content:
        return "unverifiable"
    
    try:
        parsed = urlparse(content)
        if parsed.scheme in ['http', 'https']:
            return verify_url(content)
        else:
            if len(content) > 10 and any(c.isalnum() for c in content):
                return "unverifiable"
            return "invalid"
    except:
        if len(content.strip()) > 0:
            return "unverifiable"
        return "invalid"


def verify_url(url: str, timeout: int = 3) -> str:
    """Verify if URL is accessible - optimized with shorter timeout."""
    try:
        response = requests.head(url, timeout=timeout, allow_redirects=True)
        if response.status_code == 200:
            return "valid"
        elif response.status_code in [301, 302, 303, 307, 308]:
            final_url = response.headers.get('Location', url)
            final_response = requests.head(final_url, timeout=timeout)
            if final_response.status_code == 200:
                return "valid"
            return "invalid"
        else:
            return "invalid"
    except requests.exceptions.Timeout:
        return "unverifiable"
    except requests.exceptions.ConnectionError:
        return "invalid"
    except:
        return "unverifiable"
