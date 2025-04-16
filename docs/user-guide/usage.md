# Stable Diffusion 2.0 Inpainting Kullanım Kılavuzu

Bu belge, Stable Diffusion 2.0 Inpainting sisteminin kullanımı için adım adım kılavuz sağlar.

## İçindekiler

1. [Giriş](#giriş)
2. [Sistem Gereksinimleri](#sistem-gereksinimleri)
3. [Arayüz Tanıtımı](#arayüz-tanıtımı)
4. [Adım Adım Kullanım](#adım-adım-kullanım)
5. [Parametreler ve Ayarlamalar](#parametreler-ve-ayarlamalar)
6. [İpuçları ve Teknikler](#i̇puçları-ve-teknikler)
7. [Sorun Giderme](#sorun-giderme)

## Giriş

Stable Diffusion 2.0 Inpainting, yapay zeka kullanarak görüntülerdeki istenmeyen alanları veya nesneleri kaldırmanıza ve yerlerine yeni içerik oluşturmanıza olanak tanır. Kullanıcı dostu arayüzü sayesinde, herhangi bir teknik bilgi gerektirmeden profesyonel sonuçlar elde edebilirsiniz.

## Sistem Gereksinimleri

Tarayıcı Gereksinimleri:
- Google Chrome (son sürüm)
- Mozilla Firefox (son sürüm)
- Microsoft Edge (son sürüm)
- Safari (son sürüm)

Donanım Gereksinimleri (İstemci bilgisayarı için):
- Minimum 4GB RAM
- Herhangi bir modern işlemci
- İnternet bağlantısı

## Arayüz Tanıtımı

Uygulama arayüzü şu ana bölümlerden oluşur:

1. **Resim Yükleme Alanı**: Düzenlemek istediğiniz görüntüyü yükleyebileceğiniz bölüm.
2. **Mask Oluşturma Alanı**: İnpainting uygulanacak bölgeleri işaretleyebileceğiniz çizim alanı.
3. **Parametre Kontrolleri**: İnpainting işlemini özelleştirmek için kullanılan parametreler.
4. **Sonuç Görüntüleme Alanı**: İşlem sonucunda oluşturulan görüntüleri gösteren bölüm.

## Adım Adım Kullanım

### 1. Resim Yükleme

- "Resim Yükle" butonuna tıklayın veya bir resmi sürükleyip bırakın.
- Yüklenen resim, ekranda görüntülenecektir.

### 2. Mask Oluşturma

- Silinmesini veya değiştirilmesini istediğiniz alanları siyah fırça ile boyayın.
- Fırça boyutunu ayarlamak için sürgüyü kullanın.
- İşaretlemeyi sıfırlamak için "Maskı Temizle" butonunu kullanın.

### 3. Parametre Ayarları

- **Prompt**: İnpainting için ne oluşturulmasını istediğinizi metin olarak belirtin (örn. "mavi gökyüzü", "yeşil çimen").
- **Negatif Prompt**: İstemediğiniz öğeleri belirtin (örn. "bulanık", "kötü kalite").
- **Guidance Scale**: Promptun etkisini belirler (1-20 arası).
- **Adım Sayısı**: Kalite/hız dengesi için adım sayısını ayarlayın (10-50 arası).
- **Seed**: Belirli bir sonucu tekrar elde etmek için seed numarası belirleyin.
- **Sonuç Sayısı**: Kaç farklı varyasyon oluşturulacağını seçin.

### 4. İnpainting İşlemi

- Tüm ayarlar tamamlandığında "İnpainting İşlemini Başlat" butonuna tıklayın.
- İşlem sırasında bir ilerleme göstergesi görünecektir.
- İşlem tamamlandığında sonuçlar ekranda görüntülenecektir.

### 5. Sonuçları Görüntüleme ve İndirme

- Birden fazla sonuç oluşturulduğunda, küçük resimlerden birini seçerek büyük görüntüde inceleyebilirsiniz.
- Beğendiğiniz sonucu indirmek için "Sonucu İndir" butonunu kullanın.

## Parametreler ve Ayarlamalar

### Prompt (Metin İsteği)

İyi bir prompt yazmak, kaliteli sonuçlar elde etmenin en önemli kısmıdır. İşte bazı ipuçları:

- Mümkün olduğunca detaylı ve açık olun
- Stil, renk, doku gibi özellikleri belirtin
- Örnek: "Güneş ışığı altında parlayan mavi deniz manzarası, berrak su"

### Guidance Scale

- **Düşük değerler (1-7)**: Daha yaratıcı ama bazen alakasız sonuçlar
- **Orta değerler (7-12)**: Çoğu durumda iyi bir denge
- **Yüksek değerler (12+)**: Prompta daha sadık ama bazen yapay görünümlü sonuçlar

### Adım Sayısı

- **Düşük adım sayısı (10-20)**: Hızlı ama daha az detaylı sonuçlar
- **Orta adım sayısı (20-30)**: İyi bir denge
- **Yüksek adım sayısı (30+)**: Yüksek kaliteli ama daha yavaş sonuçlar

## İpuçları ve Teknikler

### Daha İyi Maske Oluşturma

- Nesnenin kenarlarını dikkatlice işaretleyin
- Tamamen silmek istediğiniz alanı tamamen kaplayın
- Büyük alanlar için daha büyük fırça boyutu kullanın

### Prompt Optimizasyonu

- Art stili belirtmek (örn. "fotoğrafik", "yağlı boya", "çizim") sonucu büyük ölçüde etkiler
- İstenmeyen detaylar için negatif prompt kullanın
- Aynı prompt ile farklı seed'ler deneyin

### İteratif İnpainting

Karmaşık düzenlemeler için adım adım yaklaşım:
1. Önce ana nesneyi silin
2. Sonucu yeniden yükleyin
3. Kalan detayları düzeltin
4. Gerekirse tekrarlayın

## Sorun Giderme

### Sık Karşılaşılan Sorunlar

1. **"İşlem başarısız oldu" hatası**
   - Çözüm: Daha küçük bir maske alanı veya daha küçük bir görüntü deneyin

2. **Maske işaretleri görünmüyor**
   - Çözüm: Tarayıcıyı yenileyin ve tekrar deneyin

3. **Sonuçlar beklenen gibi değil**
   - Çözüm: Promtu daha detaylı hale getirin veya farklı bir seed ile tekrar deneyin

4. **Uygulama yanıt vermiyor**
   - Çözüm: Tarayıcıyı yenileyin, çok büyük görüntülerden kaçının

### İletişim ve Destek

Teknik destek için: support@yourdomain.com

Lisans ve satın alma için: sales@yourdomain.com