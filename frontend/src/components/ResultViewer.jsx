import React, { useState } from 'react';

export const ResultViewer = ({ results }) => {
  const [selectedIndex, setSelectedIndex] = useState(0);
  
  if (results.length === 0) return null;
  
  return (
    <div className="w-full">
      <h2 className="text-xl font-semibold text-gray-800 mb-4">Sonuçlar</h2>
      
      {results.length > 1 && (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          {results.map((result, index) => (
            <div 
              key={index} 
              className={`border p-2 cursor-pointer ${selectedIndex === index ? 'border-blue-500 ring-2 ring-blue-300' : 'border-gray-300'}`}
              onClick={() => setSelectedIndex(index)}
            >
              <img src={result.image} alt={`Sonuç ${index + 1}`} className="max-w-full" />
              <div className="mt-2 text-xs text-gray-500">
                <p>Seed: {result.seed}</p>
              </div>
            </div>
          ))}
        </div>
      )}
      
      <div className="mt-4">
        <h3 className="text-lg font-semibold text-gray-800 mb-2">
          {results.length > 1 ? 'Seçilen Sonuç' : 'Sonuç'}
        </h3>
        <div className="border border-gray-300 p-1 inline-block">
          <img src={results[selectedIndex].image} alt="İnpainting Sonucu" className="max-w-full" />
        </div>
        
        <div className="mt-4">
          <a
            href={results[selectedIndex].image}
            download="sd_inpainting_result.png"
            className="bg-green-600 text-white py-2 px-6 rounded-lg font-semibold hover:bg-green-700">
          
            Sonucu İndir</a> 
        </div>
      </div>
    </div>
  );
};