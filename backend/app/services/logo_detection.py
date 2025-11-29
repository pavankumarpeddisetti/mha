"""
Logo detection - Optimized for speed.
"""
import cv2
import numpy as np
from PIL import Image
import os
from pathlib import Path
from app.models.schemas import LogoDetectionData, LogoMatch
from app.config import LOGOS_DIR, LOGO_MATCH_THRESHOLD


def detect_logos(image: Image.Image) -> LogoDetectionData:
    """
    Fast logo detection - optimized for speed.
    """
    matches = []
    flag = False
    
    try:
        # Quick check if logos directory exists and has files
        if not LOGOS_DIR.exists() or not any(LOGOS_DIR.iterdir()):
            return LogoDetectionData(matches=[], flag=False)
        
        # Convert PIL to OpenCV format
        opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        gray_image = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)
        
        # Resize for faster processing
        h, w = gray_image.shape
        if w > 800:
            ratio = 800 / w
            gray_image = cv2.resize(gray_image, (800, int(h * ratio)), interpolation=cv2.INTER_LINEAR)
        
        # Load reference logos (limit to first 10 for speed)
        reference_logos = load_reference_logos(limit=10)
        
        if not reference_logos:
            return LogoDetectionData(matches=[], flag=False)
        
        # Fast matching with early exit
        for logo_name, logo_image in reference_logos.items():
            confidence = match_logo_fast(gray_image, logo_image)
            
            if confidence >= LOGO_MATCH_THRESHOLD:
                matches.append(LogoMatch(name=logo_name, confidence=confidence))
                # Early exit if high confidence match found
                if confidence > 0.8:
                    break
        
        # Sort matches by confidence
        matches.sort(key=lambda x: x.confidence, reverse=True)
        
        # Flag if all matches are low confidence
        if matches and all(m.confidence < 0.7 for m in matches):
            flag = True
        
        return LogoDetectionData(matches=matches, flag=flag)
        
    except Exception as e:
        print(f"Error in logo detection: {str(e)}")
        return LogoDetectionData(matches=[], flag=False)


def load_reference_logos(limit: int = 10) -> dict:
    """Load reference logos - limit for speed."""
    logos = {}
    
    try:
        if not LOGOS_DIR.exists():
            return logos
        
        image_extensions = ['.png', '.jpg', '.jpeg', '.bmp']
        count = 0
        
        for file_path in LOGOS_DIR.iterdir():
            if count >= limit:
                break
            if file_path.suffix.lower() in image_extensions:
                try:
                    logo_image = cv2.imread(str(file_path), cv2.IMREAD_GRAYSCALE)
                    if logo_image is not None:
                        logo_name = file_path.stem
                        logos[logo_name] = logo_image
                        count += 1
                except:
                    continue
                    
    except Exception as e:
        print(f"Error loading reference logos: {str(e)}")
    
    return logos


def match_logo_fast(certificate_image: np.ndarray, logo_image: np.ndarray) -> float:
    """Fast logo matching using optimized template matching."""
    try:
        # Resize logo if needed
        cert_h, cert_w = certificate_image.shape
        logo_h, logo_w = logo_image.shape
        
        if logo_h > cert_h or logo_w > cert_w:
            scale = min(cert_h / logo_h, cert_w / logo_w) * 0.9
            new_w = int(logo_w * scale)
            new_h = int(logo_h * scale)
            logo_image = cv2.resize(logo_image, (new_w, new_h), interpolation=cv2.INTER_LINEAR)
        
        # Fast template matching
        result = cv2.matchTemplate(certificate_image, logo_image, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)
        
        return max(0.0, min(1.0, max_val))
        
    except Exception as e:
        print(f"Error matching logo: {str(e)}")
        return 0.0
