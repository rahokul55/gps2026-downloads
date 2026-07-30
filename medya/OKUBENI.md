# Medya klasörü

Sitedeki galeri doğrudan bu klasörden beslenir.

- `gorsel/` — ekran görüntüleri: `.png`, `.jpg`, `.webp`, `.gif`
- `video/` — tanıtım videoları: `.mp4`, `.webm`
- `basliklar.json` — dosya adına göre başlık, açıklama ve sıra
- `medya.json` — **otomatik üretilir**, elle düzenlemeyin
- `kucuk/` — **otomatik üretilir**, küçük önizlemeler

## Dosya eklemek

`gorsel` veya `video` klasörünü GitHub'da açın, `Add file → Upload files` ile
dosyaları bırakın ve commit edin. Birkaç dakika içinde `Medya dizini` iş akışı
`medya.json` dosyasını yeniler ve galeri kendiliğinden güncellenir.

Dosya adı başlık olur: `sirket-paneli.png` → “Sirket paneli”. Türkçe karakterli
düzgün bir başlık için `basliklar.json` kullanın.

## Boyut sınırları

| Tür | Önerilen | Üst sınır |
| --- | --- | --- |
| Görsel | 2 MB altı | 10 MB |
| Video | 20 MB altı | 50 MB |

Depo boyutu şişmesin diye uzun videoları buraya değil, `medya` etiketli bir
Release'e yükleyin; iş akışı oradaki dosyaları da galeriye alır.

Yüklenen her dosya herkese açıktır. Kişisel bilgi, oyun anahtarı veya ekranında
e-posta görünen görsel yüklemeyin.
