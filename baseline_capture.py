#!/usr/bin/env python3
"""
UI Sentinel - Referans Görüntü Alma
Bu dosya, test edilecek sayfaların referans ekran görüntülerini alır.
"""

import sys
import os

# src klasörünü Python path'ine ekle
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from visual_test import VisualTest


def main():
    """Referans görüntüleri alır"""
    print(" UI Sentinel - Referans Görüntü Alma")
    print("=" * 50)
    
    # VisualTest'i başlat
    visual_test = VisualTest()
    
    try:
        # Sadece referans görüntüleri al
        success = visual_test.run_baseline_only()
        
        if success:
            print("\n Referans görüntüleri başarıyla alındı!")
            print(" Görüntüler 'baseline/' klasöründe saklandı")
            print("\n Sonraki adım: Test görüntüleri almak için 'run_tests.py' çalıştırın")
        else:
            print("\n Referans görüntü alma başarısız!")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n İşlem kullanıcı tarafından durduruldu")
        sys.exit(1)
    except Exception as e:
        print(f"\n Hata: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 