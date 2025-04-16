import React, { useState } from 'react';
import { startInpaintingProcess } from '../services/api';
import { checkInpaintingStatus } from '../services/checkInpaintingStatus'; // Bu satırı ekleyin

export const ParametersForm = ({ originalImage, mask, setIsProcessing, isProcessing, setResults }) => {

  const [prompt, setPrompt] = useState('');
  const [negativePrompt, setNegativePrompt] = useState('');
  const [guidanceScale, setGuidanceScale] = useState(7.5);
  const [numInferenceSteps, setNumInferenceSteps] = useState(30);
  const [seed, setSeed] = useState(-1);
  const [numOutputs, setNumOutputs] = useState(1);
  
  const generateRandomSeed = () => {
    setSeed(Math.floor(Math.random() * 2147483647));
  };
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!originalImage || !mask) {
      alert('Lütfen bir resim yükleyin ve mask oluşturun');
      return;
    }
    
    setIsProcessing(true);
    setResults([]);
    
    try {
      const originalImageBlob = await fetch(originalImage).then(r => r.blob());
      const maskBlob = await fetch(mask).then(r => r.blob());
      
      const formData = new FormData();
      formData.append('image', originalImageBlob, 'image.png');
      formData.append('mask', maskBlob, 'mask.png');
      formData.append('prompt', prompt);
      formData.append('negative_prompt', negativePrompt);
      formData.append('guidance_scale', guidanceScale);
      formData.append('num_inference_steps', numInferenceSteps);
      formData.append('seed', seed);
      formData.append('num_outputs', numOutputs);
      
      const response = await startInpaintingProcess(formData);
      
      if (response && response.id) {
        // Sonuçları kontrol etmek için polling yap
        const pollInterval = setInterval(async () => {
          const result = await checkInpaintingStatus(response.id);
          
          if (result.status === 'completed') {
            clearInterval(pollInterval);
            setResults(result.images || []);
            setIsProcessing(false);
          } else if (result.status === 'failed') {
            clearInterval(pollInterval);
            alert(`İşlem başarısız oldu: ${result.error || 'Bilinmeyen hata'}`);
            setIsProcessing(false);
          }
        }, 2000);
      }
    } catch (error) {
      console.error('Inpainting hatası:', error);
      alert('İşlem sırasında bir hata oluştu');
      setIsProcessing(false);
    }
  };
  
  return (
    <div className="w-full mt-6 mb-4 bg-white p-4 rounded-lg shadow-sm border border-gray-200">
      <h2 className="text-xl font-semibold text-gray-800 mb-4">Inpainting Parametreleri</h2>
      
      <form onSubmit={handleSubmit}>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-gray-700 text-sm font-bold mb-2">
              Prompt (İstenilen içeriği tanımlayın)
            </label>
            <textarea
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              className="w-full p-2 border border-gray-300 rounded-md"
              rows="3"
              placeholder="İnpainting için yapay zekaya ne oluşturmasını istediğinizi açıklayın..."
            />
          </div>
          
          <div>
            <label className="block text-gray-700 text-sm font-bold mb-2">
              Negatif Prompt (İstenmeyen içeriği tanımlayın)
            </label>
            <textarea
              value={negativePrompt}
              onChange={(e) => setNegativePrompt(e.target.value)}
              className="w-full p-2 border border-gray-300 rounded-md"
              rows="3"
              placeholder="İstemediğiniz özellikleri buraya yazın (örn: bulanık, kötü kalite)..."
            />
          </div>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mt-4">
          <div>
            <label className="block text-gray-700 text-sm font-bold mb-2">
              Guidance Scale (Prompt etkisi)
            </label>
            <div className="flex items-center">
              <input
                type="range"
                min="1"
                max="20"
                step="0.1"
                value={guidanceScale}
                onChange={(e) => setGuidanceScale(parseFloat(e.target.value))}
                className="w-full"
              />
              <span className="ml-2 text-sm text-gray-700">{guidanceScale}</span>
            </div>
          </div>
          
          <div>
            <label className="block text-gray-700 text-sm font-bold mb-2">
              Adım Sayısı
            </label>
            <div className="flex items-center">
              <input
                type="range"
                min="10"
                max="50"
                value={numInferenceSteps}
                onChange={(e) => setNumInferenceSteps(parseInt(e.target.value))}
                className="w-full"
              />
              <span className="ml-2 text-sm text-gray-700">{numInferenceSteps}</span>
            </div>
          </div>
          
          <div>
            <label className="block text-gray-700 text-sm font-bold mb-2">
              Seed
            </label>
            <div className="flex items-center">
              <input
                type="number"
                value={seed}
                onChange={(e) => setSeed(parseInt(e.target.value))}
                className="w-24 p-1 border border-gray-300 rounded-md"
              />
              <button
                type="button"
                onClick={generateRandomSeed}
                className="ml-2 bg-gray-200 text-gray-700 px-2 py-1 rounded text-xs"
              >
                Rastgele
              </button>
              <span className="ml-2 text-xs text-gray-500">(-1: otomatik)</span>
            </div>
          </div>
          
          <div>
            <label className="block text-gray-700 text-sm font-bold mb-2">
              Sonuç Sayısı
            </label>
            <select
              value={numOutputs}
              onChange={(e) => setNumOutputs(parseInt(e.target.value))}
              className="w-full p-1 border border-gray-300 rounded-md"
            >
              <option value="1">1 sonuç</option>
              <option value="2">2 sonuç</option>
              <option value="4">4 sonuç</option>
            </select>
          </div>
        </div>
        
        <div className="mt-6">
          <button
            type="submit"
            disabled={!mask || isProcessing}
            className={`py-3 px-8 rounded-lg font-semibold ${
              !mask || isProcessing
                ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                : 'bg-blue-600 text-white hover:bg-blue-700'
            }`}
          >
            {isProcessing ? 'İşleniyor...' : 'Inpainting İşlemini Başlat'}
          </button>
        </div>
      </form>
    </div>
  );
};