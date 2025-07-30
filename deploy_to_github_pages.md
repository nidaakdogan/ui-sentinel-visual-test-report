# 🚀 HTML Raporu GitHub Pages'te Yayınlama

## Adım 1: GitHub Repository Oluştur
```bash
# Yeni bir repository oluştur
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/KULLANICI_ADIN/AIVisionTest.git
git push -u origin main
```

## Adım 2: GitHub Pages Ayarları
1. GitHub'da repository'nize gidin
2. **Settings** > **Pages** sekmesine tıklayın
3. **Source** kısmında **Deploy from a branch** seçin
4. **Branch** olarak **main** seçin
5. **Folder** olarak **/ (root)** seçin
6. **Save** butonuna tıklayın

## Adım 3: Raporu Yayınla
```bash
# En son raporu ana dizine kopyala
cp reports/ui_sentinel_report_*.html index.html

# Commit ve push yap
git add index.html
git commit -m "Add latest report"
git push origin main
```

## Adım 4: Erişim
Raporunuz şu adreste yayınlanacak:
`https://KULLANICI_ADIN.github.io/AIVisionTest/`

---

## 🔄 Otomatik Güncelleme Scripti
```bash
# deploy.sh dosyası oluştur
echo '#!/bin/bash
cp reports/ui_sentinel_report_*.html index.html
git add index.html
git commit -m "Update report $(date)"
git push origin main
echo "Rapor güncellendi: https://KULLANICI_ADIN.github.io/AIVisionTest/"' > deploy.sh

chmod +x deploy.sh
```

Kullanım: `./deploy.sh` 