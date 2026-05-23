import time
from datetime import datetime

from playwright.sync_api import sync_playwright


def get_article_links(page, category_url):
    page.goto(category_url, wait_until="domcontentloaded")
    time.sleep(2)

    print("SCRAPING LIST ITEMS")

    headlines = page.locator('.sumry-body')

    links = []
    for headline in headlines.element_handles():
        link = headline.query_selector("h3 a")
        if not link:
            continue
        links.append({
            'Title': link.inner_text(),
            'URL': link.get_attribute("href"),
        })
    return links


DEFAULT_CATEGORIES = [
    'https://www.channelstv.com/category/politics/',
    'https://www.channelstv.com/category/sports/',
    'https://www.channelstv.com/category/crime-watch/',
]


def scrape_channels(save_callback=None, categories=None):
    if categories is None:
        categories = DEFAULT_CATEGORIES

    with sync_playwright() as pw:
        browser = pw.chromium.launch(
            headless=False,
        )
        page = browser.new_page()

        for category_url in categories:
            print(f"\n=== CATEGORY: {category_url} ===")
            links = get_article_links(page, category_url)

            for job in links:
                print(f"  SCRAPING {job['Title']}")

                try:
                    page.goto(job['URL'], wait_until="domcontentloaded", timeout=30000)
                except Exception as e:
                    print(f"  SKIPPED (load failed): {e}")
                    continue

                time.sleep(2)

                item = {
                    "Title": job['Title'],
                    "URL": job["URL"],
                    "Content": "",
                    "Published_at": None,
                    "Source": category_url,
                }

                content_elem = page.query_selector(".detail-grid")
                if content_elem:
                    item["Content"] = content_elem.inner_text()

                time_meta = page.query_selector('meta[property="article:published_time"]')
                if time_meta:
                    raw = time_meta.get_attribute("content")
                    try:
                        item["Published_at"] = datetime.fromisoformat(raw)
                    except ValueError:
                        pass

                if save_callback:
                    try:
                        save_callback(item)
                    except Exception as e:
                        print(f"    SKIPPED (save failed): {e}")

        browser.close()
