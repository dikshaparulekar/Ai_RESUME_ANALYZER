# backend/resume_parser.py
import pdfplumber
import easyocr
from PIL import Image
import io
import warnings

# Suppress EasyOCR warnings
warnings.filterwarnings('ignore')

# Initialize EasyOCR reader once (English only)
try:
    reader = easyocr.Reader(['en'], gpu=False)  # Force CPU if GPU issues occur
except Exception as e:
    print(f"EasyOCR initialization error: {e}")
    reader = None

def extract_text_from_pdf(pdf_file):
    """Enhanced PDF text extraction"""
    try:
        if not pdf_file:
            return ""
            
        with pdfplumber.open(pdf_file) as pdf:
            return "\n".join(
                page.extract_text() or "" 
                for page in pdf.pages
            ).strip()
    except Exception as e:
        print(f"PDF Error: {str(e)[:200]}")  # Truncate long errors
        return ""

def extract_text_from_image(image_file):
    """Robust image text extraction"""
    if not reader:
        return "OCR engine not initialized"
    
    try:
        if not image_file:
            return ""
            
        img_bytes = io.BytesIO(image_file.read())
        results = reader.readtext(img_bytes.getvalue(), detail=0)
        return " ".join(results).strip()
    except Exception as e:
        print(f"Image Error: {str(e)[:200]}")
        return ""