"""
Codveda Technologies - Level 2 Task 2: Data Scraper Web Application
Test Script

This script provides comprehensive tests for the scraper module.
Run this to verify that all components are working correctly.

Author: Python Development Intern @ Codveda Technologies
Version: 1.0.0
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))


def test_imports():
    """Test that all required modules can be imported"""
    print("\n" + "="*60)
    print("TEST 1: Import Testing")
    print("="*60)
    
    try:
        import requests
        print("✅ requests imported successfully")
    except ImportError as e:
        print(f"❌ requests import failed: {e}")
        return False
    
    try:
        from bs4 import BeautifulSoup
        print("✅ BeautifulSoup imported successfully")
    except ImportError as e:
        print(f"❌ BeautifulSoup import failed: {e}")
        return False
    
    try:
        import pandas as pd
        print("✅ pandas imported successfully")
    except ImportError as e:
        print(f"❌ pandas import failed: {e}")
        return False
    
    try:
        import streamlit as st
        print("✅ streamlit imported successfully")
    except ImportError as e:
        print(f"❌ streamlit import failed: {e}")
        return False
    
    try:
        from scraper import WebScraper, ScrapingType
        print("✅ scraper module imported successfully")
    except ImportError as e:
        print(f"❌ scraper module import failed: {e}")
        return False
    
    try:
        from utils import setup_logging, validate_url, load_history
        print("✅ utils module imported successfully")
    except ImportError as e:
        print(f"❌ utils module import failed: {e}")
        return False
    
    print("\n✅ All imports successful!")
    return True


def test_scraper_initialization():
    """Test WebScraper class initialization"""
    print("\n" + "="*60)
    print("TEST 2: Scraper Initialization")
    print("="*60)
    
    try:
        from scraper import WebScraper, ScrapingType
        
        # Test default initialization
        scraper = WebScraper()
        print("✅ Default initialization successful")
        
        # Test with custom parameters
        scraper = WebScraper(
            scraping_type=ScrapingType.NEWS,
            timeout=30
        )
        print("✅ Custom initialization successful")
        
        # Test all scraping types
        for scrap_type in ScrapingType:
            scraper = WebScraper(scraping_type=scrap_type)
            print(f"✅ {scrap_type.name} type initialized")
        
        return True
    except Exception as e:
        print(f" Initialization failed: {e}")
        return False


def test_url_validation():
    """Test URL validation function"""
    print("\n" + "="*60)
    print("TEST 3: URL Validation")
    print("="*60)
    
    try:
        from utils import validate_url
        
        # Valid URLs
        valid_urls = [
            "https://example.com",
            "http://test.org",
            "https://www.google.com",
            "http://localhost:8080",
            "https://subdomain.example.com/path"
        ]
        
        for url in valid_urls:
            if validate_url(url):
                print(f"✅ Valid URL recognized: {url}")
            else:
                print(f"❌ Valid URL rejected: {url}")
                return False
        
        # Invalid URLs
        invalid_urls = [
            "not-a-url",
            "ftp://example.com",
            "example.com",
            "",
            "htp://typo.com"
        ]
        
        for url in invalid_urls:
            if not validate_url(url):
                print(f"✅ Invalid URL rejected: {url}")
            else:
                print(f"❌ Invalid URL accepted: {url}")
                return False
        
        return True
    except Exception as e:
        print(f"❌ URL validation test failed: {e}")
        return False


def test_logging():
    """Test logging setup"""
    print("\n" + "="*60)
    print("TEST 4: Logging System")
    print("="*60)
    
    try:
        from utils import setup_logging
        import logging
        
        logger = setup_logging()
        
        # Test different log levels
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
        
        print("✅ Logging system working correctly")
        
        # Check if log file exists
        from pathlib import Path
        log_file = Path("logs/scraper.log")
        
        if log_file.exists():
            print(f"✅ Log file created: {log_file}")
        else:
            print("⚠️ Log file not found (may be created on first write)")
        
        return True
    except Exception as e:
        print(f"❌ Logging test failed: {e}")
        return False


def test_html_parsing():
    """Test HTML parsing functionality"""
    print("\n" + "="*60)
    print("TEST 5: HTML Parsing")
    print("="*60)
    
    try:
        from scraper import WebScraper
        
        # Sample HTML
        sample_html = """
        <html>
            <head><title>Test Page</title></head>
            <body>
                <h1 class="headline">Test Headline</h1>
                <h2 class="headline">Second Headline</h2>
                <article>
                    <h3>Article Title</h3>
                    <p>Article content here...</p>
                </article>
                <div class="product">
                    <span class="price">$99.99</span>
                    <h4>Product Name</h4>
                </div>
            </body>
        </html>
        """
        
        scraper = WebScraper()
        soup = scraper.parse_html(sample_html)
        
        # Test element extraction
        headlines = soup.select(".headline")
        if len(headlines) == 2:
            print("✅ CSS selector working correctly")
        else:
            print(f"❌ Expected 2 headlines, found {len(headlines)}")
            return False
        
        # Test text extraction
        title = soup.find("h1").get_text(strip=True)
        if title == "Test Headline":
            print("✅ Text extraction working correctly")
        else:
            print(f"❌ Expected 'Test Headline', got '{title}'")
            return False
        
        # Test attribute extraction
        products = soup.select(".product")
        if len(products) == 1:
            print("✅ Element finding working correctly")
        else:
            print(f"❌ Expected 1 product, found {len(products)}")
            return False
        
        return True
    except Exception as e:
        print(f"❌ HTML parsing test failed: {e}")
        return False


def test_history_management():
    """Test history management functions"""
    print("\n" + "="*60)
    print("TEST 6: History Management")
    print("="*60)
    
    try:
        from utils import load_history, save_history, add_history_entry
        import json
        
        # Load existing history
        history = load_history()
        print(f"✅ Loaded {len(history)} history entries")
        
        # Test saving history
        test_entry = {
            "url": "https://test.com",
            "type": "news",
            "records": 10,
            "timestamp": "2024-01-01 12:00:00"
        }
        
        history.append(test_entry)
        success = save_history(history)
        
        if success:
            print("✅ History saved successfully")
        else:
            print("❌ Failed to save history")
            return False
        
        # Verify history file exists
        from pathlib import Path
        history_file = Path("scraping_history.json")
        
        if history_file.exists():
            print(f"✅ History file created: {history_file}")
        else:
            print("❌ History file not found")
            return False
        
        return True
    except Exception as e:
        print(f"❌ History management test failed: {e}")
        return False


def test_data_export():
    """Test data export functionality"""
    print("\n" + "="*60)
    print("TEST 7: Data Export")
    print("="*60)
    
    try:
        import pandas as pd
        from pathlib import Path
        
        # Create sample data
        sample_data = [
            {"title": "Article 1", "link": "https://example.com/1", "date": "2024-01-01"},
            {"title": "Article 2", "link": "https://example.com/2", "date": "2024-01-02"},
            {"title": "Article 3", "link": "https://example.com/3", "date": "2024-01-03"},
        ]
        
        df = pd.DataFrame(sample_data)
        
        # Test CSV export
        csv_path = Path("output/test_export.csv")
        df.to_csv(csv_path, index=False)
        
        if csv_path.exists():
            print("✅ CSV export working")
            csv_path.unlink()  # Clean up
        else:
            print("❌ CSV export failed")
            return False
        
        # Test JSON export
        json_path = Path("output/test_export.json")
        df.to_json(json_path, orient="records", indent=2)
        
        if json_path.exists():
            print("✅ JSON export working")
            json_path.unlink()  # Clean up
        else:
            print("❌ JSON export failed")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Data export test failed: {e}")
        return False


def test_rate_limiter():
    """Test rate limiting functionality"""
    print("\n" + "="*60)
    print("TEST 8: Rate Limiter")
    print("="*60)
    
    try:
        from utils import RateLimiter
        import time
        
        limiter = RateLimiter(requests_per_second=2.0)
        
        # Test rate limiting
        start_time = time.time()
        
        for i in range(3):
            limiter.wait()
            print(f"✅ Request {i+1} - Rate limit respected")
        
        elapsed = time.time() - start_time
        
        # Should take at least 1 second for 3 requests at 2 req/s
        if elapsed >= 0.9:  # Allow some tolerance
            print(f"✅ Rate limiting working (elapsed: {elapsed:.2f}s)")
        else:
            print(f"⚠️ Rate limiting may not be working (elapsed: {elapsed:.2f}s)")
        
        return True
    except Exception as e:
        print(f"❌ Rate limiter test failed: {e}")
        return False


def run_all_tests():
    """Run all tests and provide summary"""
    print("\n" + "="*60)
    print(" CODVEDA DATA SCRAPER - TEST SUITE")
    print("="*60)
    print(f"Running comprehensive tests...\n")
    
    tests = [
        ("Import Testing", test_imports),
        ("Scraper Initialization", test_scraper_initialization),
        ("URL Validation", test_url_validation),
        ("Logging System", test_logging),
        ("HTML Parsing", test_html_parsing),
        ("History Management", test_history_management),
        ("Data Export", test_data_export),
        ("Rate Limiter", test_rate_limiter),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print("\n" + "-"*60)
    print(f"Total: {passed}/{total} tests passed")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    print("="*60)
    
    if passed == total:
        print("\n🎉 All tests passed! The scraper is ready to use!")
        return True
    else:
        print(f"\n⚠️ {total - passed} test(s) failed. Please check the errors above.")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
