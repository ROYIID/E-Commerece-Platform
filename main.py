import pandas as pd
from src.recommender import build_sparse_matrix, compute_item_similarity_sparse, get_similar_items_sparse
from src.content_recommender import prepare_text_features, compute_content_similarity, get_similar_items_content

# ===============================
# 1️⃣ Load cleaned data
# ===============================
print("📂 Loading cleaned datasets...")
reviews = pd.read_csv("data/processed/reviews_clean.csv")
meta = pd.read_csv("data/processed/meta_clean.csv")

# ===============================
# 2️⃣ Collaborative Filtering
# ===============================
print("\n🔧 Running Collaborative Filtering...")

matrix, user_map, item_map = build_sparse_matrix(reviews)
item_similarity_sparse =  (matrix)

example_item_cf = list(item_map.keys())[0]
similar_items_cf = get_similar_items_sparse(example_item_cf, item_map, item_similarity_sparse, top_n=5)

print(f"\n🎯 Collaborative Filtering Recommendations for {example_item_cf}:")
print(similar_items_cf)

# ===============================
# 3️⃣ Content-Based Filtering
# ===============================
print("\n🔧 Running Content-Based Filtering...")

tfidf_matrix = prepare_text_features(meta)
content_similarity = compute_content_similarity(tfidf_matrix)

example_item_cb = meta["item_id"].iloc[0]
similar_items_cb = get_similar_items_content(example_item_cb, meta, content_similarity, top_n=5)

print(f"\n🎯 Content-Based Recommendations for {example_item_cb}:")
print(similar_items_cb)

# ===============================
# 4️⃣ Summary
# ===============================
print("\n✅ Recommender systems executed successfully!")
