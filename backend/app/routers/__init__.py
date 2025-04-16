from fastapi import APIRouter
from .inpainting import router as inpainting_router
from .license import router as license_router

api_router = APIRouter()
api_router.include_router(inpainting_router)
api_router.include_router(license_router)