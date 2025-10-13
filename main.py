import pandas as pd
from src.recommender import (
    build_sparse_matrix,
    compute_item_similarity_sparse,
    get_similar_items_sparse
)
from src.content_recommender import (
    prepare_text_features,
    get_similar_items_content
)

# ===============================
# 1️⃣ Load cleaned data
# ===============================
print("📂 Loading cleaned datasets...")
reviews = pd.read_csv("data/processed/reviews_clean.csv")
meta = pd.read_csv("data/processed/meta_clean.csv")

# If too large, limit meta rows temporarily for testing
if len(meta) > 100000:
    print(f"⚠️ Dataset too large ({len(meta):,} rows) — using a subset of 100,000 for content-based part.")
    meta = meta.sample(100000, random_state=42).reset_index(drop=True)

# ===============================
# 2️⃣ Collaborative Filtering
# ===============================
print("\n🔧 Running Collaborative Filtering...")

# Build user-item matrix
matrix, user_map, item_map = build_sparse_matrix(reviews)

# Compute item similarity (sparse cosine)
item_similarity_sparse = compute_item_similarity_sparse(matrix)

# Pick an example item
example_item_cf = list(item_map.keys())[0]
similar_items_cf = get_similar_items_sparse(example_item_cf, item_map, item_similarity_sparse, top_n=5)

print(f"\n🎯 Collaborative Filtering Recommendations for '{example_item_cf}':")
print(similar_items_cf)

# ===============================
# 3️⃣ Content-Based Filtering
# ===============================
print("\n🔧 Running Content-Based Filtering...")

# Build TF-IDF matrix (optimized inside the function)
tfidf_matrix = prepare_text_features(meta)

# Pick an example item (by index)
example_index_cb = 0
example_item_cb = meta.loc[example_index_cb, 'title']

# Get top similar items (optimized local similarity computation)
similar_items_cb = get_similar_items_content(example_index_cb, tfidf_matrix, meta, top_n=5)

print(f"\n🎯 Content-Based Recommendations for: '{example_item_cb}'")
print(similar_items_cb[['title', 'main_category']])

# ===============================
# 4️⃣ Summary
# ===============================
print("\n✅ Both recommenders executed successfully!")
