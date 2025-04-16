import torch
import io
import base64
import time
import logging
import numpy as np
from PIL import Image
from app.utils.auto_device_detection import process_with_auto_tiling

logger = logging.getLogger(__name__)

async def process_inpainting(
    model,
    config,
    task_id: str,
    image_data: bytes,
    mask_data: bytes,
    prompt: str,
    negative_prompt: str,
    guidance_scale: float,
    num_inference_steps: int,
    seed: int,
    num_outputs: int,
    active_tasks: dict
):
    """Arka planda inpainting işlemini gerçekleştirme"""
    try:
        # Durumu güncelle
        active_tasks[task_id]["status"] = "processing"
        
        # Resim ve maskeyi yükle
        init_image = Image.open(io.BytesIO(image_data)).convert("RGB")
        mask_image = Image.open(io.BytesIO(mask_data)).convert("RGB")
        
        # Görüntüleri işle ve uygun boyutlara getir
        width, height = init_image.size
        
        # SD 2.0 için resimleri 8'in katları olacak şekilde yeniden boyutlandır
        if width % 8 != 0 or height % 8 != 0:
            width = (width // 8) * 8
            height = (height // 8) * 8
            init_image = init_image.resize((width, height))
            mask_image = mask_image.resize((width, height))
        
        # Maskı hazırla (siyah alanlar inpainting için, beyaz alanlar korunur)
        mask_image = mask_image.convert("L")
        
        # Seed'i ayarla
        if seed == -1:
            seed = int(time.time()) % 2**32
            
        output_images = []
        
        # Her bir çıktı için işlem yap
        for i in range(num_outputs):
            current_seed = seed + i
            
            # Akıllı tiling ile inpainting işlemini gerçekleştir
            logger.info(f"İşlem başlatılıyor: {task_id}, çıktı {i+1}/{num_outputs}")
            result_image = process_with_auto_tiling(
                pipe=model,
                image=init_image,
                mask_image=mask_image,
                prompt=prompt,
                negative_prompt=negative_prompt,
                guidance_scale=guidance_scale,
                num_inference_steps=num_inference_steps,
                seed=current_seed,
                config=config
            )
            
            # Dosya adı oluştur ve kaydet
            filename = f"output/{task_id}_{i}.png"
            result_image.save(filename)
            
            # Base64 dönüşümü
            buffered = io.BytesIO()
            result_image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            # Sonuçları listeye ekle
            output_images.append({
                "image": f"data:image/png;base64,{img_str}",
                "seed": current_seed,
                "prompt": prompt
            })
        
        # Durumu güncelle
        active_tasks[task_id]["status"] = "completed"
        active_tasks[task_id]["images"] = output_images
        active_tasks[task_id]["completed_at"] = time.time()
        
        logger.info(f"Görev {task_id} başarıyla tamamlandı")
        
    except Exception as e:
        logger.error(f"Görev {task_id} işlenirken hata oluştu: {str(e)}")
        active_tasks[task_id]["status"] = "failed"
        active_tasks[task_id]["error"] = str(e)
        active_tasks[task_id]["completed_at"] = time.time()