import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Stable Diffusion 2.0 Inpainting API"
    debug: bool = os.environ.get("DEBUG", "0") == "1"
    development_mode: bool = os.environ.get("DEVELOPMENT_MODE", "0") == "1"
    
    # SD model ayarları
    model_id: str = "stabilityai/stable-diffusion-2-inpainting"
    use_cpu: bool = os.environ.get("USE_CPU", "0") == "1"
    
    # API ayarları
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Lisans ayarları
    license_required: bool = not development_mode  # Geliştirme modunda lisans gerekmez
    
    # Çıktı ayarları
    output_dir: str = "output"
    max_output_storage_days: int = 7  # Çıktıların kaç gün saklanacağı
    
    # Güvenlik ayarları
    allowed_origins: list = ["*"]  # CORS için izin verilen originler
    
    class Config:
        env_file = ".env"

settings = Settings()