# 🔍 UI Sentinel - Visual UI Test Automation

**UI Sentinel** is an advanced visual UI test automation tool developed by AIVisionTest. It automatically tests the visual consistency of web pages and generates detailed reports.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Selenium](https://img.shields.io/badge/Selenium-4.0+-green.svg)](https://selenium-python.readthedocs.io/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.0+-red.svg)](https://opencv.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## ✨ Features

### 🎯 **Core Features**
- **Automatic screenshot capture**: Precise image capture with Selenium WebDriver
- **Pixel-perfect comparison**: Advanced visual analysis with OpenCV
- **Multi-page support**: Test multiple pages simultaneously
- **Smart pop-up management**: Automatic pop-up closing and theme consistency
- **Detailed reporting**: Comprehensive reports in HTML, JSON and PDF formats

### 🔍 **Advanced Visual Comparison**
- **Color-coded difference maps**: Visually highlight changed areas
- **Similarity scoring**: Percentage-based similarity calculation
- **Tolerance settings**: Customizable threshold values per page
- **Optimized visual analysis**: Difference maps and overlays scaled 1.2x (sharper)

### 📊 **Reporting System**
- **English reports**: Default English language support
- **Multiple formats**: HTML, JSON and PDF reports
- **Visual comparison**: 4-grid layout
- **Zoom functionality**: Magnification in difference maps
- **Responsive design**: Mobile-friendly report interface

### 🎨 **Visual Comparison System**
- **4-grid layout**: Reference, Test, Difference Map, Overlay
- **Color coding**:
  - **🟠 Orange**: Changed areas (attention required)
  - **⚪ White**: Unchanged areas (safe)
- **Optimized visual analysis**: Difference maps and overlays scaled 1.2x (sharper)

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.8+
Chrome Browser
ChromeDriver (automatically managed)
```

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/AIVisionTest.git
cd AIVisionTest
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run tests**
```bash
python run_tests.py
```

4. **View reports**
```bash
# Open the latest HTML report
start reports/ui_sentinel_report_*.html
```

## 📁 Project Structure

```
AIVisionTest/
├── src/
│   ├── screenshot_capture.py    # Screenshot capture
│   ├── image_comparison.py      # Visual comparison
│   ├── report_generator.py      # Report generation
│   └── visual_test.py          # Main test logic
├── config/
│   ├── test_config.json        # Test settings
│   └── language_config.json    # Language settings
├── baseline/                   # Reference images
├── screenshots/               # Test images
├── results/                   # Difference images
├── reports/                   # Generated reports
├── dashboard/                 # Web dashboard
├── tests/                     # Test files
├── requirements.txt           # Python dependencies
└── README.md                 # This file
```

## ⚙️ Configuration

### Test Settings (`config/test_config.json`)
```json
{
  "browser": {
    "name": "chrome",
    "headless": false,
    "window_size": {
      "width": 1920,
      "height": 1080
    }
  },
  "test_pages": [
    {
      "name": "google_homepage",
      "url": "https://www.google.com",
      "wait_time": 3,
      "description": "Google homepage test"
    }
  ],
  "comparison_settings": {
    "threshold": 0.80,
    "tolerance": 10,
    "highlight_differences": true,
    "save_differences": true
  }
}
```

### Language Settings (`config/language_config.json`)
```json
{
  "en": {
    "summary_cards": {
      "total_tests": "Total Tests",
      "passed_tests": "Passed Tests"
    }
  },
  "tr": {
    "summary_cards": {
      "total_tests": "Toplam Test",
      "passed_tests": "Geçen Test"
    }
  }
}
```

## 📊 Reporting System

### HTML Report
- **Modern design**: Professional appearance with Inter font
- **Statistics cards**: Hover effects and color coding
- **Visual comparison**: 4-grid layout
- **Color legend**: Guide explaining difference types
- **Lightbox**: Full-screen visual viewing
- **Responsive**: Mobile-friendly design

### JSON Report
```json
{
  "project_name": "UI Sentinel - Powered by AIVisionTest",
  "summary": {
    "total_tests": 3,
    "passed_tests": 3,
    "failed_tests": 0,
    "pass_rate": 100.0
  },
  "results": [
    {
      "page_name": "google_homepage",
      "passed": true,
      "similarity_score": 0.8099,
      "difference_percentage": 19.01
    }
  ]
}
```

## 🎨 Visual Comparison System

### Color Coding
- **🟠 Orange**: Changed areas (attention required)
- **⚪ White**: Unchanged areas (safe)

### Visual Layout
1. **Reference Image**: Baseline image
2. **Test Image**: Current state
3. **Difference Map**: Color comparison (1.2x scaled)
4. **Overlay View**: Transparent overlay (1.2x scaled)

### Difference Analysis System
- **Automatic evaluation**: Analysis based on difference percentage
- **Explanatory texts**: Meaning of changes
- **Categorized results**: Major, minor, or none
- **User guidance**: Guide on what to do

## 🔧 Performance and Features

### Test Performance
- **Fast comparison**: OpenCV optimization
- **Memory efficient**: Optimized for large images
- **Parallel processing**: Multiple page tests

### Reliability
- **Theme fixing**: For dynamic sites like Google
- **Error tolerance**: Resilient to network issues
- **Automatic cleanup**: Clean temporary files

## 📈 Dashboard Features

- **Real-time monitoring**: Live tracking of test results
- **Modern interface**: Clean and user-friendly design
- **Auto-refresh**: Automatic data updates
- **Responsive design**: Compatible with all devices

## 🛠️ Development

### Adding New Tests
1. Add new page to `config/test_config.json`
2. Place reference image in `baseline/` folder
3. Run the test

### Adding Language Support
1. Add new language to `config/language_config.json`
2. Translate all texts
3. Update report generator

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📋 GitHub Deployment Steps

### Step 1: Prepare Repository
```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: UI Sentinel Visual Test Automation"
```

### Step 2: Create GitHub Repository
1. Go to [GitHub](https://github.com)
2. Click "New repository"
3. Name: `AIVisionTest`
4. Description: `Advanced visual UI test automation tool with Selenium and OpenCV`
5. Make it **Public** or **Private**
6. **Don't** initialize with README (we already have one)
7. Click "Create repository"

### Step 3: Push to GitHub
```bash
# Add remote origin
git remote add origin https://github.com/yourusername/AIVisionTest.git

# Push to main branch
git branch -M main
git push -u origin main
```

### Step 4: Add GitHub Actions (Optional)
Create `.github/workflows/test.yml`:
```yaml
name: UI Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.8'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Install Chrome
      run: |
        wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
        echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list
        apt-get update
        apt-get install -y google-chrome-stable
    
    - name: Run tests
      run: python run_tests.py
```

### Step 5: Add Repository Badges
Add these to your README:
```markdown
[![Tests](https://github.com/yourusername/AIVisionTest/workflows/UI%20Tests/badge.svg)](https://github.com/yourusername/AIVisionTest/actions)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
```

### Step 6: Create Release
1. Go to "Releases" in your GitHub repository
2. Click "Create a new release"
3. Tag: `v1.0.0`
4. Title: `UI Sentinel v1.0.0`
5. Description: Add release notes
6. Upload `requirements.txt` and other important files
7. Publish release

## 🎯 Usage Examples

### Basic Test Run
```bash
python run_tests.py
```

### Custom Configuration
```python
from src.visual_test import VisualTest

# Create test instance
test = VisualTest()

# Run with custom settings
test.run_tests(
    pages=['google_homepage', 'github_homepage'],
    threshold=0.85,
    tolerance=5
)
```

### Generate Reports Only
```python
from src.report_generator import ReportGenerator

generator = ReportGenerator()
reports = generator.generate_reports(comparison_results)
```

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/AIVisionTest/issues)
- **Documentation**: [Wiki](https://github.com/yourusername/AIVisionTest/wiki)
- **Email**: your-email@example.com

---

**UI Sentinel** - Test your web applications' visual consistency safely with AIVisionTest! 🚀


