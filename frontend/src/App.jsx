import React, { useState, useEffect } from 'react';
import { Canvas } from './components/Canvas';
import { ImageUploader } from './components/ImageUploader';
import { ResultViewer } from './components/ResultViewer';
import { ParametersForm } from './components/ParametersForm';
import { fetchDeviceInfo } from './services/api';

function App() {
  const [originalImage, setOriginalImage] = useState(null);
  const [mask, setMask] = useState(null);
  const [results, setResults] = useState([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [deviceInfo, setDeviceInfo] = useState(null);
  
  useEffect(() => {
    // Cihaz bilgilerini al
    const getDeviceInfo = async () => {
      try {
        const data = await fetchDeviceInfo();
        setDeviceInfo(data);
      } catch (error) {
        console.error("Cihaz bilgileri alınamadı:", error);
      }
    };
    
    getDeviceInfo();
  }, []);
  
  return (
    <div className="flex flex-col items-center max-w-6xl mx-auto p-4 bg-gray-50 min-h-screen">
      <h1 className="text-3xl font-bold mb-2 text-blue-700">Stable Diffusion 2.0 Inpainting</h1>
      <p className="text-gray-600 mb-6">Görüntülerdeki istenmeyen alanları yapay zeka ile doldurun</p>
      
      {deviceInfo && (
        <div className={`border-l-4 p-4 mb-6 rounded ${deviceInfo.device === 'cuda' ? 'bg-green-50 border-green-400' : 'bg-blue-50 border-blue-400'}`}>
          <p className={`font-medium ${deviceInfo.device === 'cuda' ? 'text-green-700' : 'text-blue-700'}`}>
            {deviceInfo.device === 'cuda' ? 'GPU Modu Aktif' : 'CPU Modu Aktif'}
          </p>
          <p className={`text-sm ${deviceInfo.device === 'cuda' ? 'text-green-600' : 'text-blue-600'}`}>
            {deviceInfo.device === 'cuda' 
              ? `${deviceInfo.gpu_name} (${deviceInfo.gpu_vram_gb.toFixed(1)}GB VRAM) kullanılıyor` 
              : 'İşlemler CPU üzerinde gerçekleştirilecek. İşlem süresi daha uzun olabilir.'}
          </p>
        </div>
      )}
      
      <ImageUploader setOriginalImage={setOriginalImage} />
      
      {originalImage && (
        <>
          <div className="flex flex-col md:flex-row gap-8 w-full">
            <Canvas 
              originalImage={originalImage} 
              setMask={setMask} 
            />
          </div>
          
          <ParametersForm 
            originalImage={originalImage}
            mask={mask}
            setIsProcessing={setIsProcessing}
            isProcessing={isProcessing}
            setResults={setResults}
          />
          
          {results.length > 0 && (
            <ResultViewer results={results} />
          )}
        </>
      )}
    </div>
  );
}

export default App;