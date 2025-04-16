import torch
import logging
import os
import psutil
import numpy as np
from diffusers import StableDiffusionInpaintPipeline

logger = logging.getLogger(__name__)

def detect_best_device():
    """
    Sistemdeki en iyi cihazı tespit eder.
    GPU varsa ve yeterli VRAM'e sahipse GPU'yu, yoksa CPU'yu döndürür.
    """
    if torch.cuda.is_available():
        try:
            # GPU bellek durumunu kontrol et
            gpu_properties = torch.cuda.get_device_properties(0)
            vram_total = gpu_properties.total_memory / 1024**3  # GB cinsinden
            
            # SD 2.0 için minimum VRAM 4.5GB olarak kabul edilir
            if vram_total >= 4.5:
                logger.info(f"GPU bulundu: {gpu_properties.name} ({vram_total:.2f}GB VRAM)")
                return "cuda"
            else:
                logger.info(f"GPU bulundu fakat yetersiz VRAM: {vram_total:.2f}GB (minimum 4.5GB gerekli)")
                return "cpu"
        except Exception as e:
            logger.warning(f"GPU kontrolü sırasında hata: {e}")
            return "cpu"
    else:
        logger.info("GPU bulunamadı, CPU kullanılacak")
        return "cpu"

def get_system_memory():
    """Sistemdeki toplam bellek miktarını GB cinsinden döndürür"""
    return psutil.virtual_memory().total / (1024**3)

def get_device_info():
    """Mevcut hesaplama kaynaklarını tespit eder ve bilgilerini döndürür"""
    info = {
        "cpu_count": psutil.cpu_count(logical=False),
        "cpu_count_logical": psutil.cpu_count(logical=True),
        "ram_total_gb": get_system_memory(),
        "has_gpu": torch.cuda.is_available(),
        "gpu_count": torch.cuda.device_count() if torch.cuda.is_available() else 0,
        "cuda_version": torch.version.cuda if torch.cuda.is_available() else None,
        "device": "cpu"
    }
    
    if info["has_gpu"]:
        try:
            gpu_properties = torch.cuda.get_device_properties(0)
            info["gpu_name"] = gpu_properties.name
            info["gpu_vram_gb"] = gpu_properties.total_memory / (1024**3)
            info["suitable_for_sd"] = info["gpu_vram_gb"] >= 4.5
            
            if info["suitable_for_sd"]:
                info["device"] = "cuda"
                info["recommended_precision"] = "float16" if info["gpu_vram_gb"] >= 6.0 else "float32"
            
        except Exception as e:
            logger.warning(f"GPU bilgilerini alırken hata: {e}")
            
    return info

def load_optimized_model(model_id="stabilityai/stable-diffusion-2-inpainting"):
    """
    Sistem kaynaklarına göre optimum yapılandırma ile modeli yükler
    """
    # Sistem bilgilerini al
    system_info = get_device_info()
    logger.info(f"Sistem bilgileri: {system_info}")
    
    # Yapılandırmayı belirle
    config = {
        "device": system_info["device"],
        "torch_dtype": torch.float16 if system_info["device"] == "cuda" and system_info.get("recommended_precision") == "float16" else torch.float32,
        "inpainting_settings": {
            "default_steps": 30 if system_info["device"] == "cuda" else 20,
            "max_resolution": 1024 if system_info["device"] == "cuda" else 768,
            "tiling_required": system_info["device"] == "cpu" or system_info.get("gpu_vram_gb", 0) < 8.0,
            "tile_size": 512 if system_info["device"] == "cuda" else 256,
            "tile_overlap": 64 if system_info["device"] == "cuda" else 32,
        }
    }
    
    # Kullanıcıya bilgi ver
    if system_info["device"] == "cuda":
        logger.info(f"GPU kullanılıyor: {system_info['gpu_name']} ({system_info['gpu_vram_gb']:.2f}GB VRAM)")
    else:
        if system_info["has_gpu"]:
            logger.info(f"GPU var ama yetersiz VRAM: {system_info['gpu_vram_gb']:.2f}GB, CPU kullanılacak")
        else:
            logger.info("GPU bulunamadı, CPU kullanılacak")
        
        logger.info(f"CPU: {system_info['cpu_count']} çekirdek, {system_info['ram_total_gb']:.2f}GB RAM")
        
    # Modeli yükle
    logger.info(f"Model yükleniyor: {model_id}")
    logger.info(f"Cihaz: {config['device']}, Veri Tipi: {config['torch_dtype']}")
    
    pipe = StableDiffusionInpaintPipeline.from_pretrained(
        model_id,
        torch_dtype=config["torch_dtype"],
        safety_checker=None  # Hızı artırmak için güvenlik kontrolünü devre dışı bırak
    )
    
    # Cihaza göre optimize et
    if config["device"] == "cuda":
        pipe = pipe.to("cuda")
        
        # GPU için optimizasyonlar
        if system_info.get("gpu_vram_gb", 0) < 8.0:
            logger.info("Düşük VRAM GPU için memory optimizasyonları uygulanıyor")
            pipe.enable_attention_slicing()
            
            # Çok düşük VRAM için ek optimizasyonlar
            if system_info.get("gpu_vram_gb", 0) < 6.0:
                logger.info("VAE CPU offloading uygulanıyor")
                pipe.vae.to("cpu")
                pipe.vae.to(torch.float32)
    else:
        pipe = pipe.to("cpu")
        
        # CPU için optimizasyonlar
        logger.info("CPU optimizasyonları uygulanıyor")
        pipe.enable_attention_slicing(slice_size=1)
        
        # CPU iş parçacığı sayısını ayarla
        torch.set_num_threads(max(4, min(system_info["cpu_count_logical"] - 2, 8)))
        
    return pipe, config

