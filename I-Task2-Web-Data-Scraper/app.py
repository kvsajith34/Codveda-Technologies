"""
Data Scraper Web Application
Main Streamlit Application
"""

from datetime import datetime
from io import BytesIO
from pathlib import Path

import pandas as pd
import streamlit as st

from scraper import ScrapingType, WebScraper
from utils import format_timestamp, load_history, normalize_url, save_history, setup_logging, validate_url


# ============================================================================
# Page setup
# ============================================================================
st.set_page_config(
    page_title="Data Scraper",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

logger = setup_logging()
OUTPUT_DIR = Path("output")
LOGS_DIR = Path("logs")
OUTPUT_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)


# ============================================================================
# Styling
# ============================================================================
st.markdown(
    """
    <style>
        .main-header {
            font-size: 2.4rem;
            font-weight: 800;
            color: #1f77b4;
            text-align: center;
            margin-bottom: 0.25rem;
        }
        .sub-header {
            font-size: 1rem;
            color: #666;
            text-align: center;
            margin-bottom: 1rem;
        }
        .hint-card {
            padding: 0.9rem 1rem;
            border: 1px solid #e8eef7;
            border-radius: 12px;
            background: #f8fbff;
        }
        .stButton > button {
            width: 100%;
            border-radius: 8px;
            font-weight: 700;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main-header">Data Scraper</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header">• Streamlit Web Scraper</div>',
    unsafe_allow_html=True,
)
st.divider()


# ============================================================================
# Session state
# ============================================================================
if "scraped_data" not in st.session_state:
    st.session_state.scraped_data = None
if "scrape_timestamp" not in st.session_state:
    st.session_state.scrape_timestamp = None
if "scrape_url" not in st.session_state:
    st.session_state.scrape_url = None
if "scrape_notes" not in st.session_state:
    st.session_state.scrape_notes = []


# ============================================================================
# Sidebar
# ============================================================================
with st.sidebar:
    st.header("⚙️ Settings")

    scraping_type_label = st.selectbox(
        "What to scrape?",
        [
            "News Headlines",
            "Product Names & Prices",
            "Article Titles",
            "Job Listings",
            "Blog Posts",
            "Custom (CSS/XPath)",
        ],
    )

    st.subheader("Advanced Options")
    show_advanced = st.checkbox("Show advanced settings", value=False)

    custom_selector = None
    custom_xpath = None
    timeout = 30
    strict_robots = False

    if show_advanced:
        custom_selector = st.text_input(
            "Custom CSS selector",
            placeholder="e.g. .quote, article h2 a, .product_pod",
        )
        custom_xpath = st.text_input(
            "Custom XPath",
            placeholder="e.g. //div[@class='quote']",
        )
        timeout = st.slider("Request timeout (seconds)", 5, 60, 30)
        strict_robots = st.checkbox(
            "Block scraping if robots.txt disallows it",
            value=False,
            help="When off, the app will warn you instead of stopping completely.",
        )

    st.divider()
    st.subheader("🧪 Quick test URLs")
    st.caption("Good starter sites for testing")
    st.markdown(
        """
        - `https://news.ycombinator.com`
        - `http://books.toscrape.com`
        - `http://quotes.toscrape.com`
        - `https://example.com`
        """
    )

    st.divider()
    st.subheader("🕘 Recent Scrapes")
    history = load_history()
    if history:
        for item in history[-5:][::-1]:
            with st.expander(item["url"][:40] + ("..." if len(item["url"]) > 40 else "")):
                st.write(f"**Type:** {item['type']}")
                st.write(f"**Records:** {item['records']}")
                st.write(f"**Time:** {item['timestamp']}")
    else:
        st.info("No scraping history yet")

    if st.button("🗑️ Clear History"):
        save_history([])
        st.rerun()


# ============================================================================
# Main controls
# ============================================================================
st.header("🌐 Enter Website URL")
raw_url = st.text_input("Website URL", placeholder="example.com or https://example.com")
url = normalize_url(raw_url) if raw_url else ""

if raw_url and not validate_url(url):
    st.error("❌ Please enter a valid URL.")

scraping_type_map = {
    "News Headlines": ScrapingType.NEWS,
    "Product Names & Prices": ScrapingType.ECOMMERCE,
    "Article Titles": ScrapingType.ARTICLE,
    "Job Listings": ScrapingType.JOBS,
    "Blog Posts": ScrapingType.BLOG,
    "Custom (CSS/XPath)": ScrapingType.CUSTOM,
}
selected_type = scraping_type_map[scraping_type_label]

with st.expander("💡 Suggested tests", expanded=False):
    st.markdown(
        """
        - **News Headlines:** `https://news.ycombinator.com`
        - **Product Names & Prices:** `http://books.toscrape.com`
        - **Article Titles:** `https://en.wikipedia.org/wiki/Main_Page`
        - **Custom CSS Selector:** `http://quotes.toscrape.com` with selector `.quote`
        - **Custom CSS Selector:** `https://example.com` with selector `h1`
        """
    )

col1, col2 = st.columns([3, 1])
with col1:
    scrape_btn = st.button("🚀 Start Scraping", type="primary", use_container_width=True)
with col2:
    if st.session_state.scraped_data is not None:
        st.metric("Records Found", len(st.session_state.scraped_data))


# ============================================================================
# Scraping action
# ============================================================================
if scrape_btn:
    if not url:
        st.warning("Please enter a URL first.")
    elif not validate_url(url):
        st.warning("Please enter a valid URL first.")
    else:
        progress_bar = st.progress(0)
        status_text = st.empty()

        try:
            with st.spinner("Scraping in progress..."):
                status_text.text("Validating request...")
                progress_bar.progress(10)

                scraper = WebScraper(
                    scraping_type=selected_type,
                    custom_css_selector=custom_selector,
                    custom_xpath=custom_xpath,
                    timeout=timeout,
                    strict_robots=strict_robots,
                )

                status_text.text("Checking robots.txt...")
                progress_bar.progress(25)

                status_text.text("Fetching page content...")
                progress_bar.progress(45)
                data = scraper.scrape(url)

                progress_bar.progress(90)
                status_text.text("Preparing results...")

                st.session_state.scraped_data = data
                st.session_state.scrape_timestamp = datetime.now()
                st.session_state.scrape_url = url
                st.session_state.scrape_notes = []

                robots_status = scraper.last_robots_status
                if robots_status.get("checked") and not robots_status.get("allowed", True) and not strict_robots:
                    st.session_state.scrape_notes.append(
                        "robots.txt may disallow generic bot scraping for this URL. The app continued because strict blocking is off."
                    )
                elif not robots_status.get("checked"):
                    st.session_state.scrape_notes.append(
                        "robots.txt could not be verified for this site, so the app proceeded cautiously."
                    )

                if data:
                    history_entry = {
                        "url": url,
                        "type": scraping_type_label,
                        "records": len(data),
                        "timestamp": format_timestamp(datetime.now()),
                    }
                    history = load_history()
                    history.append(history_entry)
                    save_history(history)

                    logger.info("Successfully scraped %s records from %s", len(data), url)
                    progress_bar.progress(100)
                    status_text.text("Complete")
                    st.success(f"✅ Successfully scraped {len(data)} records.")
                else:
                    logger.warning("No data extracted from %s", url)
                    progress_bar.progress(100)
                    status_text.text("Complete")
                    st.warning("No data was extracted. Try a different scrape type or use a custom selector.")
        except Exception as exc:
            st.session_state.scraped_data = None
            st.session_state.scrape_notes = []
            logger.exception("Scraping failed for %s", url)
            st.error(f"❌ Error: {exc}")
        finally:
            progress_bar.empty()
            status_text.empty()


# ============================================================================
# Results
# ============================================================================
if st.session_state.scrape_notes:
    for note in st.session_state.scrape_notes:
        st.info(note)

if st.session_state.scraped_data is not None:
    st.divider()
    st.header("📊 Scraped Results")

    df = pd.DataFrame(st.session_state.scraped_data)

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Total Records", len(df))
    with m2:
        st.metric("Columns", len(df.columns))
    with m3:
        st.metric(
            "Timestamp",
            st.session_state.scrape_timestamp.strftime("%H:%M:%S") if st.session_state.scrape_timestamp else "N/A",
        )
    with m4:
        st.metric(
            "Source",
            st.session_state.scrape_url[:18] + "..." if st.session_state.scrape_url else "N/A",
        )

    st.subheader("👁️ Preview (First 5 Results)")
    st.dataframe(df.head(5), use_container_width=True, hide_index=True)

    with st.expander("📋 View Full Data"):
        st.dataframe(df, use_container_width=True, hide_index=True)

    st.divider()
    st.header("📥 Export Data")
    export_col1, export_col2, export_col3 = st.columns(3)

    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_filename = f"scraped_data_{timestamp_str}"

    with export_col1:
        csv_data = df.to_csv(index=False)
        st.download_button(
            "Download CSV",
            data=csv_data,
            file_name=f"{base_filename}.csv",
            mime="text/csv",
            use_container_width=True,
        )

    with export_col2:
        json_data = df.to_json(orient="records", indent=2)
        st.download_button(
            "Download JSON",
            data=json_data,
            file_name=f"{base_filename}.json",
            mime="application/json",
            use_container_width=True,
        )

    with export_col3:
        try:
            buffer = BytesIO()
            df.to_excel(buffer, index=False, engine="openpyxl")
            st.download_button(
                "Download Excel",
                data=buffer.getvalue(),
                file_name=f"{base_filename}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )
        except Exception:
            st.info("Install openpyxl to enable Excel export.")

    try:
        save_path = OUTPUT_DIR / f"{base_filename}.csv"
        df.to_csv(save_path, index=False)
        st.caption(f"Saved a CSV copy to `{save_path}`")
    except Exception as exc:
        logger.error("Failed to save CSV locally: %s", exc)


# ============================================================================
# Footer info
# ============================================================================
st.divider()
left, right = st.columns(2)
with left:
    st.markdown(
        """
        **Included Features**
        - Smart extractors for common site types
        - Custom CSS selector and XPath support
        - CSV, JSON, and Excel export
        - Session-based scrape history
        - Logging and basic rate limiting
        """
    )
with right:
    st.markdown(
        """
        **Testing Suggestions**
        - Use `https://news.ycombinator.com` for news
        - Use `http://books.toscrape.com` for products
        - Use `http://quotes.toscrape.com` with `.quote`
        - Use `https://example.com` with `h1`
        """
    )

st.divider()
st.markdown(
    "<div style='text-align:center;color:#666;'>Data Scraper web by KVSA</div>",
    unsafe_allow_html=True,
)
