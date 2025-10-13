import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity


def build_sparse_matrix(reviews_df):
    """Create a sparse user-item rating matrix."""
    # Map users and items to integer indices
    user_map = {u: i for i, u in enumerate(reviews_df['user_id'].unique())}
    item_map = {i: j for j, i in enumerate(reviews_df['item_id'].unique())}

    # Convert to index values
    user_indices = reviews_df['user_id'].map(user_map)
    item_indices = reviews_df['item_id'].map(item_map)
    ratings = reviews_df['rating'].astype(float)

    # Create sparse matrix
    matrix = csr_matrix(
        (ratings, (user_indices, item_indices)),
        shape=(len(user_map), len(item_map))
    )

    return matrix, user_map, item_map


def compute_item_similarity_sparse(matrix):
    """Compute item-item similarity using sparse matrix (cosine)."""
    similarity = cosine_similarity(matrix.T, dense_output=False)
    return similarity


def get_similar_items_sparse(item_name, item_map, item_similarity, top_n=5):
    """Find top-N similar items using sparse similarity matrix."""
    from numpy import argsort

    if item_name not in item_map:
        raise ValueError(f"Item '{item_name}' not found in map.")

    item_idx = item_map[item_name]
    sim_scores = item_similarity[item_idx].toarray().flatten()
    top_indices = argsort(sim_scores)[::-1][1:top_n + 1]

    reverse_map = {v: k for k, v in item_map.items()}
    return [reverse_map[i] for i in top_indices]
