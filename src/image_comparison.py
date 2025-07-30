import cv2
import numpy as np
import os
from PIL import Image, ImageDraw
import json
from datetime import datetime


class ImageComparison:
    def __init__(self, config_file="config/test_config.json"):
        """ImageComparison sınıfını başlatır"""
        self.config = self._load_config(config_file)
        self.threshold = self.config.get('comparison_settings', {}).get('threshold', 0.95)
        self.fail_threshold = self.config.get('comparison_settings', {}).get('fail_threshold', 0.85)
        self.tolerance = self.config.get('comparison_settings', {}).get('tolerance', 5)
        self.min_difference_pixels = self.config.get('comparison_settings', {}).get('min_difference_pixels', 100)
        self.highlight_differences = self.config.get('comparison_settings', {}).get('highlight_differences', True)
        self.save_differences = self.config.get('comparison_settings', {}).get('save_differences', True)
    
    def _load_config(self, config_file):
        """Konfigürasyon dosyasını yükler"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Hata: {config_file} dosyası bulunamadı!")
            return {}
    
    def load_image(self, image_path):
        """Görüntüyü yükler ve ön işleme yapar"""
        try:
            if not os.path.exists(image_path):
                print(f"❌ Görüntü dosyası bulunamadı: {image_path}")
                return None
            
            # Görüntüyü OpenCV ile yükle
            image = cv2.imread(image_path)
            if image is None:
                print(f"❌ Görüntü yüklenemedi: {image_path}")
                return None
            
            # Görüntüyü gri tonlamaya çevir (daha iyi karşılaştırma için)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            return gray
            
        except Exception as e:
            print(f"❌ Görüntü yükleme hatası: {e}")
            return None
    
    def compare_images(self, baseline_path, test_path, page_name):
        """İki görüntüyü karşılaştırır ve farkları tespit eder"""
        print(f"🔍 {page_name} sayfası karşılaştırılıyor...")
        
        # Görüntüleri yükle
        baseline_img = self.load_image(baseline_path)
        test_img = self.load_image(test_path)
        
        if baseline_img is None or test_img is None:
            return {
                'success': False,
                'error': 'Görüntü yüklenemedi',
                'page_name': page_name
            }
        
        # Görüntü boyutlarını kontrol et
        if baseline_img.shape != test_img.shape:
            print(f"⚠️ Görüntü boyutları farklı: {baseline_img.shape} vs {test_img.shape}")
            # Test görüntüsünü baseline boyutuna yeniden boyutlandır
            test_img = cv2.resize(test_img, (baseline_img.shape[1], baseline_img.shape[0]))
        
        # Sayfa özel ayarlarını kontrol et
        page_config = None
        for page in self.config.get('test_pages', []):
            if page['name'] == page_name:
                page_config = page
                break
        
        # Özel ayarları uygula
        tolerance = page_config.get('special_settings', {}).get('tolerance', self.tolerance)
        threshold = page_config.get('special_settings', {}).get('threshold', self.threshold)
        fail_threshold = page_config.get('special_settings', {}).get('fail_threshold', self.fail_threshold)
        min_diff_pixels = page_config.get('special_settings', {}).get('min_difference_pixels', self.min_difference_pixels)
        
        if page_config and page_config.get('special_settings'):
            print(f"🎯 {page_name} için özel ayarlar kullanılıyor: tolerance={tolerance}, threshold={threshold}")
        
        # Görüntü farkını hesapla - daha hassas karşılaştırma
        diff = cv2.absdiff(baseline_img, test_img)
        
        # Fark eşiğini uygula - özel tolerance ile
        _, thresh = cv2.threshold(diff, tolerance, 255, cv2.THRESH_BINARY)
        
        # Morfolojik işlemler ile gürültüyü azalt
        kernel = np.ones((3,3), np.uint8)  # Daha büyük kernel
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        
        # Fark yüzdesini hesapla
        total_pixels = baseline_img.shape[0] * baseline_img.shape[1]
        different_pixels = np.count_nonzero(thresh)
        difference_percentage = (different_pixels / total_pixels) * 100
        
        # Benzerlik skorunu hesapla
        similarity_score = 1 - (difference_percentage / 100)
        
        # Gelişmiş PASS/FAIL mantığı - özel ayarlarla
        passed = True
        if different_pixels < min_diff_pixels:
            # Çok az fark varsa PASS
            passed = True
        elif similarity_score >= threshold:
            # Yüksek benzerlik varsa PASS
            passed = True
        elif similarity_score < fail_threshold:
            # Düşük benzerlik varsa FAIL
            passed = False
        else:
            # Orta seviye benzerlik - fark yüzdesine göre karar ver
            passed = difference_percentage < 10.0  # %10'dan az fark PASS
        
        # Sonuçları hazırla
        result = {
            'success': True,
            'page_name': page_name,
            'baseline_path': baseline_path,
            'test_path': test_path,
            'similarity_score': similarity_score,
            'difference_percentage': difference_percentage,
            'total_pixels': total_pixels,
            'different_pixels': different_pixels,
            'passed': passed,
            'timestamp': datetime.now().isoformat()
        }
        
        # Fark görüntüsü oluştur - her zaman oluştur (fark olsun veya olmasın)
        if self.save_differences:
            diff_image_path = self._create_difference_image(
                baseline_path, test_path, thresh, page_name
            )
            result['difference_image_path'] = diff_image_path
        
        # Sonuçları yazdır
        status = "✅ PASS" if result['passed'] else "❌ FAIL"
        print(f"{status} {page_name}: Benzerlik: {similarity_score:.2%}, Fark: {difference_percentage:.2f}% ({different_pixels} piksel)")
        
        return result
    
    def _create_difference_image(self, baseline_path, test_path, diff_mask, page_name):
        """Fark görüntüsü oluşturur ve kaydeder"""
        try:
            # Results klasörünü oluştur
            results_dir = "results"
            os.makedirs(results_dir, exist_ok=True)
            
            # Baseline ve test görüntülerini yükle
            baseline_color = cv2.imread(baseline_path)
            test_color = cv2.imread(test_path)
            
            # Test görüntüsünü baseline boyutuna yeniden boyutlandır
            if baseline_color.shape != test_color.shape:
                test_color = cv2.resize(test_color, (baseline_color.shape[1], baseline_color.shape[0]))
            
            # Fark maskesini renkli hale getir
            diff_color = cv2.cvtColor(diff_mask, cv2.COLOR_GRAY2BGR)
            
            # Daha anlaşılır ve göze yumuşak renkler kullan
            # Açık yeşil: Değişmeyen alanlar (güvenli)
            # Sarı: Değişen alanlar (dikkat edilmesi gereken)
            # Sadece değişiklikleri turuncu ile işaretle
            diff_color[diff_mask > 0] = [0, 165, 255]  # BGR formatında turuncu (değişen alanlar)
            
            # Değişmeyen alanları beyaz yap (nötr arka plan)
            unchanged_mask = (diff_mask == 0)
            diff_color[unchanged_mask] = [255, 255, 255]  # BGR formatında beyaz (değişmeyen alanlar)
            
            # Overlay görüntüsü oluştur (sadece değişiklikleri vurgula)
            overlay = test_color.copy()
            overlay[diff_mask > 0] = [0, 165, 255]  # Turuncu overlay (değişen alanlar)
            
            # Overlay'i şeffaf yap
            alpha = 0.4  # Biraz daha görünür şeffaflık
            overlay_image = cv2.addWeighted(test_color, 1-alpha, overlay, alpha, 0)
            
            # Görüntüleri yan yana birleştir
            # 1. Referans görüntü | 2. Test görüntüsü | 3. Fark haritası | 4. Overlay
            combined = np.hstack([baseline_color, test_color, diff_color, overlay_image])
            
            # Fark görüntüsünü kaydet
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            diff_image_path = os.path.join(results_dir, f"{page_name}_diff_{timestamp}.png")
            cv2.imwrite(diff_image_path, combined)
            
            # Fark sayısını kontrol et ve uyarı ver
            different_pixels = np.count_nonzero(diff_mask)
            if different_pixels > 0:
                print(f"📊 Fark görüntüsü kaydedildi: {diff_image_path} ({different_pixels} farklı piksel)")
            else:
                print(f"📊 Fark görüntüsü kaydedildi: {diff_image_path} (fark tespit edilmedi)")
            
            return diff_image_path
            
        except Exception as e:
            print(f"❌ Fark görüntüsü oluşturma hatası: {e}")
            return None
    
    def compare_all_pages(self, baseline_dir="baseline", screenshots_dir="screenshots"):
        """Tüm sayfaların karşılaştırmasını yapar"""
        print("🚀 Tüm sayfaların görsel karşılaştırması başlatılıyor...")
        
        results = []
        passed_count = 0
        total_count = 0
        
        # Test sayfalarını al
        test_pages = self.config.get('test_pages', [])
        
        for page_config in test_pages:
            page_name = page_config['name']
            baseline_path = os.path.join(baseline_dir, f"{page_name}.png")
            test_path = os.path.join(screenshots_dir, f"{page_name}.png")
            
            # Dosyaların varlığını kontrol et
            if not os.path.exists(baseline_path):
                print(f"⚠️ Referans görüntü bulunamadı: {baseline_path}")
                continue
                
            if not os.path.exists(test_path):
                print(f"⚠️ Test görüntüsü bulunamadı: {test_path}")
                continue
            
            # Karşılaştırma yap
            result = self.compare_images(baseline_path, test_path, page_name)
            results.append(result)
            
            if result['success']:
                total_count += 1
                if result['passed']:
                    passed_count += 1
        
        # Özet istatistikler
        summary = {
            'total_tests': total_count,
            'passed_tests': passed_count,
            'failed_tests': total_count - passed_count,
            'pass_rate': (passed_count / total_count * 100) if total_count > 0 else 0,
            'results': results,
            'timestamp': datetime.now().isoformat()
        }
        
        print(f"\n📊 Özet:")
        print(f"  Toplam Test: {summary['total_tests']}")
        print(f"  Geçen: {summary['passed_tests']}")
        print(f"  Kalan: {summary['failed_tests']}")
        print(f"  Başarı Oranı: {summary['pass_rate']:.1f}%")
        
        return summary


def main():
    """Ana fonksiyon - test görüntülerini karşılaştırır"""
    comparison = ImageComparison()
    
    try:
        # Tüm sayfaları karşılaştır
        summary = comparison.compare_all_pages()
        
        # Sonuçları JSON olarak kaydet
        results_dir = "reports"
        os.makedirs(results_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = os.path.join(results_dir, f"comparison_report_{timestamp}.json")
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"📄 Rapor kaydedildi: {report_path}")
        
    except Exception as e:
        print(f"❌ Hata: {e}")


if __name__ == "__main__":
    main() 