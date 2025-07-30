# 🌐 HTML Raporu Netlify'da Yayınlama

## Adım 1: Netlify Hesabı Oluştur
1. [netlify.com](https://netlify.com)'a gidin
2. **Sign up** ile hesap oluşturun (GitHub ile giriş yapabilirsiniz)

## Adım 2: Raporu Yükle
### Yöntem A: Drag & Drop
1. `reports/ui_sentinel_report_*.html` dosyasını `index.html` olarak yeniden adlandırın
2. Netlify dashboard'da **Sites** bölümüne gidin
3. Dosyayı sürükleyip bırakın

### Yöntem B: GitHub'dan
1. GitHub repository'nizi Netlify'a bağlayın
2. **Build command**: boş bırakın
3. **Publish directory**: `/` (root)
4. **Deploy** butonuna tıklayın

## Adım 3: Özel Domain (İsteğe Bağlı)
1. **Domain settings** > **Custom domains**
2. Kendi domain'inizi ekleyin

## Adım 4: Erişim
Raporunuz şu adreste yayınlanacak:
`https://random-name.netlify.app/`

---

## 🔄 Otomatik Güncelleme
GitHub repository'nizi Netlify'a bağlarsanız, her commit'te otomatik güncellenir. 