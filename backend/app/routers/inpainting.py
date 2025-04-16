from fastapi import APIRouter, UploadFile, File, Form, HTTPException, BackgroundTasks, Request
from fastapi.responses import JSONResponse
from typing import List, Optional
import logging
import uuid
import time
import os
from app.models.inpainting import InpaintingResult
from app.services.inpainting_service import process_inpainting

router = APIRouter(
    prefix="/inpaint",
    tags=["inpainting"],
    responses={404: {"description": "Not found"}},
)

logger = logging.getLogger(__name__)
active_tasks = {}

@router.post("/", response_model=InpaintingResult)
async def inpaint(
    background_tasks: BackgroundTasks,
    request: Request,
    image: UploadFile = File(...),
    mask: UploadFile = File(...),
    prompt: str = Form(""),
    negative_prompt: str = Form(""),
    guidance_scale: float = Form(7.5),
    num_inference_steps: int = Form(30),
    seed: int = Form(-1),
    num_outputs: int = Form(1),
):
    """Inpainting işlemini asenkron olarak başlatma"""
    model = request.app.state.model
    config = request.app.state.config
    
    if model is None:
        raise HTTPException(status_code=503, detail="Model henüz yüklenmedi veya yükleme başarısız oldu")
    
    try:
        # Benzersiz bir ID oluştur
        task_id = str(uuid.uuid4())
        
        # Resim ve maske dosyalarını oku
        image_data = await image.read()
        mask_data = await mask.read()
        
        # Durumu güncelle
        active_tasks[task_id] = {
            "status": "pending",
            "created_at": time.time(),
            "params": {
                "prompt": prompt,
                "negative_prompt": negative_prompt,
                "guidance_scale": guidance_scale,
                "num_inference_steps": num_inference_steps,
                "seed": seed,
                "num_outputs": num_outputs,
            }
        }
        
        # Arkaplan görevi olarak inpainting işlemini başlat
        background_tasks.add_task(
            process_inpainting, 
            model=model,
            config=config,
            task_id=task_id, 
            image_data=image_data, 
            mask_data=mask_data, 
            prompt=prompt, 
            negative_prompt=negative_prompt, 
            guidance_scale=guidance_scale, 
            num_inference_steps=num_inference_steps, 
            seed=seed, 
            num_outputs=num_outputs,
            active_tasks=active_tasks
        )
        
        return InpaintingResult(
            id=task_id,
            status="pending"
        )
    
    except Exception as e:
        logger.error(f"Inpainting işlemi başlatılırken hata: {str(e)}")
        raise HTTPException(status_code=500, detail=f"İşlem başlatılamadı: {str(e)}")

@router.get("/{task_id}", response_model=InpaintingResult)
async def get_inpaint_result(task_id: str):
    """Belirli bir inpainting görevinin sonucunu alma"""
    if task_id not in active_tasks:
        raise HTTPException(status_code=404, detail="Belirtilen ID ile bir görev bulunamadı")
    
    task_info = active_tasks[task_id]
    
    # Sonucu döndür
    return InpaintingResult(
        id=task_id,
        status=task_info["status"],
        images=task_info.get("images"),
        error=task_info.get("error")
    )

@router.get("/", response_model=List[str])
async def list_active_tasks():
    """Aktif görevlerin listesini alma"""
    # Sadece ID'leri döndür
    return list(active_tasks.keys())