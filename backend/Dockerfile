# CUDA ve CPU desteğine sahip temel imaj
FROM pytorch/pytorch:2.0.0-cuda11.7-cudnn8-runtime

WORKDIR /app

# Sistem bağımlılıklarını yükle
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Python bağımlılıklarını kopyala ve yükle
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Uygulama kodlarını kopyala
COPY . .

# Çıktı klasörünü oluştur
RUN mkdir -p output

# Uygulamayı çalıştır
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]