"""
OCR utilities using PaddleOCR for high-accuracy text extraction.
"""
import fitz  # PyMuPDF
import numpy as np
import cv2
from paddleocr import PaddleOCR
from PIL import Image
import io

# Initialize PaddleOCR once (reuse across requests)
ocr = PaddleOCR(use_angle_cls=True, lang='en')


def pdf_to_images(file_bytes):
    """Convert PDF pages to high-quality PNG images."""
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    images = []
    for page in doc:
        pix = page.get_pixmap(dpi=300)
        images.append(pix.pil_tobytes(format="PNG"))
    doc.close()
    return images


def preprocess_image(image_bytes):
    """Preprocessing steps for maximizing OCR accuracy."""
    img = Image.open(io.BytesIO(image_bytes))
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Bilateral filter for noise reduction while preserving edges
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    # Otsu thresholding for optimal binarization
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh


def run_ocr(image_bytes):
    """Execute OCR on a preprocessed image using PaddleOCR."""
    try:
        img = preprocess_image(image_bytes)
        result = ocr.ocr(img, cls=True)
        
        text = ""
        if result and result[0]:
            for line in result[0]:
                if line and len(line) > 1:
                    text += line[1][0] + " "
        
        return text.strip()
    except Exception as e:
        print(f"OCR error: {str(e)}")
        return ""

