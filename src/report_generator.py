import json
import os
from datetime import datetime
from jinja2 import Template
import base64




class ReportGenerator:
    def __init__(self, config_file="config/test_config.json", language="en"):
        """Initialize ReportGenerator class"""
        self.config = self._load_config(config_file)
        self.language = language
        self.language_config = self._load_language_config()
        self.reports_dir = "reports"
        os.makedirs(self.reports_dir, exist_ok=True)
    
    def _load_config(self, config_file):
        """Konfigürasyon dosyasını yükler"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Hata: {config_file} dosyası bulunamadı!")
            return {}
    
    def _load_language_config(self):
        """Dil konfigürasyonunu yükler"""
        try:
            with open("config/language_config.json", 'r', encoding='utf-8') as f:
                config = json.load(f)
                return config.get(self.language, config.get('en', {}))
        except FileNotFoundError:
            print(f"Uyarı: config/language_config.json dosyası bulunamadı! Varsayılan dil kullanılıyor.")
            return {}
    
    def _get_text(self, key_path, **kwargs):
        """Dil konfigürasyonundan metin alır ve formatlar"""
        keys = key_path.split('.')
        text = self.language_config
        for key in keys:
            text = text.get(key, key_path)
        
        if isinstance(text, str):
            return text.format(**kwargs)
        return key_path
    
    def _image_to_base64(self, image_path):
        """Görüntüyü base64 formatına çevirir"""
        try:
            if os.path.exists(image_path):
                with open(image_path, "rb") as image_file:
                    return base64.b64encode(image_file.read()).decode('utf-8')
            return None
        except Exception as e:
            print(f"❌ Görüntü base64 dönüştürme hatası: {e}")
            return None
    
    def generate_json_report(self, comparison_results):
        """JSON formatında rapor oluşturur"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = os.path.join(self.reports_dir, f"ui_sentinel_report_{timestamp}.json")
        
        report_data = {
            'project_name': 'UI Sentinel - Powered by AIVisionTest',
            'report_type': 'visual_comparison',
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_tests': comparison_results.get('total_tests', 0),
                'passed_tests': comparison_results.get('passed_tests', 0),
                'failed_tests': comparison_results.get('failed_tests', 0),
                'pass_rate': comparison_results.get('pass_rate', 0)
            },
            'test_results': comparison_results.get('results', []),
            'configuration': {
                'threshold': self.config.get('comparison_settings', {}).get('threshold', 0.95),
                'tolerance': self.config.get('comparison_settings', {}).get('tolerance', 5)
            }
        }
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        print(f"📄 JSON rapor kaydedildi: {report_path}")
        return report_path
    
    def generate_html_report(self, comparison_results):
        """HTML formatında detaylı rapor oluşturur"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = os.path.join(self.reports_dir, f"ui_sentinel_report_{timestamp}.html")
        
        html_template = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>UI Sentinel - Powered by AIVisionTest</title>
            <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
            <style>
                * {
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }
                
                body {
                    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                    color: #2c3e50;
                    line-height: 1.6;
                    min-height: 100vh;
                }
                
                .container {
                    max-width: 1400px;
                    margin: 0 auto;
                    padding: 20px;
                }
                
                /* Enhanced Header Design */
                .header {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 40px 30px;
                    border-radius: 16px;
                    text-align: center;
                    margin-bottom: 30px;
                    box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
                    position: relative;
                    overflow: hidden;
                }
                
                .header::before {
                    content: '';
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    bottom: 0;
                    background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, transparent 50%, rgba(255,255,255,0.1) 100%);
                    pointer-events: none;
                }
                
                .header h1 {
                    font-size: 3.2rem;
                    font-weight: 700;
                    margin-bottom: 8px;
                    text-shadow: 0 4px 8px rgba(0,0,0,0.3);
                    position: relative;
                    z-index: 1;
                }
                
                .header .subtitle {
                    font-size: 1.1rem;
                    color: rgba(255,255,255,0.9);
                    font-weight: 400;
                    margin-bottom: 15px;
                    position: relative;
                    z-index: 1;
                }
                
                .header .description {
                    font-size: 1.3rem;
                    font-weight: 500;
                    margin-bottom: 10px;
                    position: relative;
                    z-index: 1;
                }
                
                .header .date {
                    font-size: 0.95rem;
                    color: rgba(255,255,255,0.8);
                    font-weight: 300;
                    position: relative;
                    z-index: 1;
                }
                
                /* PDF Download Button */
                .download-pdf-btn {
                    background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
                    color: white;
                    border: none;
                    padding: 12px 24px;
                    border-radius: 25px;
                    font-size: 1rem;
                    font-weight: 600;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    box-shadow: 0 4px 15px rgba(255, 107, 107, 0.4);
                    position: relative;
                    z-index: 1;
                    margin-top: 15px;
                }
                
                .download-pdf-btn:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 6px 20px rgba(255, 107, 107, 0.6);
                    background: linear-gradient(135deg, #ff5252 0%, #d63031 100%);
                }
                
                .download-pdf-btn:active {
                    transform: translateY(0);
                    box-shadow: 0 2px 10px rgba(255, 107, 107, 0.4);
                }
                
                /* Enhanced Statistic Cards */
                .stats-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                    gap: 25px;
                    margin-bottom: 35px;
                }
                
                .stat-card {
                    background: white;
                    padding: 30px 25px;
                    border-radius: 16px;
                    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
                    text-align: center;
                    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
                    border: 1px solid rgba(0,0,0,0.05);
                    position: relative;
                    overflow: hidden;
                }
                
                .stat-card::before {
                    content: '';
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    height: 4px;
                    background: linear-gradient(90deg, #667eea, #764ba2);
                    transform: scaleX(0);
                    transition: transform 0.3s ease;
                }
                
                .stat-card:hover {
                    transform: translateY(-8px);
                    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
                }
                
                .stat-card:hover::before {
                    transform: scaleX(1);
                }
                
                .stat-card.passed {
                    border-left: 4px solid #10b981;
                }
                
                .stat-card.failed {
                    border-left: 4px solid #ef4444;
                }
                
                .stat-card .icon {
                    font-size: 2.5rem;
                    margin-bottom: 15px;
                    display: block;
                }
                
                .stat-card.passed .icon {
                    color: #10b981;
                }
                
                .stat-card.failed .icon {
                    color: #ef4444;
                }
                
                .stat-card .value {
                    font-size: 2.8rem;
                    font-weight: 700;
                    margin-bottom: 8px;
                    color: #1f2937;
                }
                
                .stat-card .label {
                    font-size: 1rem;
                    color: #6b7280;
                    font-weight: 500;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                }
                
                /* Single Column Layout */
                .report-content {
                    background: white;
                    padding: 40px;
                    border-radius: 16px;
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                    margin-top: 25px;
                }
                
                .metrics-section {
                    margin-bottom: 40px;
                }
                
                /* Enhanced Test Details */
                .test-detail {
                    background: #f8fafc;
                    border: 1px solid #e2e8f0;
                    border-radius: 12px;
                    padding: 25px;
                    margin-bottom: 30px;
                    transition: all 0.3s ease;
                }
                
                .test-detail:hover {
                    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
                    border-color: #cbd5e1;
                }
                
                .test-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 20px;
                    padding-bottom: 15px;
                    border-bottom: 2px solid #e2e8f0;
                }
                
                .test-name {
                    font-size: 1.4rem;
                    font-weight: 600;
                    color: #1f2937;
                }
                
                .test-status {
                    padding: 8px 16px;
                    border-radius: 20px;
                    font-weight: 600;
                    font-size: 0.9rem;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                }
                
                .test-status.passed {
                    background: #dcfce7;
                    color: #166534;
                }
                
                .test-status.failed {
                    background: #fee2e2;
                    color: #991b1b;
                }
                
                .test-metrics {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 20px;
                    margin-bottom: 25px;
                }
                
                .metric-item {
                    text-align: center;
                    padding: 15px;
                    background: white;
                    border-radius: 8px;
                    border: 1px solid #e5e7eb;
                }
                
                .metric-value {
                    font-size: 1.8rem;
                    font-weight: 700;
                    color: #1f2937;
                    margin-bottom: 5px;
                }
                
                .metric-label {
                    font-size: 0.85rem;
                    color: #6b7280;
                    font-weight: 500;
                    text-transform: uppercase;
                    letter-spacing: 0.3px;
                }
                
                /* Enhanced Visual Comparison Section */
                .visual-comparison {
                        margin-top: 15px;
                    }
                
                /* Test Summary Cards */
                .test-summary-cards {
                    display: grid;
                    grid-template-columns: repeat(4, 1fr);
                    gap: 20px;
                    margin-bottom: 30px;
                }
                
                .summary-card {
                    background: #ffffff;
                    border: 2px solid #e9ecef;
                    border-radius: 12px;
                    padding: 20px;
                    text-align: center;
                    transition: all 0.3s ease;
                    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
                }
                
                .summary-card:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
                }
                
                .card-icon {
                    font-size: 2rem;
                    margin-bottom: 10px;
                }
                
                .card-label {
                    font-size: 0.9rem;
                    color: #6c757d;
                    font-weight: 500;
                    margin-bottom: 8px;
                }
                
                .card-value {
                    font-size: 1.5rem;
                    font-weight: 700;
                    color: #212529;
                }
                
                .card-value.passed {
                    color: #198754;
                }
                
                .card-value.failed {
                    color: #dc3545;
                }

                /* Section Titles */
                .section-title {
                    font-size: 1.4rem;
                    font-weight: 600;
                    color: #495057;
                    margin-bottom: 20px;
                    text-align: center;
                    border-bottom: 2px solid #e9ecef;
                    padding-bottom: 10px;
                }

                /* Side-by-Side Image Comparison */
                .image-comparison-section {
                    margin-bottom: 15px;
                }
                
                .side-by-side-images {
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 15px;
                }
                
                .image-container {
                    text-align: center;
                }
                
                .image-container h4 {
                    font-size: 1.2rem;
                    font-weight: 600;
                    color: #495057;
                    margin-bottom: 15px;
                }
                
                .image-container img {
                    width: 100%;
                    height: auto;
                    border: 3px solid #dee2e6;
                    border-radius: 12px;
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
                    transition: all 0.3s ease;
                    cursor: pointer;
                }
                
                .image-container img:hover {
                    transform: scale(1.02);
                    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
                }

                /* Single Difference Map */
                .difference-map-section {
                    margin-bottom: 15px;
                }
                
                .difference-map-container {
                    text-align: center;
                }
                
                .difference-map-image {
                    max-width: 100%;
                    height: auto;
                    border: 3px solid #dee2e6;
                    border-radius: 12px;
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
                    transition: all 0.3s ease;
                    cursor: pointer;
                }
                
                .difference-map-image:hover {
                    transform: scale(1.02);
                    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
                }

                /* Simple Color Legend */
                .color-legend-simple {
                    display: flex;
                    justify-content: center;
                    gap: 20px;
                    margin-bottom: 15px;
                    padding: 10px;
                    background: #f8f9fa;
                    border-radius: 12px;
                    border: 1px solid #e9ecef;
                }
                
                .legend-item {
                    display: flex;
                    align-items: center;
                    gap: 10px;
                    font-size: 1rem;
                    font-weight: 500;
                    color: #495057;
                }
                
                .legend-color {
                    font-size: 1.5rem;
                }

                /* Analysis Summary */
                .analysis-summary {
                    margin-bottom: 20px;
                }
                
                .analysis-message {
                    padding: 20px;
                    border-radius: 12px;
                    border-left: 5px solid;
                }
                
                .analysis-message.major {
                    background: #f8d7da;
                    border-left-color: #dc3545;
                }
                
                .analysis-message.moderate {
                    background: #fff3cd;
                    border-left-color: #ffc107;
                }
                
                .analysis-message.minor {
                    background: #d1ecf1;
                    border-left-color: #17a2b8;
                }
                
                .analysis-message.perfect {
                    background: #d4edda;
                    border-left-color: #28a745;
                }
                
                .analysis-message h4 {
                    margin: 0 0 10px 0;
                    font-size: 1.1rem;
                    font-weight: 600;
                }
                
                .analysis-message p {
                    margin: 0;
                    font-size: 1rem;
                    color: #495057;
                    line-height: 1.5;
                }


                

                
                /* Lightbox Styles */
                .lightbox {
                    display: none;
                    position: fixed;
                    z-index: 1000;
                    left: 0;
                    top: 0;
                    width: 100%;
                    height: 100%;
                    background-color: rgba(0, 0, 0, 0.9);
                    opacity: 0;
                    transition: opacity 0.3s ease;
                }
                
                .lightbox.show {
                    opacity: 1;
                }
                
                .lightbox-content {
                    position: absolute;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%) scale(0.8);
                    transition: transform 0.3s ease;
                    max-width: 90%;
                    max-height: 90%;
                }
                
                .lightbox.show .lightbox-content {
                    transform: translate(-50%, -50%) scale(1);
                }
                
                .lightbox-img {
                    max-width: 100%;
                    max-height: 100%;
                    border-radius: 8px;
                    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
                }
                
                .close-lightbox {
                    position: absolute;
                    top: 20px;
                    right: 30px;
                    color: white;
                    font-size: 2rem;
                    font-weight: bold;
                    cursor: pointer;
                    background: none;
                    border: none;
                    padding: 10px;
                    border-radius: 50%;
                    transition: background-color 0.3s ease;
                }
                
                .close-lightbox:hover {
                    background-color: rgba(255, 255, 255, 0.1);
                }
                
                /* Footer */
                .footer {
                    text-align: center;
                    margin-top: 50px;
                    padding: 30px;
                    background: #f8fafc;
                    border-radius: 12px;
                    border-top: 1px solid #e2e8f0;
                }
                
                .footer p {
                    margin-bottom: 8px;
                    color: #6b7280;
                }
                
                .footer .powered-by {
                    font-size: 1.1rem;
                    font-weight: 600;
                    color: #374151;
                    margin-bottom: 5px;
                }
                
                .footer .description {
                    font-size: 0.9rem;
                    color: #9ca3af;
                }
                
                /* Responsive Design Improvements - Fixed */
                @media (max-width: 1200px) {
                    .comparison-grid {
                        grid-template-columns: 1fr;
                        gap: 20px;
                    }
                    
                    .comparison-image:nth-child(3) img,
                    .comparison-image:nth-child(4) img {
                        transform: scale(1.05);
                        margin: 10px 0;
                    }
                }
                
                @media (max-width: 768px) {
                    .container {
                        padding: 10px;
                    }
                    
                    .header {
                        padding: 20px 15px;
                    }
                    
                    .header h1 {
                        font-size: 2rem;
                    }
                    
                    .stats-grid {
                        grid-template-columns: 1fr;
                        gap: 15px;
                    }
                    
                    .comparison-grid {
                        grid-template-columns: 1fr;
                        gap: 15px;
                    }
                    
                    .color-legend {
                        flex-direction: column;
                        gap: 10px;
                        padding: 15px;
                    }
                    
                    .test-metrics {
                        grid-template-columns: 1fr;
                        gap: 15px;
                    }
                    
                    .comparison-image:nth-child(3) img,
                    .comparison-image:nth-child(4) img {
                        transform: scale(1.02);
                        margin: 5px 0;
                    }
                    
                    .difference-map-image {
                        max-width: 100%;
                        height: auto;
                    }
                    
                    .report-content {
                        padding: 20px;
                    }
                }
                
                @media (max-width: 480px) {
                    .comparison-image:nth-child(3) img,
                    .comparison-image:nth-child(4) img {
                        transform: none;
                        margin: 5px 0;
                    }
                    
                    .comparison-image img {
                        min-height: 150px;
                    }
                    
                    .difference-map-image {
                        max-width: 100%;
                        height: auto;
                    }
                }
                
                /* Print Styles for PDF */
                @media print {
                    .download-pdf-btn {
                        display: none !important;
                    }
                    
                    body {
                        background: white !important;
                        color: black !important;
                        font-size: 12px !important;
                        line-height: 1.3 !important;
                        margin: 0 !important;
                        padding: 10px !important;
                    }
                    
                    .container {
                        max-width: none !important;
                        padding: 0 !important;
                        margin: 0 !important;
                    }
                    
                    .header {
                        background: white !important;
                        color: black !important;
                        box-shadow: none !important;
                        padding: 15px !important;
                        margin-bottom: 15px !important;
                        border: 2px solid #333 !important;
                    }
                    
                    .header h1 {
                        font-size: 24px !important;
                        margin-bottom: 5px !important;
                    }
                    
                    .header .subtitle,
                    .header .description {
                        font-size: 14px !important;
                        margin-bottom: 5px !important;
                    }
                    
                    .header .date {
                        font-size: 12px !important;
                    }
                    
                    .stats-grid {
                        grid-template-columns: repeat(4, 1fr) !important;
                        gap: 10px !important;
                        margin-bottom: 20px !important;
                    }
                    
                    .stat-card {
                        box-shadow: none !important;
                        border: 1px solid #ccc !important;
                        padding: 10px !important;
                    }
                    
                    .stat-card .icon {
                        font-size: 20px !important;
                        margin-bottom: 5px !important;
                    }
                    
                    .stat-card .value {
                        font-size: 18px !important;
                        margin-bottom: 3px !important;
                    }
                    
                    .stat-card .label {
                        font-size: 10px !important;
                    }
                    
                    .report-content {
                        box-shadow: none !important;
                        border: 1px solid #ccc !important;
                        padding: 15px !important;
                        margin-top: 15px !important;
                    }
                    
                    .test-detail {
                        padding: 10px !important;
                        margin-bottom: 15px !important;
                        page-break-inside: avoid !important;
                        border: 1px solid #ddd !important;
                    }
                    
                    .test-header {
                        margin-bottom: 10px !important;
                        padding-bottom: 8px !important;
                    }
                    
                    .test-name {
                        font-size: 16px !important;
                    }
                    
                    .test-status {
                        padding: 4px 8px !important;
                        font-size: 10px !important;
                    }
                    
                    .test-metrics {
                        grid-template-columns: repeat(4, 1fr) !important;
                        gap: 10px !important;
                        margin-bottom: 15px !important;
                    }
                    
                    .metric-item {
                        padding: 8px !important;
                    }
                    
                    .metric-value {
                        font-size: 14px !important;
                    }
                    
                    .metric-label {
                        font-size: 10px !important;
                    }
                    
                    .test-summary-cards {
                        grid-template-columns: repeat(4, 1fr) !important;
                        gap: 10px !important;
                        margin-bottom: 15px !important;
                    }
                    
                    .summary-card {
                        padding: 10px !important;
                    }
                    
                    .card-icon {
                        font-size: 16px !important;
                        margin-bottom: 5px !important;
                    }
                    
                    .card-label {
                        font-size: 9px !important;
                        margin-bottom: 3px !important;
                    }
                    
                    .card-value {
                        font-size: 12px !important;
                    }
                    
                    .section-title {
                        font-size: 14px !important;
                        margin-bottom: 10px !important;
                        padding-bottom: 5px !important;
                    }
                    
                    .side-by-side-images {
                        gap: 8px !important;
                    }
                    
                    .image-container h4 {
                        font-size: 10px !important;
                        margin-bottom: 5px !important;
                    }
                    
                    .image-container img {
                        max-width: 40% !important;
                        height: auto !important;
                        max-height: 150px !important;
                    }
                    
                    .difference-map-container img {
                        max-width: 50% !important;
                        height: auto !important;
                        max-height: 180px !important;
                    }
                    
                    .color-legend-simple {
                        gap: 10px !important;
                        margin-bottom: 8px !important;
                        padding: 5px !important;
                    }
                    
                    .legend-item {
                        font-size: 10px !important;
                        gap: 5px !important;
                    }
                    
                    .legend-color {
                        font-size: 12px !important;
                    }
                    
                    .analysis-message {
                        padding: 5px !important;
                        margin-bottom: 5px !important;
                    }
                    
                    .analysis-message h4 {
                        font-size: 12px !important;
                        margin-bottom: 5px !important;
                    }
                    
                    .analysis-message p {
                        font-size: 10px !important;
                    }
                    
                    .footer {
                        margin-top: 20px !important;
                        padding: 15px !important;
                        font-size: 10px !important;
                    }
                    
                    .lightbox {
                        display: none !important;
                    }
                    
                    /* Force page breaks */
                    .test-detail:nth-child(2n) {
                        page-break-before: always !important;
                    }
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🔍 UI Sentinel</h1>
                    <p class="subtitle">Powered by AIVisionTest</p>
                    <p class="description">Visual UI Test Automation Report</p>
                    <p class="date">Report Date: {{ report_date }}</p>
                    <button id="downloadPdfBtn" class="download-pdf-btn" onclick="downloadAsPDF()">
                        📄 Download PDF
                    </button>
                </div>
                
                <div class="stats-grid">
                    <div class="stat-card passed">
                        <span class="icon">📊</span>
                        <div class="value">{{ summary.total_tests }}</div>
                        <div class="label">{{ texts.summary_cards.total_tests }}</div>
                    </div>
                    <div class="stat-card passed">
                        <span class="icon">✅</span>
                        <div class="value">{{ summary.passed_tests }}</div>
                        <div class="label">{{ texts.summary_cards.passed_tests }}</div>
                    </div>
                    <div class="stat-card failed">
                        <span class="icon">❌</span>
                        <div class="value">{{ summary.failed_tests }}</div>
                        <div class="label">{{ texts.summary_cards.failed_tests }}</div>
                    </div>
                    <div class="stat-card {% if summary.pass_rate >= 80 %}passed{% else %}failed{% endif %}">
                        <span class="icon">📈</span>
                        <div class="value">{{ "%.1f"|format(summary.pass_rate) }}%</div>
                        <div class="label">{{ texts.summary_cards.pass_rate }}</div>
                    </div>
                </div>
                
                <div class="report-content">
                    {% for result in test_results %}
                    <div class="test-detail">
                        <div class="test-header">
                            <h3 class="test-name">{{ result.page_name|title }}</h3>
                            <span class="test-status {% if result.passed %}passed{% else %}failed{% endif %}">
                                {% if result.passed %}PASSED{% else %}FAILED{% endif %}
                            </span>
                        </div>
                        
                        <div class="test-metrics">
                            <div class="metric-item">
                                <div class="metric-value">{{ "%.2f"|format(result.similarity_score) }}</div>
                                <div class="metric-label">{{ texts.test_details.similarity_score }}</div>
                            </div>
                            <div class="metric-item">
                                <div class="metric-value">{{ "%.2f"|format(result.difference_percentage) }}%</div>
                                <div class="metric-label">{{ texts.test_details.difference_percentage }}</div>
                            </div>
                            <div class="metric-item">
                                <div class="metric-value">{{ result.different_pixels }}</div>
                                <div class="metric-label">{{ texts.test_details.different_pixels }}</div>
                            </div>
                            <div class="metric-item">
                                <div class="metric-value">{{ result.test_time }}</div>
                                <div class="metric-label">{{ texts.test_details.test_time }}</div>
                            </div>
                        </div>
                        
                        <div class="visual-comparison">
                            <!-- Test Summary Cards -->
                            <div class="test-summary-cards">
                                <div class="summary-card result">
                                    <div class="card-icon">📊</div>
                                    <div class="card-content">
                                        <div class="card-label">Test Result</div>
                                        <div class="card-value {% if result.passed %}passed{% else %}failed{% endif %}">
                                            {% if result.passed %}PASSED ✅{% else %}FAILED ❌{% endif %}
                                        </div>
                                    </div>
                            </div>
                            
                                <div class="summary-card similarity">
                                    <div class="card-icon">📈</div>
                                    <div class="card-content">
                                        <div class="card-label">Similarity Rate</div>
                                        <div class="card-value">{{ "%.2f"|format(result.similarity_score * 100) }}%</div>
                                </div>
                                </div>
                                
                                <div class="summary-card difference">
                                    <div class="card-icon">🔍</div>
                                    <div class="card-content">
                                        <div class="card-label">Difference Rate</div>
                                        <div class="card-value">{{ "%.2f"|format(result.difference_percentage) }}%</div>
                                </div>
                            </div>
                            
                                <div class="summary-card pixels">
                                    <div class="card-icon">🎯</div>
                                    <div class="card-content">
                                        <div class="card-label">Difference Pixels</div>
                                        <div class="card-value">{{ result.different_pixels }}</div>
                                    </div>
                                </div>
                            </div>
                            
                            <!-- Side-by-Side Image Comparison -->
                            <div class="image-comparison-section">
                                <h3 class="section-title">Image Comparison</h3>
                                <div class="side-by-side-images">
                                    <div class="image-container">
                                        <h4>Reference Image</h4>
                                    <img src="data:image/png;base64,{{ result.baseline_image_base64 }}" 
                                         onclick="openLightbox(event, 'baseline')" 
                                         alt="Baseline Image">
                                </div>
                                    <div class="image-container">
                                        <h4>Test Image</h4>
                                    <img src="data:image/png;base64,{{ result.test_image_base64 }}" 
                                         onclick="openLightbox(event, 'test')" 
                                         alt="Test Image">
                                </div>
                                </div>
                            </div>

                            <!-- Single Difference Map -->
                            <div class="difference-map-section">
                                <h3 class="section-title">Difference Map</h3>
                                <div class="difference-map-container">
                                    <img src="data:image/png;base64,{{ result.diff_map_base64 }}" 
                                         onclick="openLightbox(event, 'diff')" 
                                         alt="Difference Map"
                                         class="difference-map-image">
                                </div>
                                </div>

                            <!-- Simple Color Legend -->
                            <div class="color-legend-simple">
                                <div class="legend-item">
                                    <div class="legend-color changed">🟠</div>
                                    <span>Changed Areas</span>
                                </div>
                                <div class="legend-item">
                                    <div class="legend-color unchanged">⚪</div>
                                    <span>Unchanged Areas</span>
                                </div>
                            </div>

                            <!-- Analysis Summary -->
                            <div class="analysis-summary">
                                {% if result.difference_percentage > 50 %}
                                    <div class="analysis-message major">
                                        <h4>🚨 Major Changes Detected</h4>
                                        <p>{{ "%.2f"|format(result.difference_percentage) }}% difference rate indicates significant page changes. This may be due to theme changes, page refresh, or major design updates.</p>
                                    </div>
                                {% elif result.difference_percentage > 10 %}
                                    <div class="analysis-message moderate">
                                        <h4>⚠️ Moderate Changes</h4>
                                        <p>{{ "%.2f"|format(result.difference_percentage) }}% difference rate indicates significant visual changes on the page. Review recommended.</p>
                                    </div>
                                {% elif result.difference_percentage > 1 %}
                                    <div class="analysis-message minor">
                                        <h4>ℹ️ Minor Changes</h4>
                                        <p>{{ "%.2f"|format(result.difference_percentage) }}% difference rate indicates minimal changes detected. Likely due to dynamic content or minor updates.</p>
                                    </div>
                                {% else %}
                                    <div class="analysis-message perfect">
                                        <h4>✅ Perfect Match</h4>
                                        <p>{{ "%.2f"|format(result.difference_percentage) }}% difference rate indicates the page is visually consistent. Visual harmony is maintained.</p>
                                    </div>
                                {% endif %}
                            </div>
                        </div>
                    </div>
                    {% endfor %}
                </div>
                
                <div class="footer">
                    <p class="powered-by">{{ texts.footer.powered_by }}</p>
                    <p class="description">{{ texts.footer.description }}</p>
                    <p>{{ texts.footer.report_time.format(date=report_date) }}</p>
                </div>
            </div>
            
            <!-- Lightbox -->
            <div id="lightbox" class="lightbox" onclick="closeLightbox()">
                <span class="close-lightbox" onclick="closeLightbox()">&times;</span>
                <div class="lightbox-content">
                    <img id="lightbox-img" class="lightbox-img" src="" alt="Enlarged Image">
                </div>
            </div>
            
            <script>
                function openLightbox(event, imageType) {
                    event.preventDefault();
                    event.stopPropagation();
                    
                    const lightbox = document.getElementById('lightbox');
                    const lightboxImg = document.getElementById('lightbox-img');
                    const clickedImg = event.target;
                    
                    lightboxImg.src = clickedImg.src;
                    
                    // Lightbox'ı göster ve animasyonu başlat
                    lightbox.style.display = 'block';
                    setTimeout(() => {
                        lightbox.classList.add('show');
                    }, 10);
                }
                
                function closeLightbox() {
                    const lightbox = document.getElementById('lightbox');
                    lightbox.classList.remove('show');
                    
                    // Animasyon bittikten sonra gizle
                    setTimeout(() => {
                        lightbox.style.display = 'none';
                    }, 300);
                }
                
                // ESC tuşu ile kapatma
                document.addEventListener('keydown', function(event) {
                    if (event.key === 'Escape') {
                        closeLightbox();
                    }
                });
                
                // PDF Download Function
                function downloadAsPDF() {
                    const button = document.getElementById('downloadPdfBtn');
                    const originalText = button.innerHTML;
                    
                    // Button loading state
                    button.innerHTML = '⏳ Generating PDF...';
                    button.disabled = true;
                    
                    // Use browser's print to PDF functionality
                    setTimeout(() => {
                        window.print();
                        
                        // Reset button after a delay
                        setTimeout(() => {
                            button.innerHTML = originalText;
                            button.disabled = false;
                        }, 2000);
                    }, 500);
                }
            </script>
        </body>
        </html>
        """
        
        # Test sonuçlarını işle
        processed_results = []
        for result in comparison_results.get('results', []):
            processed_result = result.copy()
            
            # Fark görüntüsünü base64'e çevir
            if result.get('difference_image_path') and os.path.exists(result['difference_image_path']):
                processed_result['difference_image_base64'] = self._image_to_base64(result['difference_image_path'])
            
            # Baseline ve test görüntülerini base64'e çevir
            baseline_path = f"baseline/{result['page_name']}.png"
            test_path = f"screenshots/{result['page_name']}.png"
            
            if os.path.exists(baseline_path):
                processed_result['baseline_image_base64'] = self._image_to_base64(baseline_path)
            
            if os.path.exists(test_path):
                processed_result['test_image_base64'] = self._image_to_base64(test_path)
            
            # Fark haritası ve overlay için aynı fark görüntüsünü kullan
            if result.get('difference_image_path') and os.path.exists(result['difference_image_path']):
                processed_result['diff_map_base64'] = self._image_to_base64(result['difference_image_path'])
                processed_result['overlay_image_base64'] = self._image_to_base64(result['difference_image_path'])
            
            processed_results.append(processed_result)
        
        # Summary verilerini düzelt
        summary = comparison_results.get('summary', {})
        if not summary:
            # Eğer summary yoksa, test sonuçlarından hesapla
            results = comparison_results.get('results', [])
            total_tests = len(results)
            passed_tests = sum(1 for r in results if r.get('passed', False))
            failed_tests = total_tests - passed_tests
            pass_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
            
            summary = {
                'total_tests': total_tests,
                'passed_tests': passed_tests,
                'failed_tests': failed_tests,
                'pass_rate': pass_rate
            }
        
        # Şablonu render et
        template = Template(html_template)
        html_content = template.render(
            summary=summary,
            test_results=processed_results,
            report_date=datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
            texts=self.language_config
        )
        
        # HTML dosyasını kaydet
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"📄 HTML rapor kaydedildi: {report_path}")
        return report_path
    

    

    
    def generate_reports(self, comparison_results):
        """JSON ve HTML raporları oluşturur"""
        print("📊 Raporlar oluşturuluyor...")
        
        # JSON raporu oluştur
        json_report_path = self.generate_json_report(comparison_results)
        
        # HTML raporu oluştur
        html_report_path = self.generate_html_report(comparison_results)
        
        reports = {
            'json_report': json_report_path,
            'html_report': html_report_path
        }
        
        return reports


 