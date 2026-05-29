"""
Codveda Technologies - Level 2 Task 2: Data Scraper Web Application
Configuration Settings

This module contains all configuration constants and settings for the application.
Centralized configuration makes it easy to modify behavior without changing core code.

Author: Python Development Intern @ Codveda Technologies
Version: 1.0.0
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# =============================================================================
# Application Settings
# =============================================================================
APP_NAME = "Codveda Data Scraper"
APP_VERSION = "1.0.0"
APP_TITLE = " Codveda Data Scraper | Level 2 Task"
APP_DESCRIPTION = "Professional Web Scraping Application for Codveda Technologies Internship"


# =============================================================================
# Directory Paths
# =============================================================================
BASE_DIR = Path(__file__).parent
LOGS_DIR = BASE_DIR / "logs"
OUTPUT_DIR = BASE_DIR / "output"

# Ensure directories exist
LOGS_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)


# =============================================================================
# Scraping Settings
# =============================================================================
# Request timeout in seconds
DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", 30))

# Maximum number of results to extract
MAX_RESULTS = int(os.getenv("MAX_RESULTS", 50))

# Minimum interval between requests (rate limiting)
RATE_LIMIT_INTERVAL = float(os.getenv("RATE_LIMIT_INTERVAL", 1.0))

# Maximum pages to scrape (for pagination)
MAX_PAGES = int(os.getenv("MAX_PAGES", 5))


# =============================================================================
# User Agent Settings
# =============================================================================
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
]


# =============================================================================
# Logging Settings
# =============================================================================
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_BACKUP_COUNT = 7  # Keep 7 days of logs


# =============================================================================
# Export Settings
# =============================================================================
EXPORT_FORMATS = ["csv", "json", "excel"]
DEFAULT_EXPORT_FORMAT = "csv"
EXPORT_FILENAME_PREFIX = "scraped_data"


# =============================================================================
# UI Settings
# =============================================================================
UI_THEME = "light"  # or "dark"
UI_LAYOUT = "wide"
SHOW_ADVANCED_BY_DEFAULT = False
HISTORY_LIMIT = 50  # Maximum history entries to keep


# =============================================================================
# Selector Mappings (Default CSS Selectors for Common Sites)
# =============================================================================
DEFAULT_SELECTORS = {
    "news": {
        "headline": ["h1", "h2", "h3", ".headline", ".title", ".article-title"],
        "link": ["a"],
        "date": ["time", ".date", ".published", ".timestamp"]
    },
    "ecommerce": {
        "product": [".product", ".product-item", ".product-card", "[data-product]"],
        "name": [".product-name", ".product-title", "h3", "h4"],
        "price": [".price", ".product-price", "[data-price]"],
        "rating": [".rating", ".stars", "[data-rating]"],
        "image": ["img"]
    },
    "article": {
        "container": ["article", ".article", ".post", ".blog-post"],
        "title": ["h1", "h2", ".article-title", ".post-title"],
        "author": [".author", ".byline", "[data-author]"],
        "date": ["time", ".date", ".published"],
        "content": [".content", ".post-content", ".article-body"]
    },
    "jobs": {
        "listing": [".job-listing", ".job-post", ".job-item", "[data-job]"],
        "title": ["h3", "h4", ".job-title", ".position-title"],
        "location": [".location", ".job-location"],
        "type": [".job-type", ".employment-type"]
    },
    "blog": {
        "post": [".blog-post", ".post", "article", ".blog-item"],
        "title": ["h2", "h3", ".post-title", ".blog-title"],
        "date": ["time", ".date", ".published"],
        "link": ["a"]
    }
}


# =============================================================================
# Error Messages
# =============================================================================
ERROR_MESSAGES = {
    "invalid_url": "❌ Please enter a valid URL (must start with http:// or https://)",
    "timeout": "️ Request timed out. The website may be slow or unreachable.",
    "forbidden": " Access forbidden (403). The website may be blocking scrapers.",
    "not_found": "📄 Page not found (404). Please check the URL.",
    "server_error": "🔧 Server error (500). Try again later.",
    "no_data": "⚠️ No data was extracted. Try using custom selectors.",
    "robots_blocked": "🤖 Scraping may be disallowed by robots.txt",
    "general_error": "❌ An unexpected error occurred. Please check the logs."
}


# =============================================================================
# Success Messages
# =============================================================================
SUCCESS_MESSAGES = {
    "scrape_complete": "✅ Successfully scraped {count} records!",
    "export_complete": "💾 Data exported successfully!",
    "history_saved": "📝 Scraping history updated!"
}


# =============================================================================
# Helper Functions
# =============================================================================
def get_setting(key: str, default=None):
    """
    Get a setting value by key.
    
    Args:
        key: Setting key
        default: Default value if key not found
        
    Returns:
        Setting value
    """
    return os.getenv(key, default)


def is_debug_mode() -> bool:
    """
    Check if application is running in debug mode.
    
    Returns:
        True if debug mode is enabled
    """
    return os.getenv("DEBUG", "False").lower() == "true"


def validate_config() -> bool:
    """
    Validate configuration settings.
    
    Returns:
        True if configuration is valid
    """
    # Check required directories
    if not LOGS_DIR.exists():
        LOGS_DIR.mkdir(parents=True, exist_ok=True)
    
    if not OUTPUT_DIR.exists():
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Check timeout is positive
    if DEFAULT_TIMEOUT <= 0:
        raise ValueError("DEFAULT_TIMEOUT must be positive")
    
    # Check max results is positive
    if MAX_RESULTS <= 0:
        raise ValueError("MAX_RESULTS must be positive")
    
    return True


# =============================================================================
# Initialize Configuration
# =============================================================================
if __name__ == "__main__":
    print("Validating configuration...")
    if validate_config():
        print("✅ Configuration is valid!")
        print(f"   - Logs Directory: {LOGS_DIR}")
        print(f"   - Output Directory: {OUTPUT_DIR}")
        print(f"   - Default Timeout: {DEFAULT_TIMEOUT}s")
        print(f"   - Max Results: {MAX_RESULTS}")
        print(f"   - Log Level: {LOG_LEVEL}")
