#!/usr/bin/env python3
"""
HTML Raporunu PDF'e Çevirme Scripti
"""

import os
import glob
from weasyprint import HTML
from datetime import datetime

def find_latest_html_report():
    """En son HTML raporunu bulur"""
    reports_dir = "reports"
    if not os.path.exists(reports_dir):
        print("❌ reports/ klasörü bulunamadı!")
        return None
    
    # En son HTML raporunu bul
    html_files = glob.glob(os.path.join(reports_dir, "ui_sentinel_report_*.html"))
    if not html_files:
        print("❌ HTML raporu bulunamadı!")
        return None
    
    # En son dosyayı al
    latest_report = max(html_files, key=os.path.getctime)
    return latest_report

def convert_html_to_pdf(html_path):
    """HTML dosyasını PDF'e çevirir"""
    try:
        # PDF dosya adını oluştur
        pdf_name = os.path.splitext(os.path.basename(html_path))[0] + ".pdf"
        pdf_path = os.path.join("reports", pdf_name)
        
        print(f"🔄 PDF oluşturuluyor: {pdf_name}")
        
        # HTML'i PDF'e çevir
        HTML(filename=html_path).write_pdf(pdf_path)
        
        print(f"✅ PDF oluşturuldu: {pdf_path}")
        return pdf_path
        
    except Exception as e:
        print(f"❌ PDF oluşturulurken hata: {e}")
        return None

def main():
    """Ana fonksiyon"""
    print("📄 HTML'den PDF'e Çevirme Aracı")
    print("=" * 40)
    
    # En son HTML raporunu bul
    html_report = find_latest_html_report()
    if not html_report:
        return
    
    print(f"📄 HTML Rapor: {os.path.basename(html_report)}")
    
    # PDF'e çevir
    pdf_path = convert_html_to_pdf(html_report)
    
    if pdf_path:
        print(f"\n🎉 Başarılı!")
        print(f"📁 PDF Dosyası: {pdf_path}")
        print(f"📏 Dosya Boyutu: {os.path.getsize(pdf_path) / (1024*1024):.1f} MB")
        print(f"\n📤 Paylaşım için hazır!")
    else:
        print("❌ PDF oluşturulamadı!")

if __name__ == "__main__":
    main() 