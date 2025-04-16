from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import time
import os
from typing import Dict, Any, List, Optional

from app.config import settings
from app.utils.auto_device_detection import get_device_info, load_optimized_model
from app.routers import api_router
from app.services.license_service import validate_license

# Ana uygulama oluştur
app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="Stable Diffusion 2.0 ile profesyonel inpainting API",
)

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router'ları ekle
app.include_router(api_router)

# Logları yapılandır
logging.basicConfig(
    level=logging.INFO if not settings.debug else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("inpainting_api.log"),
    ],
)
logger = logging.getLogger(__name__)

# Çıktı klasörünü oluştur
os.makedirs(settings.output_dir, exist_ok=True)

@app.on_event("startup")
async def startup_event():
    """Uygulama başlatıldığında çalışacak kod"""
    logger.info(f"Sistem cihaz bilgileri tespit ediliyor...")
    
    # Model ve config'i yükle
    try:
        model, config = load_optimized_model(
            model_id=settings.model_id
        )
        app.state.model = model
        app.state.config = config
        logger.info(f"Model başarıyla yüklendi. Çalışma cihazı: {model.device}")
    except Exception as e:
        logger.error(f"Model yüklenirken hata oluştu: {e}")
        app.state.model = None
        app.state.config = None

@app.on_event("shutdown")
async def shutdown_event():
    """Uygulama kapatıldığında çalışacak kod"""
    logger.info("Uygulama kapatılıyor...")
    
    # Eğer gerekiyorsa burada temizlik işlemleri yapılabilir
    # Örneğin geçici dosyaları silme, vs.

# Lisans doğrulama middleware'i
@app.middleware("http")
async def validate_license_middleware(request: Request, call_next):
    # API isteği olmayan endpoint'ler için doğrulama atlanır
    public_endpoints = ["/", "/docs", "/redoc", "/openapi.json", "/device-info"]
    
    if request.url.path in public_endpoints or request.url.path.startswith("/static/"):
        return await call_next(request)
    
    # Geliştirme modunda lisans kontrolünü atla
    if settings.development_mode:
        response = await call_next(request)
        return response
    
    # Lisans anahtarını kontrol et
    license_key = request.headers.get("X-License-Key")
    
    if not license_key:
        return JSONResponse(
            status_code=403,
            content={"detail": "Lisans anahtarı gereklidir"}
        )
    
    # Lisans doğrulama 
    valid_license = await validate_license(license_key)
    
    if not valid_license["valid"]:
        return JSONResponse(
            status_code=403,
            content={"detail": valid_license["message"]}
        )
    
    # İşleme devam et
    response = await call_next(request)
    return response

@app.get("/")
async def root():
    """API durumunu kontrol etmek için root endpoint"""
    device_info = get_device_info()
    
    return {
        "status": "active", 
        "app_name": settings.app_name,
        "version": "1.0.0",
        "device": device_info["device"],
        "model_loaded": app.state.model is not None
    }

@app.get("/device-info")
async def get_device_info_endpoint():
    """Mevcut cihaz bilgilerini döndürür"""
    info = get_device_info()
    return info

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host=settings.host, 
        port=settings.port, 
        reload=settings.debug
    )