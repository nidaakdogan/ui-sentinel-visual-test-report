import os
import json
from screenshot_capture import ScreenshotCapture

class BaselineCapture:
    def __init__(self, config_file="config/test_config.json"):
        self.config_file = config_file
        self.config = self._load_config()
        self.screenshot_capture = ScreenshotCapture(config_file)
    
    def _load_config(self):
        """Konfigürasyon dosyasını yükler"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Konfigürasyon dosyası yüklenemedi: {e}")
            return {}
    
    def capture_baseline_screenshots(self):
        """Referans ekran görüntülerini alır"""
        print("🎯 Referans ekran görüntüleri alınıyor...")
        
        baseline_dir = "baseline"
        os.makedirs(baseline_dir, exist_ok=True)
        
        results = []
        
        for page_config in self.config.get('test_pages', []):
            # Baseline için screenshots_dir'i geçici olarak baseline olarak ayarla
            original_screenshots_dir = self.screenshot_capture.screenshots_dir
            self.screenshot_capture.screenshots_dir = baseline_dir
            
            screenshot_path = self.screenshot_capture.capture_screenshot(page_config)
            
            # screenshots_dir'i geri al
            self.screenshot_capture.screenshots_dir = original_screenshots_dir
            
            if screenshot_path:
                results.append({
                    'page_name': page_config['name'],
                    'screenshot_path': screenshot_path,
                    'status': 'success'
                })
            else:
                results.append({
                    'page_name': page_config['name'],
                    'screenshot_path': None,
                    'status': 'failed'
                })
        
        print(f"✅ {len(results)} adet referans ekran görüntüsü alındı")
        return results

def main():
    """Ana fonksiyon"""
    capture = BaselineCapture()
    results = capture.capture_baseline_screenshots()
    
    print("📊 Baseline Capture Sonuçları:")
    for result in results:
        status = "✅" if result['status'] == 'success' else "❌"
        print(f"{status} {result['page_name']}: {result['status']}")

if __name__ == "__main__":
    main() 