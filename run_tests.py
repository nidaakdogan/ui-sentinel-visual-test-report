#!/usr/bin/env python3
"""
UI Sentinel - Test Çalıştırma
Bu dosya, tam test sürecini çalıştırır (referans + test + karşılaştırma + rapor).
"""

import sys
import os

# src klasörünü Python path'ine ekle
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from visual_test import VisualTest


def main():
    """Tam test sürecini çalıştırır"""
    print("🚀 UI Sentinel - Test Süreci Başlatılıyor")
    print("=" * 60)
    
    # VisualTest'i başlat
    visual_test = VisualTest()
    
    try:
        # Tam test sürecini çalıştır
        success = visual_test.run_full_test()
        
        if success:
            print("\n🎉 Test süreci başarıyla tamamlandı!")
            print("📊 Raporlar 'reports/' klasöründe oluşturuldu")
            print("🔍 Fark görüntüleri 'results/' klasöründe saklandı")
            print("\n📄 HTML raporunu tarayıcıda açarak sonuçları görüntüleyebilirsiniz")
        else:
            print("\n❌ Test süreci başarısız!")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⏹️ İşlem kullanıcı tarafından durduruldu")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Hata: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 