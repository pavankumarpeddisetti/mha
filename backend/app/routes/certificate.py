"""
Certificate analysis & hashing routes - unified module
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models.schemas import CertificateAnalysisResponse
from app.services.pdf_to_png import convert_pdf_to_png
from app.services.ocr_extraction import extract_ocr_data
from app.services.metadata_parser import parse_metadata
from app.services.qr_verification import verify_qr_code
from app.services.logo_detection import detect_logos
from app.services.tamper_detection import detect_tampering
from app.services.trust_scoring import calculate_trust_score
from app.services.blockchain_hash import generate_sha256_hash

import base64
import io
from PIL import Image

router = APIRouter(tags=["certificate"])


@router.post("/analyze-certificate", response_model=CertificateAnalysisResponse)
async def analyze_certificate(file: UploadFile = File(...)):
    """
    Analyze a PDF certificate for authenticity - optimized for speed.
    """
    try:
        # Validate file type
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="File must be a PDF")

        # Read file content
        file_content = await file.read()

        # Step 1: Convert PDF to PNG
        certificate_image = convert_pdf_to_png(file_content)
        if not certificate_image:
            raise HTTPException(status_code=400, detail="Failed to convert PDF to image")

        # Resize image for faster processing
        original_image = certificate_image.copy()
        img_array = certificate_image.size
        max_dim = 1200
        if max(img_array) > max_dim:
            ratio = max_dim / max(img_array)
            new_size = (int(img_array[0] * ratio), int(img_array[1] * ratio))
            certificate_image = certificate_image.resize(new_size, Image.Resampling.LANCZOS)

        # Encode original image to base64 for preview
        img_buffer = io.BytesIO()
        original_image.save(img_buffer, format='PNG', optimize=True)
        preview_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')

        # Step 2: Extract OCR data
        ocr_data = extract_ocr_data(certificate_image)

        # Step 3: Parse metadata
        metadata = parse_metadata(file_content)

        # Step 4: Verify QR code
        qr_data = verify_qr_code(certificate_image)

        # Step 5: Detect logos
        logo_data = detect_logos(certificate_image)

        # Step 6: Detect tampering
        tamper_report = detect_tampering(certificate_image)

        # Step 7: Calculate trust score
        trust_evaluation = calculate_trust_score(
            ocr_data=ocr_data,
            metadata=metadata,
            qr_data=qr_data,
            logo_data=logo_data,
            tamper_report=tamper_report
        )

        # Build response
        response = CertificateAnalysisResponse(
            certificate_preview=preview_base64,
            ocr=ocr_data,
            metadata=metadata,
            qr=qr_data,
            logo_detection=logo_data,
            tamper_report=tamper_report,
            trust_evaluation=trust_evaluation
        )

        return response

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.post("/generate-hash")
async def generate_certificate_hash(file: UploadFile = File(...)):
    """
    Generate SHA-256 hash of certificate text.
    """
    try:
        file_bytes = await file.read()

        # Extract text (OCR or fallback)
        result = extract_ocr_data(file_bytes)
        text = result.get("text", "")

        # Generate hash
        sha_value = generate_sha256_hash(text)

        return {
            "sha256": sha_value,
            "text_length": len(text),
            "source_used": result.get("source", "unknown")
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hash generation failed: {str(e)}")