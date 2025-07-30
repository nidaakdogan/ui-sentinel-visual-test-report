import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
import json
import cv2
import numpy as np


class ScreenshotCapture:
    def __init__(self, config_file="config/test_config.json"):
        """Screenshot capture sınıfını başlatır"""
        self.config_file = config_file
        self.config = self._load_config()
        self.driver = None
        self.screenshots_dir = "screenshots"
        
        # Browser ayarlarını yapılandır
        self.setup_browser()
    
    def _load_config(self):
        """Konfigürasyon dosyasını yükler"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Hata: {self.config_file} dosyası bulunamadı!")
            return {}
    
    def setup_browser(self):
        """Browser ayarlarını yapılandırır"""
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.service import Service
            from webdriver_manager.chrome import ChromeDriverManager
            from selenium.webdriver.chrome.options import Options
            
            # Chrome options - minimal ayarlar
            chrome_options = Options()
            
            # Headless modu KESINLIKLE KAPAT
            # chrome_options.add_argument("--headless")
            
            # Temel ayarlar
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--window-size=1920,1080")
            
            # WebDriver'ı başlat
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            print("✅ Chrome WebDriver başarıyla başlatıldı")
            
        except Exception as e:
            print(f"❌ WebDriver başlatma hatası: {e}")
            raise
    
    def capture_screenshot(self, page_config):
        """Belirtilen sayfanın ekran görüntüsünü alır"""
        page_name = page_config['name']
        url = page_config['url']
        wait_time = page_config.get('wait_time', 5)  # Daha uzun bekleme
        
        print(f"📸 {page_name} sayfasının ekran görüntüsü alınıyor...")
        print(f"🌐 URL: {url}")
        
        try:
            # Sayfaya git
            self.driver.get(url)
            
            # Google için özel bekleme
            if 'google' in page_name.lower():
                print("🎯 Google sayfası için özel bekleme uygulanıyor...")
                wait_time = max(wait_time, 8)  # En az 8 saniye bekle
            
            # Sayfanın tamamen yüklenmesini bekle
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.common.by import By
            
            # Sayfa yüklenmesini bekle
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # JavaScript'in çalışmasını bekle
            WebDriverWait(self.driver, 20).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            
            # Sayfanın yüklenmesini bekle
            time.sleep(wait_time)
            
            # Google için ek kontrol
            if 'google' in page_name.lower():
                # Google logosunun yüklenip yüklenmediğini kontrol et
                try:
                    logo = self.driver.find_element(By.ID, "hplogo")
                    if logo.is_displayed():
                        print("✅ Google logosu yüklendi")
                    else:
                        print("⚠️ Google logosu görünmüyor, ek bekleme...")
                        time.sleep(3)
                except:
                    print("⚠️ Google logosu bulunamadı, ek bekleme...")
                    time.sleep(3)
                
                # Gemini pop-up'ını kapat
                try:
                    # Pop-up'ın yüklenmesini bekle
                    time.sleep(3)
                    
                    # Daha kapsamlı pop-up kapatma
                    self.driver.execute_script("""
                        // Tüm pop-up'ları bul ve kapat
                        const selectors = [
                            '[role="dialog"]',
                            '.gemini-popup',
                            '[data-testid*="popup"]',
                            '[data-testid*="modal"]',
                            '.modal',
                            '.popup',
                            '[aria-modal="true"]'
                        ];
                        
                        selectors.forEach(selector => {
                            const elements = document.querySelectorAll(selector);
                            elements.forEach(element => {
                                // Kapatma butonlarını bul
                                const closeButtons = element.querySelectorAll('button, [role="button"], .close, [aria-label*="close"], [aria-label*="kapat"]');
                                closeButtons.forEach(btn => {
                                    if (btn.textContent.toLowerCase().includes('close') || 
                                        btn.textContent.toLowerCase().includes('kapat') ||
                                        btn.getAttribute('aria-label')?.toLowerCase().includes('close') ||
                                        btn.getAttribute('aria-label')?.toLowerCase().includes('kapat')) {
                                        btn.click();
                                        console.log('Pop-up kapatıldı:', selector);
                                    }
                                });
                            });
                        });
                        
                        // ESC tuşu simülasyonu
                        document.dispatchEvent(new KeyboardEvent('keydown', {key: 'Escape', keyCode: 27}));
                    """)
                    print("✅ Pop-up kapatma işlemi tamamlandı")
                    time.sleep(1)
                        
                except Exception as e:
                    print(f"⚠️ Pop-up kapatma hatası: {e}")
                
                # Google için tema tutarlılığı sağla
                if "google" in page_config['url'].lower():
                    try:
                        self.driver.execute_script("""
                            // Google'da tema tutarlılığı sağla
                            console.log('Google tema kontrolü başlatılıyor...');
                            
                            // 1. CSS enjeksiyonu ile tema zorla
                            const style = document.createElement('style');
                            style.textContent = `
                                * {
                                    background-color: #ffffff !important;
                                    color: #000000 !important;
                                    border-color: #e0e0e0 !important;
                                }
                                body, html {
                                    background-color: #ffffff !important;
                                    color: #000000 !important;
                                }
                                [class*="dark"], [class*="Dark"] {
                                    background-color: #ffffff !important;
                                    color: #000000 !important;
                                }
                                [data-theme="dark"] {
                                    background-color: #ffffff !important;
                                    color: #000000 !important;
                                }
                            `;
                            document.head.appendChild(style);
                            
                            // 2. Body class'larını kontrol et
                            const body = document.body;
                            const html = document.documentElement;
                            
                            // 3. Tüm tema class'larını temizle
                            body.classList.remove('dark', 'dark-theme', 'dark-mode', 'Dark', 'DarkTheme', 'DarkMode');
                            html.classList.remove('dark', 'dark-theme', 'dark-mode', 'Dark', 'DarkTheme', 'DarkMode');
                            
                            // 4. Light tema class'larını ekle
                            body.classList.add('light', 'light-theme', 'light-mode', 'Light', 'LightTheme', 'LightMode');
                            html.classList.add('light', 'light-theme', 'light-mode', 'Light', 'LightTheme', 'LightMode');
                            
                            // 5. CSS değişkenlerini zorla
                            document.documentElement.style.setProperty('--color-scheme', 'light');
                            document.documentElement.style.setProperty('--background-color', '#ffffff');
                            document.documentElement.style.setProperty('--text-color', '#000000');
                            document.documentElement.style.setProperty('color-scheme', 'light');
                            
                            // 6. Google'ın kendi tema ayarlarını kontrol et
                            const themeButtons = document.querySelectorAll('[aria-label*="theme"], [aria-label*="tema"], [data-testid*="theme"], [title*="theme"], [title*="tema"]');
                            themeButtons.forEach(btn => {
                                if (btn.textContent.toLowerCase().includes('light') || 
                                    btn.textContent.toLowerCase().includes('açık') ||
                                    btn.getAttribute('aria-label')?.toLowerCase().includes('light') ||
                                    btn.getAttribute('aria-label')?.toLowerCase().includes('açık') ||
                                    btn.getAttribute('title')?.toLowerCase().includes('light') ||
                                    btn.getAttribute('title')?.toLowerCase().includes('açık')) {
                                    btn.click();
                                    console.log('Light tema seçildi');
                                }
                            });
                            
                            // 7. Meta tag'leri kontrol et
                            const metaTheme = document.querySelector('meta[name="color-scheme"]');
                            if (metaTheme) {
                                metaTheme.setAttribute('content', 'light');
                            }
                            
                            // 8. Tüm elementleri zorla light tema yap
                            const allElements = document.querySelectorAll('*');
                            allElements.forEach(el => {
                                if (el.style.backgroundColor === 'rgb(0, 0, 0)' || 
                                    el.style.backgroundColor === 'black' ||
                                    el.style.color === 'rgb(255, 255, 255)' ||
                                    el.style.color === 'white') {
                                    el.style.backgroundColor = '#ffffff';
                                    el.style.color = '#000000';
                                }
                            });
                            
                            console.log('Google tema kontrolü tamamlandı');
                        """)
                        print("✅ Google tema tutarlılığı sağlandı")
                        time.sleep(3)  # Daha uzun bekleme
                    except Exception as e:
                        print(f"⚠️ Google tema kontrolü hatası: {e}")
            
            # Ekran görüntüsü al
            screenshot_path = f"{self.screenshots_dir}/{page_name}.png"
            self.driver.save_screenshot(screenshot_path)
            
            print(f"✅ Ekran görüntüsü kaydedildi: {screenshot_path}")
            return screenshot_path
            
        except Exception as e:
            print(f"❌ Ekran görüntüsü alma hatası: {e}")
            return None
    
    def capture_baseline_screenshots(self):
        """Tüm test sayfalarının referans ekran görüntülerini alır"""
        print("🎯 Referans ekran görüntüleri alınıyor...")
        
        # Baseline klasörünü oluştur
        baseline_dir = "baseline"
        os.makedirs(baseline_dir, exist_ok=True)
        
        # screenshots_dir'i geçici olarak baseline olarak ayarla
        original_screenshots_dir = self.screenshots_dir
        self.screenshots_dir = baseline_dir
        
        results = []
        
        for page_config in self.config.get('test_pages', []):
            screenshot_path = self.capture_screenshot(page_config)
            if screenshot_path:
                results.append({
                    'page_name': page_config['name'],
                    'screenshot_path': screenshot_path,
                    'url': page_config['url']
                })
        
        # screenshots_dir'i geri al
        self.screenshots_dir = original_screenshots_dir
        
        print(f"✅ {len(results)} adet referans ekran görüntüsü alındı")
        return results
    
    def capture_test_screenshots(self):
        """Test sırasında ekran görüntüleri alır"""
        print("🧪 Test ekran görüntüleri alınıyor...")
        
        # Screenshots klasörünü oluştur
        screenshots_dir = "screenshots"
        os.makedirs(screenshots_dir, exist_ok=True)
        self.screenshots_dir = screenshots_dir # screenshots_dir'i sınıf değişkenine ata
        
        results = []
        
        for page_config in self.config.get('test_pages', []):
            screenshot_path = self.capture_screenshot(page_config)
            if screenshot_path:
                results.append({
                    'page_name': page_config['name'],
                    'screenshot_path': screenshot_path,
                    'url': page_config['url']
                })
        
        print(f"✅ {len(results)} adet test ekran görüntüsü alındı")
        return results
    
    def close_driver(self):
        """WebDriver'ı kapatır"""
        if self.driver:
            self.driver.quit()
            print("🔒 WebDriver kapatıldı")


def main():
    """Ana fonksiyon - referans ekran görüntüleri alır"""
    capture = ScreenshotCapture()
    
    try:
        # Referans ekran görüntülerini al
        results = capture.capture_baseline_screenshots()
        
        print("\n📊 Sonuçlar:")
        for result in results:
            print(f"  - {result['page_name']}: {result['screenshot_path']}")
            
    except Exception as e:
        print(f"❌ Hata: {e}")
    finally:
        capture.close_driver()


if __name__ == "__main__":
    main() 