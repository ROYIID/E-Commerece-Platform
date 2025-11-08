from sqlalchemy import text
import pandas as pd
from sqlalchemy import create_engine
import psycopg
from src.database.config import user, password,database




df_meta = pd.read_csv("data/processed/meta_clean.csv")
df_reviews = pd.read_csv("data/processed/reviews_clean_500k.csv")

print(df_meta.head())
print(df_reviews.head())


print("Meta csv: ")
print(df_meta.info())

print("Reviews csv:")
print(df_reviews.info())



engine = create_engine(f"postgresql+psycopg2://{user}:{password}@localhost:5432/{database}")

meta = pd.read_csv(
    r'E:\Projects\E-commerce Platform\data\processed\meta_clean_500k.csv',
    encoding='utf-8',
    quoting=1,  
    on_bad_lines='skip'  
)

# Upload to PostgreSQL
meta.to_sql('meta', engine, if_exists='replace', index=False)

print("Loading reviews CSV...")
reviews = pd.read_csv(
    r'E:\Projects\E-commerce Platform\data\processed\reviews_clean_500k.csv',
    encoding='utf-8',
    quoting=1,
    on_bad_lines='skip'
)
print("Reviews loaded:", len(reviews), "rows")

# Upload to PostgreSQL
reviews.to_sql('reviews', engine, if_exists='replace', index=False)
print("✅ Reviews table uploaded successfully")



