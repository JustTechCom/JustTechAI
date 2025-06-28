# Stable Diffusion 2.0 İnpainting Sistemi

Bu sistem, Stable Diffusion 2.0 kullanarak gelişmiş inpainting işlemleri yapabilen profesyonel bir uygulamadır. Sistem, donanım kaynaklarını otomatik olarak tespit ederek en iyi performansı sağlayacak şekilde kendini yapılandırır.

## Temel Özellikler

- **Otomatik Cihaz Tespiti**: GPU/CPU otomatik seçimi
- **Yüksek Kaliteli İnpainting**: Stable Diffusion 2.0 modeli
- **Metin Tabanlı Kontrol**: Prompt ile sonuçları yönetme
- **Çoklu Sonuç Üretebilme**: Aynı maske için farklı varyasyonlar
- **Donanım Optimizasyonları**: Hem GPU hem CPU için optimize edilmiş

## Kurulum

### Docker ile Kurulum

1. Bu repo'yu klonlayın:
```bash
git clone https://github.com/kadirertancam/JustTechAI.git
cd JustTechAI

Docker Compose ile sistemi başlatın:

bashdocker-compose up -d

Tarayıcınızda şu adrese gidin:

http://localhost:3000
Lisanslama
Bu sistem ticari bir üründür ve lisans anahtarı ile çalışır. Lisans almak için iletişime geçin:
destekadresi@domain.com
Yeni bir lisans oluşturmak için:
bashcd scripts
python generate_license.py --name "Müşteri Adı" --email "musteri@email.com" --plan pro --days 365
Kullanım

Web arayüzünü açın
Bir resim yükleyin
Siyah fırça ile inpainting uygulanacak alanları işaretleyin
Promptunuzu yazın (örn. "mavi gökyüzü", "yeşil çimen", vb.)
İsteğe bağlı olarak Guidance Scale, Adım Sayısı gibi parametreleri ayarlayın
"Inpainting İşlemini Başlat" düğmesine tıklayın
İşlem tamamlanınca sonuçları görüntüleyin ve isterseniz indirin

Sistem Gereksinimleri
Minimum Gereksinimler

8GB RAM
4 çekirdekli CPU
10GB depolama alanı

Önerilen Gereksinimler

NVIDIA GPU (en az 4.5GB VRAM)
CUDA 11.4+
16GB RAM
6+ çekirdekli CPU
15GB depolama alanı

Sorun Giderme
Sık karşılaşılan sorunlar için:

"CUDA cihazı bulunamadı" hatası:

NVIDIA sürücülerinin güncel olduğundan emin olun
nvidia-smi komutunu çalıştırarak GPU'nun görünür olup olmadığını kontrol edin


"Bellek yetersiz" hatası:

Daha küçük görüntülerle çalışın
Daha az sayıda sonuç isteyin (1 veya 2)


"Lisans geçersiz" hatası:

Lisans anahtarınızın geçerli ve aktif olduğundan emin olun
Lisans sürenizin dolup dolmadığını kontrol edin



İletişim ve Destek
Ticari kullanım ve destek için iletişime geçin:
destekadresi@domain.com


Not: Stable Diffusion 2.0, Stability AI tarafından geliştirilmiştir ve CreativeML Open RAIL-M lisansı altında dağıtılmaktadır.

Bu dosyalar, profesyonel bir Stable Diffusion 2.0 inpainting sistemi için temel bir kod tabanını oluşturmaktadır. Sistemde:

1. Otomatik donanım tespiti
2. Lisanslama altyapısı
3. Frontend ve backend entegrasyonu
4. Docker ile kolay dağıtım

özellikleri bulunmaktadır. Bu yapı, ticari bir ürün olarak kullanıma hazırdır ve gerektiğinde özel ihtiyaçlara göre genişletilebilir. 

Dosya yapısını ve kodları kendi projenize uyarladığınızda, tamamen fonksiyonel bir sistem elde edeceksiniz. Lütfen herhangi bir özel ihtiyacınız veya sorunuz olursa belirtin!