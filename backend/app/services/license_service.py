import jwt
import time
import os
import json
import logging
import hashlib
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# Örnek lisans veritabanı (gerçekte bir veritabanında saklanır)
# Gerçek uygulamada bu PostgreSQL veya başka bir veritabanında tutulacaktır
LICENSES_FILE = "config/licenses.json"

def get_licenses():
    """Lisans veritabanını yükle"""
    if os.path.exists(LICENSES_FILE):
        with open(LICENSES_FILE, "r") as f:
            return json.load(f)
    return {}

def save_licenses(licenses):
    """Lisans veritabanını kaydet"""
    os.makedirs(os.path.dirname(LICENSES_FILE), exist_ok=True)
    with open(LICENSES_FILE, "w") as f:
        json.dump(licenses, f, indent=2)

def generate_license_key(customer_info):
    """Lisans anahtarı oluştur"""
    timestamp = int(time.time())
    data = f"{customer_info['name']}:{customer_info['email']}:{timestamp}"
    hash_obj = hashlib.sha256(data.encode())
    license_key = f"SDINPAINT-{hash_obj.hexdigest()[:16].upper()}"
    return license_key

def validate_license(license_key):
    """Lisans anahtarını doğrula"""
    licenses = get_licenses()
    
    if license_key not in licenses:
        return {
            "valid": False,
            "message": "Geçersiz lisans anahtarı"
        }
    
    license_data = licenses[license_key]
    
    # Lisans süresi kontrolü
    if datetime.now() > datetime.fromisoformat(license_data["expiry_date"]):
        return {
            "valid": False,
            "message": "Lisans süresi dolmuş"
        }
    
    # Aktiflik kontrolü
    if not license_data["active"]:
        return {
            "valid": False,
            "message": "Lisans deaktive edilmiş"
        }
    
    # Kullanım limiti kontrolü
    if license_data["usage_count"] >= license_data["usage_limit"] and license_data["usage_limit"] > 0:
        return {
            "valid": False,
            "message": "Kullanım limiti aşıldı"
        }
    
    # Kullanım sayacını artır
    licenses[license_key]["usage_count"] += 1
    licenses[license_key]["last_used"] = datetime.now().isoformat()
    save_licenses(licenses)
    
    return {
        "valid": True,
        "plan": license_data["plan"],
        "customer": license_data["customer_name"],
        "usage_count": license_data["usage_count"],
        "usage_limit": license_data["usage_limit"],
        "expires": license_data["expiry_date"]
    }

def create_license(customer_info, plan_type, expiry_days=365, usage_limit=0):
    """Yeni bir lisans oluştur"""
    licenses = get_licenses()
    
    # Lisans anahtarı oluştur
    license_key = generate_license_key(customer_info)
    
    # Lisans verisini oluştur
    license_data = {
        "customer_name": customer_info["name"],
        "customer_email": customer_info["email"],
        "plan": plan_type,
        "creation_date": datetime.now().isoformat(),
        "expiry_date": (datetime.now() + timedelta(days=expiry_days)).isoformat(),
        "usage_count": 0,
        "usage_limit": usage_limit,  # 0 = sınırsız
        "active": True,
        "last_used": None
    }
    
    # Veritabanına ekle
    licenses[license_key] = license_data
    save_licenses(licenses)
    
    return {
        "license_key": license_key,
        "license_data": license_data
    }

def deactivate_license(license_key):
    """Lisansı deaktif et"""
    licenses = get_licenses()
    
    if license_key not in licenses:
        return {
            "success": False,
            "message": "Lisans bulunamadı"
        }
    
    licenses[license_key]["active"] = False
    save_licenses(licenses)
    
    return {
        "success": True,
        "message": "Lisans deaktif edildi"
    }

def extend_license(license_key, additional_days):
    """Lisans süresini uzat"""
    licenses = get_licenses()
    
    if license_key not in licenses:
        return {
            "success": False,
            "message": "Lisans bulunamadı"
        }
    
    current_expiry = datetime.fromisoformat(licenses[license_key]["expiry_date"])
    new_expiry = current_expiry + timedelta(days=additional_days)
    
    licenses[license_key]["expiry_date"] = new_expiry.isoformat()
    save_licenses(licenses)
    
    return {
        "success": True,
        "message": f"Lisans {additional_days} gün uzatıldı",
        "new_expiry_date": new_expiry.isoformat()
    }