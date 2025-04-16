const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const checkInpaintingStatus = async (taskId) => {
  const response = await fetch(`${API_BASE_URL}/inpaint/${taskId}`);
  
  if (!response.ok) {
    throw new Error('İşlem durumu alınamadı');
  }
  
  return await response.json();
};