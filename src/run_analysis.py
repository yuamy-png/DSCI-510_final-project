"""run_analysis.py
Analysis pipeline: loads cleaned articles, computes word frequencies, TF-IDF, VADER sentiment,
and performs a small KMeans clustering on TF-IDF vectors.
Outputs CSV summaries into the results/ directory.

Usage:
    python src/run_analysis.py --in_path data/processed/cleaned_articles.csv --out_dir results/ --k 2
"""
import os, argparse
import pandas as pd
from collections import Counter
from utils_text import clean_text, tokenize, word_frequency
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

def compute_word_freqs(texts, top_n=50):
    counter = Counter()
    for t in texts:
        toks = tokenize(t)
        counter.update(toks)
    most = counter.most_common(top_n)
    return pd.DataFrame(most, columns=['word','count'])

def compute_sentiment(texts):
    analyzer = SentimentIntensityAnalyzer()
    scores = [analyzer.polarity_scores(t)['compound'] for t in texts]
    return scores

def main(in_path, out_dir, k_clusters):
    os.makedirs(out_dir, exist_ok=True)
    df = pd.read_csv(in_path)
    # ensure text column exists
    if 'text' not in df.columns:
        raise ValueError('Input CSV must contain a "text" column.')

    # Basic article-level metrics
    df['clean_text'] = df['text'].fillna('').apply(clean_text)
    df['word_count'] = df['clean_text'].apply(lambda s: len(tokenize(s)))
    df['sentiment_compound'] = compute_sentiment(df['clean_text'].tolist())

    # Save article metrics
    article_metrics_path = os.path.join(out_dir, 'article_metrics.csv')
    df.to_csv(article_metrics_path, index=False)

    # Word frequencies
    wf = compute_word_freqs(df['clean_text'].tolist(), top_n=200)
    wf.to_csv(os.path.join(out_dir, 'word_frequency.csv'), index=False)

    # TF-IDF and KMeans clustering (small k)
    vectorizer = TfidfVectorizer(max_df=0.85, min_df=1, ngram_range=(1,2))
    tfidf = vectorizer.fit_transform(df['clean_text'].tolist())

    if tfidf.shape[0] >= k_clusters and k_clusters > 0:
        km = KMeans(n_clusters=k_clusters, random_state=42, n_init=10)
        labels = km.fit_predict(tfidf)
        df['cluster'] = labels
        # Save cluster assignments
        df[['title','url','cluster']].to_csv(os.path.join(out_dir,'article_clusters.csv'), index=False)
        # PCA for 2D projection (for visualization)
        pca = PCA(n_components=2, random_state=42)
        coords = pca.fit_transform(tfidf.toarray())
        coords_df = pd.DataFrame(coords, columns=['x','y'])
        coords_df['title'] = df['title'].values
        coords_df['cluster'] = labels
        coords_df.to_csv(os.path.join(out_dir,'tfidf_pca_coords.csv'), index=False)
    else:
        print('Skipping clustering: not enough samples for k=', k_clusters)

    print('Analysis outputs saved to', out_dir)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--in_path', type=str, default='data/processed/cleaned_articles.csv')
    parser.add_argument('--out_dir', type=str, default='results/')
    parser.add_argument('--k', type=int, default=2, help='number of clusters for KMeans')
    args = parser.parse_args()
    main(args.in_path, args.out_dir, args.k)