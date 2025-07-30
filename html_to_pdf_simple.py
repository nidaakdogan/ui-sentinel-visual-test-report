#!/usr/bin/env python3
"""
HTML Raporunu PDF'e Çevirme Scripti (Selenium ile)
"""

import os
import glob
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
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
    """HTML dosyasını PDF'e çevirir (Selenium ile)"""
    try:
        # PDF dosya adını oluştur
        pdf_name = os.path.splitext(os.path.basename(html_path))[0] + ".pdf"
        pdf_path = os.path.join("reports", pdf_name)
        
        print(f"🔄 PDF oluşturuluyor: {pdf_name}")
        
        # Chrome ayarları
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Görünmez mod
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--print-to-pdf=" + os.path.abspath(pdf_path))
        chrome_options.add_argument("--print-to-pdf-no-header")
        
        # WebDriver başlat
        driver = webdriver.Chrome(options=chrome_options)
        
        # HTML dosyasını aç
        file_url = "file:///" + os.path.abspath(html_path).replace("\\", "/")
        driver.get(file_url)
        
        # Sayfanın yüklenmesini bekle
        time.sleep(3)
        
        # PDF olarak yazdır
        driver.execute_script("window.print();")
        
        # Biraz bekle
        time.sleep(5)
        
        # Driver'ı kapat
        driver.quit()
        
        if os.path.exists(pdf_path):
            print(f"✅ PDF oluşturuldu: {pdf_path}")
            return pdf_path
        else:
            print("❌ PDF dosyası oluşturulamadı!")
            return None
        
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