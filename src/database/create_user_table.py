import pandas as pd
import random
from sqlalchemy import create_engine, text
from src.database.config import user, password,database
import psycopg

# Connect to PostgreSQL
engine = create_engine(f"postgresql+psycopg://{user}:{password}@localhost:5432/{database}")

# Step 1️⃣: Read existing user_ids from reviews
with engine.connect() as conn:
    reviews_users = pd.read_sql("SELECT DISTINCT user_id FROM reviews;", conn)
    existing_users = pd.read_sql("SELECT user_id FROM users;", conn)

# Step 2️⃣: Remove already existing users (if any)
existing_user_ids = set(existing_users["user_id"])
new_users_df = reviews_users[~reviews_users["user_id"].isin(existing_user_ids)].copy()

print(f"🧩 Found {len(new_users_df)} new users to add.")

# Step 3️⃣: Generate random realistic user details
first_names = [
    "Alex", "Sam", "Chris", "Taylor", "Jordan", "Riley", "Jamie", "Morgan", "Casey", "Dylan",
    "Ava", "Olivia", "Liam", "Mia", "Noah", "Sophia", "Ethan", "Isabella", "Logan", "Ella"
]
last_names = [
    "Smith", "Johnson", "Brown", "Williams", "Jones", "Garcia", "Miller", "Davis",
    "Wilson", "Anderson", "Taylor", "Thomas", "Moore", "Martin", "Jackson", "White"
]
domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "icloud.com", "mail.com"]

def gen_user(first, last):
    patterns = [
        f"{first.lower()}.{last.lower()}",
        f"{first.lower()}_{last.lower()}",
        f"{first[0].lower()}{last.lower()}",
        f"{first.lower()}{random.randint(10,999)}"
    ]
    prefix = random.choice(patterns)
    domain = random.choice(domains)
    email = f"{prefix}@{domain}"
    username = prefix.replace('.', '').replace('_', '')
    return username, email

# Step 4️⃣: Fill columns
new_users_df["first_name"] = [random.choice(first_names) for _ in range(len(new_users_df))]
new_users_df["last_name"] = [random.choice(last_names) for _ in range(len(new_users_df))]
user_info = [gen_user(f, l) for f, l in zip(new_users_df["first_name"], new_users_df["last_name"])]
new_users_df["username"] = [u for u, _ in user_info]
new_users_df["email"] = [e for _, e in user_info]

# Step 5️⃣: Insert into users table
if not new_users_df.empty:
    new_users_df.to_sql("users", engine, if_exists="append", index=False)
    print(f"✅ {len(new_users_df)} new users added successfully.")
else:
    print("✅ No new users to add. All already exist.")
