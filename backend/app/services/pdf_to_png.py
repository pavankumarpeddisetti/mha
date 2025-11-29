"""
PDF to PNG conversion service - Optimized.
Converts PDF certificate to PNG image for analysis.
"""
from PIL import Image
import fitz  # PyMuPDF
import io
from typing import Optional


def convert_pdf_to_png(pdf_content: bytes, dpi: int = 200) -> Optional[Image.Image]:
    """
    Convert PDF content to PNG image - optimized for speed.
    
    Args:
        pdf_content: PDF file content as bytes
        dpi: Resolution for conversion (default 200 for speed)
        
    Returns:
        PIL Image object or None if conversion fails
    """
    try:
        # Open PDF from bytes
        pdf_document = fitz.open(stream=pdf_content, filetype="pdf")
        
        # Check if PDF has pages
        if pdf_document.page_count == 0:
            pdf_document.close()
            return None
        
        # Get first page (certificates are usually single page)
        page = pdf_document[0]
        
        # Convert page to image with optimized DPI (200 instead of 300 for speed)
        mat = fitz.Matrix(dpi / 72, dpi / 72)  # 72 is default DPI
        pix = page.get_pixmap(matrix=mat)
        
        # Convert to PIL Image
        img_data = pix.tobytes("png")
        image = Image.open(io.BytesIO(img_data))
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        pdf_document.close()
        return image
        
    except Exception as e:
        print(f"Error converting PDF to PNG: {str(e)}")
        return None
