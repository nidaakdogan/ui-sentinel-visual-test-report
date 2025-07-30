#!/usr/bin/env python3
"""
UI Sentinel - Görsel Karşılaştırma Testleri
Bu dosya, görsel karşılaştırma fonksiyonlarını test eder.
"""

import pytest
import os
import sys
import cv2
import numpy as np
from PIL import Image

# src klasörünü Python path'ine ekle
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from image_comparison import ImageComparison


class TestImageComparison:
    """Görsel karşılaştırma testleri"""
    
    @pytest.fixture
    def image_comparison(self):
        """ImageComparison örneği oluşturur"""
        return ImageComparison()
    
    @pytest.fixture
    def test_images_dir(self):
        """Test görüntüleri klasörü"""
        return os.path.join(os.path.dirname(__file__), 'test_images')
    
    def create_test_image(self, path, size=(100, 100), color=(255, 255, 255)):
        """Test görüntüsü oluşturur"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        image = Image.new('RGB', size, color)
        image.save(path)
        return path
    
    def test_load_image_success(self, image_comparison, test_images_dir):
        """Görüntü yükleme başarı testi"""
        # Test görüntüsü oluştur
        test_image_path = os.path.join(test_images_dir, 'test.png')
        self.create_test_image(test_image_path)
        
        # Görüntüyü yükle
        result = image_comparison.load_image(test_image_path)
        
        # Sonuçları kontrol et
        assert result is not None
        assert isinstance(result, np.ndarray)
        assert result.shape == (100, 100)  # Gri tonlama
        
        # Temizlik
        os.remove(test_image_path)
    
    def test_load_image_not_found(self, image_comparison):
        """Görüntü bulunamadı testi"""
        result = image_comparison.load_image('nonexistent.png')
        assert result is None
    
    def test_compare_identical_images(self, image_comparison, test_images_dir):
        """Aynı görüntüleri karşılaştırma testi"""
        # İki aynı görüntü oluştur
        image1_path = os.path.join(test_images_dir, 'image1.png')
        image2_path = os.path.join(test_images_dir, 'image2.png')
        
        self.create_test_image(image1_path)
        self.create_test_image(image2_path)
        
        # Karşılaştırma yap
        result = image_comparison.compare_images(image1_path, image2_path, 'test_page')
        
        # Sonuçları kontrol et
        assert result['success'] is True
        assert result['similarity_score'] == 1.0
        assert result['difference_percentage'] == 0.0
        assert result['passed'] is True
        
        # Temizlik
        os.remove(image1_path)
        os.remove(image2_path)
    
    def test_compare_different_images(self, image_comparison, test_images_dir):
        """Farklı görüntüleri karşılaştırma testi"""
        # Farklı görüntüler oluştur
        image1_path = os.path.join(test_images_dir, 'image1.png')
        image2_path = os.path.join(test_images_dir, 'image2.png')
        
        # Beyaz görüntü
        self.create_test_image(image1_path, color=(255, 255, 255))
        # Siyah görüntü
        self.create_test_image(image2_path, color=(0, 0, 0))
        
        # Karşılaştırma yap
        result = image_comparison.compare_images(image1_path, image2_path, 'test_page')
        
        # Sonuçları kontrol et
        assert result['success'] is True
        assert result['similarity_score'] < 1.0
        assert result['difference_percentage'] > 0.0
        assert result['passed'] is False
        
        # Temizlik
        os.remove(image1_path)
        os.remove(image2_path)
    
    def test_compare_images_different_sizes(self, image_comparison, test_images_dir):
        """Farklı boyutlardaki görüntüleri karşılaştırma testi"""
        # Farklı boyutlarda görüntüler oluştur
        image1_path = os.path.join(test_images_dir, 'image1.png')
        image2_path = os.path.join(test_images_dir, 'image2.png')
        
        self.create_test_image(image1_path, size=(100, 100))
        self.create_test_image(image2_path, size=(200, 200))
        
        # Karşılaştırma yap
        result = image_comparison.compare_images(image1_path, image2_path, 'test_page')
        
        # Sonuçları kontrol et
        assert result['success'] is True
        assert result['similarity_score'] >= 0.0
        assert result['similarity_score'] <= 1.0
        
        # Temizlik
        os.remove(image1_path)
        os.remove(image2_path)
    
    def test_threshold_settings(self, image_comparison, test_images_dir):
        """Eşik ayarları testi"""
        # Farklı eşik değerleri ile test et
        image1_path = os.path.join(test_images_dir, 'image1.png')
        image2_path = os.path.join(test_images_dir, 'image2.png')
        
        self.create_test_image(image1_path, color=(255, 255, 255))
        self.create_test_image(image2_path, color=(200, 200, 200))  # Biraz farklı
        
        # Yüksek eşik ile test
        image_comparison.threshold = 0.99
        result_high = image_comparison.compare_images(image1_path, image2_path, 'test_page')
        
        # Düşük eşik ile test
        image_comparison.threshold = 0.5
        result_low = image_comparison.compare_images(image1_path, image2_path, 'test_page')
        
        # Sonuçları kontrol et
        assert result_high['passed'] != result_low['passed']
        
        # Temizlik
        os.remove(image1_path)
        os.remove(image2_path)


if __name__ == "__main__":
    pytest.main([__file__]) 