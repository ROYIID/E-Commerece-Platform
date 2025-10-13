import pandas as pd
from sqlalchemy import create_engine, text

user = "root"
password = "Diyorbek098%40"
host = "localhost"
port = 3306
database = "e-commerce"

csv_file = r"C:\Users\User\Desktop\Project\reviews_clean.csv"

engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}")

chunksize = 50000  # 50K rows at a time

for chunk in pd.read_csv(csv_file, chunksize=chunksize, encoding="utf-8"):
    chunk.to_sql("reviews", con=engine, if_exists="append", index=False)
    print("✅ Imported another", len(chunk), "rows")

print("🎉 Import completed successfully!")
