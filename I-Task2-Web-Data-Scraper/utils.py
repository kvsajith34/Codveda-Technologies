"""
Codveda Technologies - Level 2 Task 2: Data Scraper Web Application
Utility Functions

This module contains helper functions for logging, history management,
URL validation, and other common utilities.

Author: Python Development Intern @ Codveda Technologies
Version: 1.0.0
"""

import logging
import os
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
import re


# ============================================================================
# Logging Configuration
# ============================================================================
def setup_logging(log_dir: str = "logs", log_level: int = logging.INFO) -> logging.Logger:
    """
    Set up logging configuration for the application.
    
    Args:
        log_dir: Directory to store log files
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        
    Returns:
        Logger instance
    """
    # Create logs directory if it doesn't exist
    Path(log_dir).mkdir(exist_ok=True)
    
    # Create logger
    logger = logging.getLogger("DataScraper")
    logger.setLevel(log_level)
    
    # Clear existing handlers
    logger.handlers = []
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File handler - rotates daily
    from logging.handlers import TimedRotatingFileHandler
    file_handler = TimedRotatingFileHandler(
        filename=os.path.join(log_dir, "scraper.log"),
        when='D',
        interval=1,
        backupCount=7
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)  # Only show warnings+ in console
    console_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


# ============================================================================
# History Management
# ============================================================================
HISTORY_FILE = "scraping_history.json"


def load_history() -> List[Dict[str, Any]]:
    """
    Load scraping history from JSON file.
    
    Returns:
        List of history entries
    """
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        logging.error(f"Failed to load history: {e}")
    
    return []


def save_history(history: List[Dict[str, Any]]) -> bool:
    """
    Save scraping history to JSON file.
    
    Args:
        history: List of history entries
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Keep only last 50 entries
        history = history[-50:]
        
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
        
        return True
    except IOError as e:
        logging.error(f"Failed to save history: {e}")
        return False


def add_history_entry(url: str, scraping_type: str, records: int) -> bool:
    """
    Add a new entry to scraping history.
    
    Args:
        url: Scraped URL
        scraping_type: Type of scraping performed
        records: Number of records extracted
        
    Returns:
        True if successful
    """
    history = load_history()
    
    entry = {
        "url": url,
        "type": scraping_type,
        "records": records,
        "timestamp": format_timestamp(datetime.now())
    }
    
    history.append(entry)
    return save_history(history)


# ============================================================================
# URL Validation
# ============================================================================
def validate_url(url: str) -> bool:
    """
    Validate if a string is a valid URL.
    
    Args:
        url: URL string to validate
        
    Returns:
        True if valid URL, False otherwise
    """
    # Basic URL pattern
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # or IP
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return bool(url_pattern.match(url))


def normalize_url(url: str) -> str:
    """
    Normalize URL by adding https:// if missing.
    
    Args:
        url: URL string
        
    Returns:
        Normalized URL
    """
    url = url.strip()
    
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    return url


def extract_domain(url: str) -> str:
    """
    Extract domain name from URL.
    
    Args:
        url: Full URL
        
    Returns:
        Domain name
    """
    try:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        return parsed.netloc
    except Exception:
        return "unknown"


# ============================================================================
# Date/Time Utilities
# ============================================================================
def format_timestamp(dt: datetime) -> str:
    """
    Format datetime object to readable string.
    
    Args:
        dt: Datetime object
        
    Returns:
        Formatted string
    """
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def parse_date(date_string: str) -> Optional[datetime]:
    """
    Parse various date formats.
    
    Args:
        date_string: Date string in various formats
        
    Returns:
        Datetime object or None
    """
    formats = [
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%d-%m-%Y",
        "%d/%m/%Y",
        "%B %d, %Y",
        "%b %d, %Y",
        "%Y-%m-%d %H:%M:%S",
        "%Y/%m/%d %H:%M:%S",
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_string, fmt)
        except ValueError:
            continue
    
    return None


# ============================================================================
# Data Processing Utilities
# ============================================================================
def clean_text(text: str) -> str:
    """
    Clean and normalize text content.
    
    Args:
        text: Raw text
        
    Returns:
        Cleaned text
    """
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters (optional)
    # text = re.sub(r'[^\w\s\-\.,]', '', text)
    
    return text.strip()


def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Truncate text to maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - 3] + "..."


def extract_price(price_string: str) -> Optional[float]:
    """
    Extract numeric price from string.
    
    Args:
        price_string: String containing price
        
    Returns:
        Float price or None
    """
    if not price_string:
        return None
    
    # Remove currency symbols and commas
    cleaned = re.sub(r'[^\d\.]', '', price_string)
    
    try:
        return float(cleaned)
    except ValueError:
        return None


# ============================================================================
# File Utilities
# ============================================================================
def ensure_directory(path: str) -> bool:
    """
    Ensure directory exists, create if not.
    
    Args:
        path: Directory path
        
    Returns:
        True if successful
    """
    try:
        Path(path).mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        logging.error(f"Failed to create directory {path}: {e}")
        return False


def get_file_size(file_path: str) -> int:
    """
    Get file size in bytes.
    
    Args:
        file_path: Path to file
        
    Returns:
        File size in bytes
    """
    try:
        return os.path.getsize(file_path)
    except OSError:
        return 0


def format_file_size(size_bytes: int) -> str:
    """
    Format file size to human-readable string.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted size string
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    
    return f"{size_bytes:.2f} TB"


# ============================================================================
# Rate Limiting Utilities
# ============================================================================
class RateLimiter:
    """
    Simple rate limiter to prevent overwhelming servers.
    """
    
    def __init__(self, requests_per_second: float = 1.0):
        """
        Initialize rate limiter.
        
        Args:
            requests_per_second: Maximum requests per second
        """
        self.requests_per_second = requests_per_second
        self.min_interval = 1.0 / requests_per_second
        self.last_request_time = 0
    
    def wait(self):
        """Wait if necessary to respect rate limit"""
        import time
        
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_interval:
            sleep_time = self.min_interval - time_since_last
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()


# ============================================================================
# Error Handling Utilities
# ============================================================================
class ScrapingError(Exception):
    """Custom exception for scraping errors"""
    pass


class URLValidationError(ScrapingError):
    """Exception for invalid URLs"""
    pass


class ContentExtractionError(ScrapingError):
    """Exception for content extraction failures"""
    pass


def safe_get(dictionary: dict, key: str, default: Any = None) -> Any:
    """
    Safely get value from dictionary.
    
    Args:
        dictionary: Dictionary to search
        key: Key to look for
        default: Default value if key not found
        
    Returns:
        Value or default
    """
    try:
        return dictionary.get(key, default)
    except Exception:
        return default


# ============================================================================
# Testing Utilities
# ============================================================================
def test_utils():
    """Run basic tests on utility functions"""
    print("Testing utility functions...")
    
    # Test URL validation
    assert validate_url("https://example.com") == True
    assert validate_url("http://test.org/path") == True
    assert validate_url("not-a-url") == False
    
    # Test text cleaning
    assert clean_text("  hello   world  ") == "hello world"
    
    # Test timestamp formatting
    ts = format_timestamp(datetime.now())
    assert len(ts) > 0
    
    print("All utility tests passed!")


if __name__ == "__main__":
    test_utils()
