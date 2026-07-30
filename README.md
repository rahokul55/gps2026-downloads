# GPS 2026 Türkçe Yama — dağıtım deposu

Bu depo **GeoPolitical Simulator 2026** için hazırlanan bağımsız Türkçe yamanın
resmî dağıtım noktasıdır. Kurulum dosyaları Releases bölümünde, tanıtım medyası
`medya/` klasöründe tutulur.

İndirme sayfası: <https://43software.com.tr>

## Depoda ne var?

| Yol | Açıklama |
| --- | --- |
| `surum.json` | Başlatıcının okuduğu sürüm bildirimi. Yeni sürüm çıkınca **ilk burası** güncellenir. |
| `medya/gorsel/` | Ekran görüntüleri (`.png`, `.jpg`, `.webp`) |
| `medya/video/` | Tanıtım videoları (`.mp4`, `.webm`) |
| `medya/basliklar.json` | Dosya adına göre başlık/açıklama karşılıkları |
| `medya/medya.json` | **Otomatik üretilir.** Elle düzenlemeyin. |
| `medya/kucuk/` | **Otomatik üretilir.** Küçük önizleme görselleri. |

Kurulum dosyalarının kendisi depoda tutulmaz; yalnızca
[Releases](../../releases) altında yayımlanır.

## Medya nasıl eklenir?

Üç yol var, üçü de aynı sonuca çıkar:

1. **GitHub üzerinden sürükle-bırak** — `medya/gorsel` klasörünü açın,
   `Add file → Upload files` ile dosyaları bırakın, commit edin.
2. **Yönetim paneli** — <https://43software.com.tr/yonetim> adresinden giriş
   yapıp medya bölümünden yükleyin; dosya buraya kendiliğinden düşer.
3. **Yerel araç** — `araclar/medya_yukle.py` bir klasördeki tüm görsel ve
   videoları buraya gönderir.

Dosya eklendiği anda `Medya dizini` iş akışı çalışır; `medya/medya.json`
dosyasını ve küçük önizlemeleri yeniden üretip commit eder. Site galeriyi bu
dizinden okur, ayrıca bir işlem gerekmez.

Dosya adı başlık olarak kullanılır: `kurulum-adim-1.png` → “Kurulum adım 1”.
Farklı bir başlık isterseniz `medya/basliklar.json` içine yazın.

## Yeni sürüm yayımlama

1. `v<sürüm>` etiketiyle bir Release açın (örnek: `v2.7`).
2. `gps2026turkceyama.exe` ve `GPS2026Baslat.exe` dosyalarını ekleyin.
3. `surum.json` içindeki `surum`, `indirme`, `sha256`, `boyut`, `notlar`
   alanlarını güncelleyip `main` dalına gönderin.

`Sürüm bildirimi denetimi` iş akışı, `surum.json` içindeki bağlantının gerçekten
yayımlanmış bir dosyayı gösterdiğini ve boyutun tuttuğunu doğrular.

Oyuncunun bilgisayarındaki `GPS2026Baslat.exe`, oyunu her açışta `surum.json`
dosyasını okur; daha yeni sürüm varsa güncellemeyi sorar.

---

Bu proje resmî değildir; oyunun geliştiricisi veya yayıncısıyla bağlantılı
değildir. Yamayı kullanmak için orijinal oyuna sahip olmanız gerekir.
