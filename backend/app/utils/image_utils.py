from PIL import Image
import numpy as np
import io
import base64

def pil_to_base64(image, format="PNG"):
    """PIL görüntüsünü base64'e dönüştür"""
    buffered = io.BytesIO()
    image.save(buffered, format=format)
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/{format.lower()};base64,{img_str}"

def base64_to_pil(base64_str):
    """Base64 string'i PIL görüntüsüne dönüştür"""
    # Öneki kaldır (eğer varsa)
    if "," in base64_str:
        base64_str = base64_str.split(",")[1]
    
    # Decode et
    img_bytes = base64.b64decode(base64_str)
    return Image.open(io.BytesIO(img_bytes))

def resize_image_to_multiple_of_8(image):
    """Görüntüyü 8'in katlarına yeniden boyutlandır (SD modelleri için)"""
    width, height = image.size
    if width % 8 == 0 and height % 8 == 0:
        return image
    
    new_width = (width // 8) * 8
    new_height = (height // 8) * 8
    return image.resize((new_width, new_height))

def invert_mask(mask_image):
    """Maskeyi ters çevir (beyaz=inpaint, siyah=koru)"""
    if mask_image.mode != "L":
        mask_image = mask_image.convert("L")
    
    mask_np = np.array(mask_image)
    mask_np = 255 - mask_np
    return Image.fromarray(mask_np)

def limit_image_size(image, max_size=1024):
    """Görüntü boyutunu sınırla (maksimum boyut)"""
    width, height = image.size
    
    if width <= max_size and height <= max_size:
        return image
    
    if width > height:
        new_width = max_size
        new_height = int(height * (max_size / width))
    else:
        new_height = max_size
        new_width = int(width * (max_size / height))
    
    return image.resize((new_width, new_height))