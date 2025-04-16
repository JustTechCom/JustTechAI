const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const fetchDeviceInfo = async () => {
  const response = await fetch(`${API_BASE_URL}/device-info`);
  if (!response.ok) {
    throw new Error('Cihaz bilgileri alınamadı');
  }
  return await response.json();
};

export const startInpaintingProcess = async (formData) => {
  const response = await fetch(`${API_BASE_URL}/inpaint`, {
    method: 'POST',
    body: formData,
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'İnpainting işlemi başlatılamadı');
  }
  
  return await response.json();
};