def process_with_auto_tiling(pipe, image, mask_image, prompt, negative_prompt, guidance_scale, 
                            num_inference_steps, seed, config):
    """
    Sistem durumuna göre otomatik olarak tiling uygulayan veya doğrudan işlem yapan fonksiyon
    """
    import torch
    import numpy as np
    from PIL import Image
    
    # Görüntü boyutlarını al
    width, height = image.size
    
    # Tiling gerekli mi kontrol et
    max_res = config["inpainting_settings"]["max_resolution"]
    tile_size = config["inpainting_settings"]["tile_size"]
    tile_overlap = config["inpainting_settings"]["tile_overlap"]
    requires_tiling = config["inpainting_settings"]["tiling_required"] or max(width, height) > max_res
    
    # Tiling gerekmiyorsa doğrudan işle
    if not requires_tiling:
        generator = torch.Generator(device=pipe.device).manual_seed(seed)
        return pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            image=image,
            mask_image=mask_image,
            guidance_scale=guidance_scale,
            num_inference_steps=num_inference_steps,
            generator=generator,
        ).images[0]
    
    # Tiling gerekiyorsa parçalara bölerek işle
    logger.info(f"Resim boyutu ({width}x{height}) büyük, tiling uygulanıyor. Tile boyutu: {tile_size}px")
    
    # Resmi NumPy dizisine dönüştür
    img_np = np.array(image)
    mask_np = np.array(mask_image.convert("L"))
    
    # Maskeyi işle (beyaz=inpaint)
    mask_np = 255 - mask_np  # Invertle
    
    # Sonuç görüntüsünü oluştur
    result_np = np.copy(img_np)
    
    # Parça koordinatlarını hesapla
    x_tiles = np.arange(0, width, tile_size - tile_overlap)
    y_tiles = np.arange(0, height, tile_size - tile_overlap)
    
    # Son parçaların doğru kenardan başlamasını sağla
    if len(x_tiles) > 1 and x_tiles[-1] + tile_size > width:
        x_tiles[-1] = width - tile_size
    if len(y_tiles) > 1 and y_tiles[-1] + tile_size > height:
        y_tiles[-1] = height - tile_size
    
    # Her bir parçayı işle
    for x_start in x_tiles:
        for y_start in y_tiles:
            # Parça koordinatlarını ayarla
            x_end = min(x_start + tile_size, width)
            y_end = min(y_start + tile_size, height)
            
            # Parçayı kes
            tile_img = Image.fromarray(img_np[y_start:y_end, x_start:x_end])
            tile_mask = Image.fromarray(mask_np[y_start:y_end, x_start:x_end])
            
            # Maskede inpainting gerekli mi kontrol et
            if np.mean(mask_np[y_start:y_end, x_start:x_end]) < 10:  # Maske neredeyse tamamen siyah ise (işlem gerekmiyor)
                continue
            
            logger.debug(f"Parça işleniyor: ({x_start},{y_start}) - ({x_end},{y_end})")
            
            # Parçayı işle
            generator = torch.Generator(device=pipe.device).manual_seed(seed)
            try:
                tile_result = pipe(
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    image=tile_img,
                    mask_image=tile_mask,
                    guidance_scale=guidance_scale,
                    num_inference_steps=num_inference_steps,
                    generator=generator,
                ).images[0]
                
                # İşlenmiş parçayı NumPy dizisine dönüştür
                tile_result_np = np.array(tile_result)
                
                # Kenar yumuşatma için maskeleme
                if tile_overlap > 0 and (x_start > 0 or y_start > 0):
                    blend_mask = np.ones((y_end - y_start, x_end - x_start))
                    
                    # Yatay geçiş maskesi
                    if x_start > 0:
                        for i in range(tile_overlap):
                            blend_mask[:, i] = i / tile_overlap
                    
                    # Dikey geçiş maskesi
                    if y_start > 0:
                        for i in range(tile_overlap):
                            blend_mask[i, :] *= i / tile_overlap
                    
                    # Geçiş maskeleme ile sonuç görüntüsünü güncelle
                    blend_mask = np.expand_dims(blend_mask, axis=2).repeat(3, axis=2)
                    result_np[y_start:y_end, x_start:x_end] = (
                        tile_result_np * blend_mask + 
                        result_np[y_start:y_end, x_start:x_end] * (1 - blend_mask)
                    ).astype(np.uint8)
                else:
                    # Maskelenmiş bölgeleri güncelle
                    mask_region = (mask_np[y_start:y_end, x_start:x_end] > 128)
                    mask_region = np.expand_dims(mask_region, axis=2).repeat(3, axis=2)
                    result_np[y_start:y_end, x_start:x_end][mask_region] = tile_result_np[mask_region]
            
            except Exception as e:
                logger.error(f"Parça işlenirken hata: {e}")
                # Hata durumunda bu parçayı atla
                continue
    
    # Sonuç görüntüsünü döndür
    return Image.fromarray(result_np)