import pandas as pd
from src.data_loader import meta, reviews

def preprocess_reviews(df):
    """Clean and prepare reviews dataset for recommendation."""
    # Keep only important columns that actually exist
    df = df[['user_id', 'asin', 'rating', 'title', 'text', 'timestamp']].copy()

    # Rename columns to consistent names
    df.rename(columns={
        'asin': 'item_id',
        'text': 'review',
        'title': 'summary'
    }, inplace=True)

    # Drop missing or empty rows
    df.dropna(subset=['user_id', 'item_id', 'rating'], inplace=True)

    # Ensure numeric rating
    df['rating'] = df['rating'].astype(float)

    # Optional: convert timestamp if you want
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s', errors='coerce')

    print(f"✅ Cleaned reviews shape: {df.shape}")
    return df


def preprocess_metadata(meta_df):
    """Simplify metadata (optional for content-based filtering)."""
    # Keep relevant columns that exist
    keep_cols = ['title', 'description', 'price', 'main_category', 'average_rating', 'parent_asin']
    existing_cols = [col for col in keep_cols if col in meta_df.columns]
    meta_df = meta_df[existing_cols].copy()

    # Rename for consistency
    if 'parent_asin' in meta_df.columns:
        meta_df.rename(columns={'parent_asin': 'item_id'}, inplace=True)

    print(f"✅ Cleaned metadata shape: {meta_df.shape}")
    return meta_df


# -------------------------------
# Save processed versions
# -------------------------------
reviews_clean = preprocess_reviews(reviews)
meta_clean = preprocess_metadata(meta)

reviews_clean.to_csv("data/processed/reviews_clean_500k.csv", index=False)
meta_clean.to_csv("data/processed/meta_clean_500k.csv", index=False)
