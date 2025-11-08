import os
import gzip
import json
import pandas as pd


# -------------------------------
# Helper: Parse gzipped JSON file
# -------------------------------
def parse_json_gz(path, limit=None):
    """Yield JSON objects line by line from a .json.gz or .jsonl.gz file."""
    with gzip.open(path, 'rt', encoding='utf-8') as f:
        for i, line in enumerate(f):
            yield json.loads(line)
            if limit and i + 1 >= limit:
                break


# -------------------------------
# Load into DataFrame
# -------------------------------
def load_df(path, limit=None):
    """Load a .json.gz file and return a pandas DataFrame (with optional row limit)."""
    data = []
    for record in parse_json_gz(path, limit=limit):
        data.append(record)
    return pd.DataFrame(data)


# -------------------------------
# Load reviews and metadata files
# -------------------------------
def load_amazon_dataset(data_dir="data/raw/", category="Electronics", limit=500000):
    """
    Load Amazon dataset (reviews + metadata) for a given category.
    Loads only up to 'limit' rows from each file to avoid memory issues.
    """

    reviews_path = os.path.join(data_dir, f"{category}.jsonl.gz")
    meta_path = os.path.join(data_dir, f"meta_{category}.jsonl.gz")

    # Check if files exist
    if not os.path.exists(reviews_path):
        raise FileNotFoundError(f"Missing: {reviews_path}")
    if not os.path.exists(meta_path):
        raise FileNotFoundError(f"Missing: {meta_path}")

    print(f"Loading first {limit:,} reviews from: {reviews_path}")
    reviews_df = load_df(reviews_path, limit=limit)
    print(f"✅ Loaded {len(reviews_df):,} reviews")

    print(f"Loading first {limit:,} items from: {meta_path}")
    meta_df = load_df(meta_path, limit=limit)
    print(f"✅ Loaded {len(meta_df):,} metadata items")

    return reviews_df, meta_df


# -------------------------------
# Run directly (for testing)
# -------------------------------
reviews, meta = load_amazon_dataset(category="Electronics", limit=500000)
print("\n🧾 Reviews sample:")
print(reviews.head())

print("\n📦 Metadata sample:")
print(meta.head())

print("Review columns:", reviews.columns.tolist())
print("Metadata columns:", meta.columns.tolist())
