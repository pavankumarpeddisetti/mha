"""
Simple OCR mode using PaddleOCR.

We ONLY extract the full raw_text and don't try to guess fields like
name, course, issuer, date, or certificate_id. Those stay empty strings.
"""
from PIL import Image
import io
from app.models.schemas import OCRData
from app.ocr_utils import run_ocr


def extract_ocr_data(image: Image.Image) -> OCRData:
    """
    Extract text data from certificate image using PaddleOCR.

    Returns:
        OCRData with raw_text filled, all other fields left empty.
    """
    try:
        # Convert PIL Image to bytes for OCR
        img_buffer = io.BytesIO()
        image.save(img_buffer, format="PNG")
        image_bytes = img_buffer.getvalue()

        # Run PaddleOCR (already defined in app.ocr_utils.run_ocr)
        raw_text = run_ocr(image_bytes) or ""

        # SIMPLE MODE: don't try to parse name/course/etc.
        return OCRData(
            name="",
            course="",
            issuer="",
            date="",
            certificate_id="",
            raw_text=raw_text.strip(),
        )

    except Exception as e:
        print(f"Error in OCR extraction: {str(e)}")
        # Return empty fields but keep structure
        return OCRData(
            name="",
            course="",
            issuer="",
            date="",
            certificate_id="",
            raw_text="",
        )
