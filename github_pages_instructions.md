# 🔗 GitHub Pages ile Link Oluşturma

## Adım 1: GitHub Repository Oluştur
1. [github.com](https://github.com)'a git
2. **New repository** butonuna tıkla
3. Repository adı: `AIVisionTest`
4. **Public** seç
5. **Create repository** butonuna tıkla

## Adım 2: Kodu GitHub'a Yükle
```bash
git remote add origin https://github.com/KULLANICI_ADIN/AIVisionTest.git
git branch -M main
git push -u origin main
```

## Adım 3: GitHub Pages Aktifleştir
1. Repository'de **Settings** sekmesine git
2. Sol menüde **Pages** seç
3. **Source** kısmında **Deploy from a branch** seç
4. **Branch** olarak **main** seç
5. **Folder** olarak **/ (root)** seç
6. **Save** butonuna tıkla

## Adım 4: Link Hazır!
Raporun şu adreste yayınlanacak:
`https://KULLANICI_ADIN.github.io/AIVisionTest/`

---
## 🚀 Hızlı Komutlar
```bash
# GitHub'a bağlan
git remote add origin https://github.com/KULLANICI_ADIN/AIVisionTest.git

# Kodu yükle
git branch -M main
git push -u origin main

# Link hazır!
echo "Rapor linki: https://KULLANICI_ADIN.github.io/AIVisionTest/"
``` 