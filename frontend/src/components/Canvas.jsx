import React, { useRef, useEffect, useState } from 'react';

export const Canvas = ({ originalImage, setMask }) => {
  const canvasRef = useRef(null);
  const maskCanvasRef = useRef(null);
  const [isDrawing, setIsDrawing] = useState(false);
  const [brushSize, setBrushSize] = useState(20);
  const ctx = useRef(null);
  const maskCtx = useRef(null);
  
  useEffect(() => {
    if (!originalImage) return;
    
    const canvas = canvasRef.current;
    const maskCanvas = maskCanvasRef.current;
    
    // Resim yüklendiğinde canvas boyutlarını ayarla
    const img = new Image();
    img.onload = () => {
      // Canvas boyutlarını ayarla
      canvas.width = img.width;
      canvas.height = img.height;
      maskCanvas.width = img.width;
      maskCanvas.height = img.height;
      
      // Resmi canvas'a çiz
      ctx.current = canvas.getContext('2d');
      ctx.current.drawImage(img, 0, 0);
      
      // Boş maske oluştur
      maskCtx.current = maskCanvas.getContext('2d');
      maskCtx.current.fillStyle = 'white';
      maskCtx.current.fillRect(0, 0, maskCanvas.width, maskCanvas.height);
    };
    img.src = originalImage;
  }, [originalImage]);
  
  const startDrawing = (e) => {
    setIsDrawing(true);
    draw(e);
  };
  
  const finishDrawing = () => {
    setIsDrawing(false);
    setMask(maskCanvasRef.current.toDataURL());
  };
  
  const draw = (e) => {
    if (!isDrawing || !maskCtx.current) return;
    
    const rect = maskCanvasRef.current.getBoundingClientRect();
    const scaleX = maskCanvasRef.current.width / rect.width;
    const scaleY = maskCanvasRef.current.height / rect.height;
    
    const x = (e.clientX - rect.left) * scaleX;
    const y = (e.clientY - rect.top) * scaleY;
    
    maskCtx.current.beginPath();
    maskCtx.current.arc(x, y, brushSize / 2, 0, Math.PI * 2);
    maskCtx.current.fillStyle = 'black';
    maskCtx.current.fill();
    
    setMask(maskCanvasRef.current.toDataURL());
  };
  
  const clearMask = () => {
    if (!maskCtx.current || !maskCanvasRef.current) return;
    
    maskCtx.current.fillStyle = 'white';
    maskCtx.current.fillRect(0, 0, maskCanvasRef.current.width, maskCanvasRef.current.height);
    
    setMask(null);
  };
  
  return (
    <div className="w-full">
      <div className="mb-4">
        <h2 className="text-xl font-semibold text-gray-800">Orijinal Resim</h2>
        <canvas
          ref={canvasRef}
          className="border border-gray-300 mt-2 max-w-full h-auto"
        />
      </div>
      
      <div className="mb-4">
        <h2 className="text-xl font-semibold text-gray-800">Mask Oluştur</h2>
        <p className="text-sm text-gray-600 mb-2">İnpainting uygulanacak alanları siyah ile işaretleyin</p>
        
        <div className="flex items-center mb-2">
          <label className="mr-2 text-sm text-gray-700">Fırça Boyutu:</label>
          <input
            type="range"
            min="5"
            max="100"
            value={brushSize}
            onChange={(e) => setBrushSize(parseInt(e.target.value))}
            className="w-32"
          />
          <span className="ml-2 text-sm text-gray-700">{brushSize}px</span>
        </div>
        
        <div className="relative inline-block">
          <canvas
            ref={maskCanvasRef}
            onMouseDown={startDrawing}
            onMouseMove={draw}
            onMouseUp={finishDrawing}
            onMouseLeave={finishDrawing}
            className="border border-gray-300 cursor-crosshair max-w-full h-auto"
          />
          <div className="absolute top-2 right-2">
            <button
              onClick={clearMask}
              className="bg-red-500 text-white px-2 py-1 rounded text-xs"
            >
              Maskı Temizle
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};