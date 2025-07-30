import os
import sys
import json
from datetime import datetime
from screenshot_capture import ScreenshotCapture
from image_comparison import ImageComparison
from report_generator import ReportGenerator


class VisualTest:
    def __init__(self, config_file="config/test_config.json"):
        """VisualTest sınıfını başlatır"""
        self.config_file = config_file
        self.screenshot_capture = None
        self.image_comparison = None
        self.report_generator = None
        
    def setup(self):
        """Test ortamını hazırlar"""
        print("🚀 UI Sentinel Test Ortamı Hazırlanıyor...")
        
        try:
            # Modülleri başlat
            self.screenshot_capture = ScreenshotCapture(self.config_file)
            self.image_comparison = ImageComparison(self.config_file)
            self.report_generator = ReportGenerator(self.config_file)
            
            print("✅ Test ortamı başarıyla hazırlandı")
            return True
            
        except Exception as e:
            print(f"❌ Test ortamı hazırlama hatası: {e}")
            return False
    
    def capture_baseline(self):
        """Referans ekran görüntülerini alır"""
        print("\n🎯 Referans Ekran Görüntüleri Alınıyor...")
        
        try:
            results = self.screenshot_capture.capture_baseline_screenshots()
            
            if results:
                print(f"✅ {len(results)} adet referans görüntü alındı")
                return True
            else:
                print("❌ Referans görüntü alınamadı")
                return False
                
        except Exception as e:
            print(f"❌ Referans görüntü alma hatası: {e}")
            return False
    
    def capture_test_screenshots(self):
        """Test ekran görüntülerini alır"""
        print("\n🧪 Test Ekran Görüntüleri Alınıyor...")
        
        try:
            results = self.screenshot_capture.capture_test_screenshots()
            
            if results:
                print(f"✅ {len(results)} adet test görüntü alındı")
                return True
            else:
                print("❌ Test görüntü alınamadı")
                return False
                
        except Exception as e:
            print(f"❌ Test görüntü alma hatası: {e}")
            return False
    
    def compare_images(self):
        """Görsel karşılaştırma yapar"""
        print("\n🔍 Görsel Karşılaştırma Başlatılıyor...")
        
        try:
            comparison_results = self.image_comparison.compare_all_pages()
            
            if comparison_results:
                print("✅ Görsel karşılaştırma tamamlandı")
                return comparison_results
            else:
                print("❌ Görsel karşılaştırma başarısız")
                return None
                
        except Exception as e:
            print(f"❌ Görsel karşılaştırma hatası: {e}")
            return None
    
    def generate_reports(self, comparison_results):
        """Raporları oluşturur"""
        print("\n📊 Raporlar Oluşturuluyor...")
        
        try:
            reports = self.report_generator.generate_reports(comparison_results)
            
            if reports:
                print("✅ Raporlar başarıyla oluşturuldu")
                return reports
            else:
                print("❌ Rapor oluşturma başarısız")
                return None
                
        except Exception as e:
            print(f"❌ Rapor oluşturma hatası: {e}")
            return None
    
    def run_full_test(self):
        """Tam test sürecini çalıştırır"""
        print("🎯 UI Sentinel - Tam Test Süreci Başlatılıyor")
        print("=" * 60)
        
        # Test ortamını hazırla
        if not self.setup():
            return False
        
        try:
            # 1. Referans görüntüleri al
            if not self.capture_baseline():
                return False
            
            # 2. Test görüntüleri al
            if not self.capture_test_screenshots():
                return False
            
            # 3. Görsel karşılaştırma yap
            comparison_results = self.compare_images()
            if not comparison_results:
                return False
            
            # 4. Raporları oluştur
            reports = self.generate_reports(comparison_results)
            if not reports:
                return False
            
            # 5. Sonuçları özetle
            self._print_summary(comparison_results, reports)
            
            return True
            
        except Exception as e:
            print(f"❌ Test süreci hatası: {e}")
            return False
        
        finally:
            # WebDriver'ı kapat
            if self.screenshot_capture:
                self.screenshot_capture.close_driver()
    
    def _print_summary(self, comparison_results, reports):
        """Test sonuçlarını özetler"""
        print("\n" + "=" * 60)
        print("📊 TEST SONUÇLARI ÖZETİ")
        print("=" * 60)
        
        summary = comparison_results.get('summary', {})
        
        print(f"🎯 Toplam Test: {summary.get('total_tests', 0)}")
        print(f"✅ Geçen Test: {summary.get('passed_tests', 0)}")
        print(f"❌ Kalan Test: {summary.get('failed_tests', 0)}")
        print(f"📈 Başarı Oranı: {summary.get('pass_rate', 0):.1f}%")
        
        print(f"\n📄 Raporlar:")
        print(f"  JSON: {reports.get('json_report', 'N/A')}")
        print(f"  HTML: {reports.get('html_report', 'N/A')}")
        
        print(f"\n📁 Dosya Konumları:")
        print(f"  Referans Görüntüler: baseline/")
        print(f"  Test Görüntüleri: screenshots/")
        print(f"  Fark Görüntüleri: results/")
        print(f"  Raporlar: reports/")
        
        print("\n🎉 Test süreci tamamlandı!")
    
    def run_baseline_only(self):
        """Sadece referans görüntüleri alır"""
        print("🎯 Sadece Referans Görüntüleri Alınıyor...")
        
        if not self.setup():
            return False
        
        try:
            success = self.capture_baseline()
            if success:
                print("✅ Referans görüntüleri başarıyla alındı")
            return success
            
        except Exception as e:
            print(f"❌ Referans görüntü alma hatası: {e}")
            return False
        
        finally:
            if self.screenshot_capture:
                self.screenshot_capture.close_driver()
    
    def run_comparison_only(self):
        """Sadece karşılaştırma yapar (mevcut görüntüler kullanır)"""
        print("🔍 Sadece Görsel Karşılaştırma Yapılıyor...")
        
        try:
            self.image_comparison = ImageComparison(self.config_file)
            self.report_generator = ReportGenerator(self.config_file)
            
            # Karşılaştırma yap
            comparison_results = self.compare_images()
            if not comparison_results:
                return False
            
            # Raporları oluştur
            reports = self.generate_reports(comparison_results)
            if not reports:
                return False
            
            # Sonuçları özetle
            self._print_summary(comparison_results, reports)
            
            return True
            
        except Exception as e:
            print(f"❌ Karşılaştırma hatası: {e}")
            return False


def main():
    """Ana fonksiyon"""
    import argparse
    
    parser = argparse.ArgumentParser(description='UI Sentinel - Görsel UI Test Otomasyonu')
    parser.add_argument('--mode', choices=['full', 'baseline', 'comparison'], 
                       default='full', help='Test modu')
    parser.add_argument('--config', default='config/test_config.json', 
                       help='Konfigürasyon dosyası')
    
    args = parser.parse_args()
    
    # VisualTest'i başlat
    visual_test = VisualTest(args.config)
    
    try:
        if args.mode == 'full':
            success = visual_test.run_full_test()
        elif args.mode == 'baseline':
            success = visual_test.run_baseline_only()
        elif args.mode == 'comparison':
            success = visual_test.run_comparison_only()
        else:
            print("❌ Geçersiz test modu")
            success = False
        
        if success:
            print("\n🎉 İşlem başarıyla tamamlandı!")
            sys.exit(0)
        else:
            print("\n❌ İşlem başarısız!")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⏹️ İşlem kullanıcı tarafından durduruldu")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Beklenmeyen hata: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 