#!/usr/bin/env python3
"""
UI Sentinel - Demo
Bu dosya, projenin tüm özelliklerini gösterir.
"""

import os
import sys
import time
from datetime import datetime

# src klasörünü Python path'ine ekle
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from visual_test import VisualTest


def print_banner():
    """Proje banner'ını yazdırır"""
    print("=" * 80)
    print("🔍 UI Sentinel - Görsel UI Test Otomasyonu")
    print("=" * 80)
    print("🚀 Selenium + OpenCV ile Görsel UI Test Otomasyonu")
    print("📊 Gerçek Zamanlı Raporlama ve Dashboard")
    print("🎯 Piksel Tabanlı Hassas Karşılaştırma")
    print("=" * 80)


def demo_baseline_capture():
    """Referans görüntü alma demo'su"""
    print("\n🎯 1. Referans Görüntü Alma Demo'su")
    print("-" * 50)
    
    visual_test = VisualTest()
    
    try:
        if visual_test.setup():
            print("✅ Test ortamı hazırlandı")
            
            if visual_test.capture_baseline():
                print("✅ Referans görüntüleri başarıyla alındı")
                print("📁 Görüntüler 'baseline/' klasöründe saklandı")
            else:
                print("❌ Referans görüntü alma başarısız")
        else:
            print("❌ Test ortamı hazırlama başarısız")
            
    except Exception as e:
        print(f"❌ Hata: {e}")
    finally:
        if visual_test.screenshot_capture:
            visual_test.screenshot_capture.close_driver()


def demo_test_execution():
    """Test çalıştırma demo'su"""
    print("\n🧪 2. Test Çalıştırma Demo'su")
    print("-" * 50)
    
    visual_test = VisualTest()
    
    try:
        if visual_test.setup():
            print("✅ Test ortamı hazırlandı")
            
            # Test görüntüleri al
            if visual_test.capture_test_screenshots():
                print("✅ Test görüntüleri başarıyla alındı")
                print("📁 Görüntüler 'screenshots/' klasöründe saklandı")
                
                # Karşılaştırma yap
                comparison_results = visual_test.compare_images()
                if comparison_results:
                    print("✅ Görsel karşılaştırma tamamlandı")
                    print(f"📊 Sonuçlar: {comparison_results.get('total_tests', 0)} test")
                    
                    # Raporları oluştur
                    reports = visual_test.generate_reports(comparison_results)
                    if reports:
                        print("✅ Raporlar başarıyla oluşturuldu")
                        print(f"📄 HTML: {reports.get('html_report', 'N/A')}")
                        print(f"📄 JSON: {reports.get('json_report', 'N/A')}")
                    else:
                        print("❌ Rapor oluşturma başarısız")
                else:
                    print("❌ Görsel karşılaştırma başarısız")
            else:
                print("❌ Test görüntü alma başarısız")
        else:
            print("❌ Test ortamı hazırlama başarısız")
            
    except Exception as e:
        print(f"❌ Hata: {e}")
    finally:
        if visual_test.screenshot_capture:
            visual_test.screenshot_capture.close_driver()


def demo_dashboard():
    """Dashboard demo'su"""
    print("\n📊 3. Dashboard Demo'su")
    print("-" * 50)
    
    print("🚀 Dashboard başlatılıyor...")
    print("🌐 Tarayıcıda http://localhost:8080 adresini açın")
    print("⏹️ Durdurmak için Ctrl+C tuşlayın")
    
    try:
        # Dashboard'u başlat
        import subprocess
        subprocess.run([sys.executable, "dashboard.py"])
    except KeyboardInterrupt:
        print("\n⏹️ Dashboard durduruldu")
    except Exception as e:
        print(f"❌ Dashboard başlatma hatası: {e}")


