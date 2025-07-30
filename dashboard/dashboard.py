#!/usr/bin/env python3
"""
UI Sentinel - Dashboard
Test sonuçlarını görselleştiren web tabanlı dashboard.
"""

import os
import json
import webbrowser
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import time


class DashboardHandler(SimpleHTTPRequestHandler):
    """Dashboard için özel HTTP handler"""
    
    def do_GET(self):
        """GET isteklerini işler"""
        if self.path == '/':
            self.path = '/dashboard.html'
        elif self.path == '/api/results':
            self.send_api_response()
            return
        
        return SimpleHTTPRequestHandler.do_GET(self)
    
    def send_api_response(self):
        """API yanıtı gönderir"""
        try:
            # En son raporu bul
            reports_dir = "../reports"
            if not os.path.exists(reports_dir):
                self.send_error(404, "Reports directory not found")
                return
            
            # En son JSON raporunu bul
            json_files = [f for f in os.listdir(reports_dir) if f.endswith('.json')]
            if not json_files:
                self.send_error(404, "No reports found")
                return
            
            # En son raporu al
            latest_report = max(json_files, key=lambda x: os.path.getctime(os.path.join(reports_dir, x)))
            report_path = os.path.join(reports_dir, latest_report)
            
            with open(report_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # CORS headers
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
            
        except Exception as e:
            self.send_error(500, f"Error: {str(e)}")


def create_dashboard_html():
    """Dashboard HTML dosyasını oluşturur"""
    html_content = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UI Sentinel - Powered by AIVisionTest</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            text-align: center;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }
        
        .header h1 {
            font-size: 3em;
            color: #667eea;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 1.2em;
            color: #666;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 25px;
            text-align: center;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
        }
        
        .stat-card h3 {
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.3em;
        }
        
        .stat-number {
            font-size: 3em;
            font-weight: bold;
            margin-bottom: 10px;
        }
        
        .stat-number.pass {
            color: #28a745;
        }
        
        .stat-number.fail {
            color: #ff9800;
        }
        
        .stat-number.total {
            color: #667eea;
        }
        
        .stat-number.rate {
            color: #ffc107;
        }
        
        .test-results {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }
        
        .test-results h2 {
            color: #667eea;
            margin-bottom: 20px;
            font-size: 2em;
        }
        
        .test-list {
            display: grid;
            gap: 15px;
        }
        
        .test-item {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            border-left: 5px solid #dee2e6;
            transition: all 0.3s ease;
        }
        
        .test-item.passed {
            border-left-color: #28a745;
            background: #d4edda;
        }
        
        .test-item.failed {
            border-left-color: #ff9800;
            background: #fff3e0;
        }
        
        .test-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        
        .test-name {
            font-size: 1.3em;
            font-weight: bold;
            color: #333;
        }
        
        .test-status {
            padding: 8px 16px;
            border-radius: 25px;
            font-weight: bold;
            font-size: 0.9em;
        }
        
        .status-passed {
            background: #28a745;
            color: white;
        }
        
        .status-failed {
            background: #ff9800;
            color: white;
        }
        
        .test-details {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 10px;
        }
        
        .detail-item {
            background: white;
            padding: 10px;
            border-radius: 5px;
            text-align: center;
        }
        
        .detail-label {
            font-size: 0.8em;
            color: #666;
            margin-bottom: 5px;
        }
        
        .detail-value {
            font-weight: bold;
            color: #333;
        }
        
        .refresh-btn {
            background: #667eea;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 25px;
            font-size: 1.1em;
            cursor: pointer;
            transition: background 0.3s ease;
            margin-bottom: 20px;
        }
        
        .refresh-btn:hover {
            background: #5a6fd8;
        }
        
        .loading {
            text-align: center;
            padding: 40px;
            color: #666;
        }
        
        .error {
            background: #f8d7da;
            color: #721c24;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 10px;
            }
            
            .header h1 {
                font-size: 2em;
            }
            
            .test-header {
                flex-direction: column;
                align-items: flex-start;
                gap: 10px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 UI Sentinel</h1>
        <p style="color: #666; font-size: 16px; margin-top: 5px;">Powered by AIVisionTest</p>
            <p>Gerçek Zamanlı Test Sonuçları</p>
            <button class="refresh-btn" onclick="loadResults()">🔄 Yenile</button>
        </div>
        
        <div id="loading" class="loading">
            <h3>📊 Veriler yükleniyor...</h3>
        </div>
        
        <div id="error" class="error" style="display: none;">
            <h3>❌ Hata</h3>
            <p id="error-message"></p>
        </div>
        
        <div id="content" style="display: none;">
            <div class="stats-grid">
                <div class="stat-card">
                    <h3>Toplam Test</h3>
                    <div class="stat-number total" id="total-tests">-</div>
                </div>
                <div class="stat-card">
                    <h3>Geçen Test</h3>
                    <div class="stat-number pass" id="passed-tests">-</div>
                </div>
                <div class="stat-card">
                    <h3>Kalan Test</h3>
                    <div class="stat-number fail" id="failed-tests">-</div>
                </div>
                <div class="stat-card">
                    <h3>Başarı Oranı</h3>
                    <div class="stat-number rate" id="pass-rate">-</div>
                </div>
            </div>
            
            <div class="test-results">
                <h2>📊 Test Sonuçları</h2>
                <div id="test-list" class="test-list">
                    <!-- Test sonuçları buraya yüklenecek -->
                </div>
            </div>
        </div>
    </div>
    
    <script>
        function loadResults() {
            // Loading göster
            document.getElementById('loading').style.display = 'block';
            document.getElementById('content').style.display = 'none';
            document.getElementById('error').style.display = 'none';
            
            fetch('/api/results')
                .then(response => {
                    if (!response.ok) {
                        throw new Error('API yanıtı alınamadı');
                    }
                    return response.json();
                })
                .then(data => {
                    displayResults(data);
                })
                .catch(error => {
                    console.error('Hata:', error);
                    document.getElementById('error').style.display = 'block';
                    document.getElementById('error-message').textContent = error.message;
                    document.getElementById('loading').style.display = 'none';
                });
        }
        
        function displayResults(data) {
            const summary = data.summary || {};
            const results = data.test_results || [];
            
            // İstatistikleri güncelle
            document.getElementById('total-tests').textContent = summary.total_tests || 0;
            document.getElementById('passed-tests').textContent = summary.passed_tests || 0;
            document.getElementById('failed-tests').textContent = summary.failed_tests || 0;
            document.getElementById('pass-rate').textContent = (summary.pass_rate || 0).toFixed(1) + '%';
            
            // Test sonuçlarını göster
            const testList = document.getElementById('test-list');
            testList.innerHTML = '';
            
            results.forEach(result => {
                const testItem = document.createElement('div');
                testItem.className = `test-item ${result.passed ? 'passed' : 'failed'}`;
                
                testItem.innerHTML = `
                    <div class="test-header">
                        <div class="test-name">${result.page_name}</div>
                        <div class="test-status ${result.passed ? 'status-passed' : 'status-failed'}">
                            ${result.passed ? '✅ PASS' : '❌ FAIL'}
                        </div>
                    </div>
                    <div class="test-details">
                        <div class="detail-item">
                            <div class="detail-label">Benzerlik</div>
                            <div class="detail-value">${((result.similarity_score || 0) * 100).toFixed(1)}%</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Fark</div>
                            <div class="detail-value">${(result.difference_percentage || 0).toFixed(1)}%</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Farklı Piksel</div>
                            <div class="detail-value">${result.different_pixels || 0}/${result.total_pixels || 0}</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Zaman</div>
                            <div class="detail-value">${formatTimestamp(result.timestamp)}</div>
                        </div>
                    </div>
                `;
                
                testList.appendChild(testItem);
            });
            
            // Loading gizle, content göster
            document.getElementById('loading').style.display = 'none';
            document.getElementById('content').style.display = 'block';
        }
        
        function formatTimestamp(timestamp) {
            if (!timestamp) return '-';
            const date = new Date(timestamp);
            return date.toLocaleString('tr-TR');
        }
        
        // Sayfa yüklendiğinde sonuçları yükle
        window.onload = function() {
            loadResults();
            
            // Her 30 saniyede bir otomatik yenile
            setInterval(loadResults, 30000);
        };
    </script>
</body>
</html>
    """
    
    # Dashboard HTML dosyasını oluştur
    dashboard_path = os.path.join(os.path.dirname(__file__), 'dashboard.html')
    with open(dashboard_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Dashboard HTML dosyası oluşturuldu: {dashboard_path}")
    return dashboard_path


def start_dashboard(port=8080):
    """Dashboard'u başlatır"""
    print(f"🚀 UI Sentinel Dashboard başlatılıyor...")
    print(f"🌐 URL: http://localhost:{port}")
    
    # Dashboard HTML dosyasını oluştur
    create_dashboard_html()
    
    # Çalışma dizinini dashboard klasörüne değiştir
    os.chdir(os.path.dirname(__file__))
    
    try:
        # HTTP sunucusunu başlat
        server = HTTPServer(('localhost', port), DashboardHandler)
        
        # Tarayıcıyı aç
        webbrowser.open(f'http://localhost:{port}')
        
        print(f"✅ Dashboard başarıyla başlatıldı!")
        print(f"📊 Tarayıcıda otomatik olarak açıldı")
        print(f"⏹️ Durdurmak için Ctrl+C tuşlayın")
        
        # Sunucuyu çalıştır
        server.serve_forever()
        
    except KeyboardInterrupt:
        print("\n⏹️ Dashboard durduruldu")
    except Exception as e:
        print(f"❌ Dashboard başlatma hatası: {e}")


def main():
    """Ana fonksiyon"""
    import argparse
    
    parser = argparse.ArgumentParser(description='UI Sentinel Dashboard')
    parser.add_argument('--port', type=int, default=8080, help='Port numarası')
    
    args = parser.parse_args()
    
    try:
        start_dashboard(args.port)
    except Exception as e:
        print(f"❌ Hata: {e}")


if __name__ == "__main__":
    main() 