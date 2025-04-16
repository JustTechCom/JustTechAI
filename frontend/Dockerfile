# Build aşaması
FROM node:16-alpine as build

WORKDIR /app

# Sadece package.json'ı kopyala (package-lock.json gerektirme)
COPY package.json ./
RUN npm install

# Kaynak kodları kopyala
COPY public/ public/
COPY src/ src/

# Üretim için build al
RUN npm run build

# Üretim aşaması
FROM nginx:alpine

# Nginx yapılandırması
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Build klasörünü Nginx'e kopyala
COPY --from=build /app/build /usr/share/nginx/html

# 80 portunu dışarı aç
EXPOSE 80

# Nginx'i başlat
CMD ["nginx", "-g", "daemon off;"]