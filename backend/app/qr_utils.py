"""
QR code detection utilities using OpenCV QRCodeDetector (no external DLLs).
"""
import cv2
import numpy as np
from PIL import Image
import io
import fitz

# Initialize one detector to reuse
qr_detector = cv2.QRCodeDetector()


def pdf_to_images_for_qr(file_bytes):
    """Convert PDF pages into images for QR detection."""
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    images = []
    for page in doc:
        pix = page.get_pixmap(dpi=300)
        images.append(pix.pil_tobytes(format="PNG"))
    doc.close()
    return images


def enhance_for_qr(img):
    """Improve clarity of QR for accurate detection."""
    # Convert to grayscale if needed
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img

    # Boost contrast using CLAHE
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    gray = clahe.apply(gray)

    # Sharpen edges
    kernel = np.array([
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0]
    ])
    sharp = cv2.filter2D(gray, -1, kernel)

    # Smooth small artifacts
    blur = cv2.medianBlur(sharp, 3)

    return blur


def decode_qr_from_image(image_bytes):
    """Detect and decode QR code from image using OpenCV QRCodeDetector."""
    try:
        pil_img = Image.open(io.BytesIO(image_bytes))
        img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

        qr_results = []

        # Attempt 1: original image
        decoded = decode_with_detector(img)
        if decoded:
            qr_results.extend(decoded)

        # Attempt 2: enhanced image
        if not qr_results:
            enhanced = enhance_for_qr(img)
            decoded = decode_with_detector(enhanced)
            if decoded:
                qr_results.extend(decoded)

        # Attempt 3: adaptive threshold
        if not qr_results:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            thresh = cv2.adaptiveThreshold(
                gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
            )
            decoded = decode_with_detector(thresh)
            if decoded:
                qr_results.extend(decoded)

        return qr_results

    except Exception as e:
        print(f"QR decoding error: {str(e)}")
        return []


def decode_with_detector(image):
    """Helper to decode QR using OpenCV detector and format results."""
    results = []
    try:
        # Try multi detection first
        retval, decoded_info, points, _ = qr_detector.detectAndDecodeMulti(image)
        if retval and decoded_info:
            for data, pts in zip(decoded_info, points):
                if data:
                    rect = points_to_rect(pts)
                    results.append({
                        "type": "QR_CODE",
                        "data": data,
                        "rect": rect,
                    })
        else:
            # Fallback to single detection
            data, pts = qr_detector.detectAndDecode(image)
            if data:
                rect = points_to_rect(pts)
                results.append({
                    "type": "QR_CODE",
                    "data": data,
                    "rect": rect,
                })
    except Exception as e:
        print(f"OpenCV QR decode error: {str(e)}")

    return results


def points_to_rect(points):
    """Convert detected points to a rectangle dictionary."""
    if points is None or len(points) == 0:
        return {"left": 0, "top": 0, "width": 0, "height": 0}

    # Points shape can be (4, 2) or nested
    pts = np.array(points, dtype=np.float32).reshape(-1, 2)
    x_coords = pts[:, 0]
    y_coords = pts[:, 1]
    left = float(np.min(x_coords))
    top = float(np.min(y_coords))
    width = float(np.max(x_coords) - left)
    height = float(np.max(y_coords) - top)

    return {
        "left": left,
        "top": top,
        "width": width,
        "height": height,
    }
