"""
get_data.py (revised with verified URLs)
Scrapes expert-written ADHD + time blindness / time management articles.
Usage:
    python src/get_data.py --out_dir data/raw/
"""

import os
import json
import argparse
import requests
from bs4 import BeautifulSoup

ARTICLE_URLS = [
    "https://www.additudemag.com/how-to-plan-ahead-when-you-have-adhd-understand-time/",
    "https://www.additudemag.com/slideshows/stop-wasting-time/",
    "https://www.additudemag.com/time-on-your-side/",
    "https://psychcentral.com/adhd/why-are-people-with-adhd-always-late",
    "https://psychcentral.com/adhd/time-management-tips-for-people-with-adhd",
    "https://psychcentral.com/adhd/the-adhd-iceberg"
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/116.0 Safari/537.36"
    )
}

def scrape_article(url: str):
    resp = requests.get(url, timeout=30, headers=HEADERS)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    title = soup.title.string.strip() if soup.title else url

    date = None
    time_tag = soup.find("time")
    if time_tag and time_tag.has_attr("datetime"):
        date = time_tag["datetime"]
    elif time_tag:
        date = time_tag.get_text(strip=True)

    main = soup.find("article") or soup.find("main") or soup
    paragraphs = [p.get_text(strip=True) for p in main.find_all("p")]
    text = "\n\n".join(p for p in paragraphs if p)

    return {"url": url, "title": title, "date": date, "text": text}

def main(out_dir: str):
    os.makedirs(out_dir, exist_ok=True)
    collected = {"articles": []}

    for url in ARTICLE_URLS:
        try:
            article = scrape_article(url)
            collected["articles"].append(article)
            print(f"✓ Scraped: {url}")
        except Exception as e:
            print(f"✗ Failed to scrape {url}: {e}")

    out_path = os.path.join(out_dir, "collected_raw.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(collected, f, ensure_ascii=False, indent=2)
    print("Saved collected data to:", out_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out_dir", type=str, default="data/raw/")
    args = parser.parse_args()
    main(args.out_dir)