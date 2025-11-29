"""
Trust score calculation service.
Calculates weighted trust score based on all analysis results.
"""
from app.models.schemas import (
    OCRData, MetadataData, QRData, LogoDetectionData,
    TamperReport, TrustEvaluation
)
from app.config import TRUST_WEIGHTS


def calculate_trust_score(
    ocr_data: OCRData,
    metadata: MetadataData,
    qr_data: QRData,
    logo_data: LogoDetectionData,
    tamper_report: TamperReport
) -> TrustEvaluation:
    """
    Calculate weighted trust score based on all analysis results.
    
    Args:
        ocr_data: OCR extraction results
        metadata: PDF metadata results
        qr_data: QR verification results
        logo_data: Logo detection results
        tamper_report: Tamper detection results
        
    Returns:
        TrustEvaluation with trust score, verdict, and reasons
    """
    scores = {}
    reasons = []
    
    # 1. OCR Score (0-100)
    ocr_score = calculate_ocr_score(ocr_data)
    scores['ocr'] = ocr_score
    if ocr_score < 50:
        reasons.append("Missing or incomplete certificate information")
    
    # 2. Metadata Score (0-100)
    metadata_score = calculate_metadata_score(metadata)
    scores['metadata'] = metadata_score
    if metadata.flags:
        reasons.extend(metadata.flags)
    
    # 3. QR Score (0-100)
    qr_score = calculate_qr_score(qr_data)
    scores['qr'] = qr_score
    if qr_data.found and qr_data.validation == 'invalid':
        reasons.append("QR code verification failed")
    elif not qr_data.found:
        reasons.append("No QR code found for verification")
    
    # 4. Logo Score (0-100)
    logo_score = calculate_logo_score(logo_data)
    scores['logo'] = logo_score
    if logo_data.flag:
        reasons.append("Low confidence logo matches detected")
    elif not logo_data.matches:
        reasons.append("No recognized issuer logos found")
    
    # 5. Tamper Score (0-100, inverted - lower tamper = higher score)
    tamper_score = calculate_tamper_score(tamper_report)
    scores['tamper'] = tamper_score
    if tamper_report.score > 0.7:
        reasons.append("High tamper detection score detected")
    elif tamper_report.score > 0.5:
        reasons.append("Moderate tamper indicators found")
    
    # Calculate weighted average
    total_score = (
        scores['ocr'] * TRUST_WEIGHTS['ocr'] +
        scores['metadata'] * TRUST_WEIGHTS['metadata'] +
        scores['qr'] * TRUST_WEIGHTS['qr'] +
        scores['logo'] * TRUST_WEIGHTS['logo'] +
        scores['tamper'] * TRUST_WEIGHTS['tamper']
    )
    
    trust_score = int(round(total_score))
    
    # Determine verdict
    if trust_score >= 80:
        verdict = "Valid"
    elif trust_score >= 60:
        verdict = "Suspicious"
    else:
        verdict = "Fake"
    
    return TrustEvaluation(
        trust_score=trust_score,
        verdict=verdict,
        reasons=reasons
    )


def calculate_ocr_score(ocr_data: OCRData) -> float:
    """Calculate OCR completeness score."""
    fields = [
        ocr_data.name,
        ocr_data.course,
        ocr_data.issuer,
        ocr_data.date,
        ocr_data.certificate_id
    ]
    
    filled_fields = sum(1 for field in fields if field and field.strip())
    score = (filled_fields / len(fields)) * 100
    
    # Bonus if raw text is substantial
    if len(ocr_data.raw_text) > 100:
        score = min(100, score + 10)
    
    return score


def calculate_metadata_score(metadata: MetadataData) -> float:
    """Calculate metadata trust score."""
    score = 100.0
    
    # Deduct points for flags
    score -= len(metadata.flags) * 20
    
    # Deduct if missing critical metadata
    if not metadata.created_date:
        score -= 10
    
    return max(0.0, score)


def calculate_qr_score(qr_data: QRData) -> float:
    """Calculate QR code verification score."""
    if not qr_data.found:
        return 50.0  # Neutral if no QR code
    
    if qr_data.validation == 'valid':
        return 100.0
    elif qr_data.validation == 'invalid':
        return 0.0
    else:
        return 50.0  # Unverifiable = neutral


def calculate_logo_score(logo_data: LogoDetectionData) -> float:
    """Calculate logo detection score."""
    if not logo_data.matches:
        return 40.0  # Lower score if no logos found
    
    # Use highest confidence match
    best_match = max(logo_data.matches, key=lambda x: x.confidence)
    
    if best_match.confidence >= 0.8:
        return 100.0
    elif best_match.confidence >= 0.6:
        return 75.0
    elif best_match.confidence >= 0.5:
        return 50.0
    else:
        return 25.0


def calculate_tamper_score(tamper_report: TamperReport) -> float:
    """Calculate tamper score (inverted - lower tamper = higher score)."""
    # Invert: tamper_score of 0.0 = trust score of 100, tamper_score of 1.0 = trust score of 0
    return (1.0 - tamper_report.score) * 100.0
