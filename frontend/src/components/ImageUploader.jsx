import React from 'react';

export const ImageUploader = ({ setOriginalImage }) => {
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    
    const reader = new FileReader();
    reader.onload = (event) => {
      setOriginalImage(event.target.result);
    };
    reader.readAsDataURL(file);
  };
  
  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
  };
  
  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      
      // Sadece resim dosyalarını kabul et
      if (!file.type.match('image.*')) {
        alert('Lütfen sadece resim dosyası yükleyin');
        return;
      }
      
      const reader = new FileReader();
      reader.onload = (event) => {
        setOriginalImage(event.target.result);
      };
      reader.readAsDataURL(file);
    }
  };
  
  return (
    <div className="mb-6 w-full">
      <label className="block text-gray-700 text-sm font-bold mb-2">
        Resim Yükle
      </label>
      
      <div 
        className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center cursor-pointer hover:bg-gray-50"
        onDragOver={handleDragOver}
        onDrop={handleDrop}
        onClick={() => document.getElementById('file-upload').click()}
      >
        <input 
          id="file-upload"
          type="file" 
          accept="image/*" 
          onChange={handleFileChange}
          className="hidden"
        />
        <div className="flex flex-col items-center justify-center">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 text-gray-400 mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          <p className="text-gray-700 font-medium mb-1">Resim yüklemek için tıklayın veya sürükleyip bırakın</p>
          <p className="text-gray-500 text-sm">PNG, JPG, WEBP dosyaları desteklenir</p>
        </div>
      </div>
    </div>
  );
};