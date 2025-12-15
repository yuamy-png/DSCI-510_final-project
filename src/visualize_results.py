"""visualize_results.py
Creates plots from the analysis outputs saved in the results/ directory.
Produces: top words bar chart, keyword comparison bar chart, sentiment bar chart, PCA scatter.

Usage:
    python src/visualize_results.py --analysis_dir results/ --out_dir results/figures/
"""
import os, argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style='whitegrid')

def plot_top_words(word_freq_path, out_path, top_n=20):
    df = pd.read_csv(word_freq_path)
    top = df.sort_values('count', ascending=False).head(top_n)
    plt.figure(figsize=(8,6))
    sns.barplot(x='count', y='word', data=top, palette='viridis')
    plt.title('Top {} words in corpus'.format(top_n))
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()

def plot_sentiment(article_metrics_path, out_path):
    df = pd.read_csv(article_metrics_path)
    plt.figure(figsize=(8,6))
    sns.barplot(x='sentiment_compound', y='title', data=df.sort_values('sentiment_compound'), palette='coolwarm')
    plt.xlabel('VADER compound sentiment score')
    plt.ylabel('Article Title')
    plt.title('Article-level sentiment scores')
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()

def plot_keyword_counts(article_metrics_path, keywords, out_path):
    df = pd.read_csv(article_metrics_path)
    # compute keyword counts per article (simple substring count)
    kw_df = []
    for _, row in df.iterrows():
        text = str(row['clean_text']).lower()
        counts = {kw: text.count(kw) for kw in keywords}
        counts['title'] = row.get('title','')
        kw_df.append(counts)
    kwdf = pd.DataFrame(kw_df).fillna(0)
    kwdf_melt = kwdf.melt(id_vars=['title'], var_name='keyword', value_name='count')
    plt.figure(figsize=(10,6))
    sns.barplot(data=kwdf_melt, x='keyword', y='count', hue='title')
    plt.title('Keyword counts per article')
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()

def plot_pca_scatter(coords_path, out_path):
    if not os.path.exists(coords_path):
        print('PCA coords file not found; skipping PCA plot.')
        return
    df = pd.read_csv(coords_path)
    plt.figure(figsize=(8,6))
    sns.scatterplot(data=df, x='x', y='y', hue='cluster', palette='deep', s=100)
    for _, row in df.iterrows():
        plt.text(row['x']+0.01, row['y']+0.01, str(row['title'])[:60], fontsize=8)
    plt.title('TF-IDF PCA projection of articles (k-means clusters)')
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()

def main(analysis_dir, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    plot_top_words(os.path.join(analysis_dir,'word_frequency.csv'), os.path.join(out_dir,'top_words.png'))
    plot_sentiment(os.path.join(analysis_dir,'article_metrics.csv'), os.path.join(out_dir,'sentiment_by_article.png'))
    keywords = ['time','late','planning','procrastination','routine','task','delay']
    plot_keyword_counts(os.path.join(analysis_dir,'article_metrics.csv'), keywords, os.path.join(out_dir,'keyword_counts.png'))
    plot_pca_scatter(os.path.join(analysis_dir,'tfidf_pca_coords.csv'), os.path.join(out_dir,'pca_clusters.png'))
    print('Saved figures to', out_dir)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--analysis_dir', type=str, default='results/')
    parser.add_argument('--out_dir', type=str, default='results/figures/')
    args = parser.parse_args()
    main(args.analysis_dir, args.out_dir)
