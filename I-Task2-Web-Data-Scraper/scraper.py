"""
Codveda Technologies - Level 2 Task 2: Data Scraper Web Application
Core Scraping Engine

This module contains the WebScraper class that handles all scraping logic.
It includes smart default extractors for common website types and supports
custom CSS/XPath selectors for advanced users.
"""

from __future__ import annotations

import logging
import random
import re
import time
from enum import Enum
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup, Tag
from lxml import html as lxml_html


# ============================================================================
# Enums and Constants
# ============================================================================
class ScrapingType(Enum):
    """Enumeration of supported scraping types."""

    NEWS = "news"
    ECOMMERCE = "ecommerce"
    ARTICLE = "article"
    JOBS = "jobs"
    BLOG = "blog"
    CUSTOM = "custom"


USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
]

DEFAULT_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Cache-Control": "max-age=0",
}


# ============================================================================
# Web Scraper Class
# ============================================================================
class WebScraper:
    """Main web scraper class."""

    def __init__(
        self,
        scraping_type: ScrapingType = ScrapingType.NEWS,
        custom_css_selector: Optional[str] = None,
        custom_xpath: Optional[str] = None,
        timeout: int = 30,
        strict_robots: bool = False,
    ):
        self.scraping_type = scraping_type
        self.custom_css_selector = (custom_css_selector or "").strip() or None
        self.custom_xpath = (custom_xpath or "").strip() or None
        self.timeout = timeout
        self.strict_robots = strict_robots
        self.session = requests.Session()
        self.logger = logging.getLogger("DataScraper")
        self._last_request_time = 0.0
        self._min_request_interval = 1.0
        self.last_robots_status: Dict[str, Any] = {
            "checked": False,
            "allowed": True,
            "message": "robots.txt not checked yet",
            "robots_url": None,
        }

        self.session.headers.update(DEFAULT_HEADERS)
        self._rotate_user_agent()

    # ----------------------------------------------------------------------
    # Internal helpers
    # ----------------------------------------------------------------------
    def _rotate_user_agent(self) -> None:
        self.session.headers["User-Agent"] = random.choice(USER_AGENTS)

    def _rate_limit(self) -> None:
        current_time = time.time()
        elapsed = current_time - self._last_request_time
        if elapsed < self._min_request_interval:
            time.sleep(self._min_request_interval - elapsed)
        self._last_request_time = time.time()

    def _selector_string(self, selectors: Any) -> str:
        if isinstance(selectors, str):
            return selectors
        if isinstance(selectors, (list, tuple, set)):
            return ", ".join(str(selector) for selector in selectors if selector)
        return str(selectors)

    def _select(self, node: Tag | BeautifulSoup, selectors: Any) -> List[Tag]:
        selector = self._selector_string(selectors)
        if not selector:
            return []
        return node.select(selector)

    def _select_one(self, node: Tag | BeautifulSoup, selectors: Any) -> Optional[Tag]:
        selector = self._selector_string(selectors)
        if not selector:
            return None
        return node.select_one(selector)

    def _clean_text(self, text: str) -> str:
        return re.sub(r"\s+", " ", text or "").strip()

    def _text_of(self, node: Any) -> str:
        if node is None:
            return ""
        if hasattr(node, "get_text"):
            return self._clean_text(node.get_text(" ", strip=True))
        return self._clean_text(str(node))

    def _attr_of(self, node: Optional[Tag], *attrs: str) -> str:
        if not node:
            return ""
        for attr in attrs:
            value = node.get(attr)
            if value:
                return str(value).strip()
        return ""

    def _absolute_url(self, base_url: str, maybe_url: str) -> str:
        if not maybe_url:
            return base_url
        return urljoin(base_url, maybe_url)

    def _first_non_empty(self, *values: str) -> str:
        for value in values:
            cleaned = self._clean_text(value)
            if cleaned:
                return cleaned
        return ""

    def _find_nearby_text(self, node: Optional[Tag], selectors: Any) -> str:
        if not node:
            return ""

        candidates: List[Optional[Tag]] = [node]
        if node.parent and isinstance(node.parent, Tag):
            candidates.append(node.parent)
        if node.find_parent() and isinstance(node.find_parent(), Tag):
            candidates.append(node.find_parent())
        article_parent = node.find_parent(["article", "li", "div", "tr"])
        if article_parent and isinstance(article_parent, Tag):
            candidates.append(article_parent)

        seen_ids = set()
        for candidate in candidates:
            if not candidate:
                continue
            if id(candidate) in seen_ids:
                continue
            seen_ids.add(id(candidate))
            found = self._select_one(candidate, selectors)
            text = self._text_of(found)
            if text:
                return text
        return ""

    def _deduplicate(self, rows: List[Dict[str, Any]], key_fields: List[str]) -> List[Dict[str, Any]]:
        unique_rows: List[Dict[str, Any]] = []
        seen = set()
        for row in rows:
            key = tuple(self._clean_text(str(row.get(field, ""))).lower() for field in key_fields)
            if not any(key):
                continue
            if key in seen:
                continue
            seen.add(key)
            unique_rows.append(row)
        return unique_rows

    def _extract_rating(self, container: Tag) -> str:
        rating_elem = self._select_one(
            container,
            [".rating", ".stars", "[data-rating]", ".star-rating", "p.star-rating"],
        )
        if not rating_elem:
            return "N/A"

        data_rating = self._attr_of(rating_elem, "data-rating", "aria-label", "title")
        if data_rating:
            return data_rating

        classes = rating_elem.get("class", [])
        if isinstance(classes, list):
            rating_words = [cls for cls in classes if cls.lower() not in {"rating", "stars", "star-rating"}]
            if rating_words:
                return " ".join(rating_words)

        return self._text_of(rating_elem) or "N/A"

    def _generic_heading_fallback(self, soup: BeautifulSoup, url: str) -> List[Dict[str, Any]]:
        rows: List[Dict[str, Any]] = []
        for elem in self._select(soup, ["h1", "h2", "h3", "h4", "a[href]"]):
            text = self._text_of(elem)
            if len(text) < 8:
                continue
            href = ""
            if isinstance(elem, Tag):
                if elem.name == "a":
                    href = self._attr_of(elem, "href")
                else:
                    link = elem.find("a", href=True)
                    href = link.get("href", "") if link else ""
            rows.append(
                {
                    "title": text,
                    "link": self._absolute_url(url, href),
                    "source": url,
                }
            )
        return self._deduplicate(rows, ["title", "link"])[:50]

    # ----------------------------------------------------------------------
    # robots.txt and fetching
    # ----------------------------------------------------------------------
    def _check_robots_txt(self, url: str) -> Dict[str, Any]:
        parsed = urlparse(url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        parser = RobotFileParser()
        parser.set_url(robots_url)

        try:
            response = self.session.get(robots_url, timeout=10)
            if response.status_code == 200 and response.text.strip():
                parser.parse(response.text.splitlines())
                allowed = parser.can_fetch("*", url)
                self.last_robots_status = {
                    "checked": True,
                    "allowed": allowed,
                    "message": "robots.txt allows scraping" if allowed else "robots.txt may disallow scraping for generic bots",
                    "robots_url": robots_url,
                }
            else:
                self.last_robots_status = {
                    "checked": True,
                    "allowed": True,
                    "message": f"robots.txt not available (status {response.status_code}), proceeding cautiously",
                    "robots_url": robots_url,
                }
        except Exception as exc:
            self.last_robots_status = {
                "checked": False,
                "allowed": True,
                "message": f"Could not verify robots.txt: {exc}",
                "robots_url": robots_url,
            }

        return self.last_robots_status

    def fetch_page(self, url: str) -> str:
        if not url.startswith(("http://", "https://")):
            raise ValueError("URL must start with http:// or https://")

        self._rate_limit()
        self._rotate_user_agent()

        try:
            response = self.session.get(url, timeout=self.timeout, allow_redirects=True)
        except requests.Timeout as exc:
            raise requests.RequestException("Request timed out. Try increasing the timeout.") from exc
        except requests.RequestException as exc:
            raise requests.RequestException(f"Failed to fetch page: {exc}") from exc

        if response.status_code == 403:
            raise requests.RequestException("Access forbidden (403). Website may be blocking scrapers.")
        if response.status_code == 404:
            raise requests.RequestException("Page not found (404).")
        if response.status_code >= 500:
            raise requests.RequestException(f"Server error ({response.status_code}). Try again later.")
        if response.status_code != 200:
            raise requests.RequestException(f"Unexpected status code: {response.status_code}")

        response.encoding = response.encoding or response.apparent_encoding or "utf-8"
        return response.text

    def parse_html(self, html: str) -> BeautifulSoup:
        return BeautifulSoup(html, "lxml")

    # ----------------------------------------------------------------------
    # Extractors
    # ----------------------------------------------------------------------
    def extract_news(self, soup: BeautifulSoup, url: str) -> List[Dict[str, Any]]:
        rows: List[Dict[str, Any]] = []
        selectors = [
            "span.titleline > a",          # Hacker News
            "a.storylink",                 # older Hacker News markup
            "[data-testid='card-headline']",  # BBC-like cards
            "h1 a",
            "h2 a",
            "h3 a",
            "article h1",
            "article h2",
            "article h3",
            ".headline",
            ".article-title",
            ".title",
            "h1",
            "h2",
            "h3",
        ]

        for elem in self._select(soup, selectors):
            title = self._text_of(elem)
            if len(title) < 8:
                continue

            href = ""
            if elem.name == "a":
                href = self._attr_of(elem, "href")
            else:
                nested_link = elem.find("a", href=True)
                href = nested_link.get("href", "") if nested_link else ""

            date_text = self._find_nearby_text(elem, ["time", ".date", ".published", ".timestamp", ".age"])

            rows.append(
                {
                    "title": title,
                    "link": self._absolute_url(url, href),
                    "date": date_text,
                    "source": url,
                }
            )

        rows = self._deduplicate(rows, ["title", "link"])
        return rows[:50] if rows else self._generic_heading_fallback(soup, url)

    def extract_ecommerce(self, soup: BeautifulSoup, url: str) -> List[Dict[str, Any]]:
        rows: List[Dict[str, Any]] = []
        containers = self._select(
            soup,
            [
                "article.product_pod",   # books.toscrape.com
                ".product_pod",
                ".product",
                ".product-item",
                ".product-card",
                ".thumbnail",
                "[data-product]",
                ".listing",
            ],
        )

        if not containers:
            price_nodes = self._select(soup, [".price_color", ".price", ".product-price", "[data-price]", ".cost"])
            for price_node in price_nodes[:50]:
                container = price_node.find_parent(["article", "div", "li", "section"])
                if not container:
                    continue
                containers.append(container)

        seen_container_ids = set()
        unique_containers: List[Tag] = []
        for container in containers:
            if id(container) in seen_container_ids:
                continue
            seen_container_ids.add(id(container))
            unique_containers.append(container)

        for container in unique_containers[:50]:
            name_elem = self._select_one(
                container,
                ["h3 a", ".product-name", ".product-title", "h3", "h4", "a[title]"],
            )
            name = self._first_non_empty(
                self._attr_of(name_elem, "title", "aria-label"),
                self._text_of(name_elem),
            )
            if len(name) < 2:
                continue

            price_elem = self._select_one(
                container,
                [".price_color", ".price", ".product-price", "[data-price]", ".cost"],
            )
            price = self._first_non_empty(self._text_of(price_elem), "N/A")

            rating = self._extract_rating(container)

            img_elem = self._select_one(container, ["img"])
            image_url = self._absolute_url(url, self._attr_of(img_elem, "src", "data-src", "data-original"))

            link_elem = self._select_one(container, ["h3 a[href]", "a[href]"])
            product_url = self._absolute_url(url, self._attr_of(link_elem, "href"))

            rows.append(
                {
                    "product_name": name,
                    "price": price,
                    "rating": rating,
                    "image_url": image_url,
                    "product_url": product_url,
                    "source": url,
                }
            )

        rows = self._deduplicate(rows, ["product_name", "product_url"])
        return rows[:50]

    def extract_article(self, soup: BeautifulSoup, url: str) -> List[Dict[str, Any]]:
        rows: List[Dict[str, Any]] = []
        article_nodes = self._select(soup, ["article", ".article", ".post", ".blog-post", "[data-article]"])

        if article_nodes:
            for article in article_nodes[:30]:
                title_elem = self._select_one(article, ["h1", "h2", "h3", ".article-title", ".post-title", ".title"])
                title = self._text_of(title_elem)
                if len(title) < 5:
                    continue

                author = self._find_nearby_text(article, [".author", ".byline", "[data-author]", ".post-author"])
                date = self._find_nearby_text(article, ["time", ".date", ".published", "[data-date]", ".post-date"])
                content_elem = self._select_one(article, [".content", ".post-content", ".article-body", "p"])
                preview = self._text_of(content_elem)[:220]

                link_elem = self._select_one(article, ["h1 a[href]", "h2 a[href]", "h3 a[href]", "a[href]"])
                link = self._absolute_url(url, self._attr_of(link_elem, "href"))

                rows.append(
                    {
                        "title": title,
                        "author": author or "Unknown",
                        "date": date,
                        "preview": preview,
                        "url": link,
                        "source": url,
                    }
                )
        else:
            main = soup.find("main") or soup.find("body") or soup
            headings = self._select(main, ["h1", "h2", "h3", ".mw-headline"])
            meta_author = ""
            author_meta = soup.find("meta", attrs={"name": re.compile(r"author", re.I)})
            if author_meta:
                meta_author = self._attr_of(author_meta, "content")

            for heading in headings[:50]:
                title = self._text_of(heading)
                if len(title) < 5:
                    continue
                link_elem = heading if heading.name == "a" else heading.find("a", href=True)
                link = self._absolute_url(url, link_elem.get("href", "") if link_elem else "")
                date = self._find_nearby_text(heading, ["time", ".date", ".published", ".timestamp"])
                rows.append(
                    {
                        "title": title,
                        "author": meta_author or "Unknown",
                        "date": date,
                        "preview": "",
                        "url": link,
                        "source": url,
                    }
                )

        rows = self._deduplicate(rows, ["title", "url"])
        return rows[:50] if rows else self._generic_heading_fallback(soup, url)

    def extract_jobs(self, soup: BeautifulSoup, url: str) -> List[Dict[str, Any]]:
        rows: List[Dict[str, Any]] = []
        containers = self._select(
            soup,
            [
                "tr.job",
                "tr[data-id]",
                ".job",
                ".job-listing",
                ".job-post",
                ".job-item",
                "[data-job]",
                ".career-item",
                ".position",
                "article",
                "li",
            ],
        )

        job_keywords = {"job", "position", "role", "hiring", "career", "apply", "full-time", "part-time", "remote"}

        for container in containers[:80]:
            text = self._text_of(container)
            has_keyword = any(keyword in text.lower() for keyword in job_keywords)
            title_elem = self._select_one(
                container,
                [
                    "h2",
                    "h3",
                    "h4",
                    ".job-title",
                    ".position-title",
                    "a[href*='/remote-jobs/']",
                    "a.preventLink",
                    "td.company_and_position a",
                    "a[href]",
                ],
            )
            title = self._text_of(title_elem)

            if len(title) < 5 and not has_keyword:
                continue
            if not title:
                title = text[:120]

            location = self._find_nearby_text(container, [".location", ".job-location", "[data-location]", ".companyLocation"])
            job_type = self._find_nearby_text(container, [".job-type", ".employment-type", "[data-type]"])
            link = self._absolute_url(url, self._attr_of(title_elem, "href"))

            rows.append(
                {
                    "title": title,
                    "location": location or "Not specified",
                    "type": job_type or "Not specified",
                    "description": text[:220],
                    "url": link,
                    "source": url,
                }
            )

        rows = self._deduplicate(rows, ["title", "url"])
        return rows[:50] if rows else self._generic_heading_fallback(soup, url)

    def extract_blog(self, soup: BeautifulSoup, url: str) -> List[Dict[str, Any]]:
        rows: List[Dict[str, Any]] = []
        containers = self._select(
            soup,
            [
                "article",
                ".crayons-story",
                ".blog-post",
                ".post",
                ".blog-item",
                ".story",
            ],
        )

        if not containers:
            containers = self._select(soup, ["h2", "h3"])

        for container in containers[:60]:
            title_elem = self._select_one(
                container,
                ["h2 a", "h3 a", ".post-title a", ".crayons-story__title a", "h2", "h3"],
            )

            if title_elem is None and isinstance(container, Tag) and container.name in {"h2", "h3"}:
                title_elem = container

            title = self._text_of(title_elem)
            if len(title) < 5:
                continue

            if title_elem and getattr(title_elem, "name", "") == "a":
                link = self._absolute_url(url, self._attr_of(title_elem, "href"))
            else:
                nested_link = container.find("a", href=True) if isinstance(container, Tag) else None
                link = self._absolute_url(url, nested_link.get("href", "") if nested_link else "")

            date = self._find_nearby_text(container, ["time", ".date", ".published", ".posted-at"])

            rows.append(
                {
                    "title": title,
                    "link": link,
                    "date": date,
                    "source": url,
                }
            )

        rows = self._deduplicate(rows, ["title", "link"])
        return rows[:50] if rows else self._generic_heading_fallback(soup, url)

    def extract_custom(self, soup: BeautifulSoup, url: str) -> List[Dict[str, Any]]:
        rows: List[Dict[str, Any]] = []

        if self.custom_css_selector:
            elements = self._select(soup, self.custom_css_selector)
            for elem in elements[:100]:
                text = self._text_of(elem)
                href = self._attr_of(elem, "href")
                src = self._attr_of(elem, "src", "data-src")
                if not text and not href and not src:
                    continue
                rows.append(
                    {
                        "element": text,
                        "tag": getattr(elem, "name", ""),
                        "href": self._absolute_url(url, href) if href else "",
                        "src": self._absolute_url(url, src) if src else "",
                        "html": str(elem)[:250],
                        "source": url,
                    }
                )
            return rows

        if self.custom_xpath:
            try:
                tree = lxml_html.fromstring(str(soup))
                matches = tree.xpath(self.custom_xpath)
                for item in matches[:100]:
                    if hasattr(item, "text_content"):
                        text = self._clean_text(item.text_content())
                        tag = getattr(item, "tag", "")
                        href = item.get("href", "") if hasattr(item, "get") else ""
                        src = item.get("src", "") if hasattr(item, "get") else ""
                        rows.append(
                            {
                                "element": text,
                                "tag": str(tag),
                                "href": self._absolute_url(url, href) if href else "",
                                "src": self._absolute_url(url, src) if src else "",
                                "html": lxml_html.tostring(item, encoding="unicode")[:250],
                                "source": url,
                            }
                        )
                    else:
                        rows.append(
                            {
                                "element": self._clean_text(str(item)),
                                "tag": "value",
                                "href": "",
                                "src": "",
                                "html": self._clean_text(str(item))[:250],
                                "source": url,
                            }
                        )
                return rows
            except Exception as exc:
                return [
                    {
                        "element": "",
                        "tag": "error",
                        "href": "",
                        "src": "",
                        "html": f"Invalid XPath or XPath extraction failed: {exc}",
                        "source": url,
                    }
                ]

        links = soup.find_all("a", href=True)
        for link in links[:50]:
            text = self._text_of(link)
            if not text:
                continue
            rows.append(
                {
                    "element": text,
                    "tag": "a",
                    "href": self._absolute_url(url, link.get("href", "")),
                    "src": "",
                    "html": str(link)[:250],
                    "source": url,
                }
            )
        return rows

    # ----------------------------------------------------------------------
    # Public API
    # ----------------------------------------------------------------------
    def scrape(self, url: str) -> List[Dict[str, Any]]:
        robots_status = self._check_robots_txt(url)
        if self.strict_robots and not robots_status.get("allowed", True):
            raise PermissionError("Scraping may be disallowed by robots.txt")

        html = self.fetch_page(url)
        if not html:
            raise ValueError("Failed to fetch page content")

        soup = self.parse_html(html)

        extraction_methods = {
            ScrapingType.NEWS: self.extract_news,
            ScrapingType.ECOMMERCE: self.extract_ecommerce,
            ScrapingType.ARTICLE: self.extract_article,
            ScrapingType.JOBS: self.extract_jobs,
            ScrapingType.BLOG: self.extract_blog,
            ScrapingType.CUSTOM: self.extract_custom,
        }

        extractor = extraction_methods.get(self.scraping_type, self.extract_custom)
        data = extractor(soup, url)

        if not data and self.scraping_type != ScrapingType.CUSTOM:
            data = self._generic_heading_fallback(soup, url)

        return data

    def __del__(self):
        try:
            self.session.close()
        except Exception:
            pass


# ============================================================================
# Standalone Function for Testing
# ============================================================================
def quick_scrape(url: str, scraping_type: str = "news") -> List[Dict[str, Any]]:
    type_map = {
        "news": ScrapingType.NEWS,
        "ecommerce": ScrapingType.ECOMMERCE,
        "article": ScrapingType.ARTICLE,
        "jobs": ScrapingType.JOBS,
        "blog": ScrapingType.BLOG,
        "custom": ScrapingType.CUSTOM,
    }
    scraper = WebScraper(scraping_type=type_map.get(scraping_type, ScrapingType.NEWS))
    return scraper.scrape(url)


if __name__ == "__main__":
    print("WebScraper module loaded successfully!")
