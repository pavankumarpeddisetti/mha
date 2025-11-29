"""
Tamper detection - Ultra-optimized for speed with smart sampling.
"""
import cv2
import numpy as np
from PIL import Image
import io
import base64
from app.models.schemas import TamperReport


def detect_tampering(image: Image.Image) -> TamperReport:
    """
    Fast tamper detection using optimized algorithms.
    """
    try:
        # Convert PIL to OpenCV
        opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Resize for faster processing (maintain aspect ratio)
        h, w = opencv_image.shape[:2]
        max_dim = 800  # Process at 800px max for speed
        if max(h, w) > max_dim:
            ratio = max_dim / max(h, w)
            new_w = int(w * ratio)
            new_h = int(h * ratio)
            opencv_image = cv2.resize(opencv_image, (new_w, new_h), interpolation=cv2.INTER_LINEAR)
        
        # Fast tamper score calculation
        score = calculate_fast_tamper_score(opencv_image)
        
        # Generate simplified heatmap
        heatmap = generate_fast_heatmap(opencv_image)
        
        return TamperReport(
            score=score,
            heatmap=heatmap
        )
        
    except Exception as e:
        print(f"Error in tamper detection: {str(e)}")
        return TamperReport(score=0.5, heatmap="")


def calculate_fast_tamper_score(image: np.ndarray) -> float:
    """Fast tamper score using key indicators only."""
    scores = []
    
    try:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # 1. Fast noise analysis
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        variance = laplacian.var()
        if variance < 30 or variance > 1000:
            scores.append(0.5)
        else:
            scores.append(0.1)
        
        # 2. Fast edge consistency (sampled)
        edges = cv2.Canny(gray, 50, 150)
        h, w = edges.shape
        # Sample 4 regions instead of all
        regions = [
            edges[0:h//2, 0:w//2],
            edges[0:h//2, w//2:w],
            edges[h//2:h, 0:w//2],
            edges[h//2:h, w//2:w]
        ]
        densities = [np.sum(r > 0) / r.size for r in regions]
        if densities:
            density_diff = max(densities) - min(densities)
            scores.append(min(1.0, density_diff * 3))
        
        # 3. Fast color analysis (simplified)
        if len(image.shape) == 3:
            b, g, r = cv2.split(image)
            hist_b = cv2.calcHist([b], [0], None, [64], [0, 256])  # Reduced bins
            hist_g = cv2.calcHist([g], [0], None, [64], [0, 256])
            hist_r = cv2.calcHist([r], [0], None, [64], [0, 256])
            
            mean_b, mean_g, mean_r = np.mean(hist_b), np.mean(hist_g), np.mean(hist_r)
            spikes = (np.sum(hist_b > mean_b * 4) + 
                     np.sum(hist_g > mean_g * 4) + 
                     np.sum(hist_r > mean_r * 4))
            scores.append(min(1.0, spikes / 20.0))
        
        # Weighted average
        if scores:
            return min(1.0, max(0.0, np.mean(scores)))
        
    except Exception as e:
        print(f"Error calculating tamper score: {str(e)}")
    
    return 0.5


def generate_fast_heatmap(image: np.ndarray) -> str:
    """Generate heatmap quickly using simplified method."""
    try:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Fast edge-based heatmap
        edges = cv2.Canny(gray, 50, 150)
        heatmap = cv2.GaussianBlur(edges, (15, 15), 0)  # Smaller kernel
        
        # Normalize and apply colormap
        heatmap = cv2.normalize(heatmap, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
        heatmap_colored = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
        
        # Blend with original (light blend for speed)
        blended = cv2.addWeighted(image, 0.7, heatmap_colored, 0.3, 0)
        
        # Convert to PIL and base64
        heatmap_pil = Image.fromarray(cv2.cvtColor(blended, cv2.COLOR_BGR2RGB))
        
        buffer = io.BytesIO()
        heatmap_pil.save(buffer, format='PNG', optimize=True)
        img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        return img_base64
        
    except Exception as e:
        print(f"Error generating heatmap: {str(e)}")
        return ""
