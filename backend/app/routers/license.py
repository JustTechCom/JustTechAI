from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel
from typing import Dict, Any, Optional
import logging
from app.services.license_service import (
    validate_license, 
    create_license, 
    deactivate_license, 
    extend_license
)
from app.config import settings

# Bu endpoint'ler sadece admin erişimi içindir ve
# normal kullanıcılara açık değildir.

router = APIRouter(
    prefix="/license",
    tags=["license"],
    responses={404: {"description": "Not found"}},
)

logger = logging.getLogger(__name__)

class CustomerInfo(BaseModel):
    name: str
    email: str

class CreateLicenseRequest(BaseModel):
    customer_info: CustomerInfo
    plan_type: str
    expiry_days: int = 365
    usage_limit: int = 0

@router.post("/create", response_model=Dict[str, Any])
async def create_license_endpoint(request: CreateLicenseRequest):
    """Yeni bir lisans oluşturur (Sadece admin)"""
    if not settings.development_mode:
        # Güvenlik önlemi: Bu endpoint sadece geliştirme modunda açıktır
        # Gerçek ortamda ayrı bir admin portal üzerinden yönetilmelidir
        raise HTTPException(status_code=403, detail="Bu endpoint sadece geliştirme modunda kullanılabilir")
    
    try:
        result = create_license(
            customer_info=request.customer_info.dict(),
            plan_type=request.plan_type,
            expiry_days=request.expiry_days,
            usage_limit=request.usage_limit
        )
        return result
    except Exception as e:
        logger.error(f"Lisans oluşturma hatası: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Lisans oluşturulamadı: {str(e)}")

@router.post("/validate", response_model=Dict[str, Any])
async def validate_license_endpoint(license_key: str = Query(...)):
    """Lisans anahtarını doğrular"""
    try:
        result = validate_license(license_key)
        return result
    except Exception as e:
        logger.error(f"Lisans doğrulama hatası: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Lisans doğrulanamadı: {str(e)}")

@router.post("/deactivate", response_model=Dict[str, Any])
async def deactivate_license_endpoint(license_key: str = Query(...)):
    """Lisansı deaktif eder (Sadece admin)"""
    if not settings.development_mode:
        raise HTTPException(status_code=403, detail="Bu endpoint sadece geliştirme modunda kullanılabilir")
    
    try:
        result = deactivate_license(license_key)
        return result
    except Exception as e:
        logger.error(f"Lisans deaktivasyon hatası: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Lisans deaktif edilemedi: {str(e)}")

@router.post("/extend", response_model=Dict[str, Any])
async def extend_license_endpoint(license_key: str = Query(...), additional_days: int = Query(...)):
    """Lisans süresini uzatır (Sadece admin)"""
    if not settings.development_mode:
        raise HTTPException(status_code=403, detail="Bu endpoint sadece geliştirme modunda kullanılabilir")
    
    try:
        result = extend_license(license_key, additional_days)
        return result
    except Exception as e:
        logger.error(f"Lisans uzatma hatası: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Lisans süresi uzatılamadı: {str(e)}")