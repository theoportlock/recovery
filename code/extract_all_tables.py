import sqlite3
import pandas as pd
import os

# Define database file and output directory
DB_PATH = "../results/m4efad.db"  # Change this to your actual SQLite file
OUTPUT_DIR = "../results"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Connect to the database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Get all table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [table[0] for table in cursor.fetchall()]

# Export each table to TSV
for table in tables:
    df = pd.read_sql(f"SELECT * FROM {table}", conn)
    df.to_csv(os.path.join(OUTPUT_DIR, f"{table}.tsv"), sep='\t', index=False)
    print(f"Exported {table}.tsv")

# Close connection
conn.close()
print("All tables exported successfully!")
