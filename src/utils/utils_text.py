"""
utils_text.py
Small helper functions for text normalization and tokenization.
"""

"""utils_text.py
Helper text processing utilities used by the analysis pipeline.
"""
import re
from collections import Counter

# Minimal stopword set - expand if needed
STOPWORDS = set([
    "the","and","to","a","in","of","for","is","on","that","with","as",
    "it","are","this","be","by","an","from","or","at","but","not",
    "your","you","we","i","our","they","was","were","has","have","had",
    "will","would","can","could","may","might","also","these","those","which"
])

def clean_text(text: str) -> str:
    if not text:
        return ""
    # Replace common non-breaking spaces and normalize whitespace
    text = text.replace('\xa0', ' ')
    text = re.sub(r'<[^>]+>', ' ', text)  # remove any stray HTML tags
    text = re.sub(r'[^\w\s\-]', ' ', text)  # keep words, whitespace and hyphens
    text = re.sub(r'\s+', ' ', text).strip()
    return text.lower()

def tokenize(text: str):
    if not text:
        return []
    text = clean_text(text)
    tokens = [t for t in text.split() if len(t) > 1 and t not in STOPWORDS]
    return tokens

def word_frequency(tokens):
    return Counter(tokens)
