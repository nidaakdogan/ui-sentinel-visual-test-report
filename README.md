# 🔍 UI Sentinel - Görsel UI Test Otomasyonu

**UI Sentinel**, web sayfalarının görsel tutarlılığını test eden gelişmiş bir otomasyon aracıdır. Selenium WebDriver ve OpenCV kullanarak pixel-perfect karşılaştırmalar yapar.

## ✨ Özellikler

### 🎯 Temel Özellikler
- **Görsel Karşılaştırma**: Baseline ve test görüntüleri arasında pixel-perfect karşılaştırma
- **Otomatik Screenshot**: Selenium ile otomatik ekran görüntüsü alma
- **Akıllı Pop-up Yönetimi**: Google gibi sitelerde pop-up'ları otomatik kapatma
- **Tema Tutarlılığı**: Light/dark tema değişikliklerini kontrol etme
- **Detaylı Raporlama**: HTML, JSON ve PDF formatlarında kapsamlı raporlar

### 📊 Raporlama Sistemi
- **HTML Raporları**: İnteraktif, zoom özellikli detaylı raporlar
- **PDF İndirme**: Tek tıkla PDF oluşturma butonu
- **Görsel Analiz**: Fark haritaları ve karşılaştırma görüntüleri
- **Metrik Kartları**: Benzerlik oranı, fark yüzdesi, piksel sayısı

### 🛠️ Teknik Özellikler
- **OpenCV**: Görüntü işleme ve karşılaştırma
- **Selenium WebDriver**: Tarayıcı otomasyonu
- **Jinja2**: HTML şablon motoru
- **Responsive Design**: Mobil uyumlu raporlar

## 🚀 Hızlı Başlangıç

### Gereksinimler
```bash
# Python 3.8+ gerekli
python --version

# Chrome tarayıcısı gerekli
# ChromeDriver otomatik indirilir
```

### Kurulum
```bash
# Repository'yi klonla
git clone https://github.com/KULLANICI_ADIN/AIVisionTest.git
cd AIVisionTest

# Bağımlılıkları yükle
pip install -r requirements.txt
```

### Kullanım
```bash
# Testleri çalıştır
python run_tests.py

# Raporları görüntüle
# reports/ klasöründeki HTML dosyalarını tarayıcıda aç
```


### Dil Ayarları (`config/language_config.json`)
```json
{
  "en": {
    "summary_cards": {
      "total_tests": "Total Tests",
      "passed_tests": "Passed Tests"
    }
  },
  "tr": {
    "summary_cards": {
      "total_tests": "Toplam Test",
      "passed_tests": "Geçen Test"
    }
  }
}
```

## 📊 Raporlama Sistemi

### HTML Raporları
- **İnteraktif Görseller**: Tıklayarak büyütme
- **Zoom Özelliği**: Fark haritalarını yakınlaştırma
- **Responsive Design**: Mobil uyumlu
- **PDF İndirme**: Tek tıkla PDF oluşturma

### Rapor İçeriği
- **Test Özeti**: Toplam, geçen, kalan test sayıları
- **Detaylı Metrikler**: Benzerlik oranı, fark yüzdesi
- **Görsel Karşılaştırma**: Baseline vs Test görüntüleri
- **Fark Haritası**: Değişen alanların görselleştirilmesi
- **Akıllı Analiz**: Otomatik değişiklik tespiti

## 🎨 Görsel Karşılaştırma Sistemi

### Karşılaştırma Algoritması
1. **Görüntü Ön İşleme**: Boyut standardizasyonu
2. **Pixel Karşılaştırma**: OpenCV ile piksel bazlı analiz
3. **Fark Tespiti**: Eşik değeri kontrolü
4. **Sonuç Analizi**: Benzerlik oranı hesaplama

### Özel Ayarlar
- **Google**: Pop-up kapatma ve tema kontrolü
- **GitHub**: Dinamik içerik toleransı
- **Stack Overflow**: Responsive tasarım uyumu

## 📈 Performans

### Test Süreleri
- **Tek Sayfa**: ~30-60 saniye
- **3 Sayfa**: ~2-3 dakika
- **Rapor Oluşturma**: ~10-15 saniye


