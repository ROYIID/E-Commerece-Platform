# src/content_recommender.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def prepare_text_features(meta_df):
    """Combine text fields and compute TF-IDF features."""
    # Combine title + description + category into one text field
    meta_df['combined_text'] = (
        meta_df['title'].fillna('') + ' ' +
        meta_df['description'].fillna('') + ' ' +
        meta_df['main_category'].fillna('')
    )

    # Initialize TF-IDF vectorizer
    vectorizer = TfidfVectorizer(
        stop_words='english',
        max_features=5000,   # limit to keep memory low
        ngram_range=(1, 2)   # use unigrams + bigrams
    )

    # Compute TF-IDF matrix
    tfidf_matrix = vectorizer.fit_transform(meta_df['combined_text'])
    print(f"✅ TF-IDF matrix shape: {tfidf_matrix.shape}")
    return tfidf_matrix


def compute_content_similarity(tfidf_matrix):
    """Compute cosine similarity between items."""
    similarity = cosine_similarity(tfidf_matrix, dense_output=False)
    return similarity


def get_similar_items_content(item_index, similarity_matrix, meta_df, top_n=5):
    """Return top-N similar items by content."""
    from numpy import argsort
    sim_scores = similarity_matrix[item_index].toarray().flatten()
    top_indices = argsort(sim_scores)[::-1][1:top_n + 1]
    return meta_df.iloc[top_indices][['title', 'description', 'main_category']]
