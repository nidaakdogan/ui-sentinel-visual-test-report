#!/usr/bin/env python3
"""
HTML Raporu Paylaşım Scripti
Bu script en son oluşturulan HTML raporunu paylaşım için hazırlar.
"""

import os
import glob
import shutil
import webbrowser
from datetime import datetime

def find_latest_report():
    """En son oluşturulan raporu bulur"""
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

def copy_to_public(report_path):
    """Raporu public klasörüne kopyalar"""
    public_dir = "public"
    if not os.path.exists(public_dir):
        os.makedirs(public_dir)
    
    # index.html olarak kopyala
    index_path = os.path.join(public_dir, "index.html")
    shutil.copy2(report_path, index_path)
    
    print(f"✅ Rapor kopyalandı: {index_path}")
    return index_path

def create_netlify_config():
    """Netlify için gerekli dosyaları oluşturur"""
    public_dir = "public"
    if not os.path.exists(public_dir):
        os.makedirs(public_dir)
    
    # netlify.toml dosyası
    netlify_config = """[build]
  publish = "public"
  command = ""

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
"""
    
    with open("netlify.toml", "w", encoding="utf-8") as f:
        f.write(netlify_config)
    
    print("✅ netlify.toml dosyası oluşturuldu")

def create_github_pages_config():
    """GitHub Pages için gerekli dosyaları oluşturur"""
    # .github/workflows/deploy.yml
    workflows_dir = ".github/workflows"
    if not os.path.exists(workflows_dir):
        os.makedirs(workflows_dir)
    
    workflow_config = """name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Copy latest report
      run: |
        cp reports/ui_sentinel_report_*.html index.html
    
    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: .
"""
    
    with open(os.path.join(workflows_dir, "deploy.yml"), "w", encoding="utf-8") as f:
        f.write(workflow_config)
    
    print("✅ GitHub Pages workflow oluşturuldu")

def main():
    """Ana fonksiyon"""
    print("🚀 HTML Raporu Paylaşım Aracı")
    print("=" * 40)
    
    # En son raporu bul
    latest_report = find_latest_report()
    if not latest_report:
        return
    
    print(f"📄 En son rapor: {os.path.basename(latest_report)}")
    
    # Menü göster
    print("\n📋 Paylaşım seçenekleri:")
    print("1. GitHub Pages için hazırla")
    print("2. Netlify için hazırla")
    print("3. Sadece public klasörüne kopyala")
    print("4. Raporu tarayıcıda aç")
    
    choice = input("\nSeçiminiz (1-4): ").strip()
    
    if choice == "1":
        # GitHub Pages
        copy_to_public(latest_report)
        create_github_pages_config()
        print("\n📤 GitHub Pages için hazırlandı!")
        print("1. git add .")
        print("2. git commit -m 'Add report'")
        print("3. git push origin main")
        print("4. GitHub'da Settings > Pages > Deploy from branch > main")
        
    elif choice == "2":
        # Netlify
        copy_to_public(latest_report)
        create_netlify_config()
        print("\n🌐 Netlify için hazırlandı!")
        print("1. netlify.com'a gidin")
        print("2. public/ klasörünü sürükleyip bırakın")
        print("3. Veya GitHub repository'nizi bağlayın")
        
    elif choice == "3":
        # Sadece kopyala
        copy_to_public(latest_report)
        print("\n✅ Rapor public/ klasörüne kopyalandı!")
        
    elif choice == "4":
        # Tarayıcıda aç
        webbrowser.open(f"file://{os.path.abspath(latest_report)}")
        print(f"\n🌐 Rapor tarayıcıda açıldı: {latest_report}")
        
    else:
        print("❌ Geçersiz seçim!")

if __name__ == "__main__":
    main() 