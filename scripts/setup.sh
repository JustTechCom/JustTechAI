#!/bin/bash

# Stable Diffusion 2.0 Inpainting Sistemi Kurulum Betiği

# Renkli çıktı için
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Stable Diffusion 2.0 Inpainting Sistemi Kurulumu${NC}"
echo "======================================================"
echo

# Docker ve Docker Compose kontrolü
echo -e "${YELLOW}Docker ve Docker Compose kontrol ediliyor...${NC}"
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Docker bulunamadı. Lütfen Docker'ı yükleyin.${NC}"
    echo "https://docs.docker.com/get-docker/"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Docker Compose bulunamadı. Lütfen Docker Compose'u yükleyin.${NC}"
    echo "https://docs.docker.com/compose/install/"
    exit 1
fi

echo -e "${GREEN}Docker ve Docker Compose mevcut.${NC}"

# NVIDIA GPU kontrolü
echo -e "${YELLOW}NVIDIA GPU kontrol ediliyor...${NC}"
if command -v nvidia-smi &> /dev/null; then
    echo -e "${GREEN}NVIDIA GPU bulundu. GPU desteği etkinleştirilecek.${NC}"
    # NVIDIA Container Toolkit kontrolü
    if ! docker info | grep -i nvidia > /dev/null; then
        echo -e "${YELLOW}NVIDIA Container Toolkit bulunamadı.${NC}"
        echo "GPU desteği için NVIDIA Container Toolkit yükleyebilirsiniz:"
        echo "https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html"
    else
        echo -e "${GREEN}NVIDIA Container Toolkit mevcut.${NC}"
    fi
else
    echo -e "${YELLOW}NVIDIA GPU bulunamadı. Sistem CPU modunda çalışacak.${NC}"
fi

# Klasör yapısını oluştur
echo -e "${YELLOW}Klasör yapısı oluşturuluyor...${NC}"
mkdir -p frontend/public frontend/src/components frontend/src/services
mkdir -p backend/app/models backend/app/routers backend/app/services backend/app/utils backend/config backend/output backend/tests
mkdir -p scripts
mkdir -p docs/api docs/user-guide docs/deployment

echo -e "${GREEN}Klasör yapısı oluşturuldu.${NC}"

# Docker-compose dosyasını oluştur
echo -e "${YELLOW}Docker Compose yapılandırması oluşturuluyor...${NC}"
cp -v docker-compose.yml docker-compose.override.yml

echo -e "${GREEN}Docker Compose yapılandırması oluşturuldu.${NC}"

# .env dosyasını oluştur
echo -e "${YELLOW}.env dosyası oluşturuluyor...${NC}"
cat > backend/.env << EOL
DEBUG=0
DEVELOPMENT_MODE=1
USE_CPU=0
EOL

echo -e "${GREEN}.env dosyası oluşturuldu.${NC}"

# Gerekli izinleri ayarla
echo -e "${YELLOW}İzinler ayarlanıyor...${NC}"
chmod +x scripts/*

echo -e "${GREEN}İzinler ayarlandı.${NC}"

echo
echo -e "${GREEN}Kurulum tamamlandı!${NC}"
echo
echo "Sistemi başlatmak için:"
echo "  docker-compose up -d"
echo
echo "Sistemi durdurmak için:"
echo "  docker-compose down"
echo
echo "Web arayüzüne erişmek için:"
echo "  http://localhost:3000"
echo
echo "İyi çalışmalar!"