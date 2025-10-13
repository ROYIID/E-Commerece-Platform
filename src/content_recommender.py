# src/content_recommender.py
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import csr_matrix
from sklearn.preprocessing import normalize


def prepare_text_features(meta_df, max_features=2000):
    """Combine text fields and compute normalized sparse TF-IDF matrix."""
    print("🔧 Preparing TF-IDF features...")

    # Combine textual fields
    meta_df['combined_text'] = (
        meta_df['title'].fillna('') + ' ' +
        meta_df['description'].fillna('') + ' ' +
        meta_df['main_category'].fillna('')
    )

    # TF-IDF vectorizer
    vectorizer = TfidfVectorizer(
        stop_words='english',
        max_features=max_features,   # smaller = faster
        ngram_range=(1, 1)
    )

    tfidf_matrix = vectorizer.fit_transform(meta_df['combined_text'])
    tfidf_matrix = normalize(tfidf_matrix)  # unit length vectors

    print(f"✅ TF-IDF matrix shape: {tfidf_matrix.shape}")
    return tfidf_matrix


def get_similar_items_content(item_index, tfidf_matrix, meta_df, top_n=5):
    """
    Efficient sparse similarity for one item.
    Uses sparse dot products instead of dense cosine_similarity.
    """
    item_vector = tfidf_matrix[item_index]

    # Sparse dot product with all items
    sim_scores = tfidf_matrix @ item_vector.T

    # Convert to flat array without densifying
    sim_scores = np.asarray(sim_scores.todense()).ravel()

    # Get top N indices (excluding itself)
    top_indices = np.argpartition(-sim_scores, range(top_n + 1))[:top_n + 1]
    top_indices = top_indices[np.argsort(-sim_scores[top_indices])]

    # Remove the item itself if present
    top_indices = [i for i in top_indices if i != item_index][:top_n]

    # Return top results
    return meta_df.iloc[top_indices][['title', 'main_category', 'description']]