def demo_file_structure():
    """Dosya yapısı demo'su"""
    print("\n📁 4. Proje Yapısı Demo'su")
    print("-" * 50)
    
    print("📂 Proje Klasörleri:")
    
    folders = [
        ("baseline/", "Referans görseller"),
        ("screenshots/", "Test görselleri"),
        ("results/", "Fark görselleri"),
        ("reports/", "Test raporları"),
        ("dashboard/", "Dashboard dosyaları"),
        ("src/", "Kaynak kod"),
        ("config/", "Konfigürasyon dosyaları"),
        ("tests/", "Test dosyaları")
    ]
    
    for folder, description in folders:
        if os.path.exists(folder):
            file_count = len([f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))])
            print(f"  ✅ {folder:<15} - {description} ({file_count} dosya)")
        else:
            print(f"  ❌ {folder:<15} - {description} (klasör yok)")


def demo_configuration():
    """Konfigürasyon demo'su"""
    print("\n⚙️ 5. Konfigürasyon Demo'su")
    print("-" * 50)
    
    config_file = "config/test_config.json"
    
    if os.path.exists(config_file):
        print(f"📄 Konfigürasyon dosyası: {config_file}")
        
        try:
            import json
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            print("🔧 Mevcut Ayarlar:")
            print(f"  🖥️ Tarayıcı: {config.get('browser', {}).get('name', 'chrome')}")
            print(f"  📏 Pencere Boyutu: {config.get('browser', {}).get('window_size', {})}")
            print(f"  🎯 Test Sayfası Sayısı: {len(config.get('test_pages', []))}")
            print(f"  📊 Eşik Değeri: {config.get('comparison_settings', {}).get('threshold', 0.95)}")
            
        except Exception as e:
            print(f"❌ Konfigürasyon okuma hatası: {e}")
    else:
        print(f"❌ Konfigürasyon dosyası bulunamadı: {config_file}")


def demo_test_results():
    """Test sonuçları demo'su"""
    print("\n📊 6. Test Sonuçları Demo'su")
    print("-" * 50)
    
    reports_dir = "reports"
    
    if os.path.exists(reports_dir):
        json_files = [f for f in os.listdir(reports_dir) if f.endswith('.json')]
        html_files = [f for f in os.listdir(reports_dir) if f.endswith('.html')]
        
        print(f"📄 Rapor Dosyaları:")
        print(f"  JSON Raporları: {len(json_files)}")
        print(f"  HTML Raporları: {len(html_files)}")
        
        if json_files:
            latest_json = max(json_files, key=lambda x: os.path.getctime(os.path.join(reports_dir, x)))
            print(f"  📄 En Son JSON: {latest_json}")
            
            try:
                import json
                with open(os.path.join(reports_dir, latest_json), 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                summary = data.get('summary', {})
                print(f"  📊 Son Test Sonuçları:")
                print(f"    Toplam Test: {summary.get('total_tests', 0)}")
                print(f"    Geçen Test: {summary.get('passed_tests', 0)}")
                print(f"    Kalan Test: {summary.get('failed_tests', 0)}")
                print(f"    Başarı Oranı: {summary.get('pass_rate', 0):.1f}%")
                
            except Exception as e:
                print(f"❌ Rapor okuma hatası: {e}")
    else:
        print("❌ Reports klasörü bulunamadı")


def main():
    """Ana demo fonksiyonu"""
    print_banner()
    
    print("\n🎬 UI Sentinel Demo Başlatılıyor...")
    print("Bu demo, projenin tüm özelliklerini gösterecek.")
    
    # Demo adımları
    demo_file_structure()
    demo_configuration()
    demo_baseline_capture()
    demo_test_execution()
    demo_test_results()
    
    print("\n🎛️ Dashboard'u başlatmak ister misiniz? (y/n): ", end="")
    try:
        response = input().lower()
        if response in ['y', 'yes', 'evet', 'e']:
            demo_dashboard()
    except KeyboardInterrupt:
        print("\n⏹️ Demo durduruldu")
    
    print("\n🎉 Demo tamamlandı!")
    print("📚 Daha fazla bilgi için README.md dosyasını okuyun")
    print("🚀 Projeyi kullanmaya başlamak için 'python run_tests.py' komutunu çalıştırın")


if __name__ == "__main__":
    main() 