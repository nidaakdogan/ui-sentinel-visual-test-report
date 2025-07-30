#!/usr/bin/env python3
"""
UI Sentinel - Dashboard Başlatıcı
Bu dosya, test sonuçlarını görselleştiren dashboard'u başlatır.
"""

import sys
import os

# Dashboard modülünü import et
sys.path.append(os.path.join(os.path.dirname(__file__), 'dashboard'))

from dashboard.dashboard import start_dashboard


def main():
    """Dashboard'u başlatır"""
    print(" UI Sentinel Dashboard Başlatılıyor...")
    print("=" * 50)
    
    try:
        # Dashboard'u başlat
        start_dashboard(port=8080)
        
    except KeyboardInterrupt:
        print("\n Dashboard durduruldu")
    except Exception as e:
        print(f" Dashboard başlatma hatası: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 