from PIL import Image
import io

_trocr_model = None
_trocr_processor = None

def _load_trocr():
    global _trocr_model, _trocr_processor
    if _trocr_model is not None:
        return _trocr_processor, _trocr_model
    try:
        from transformers import TrOCRProcessor, VisionEncoderDecoderModel
        print("[OCR] Loading TrOCR model (first time takes ~2 min)...")
        _trocr_processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
        _trocr_model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten")
        print("[OCR] TrOCR loaded successfully.")
        return _trocr_processor, _trocr_model
    except Exception as e:
        print(f"[OCR] TrOCR failed to load: {e}")
        return None, None

def _split_into_lines(image):
    """Split image into horizontal strips for line-by-line OCR."""
    import numpy as np
    img_array = np.array(image.convert("L"))
    
    # Find rows that are mostly white (gaps between lines)
    row_means = img_array.mean(axis=1)
    threshold = row_means.mean() + (255 - row_means.mean()) * 0.3
    
    is_blank = row_means > threshold
    
    lines = []
    start = None
    for i, blank in enumerate(is_blank):
        if not blank and start is None:
            start = i
        elif blank and start is not None:
            if i - start > 10:  # Skip tiny strips
                lines.append((start, i))
            start = None
    if start is not None and len(img_array) - start > 10:
        lines.append((start, len(img_array)))
    
    # If no lines detected, treat whole image as one line
    if not lines:
        lines = [(0, len(img_array))]
    
    return lines

async def extract_text_from_image(image_bytes, content_type="image/png"):
    """Extract text from handwritten note image using TrOCR."""
    processor, model = _load_trocr()
    
    if processor is None or model is None:
        return _fallback_ocr(image_bytes)
    
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        
        # Split into lines for better accuracy
        lines = _split_into_lines(image)
        
        extracted_lines = []
        for top, bottom in lines:
            # Crop line from image
            line_img = image.crop((0, top, image.width, bottom))
            
            # Skip very thin strips
            if line_img.height < 10:
                continue
            
            # Run TrOCR on this line
            pixel_values = processor(images=line_img, return_tensors="pt").pixel_values
            generated_ids = model.generate(pixel_values, max_new_tokens=200)
            text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
            
            if text.strip():
                extracted_lines.append(text.strip())
        
        result = "\n".join(extracted_lines)
        print(f"[OCR] TrOCR extracted {len(result)} chars from {len(lines)} lines")
        return result if result.strip() else "[No text detected in image]"
    
    except Exception as e:
        print(f"[OCR] TrOCR processing failed: {e}")
        return _fallback_ocr(image_bytes)

def _fallback_ocr(image_bytes):
    """Fallback to EasyOCR or error message."""
    try:
        import easyocr
        reader = easyocr.Reader(["en"], gpu=False)
        results = reader.readtext(image_bytes)
        text = "\n".join([r[1] for r in results])
        print(f"[OCR] EasyOCR fallback extracted {len(text)} chars")
        return text if text.strip() else "[No text detected]"
    except ImportError:
        return "[Error: Install transformers and Pillow for OCR: pip install transformers Pillow torch]"
    except Exception as e:
        return f"[OCR Error: {e}]"