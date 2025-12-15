"""
clean_data.py
Cleans raw scraped article data and produces a structured CSV.

Usage:
    python src/clean_data.py
"""

import json
import os
import pandas as pd
import re

RAW_PATH = "data/raw/collected_raw.json"
OUT_DIR = "data/processed/"
os.makedirs(OUT_DIR, exist_ok=True)

def strip_html_artifacts(text: str) -> str:
    """Remove leftover HTML-like artifacts or repeated whitespace."""
    if not text:
        return ""
    text = re.sub(r"\s+", " ", text)  # normalize whitespace
    text = re.sub(r"<[^>]+>", " ", text)  # remove HTML tags if any appear
    return text.strip()

def main():
    # Load raw JSON
    with open(RAW_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    cleaned_records = []

    for art in data.get("articles", []):
        text = strip_html_artifacts(art.get("text", ""))
        title = strip_html_artifacts(art.get("title", ""))
        date = art.get("date", None)
        url = art.get("url", "")

        # Skip extremely short articles (scraper failed)
        if len(text) < 100:
            continue

        cleaned_records.append({
            "url": url,
            "title": title,
            "date": date,
            "text": text
        })

    # Convert to DataFrame
    df = pd.DataFrame(cleaned_records)

    # Save cleaned CSV
    out_path = os.path.join(OUT_DIR, "cleaned_articles.csv")
    df.to_csv(out_path, index=False)

    print(f"Cleaned dataset saved to: {out_path}")
    print(f"Total cleaned articles: {len(df)}")

if __name__ == "__main__":
    main()