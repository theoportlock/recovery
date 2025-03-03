import sqlite3
import pandas as pd
import os
import sys

# Define the path to the database
DATABASE_PATH = sys.argv[1]

# Define the path to the directory containing the TSV files
TSV_DIR = '../results/'

def table_exists(conn, table_name):
    """
    Check if a table exists in the database.
    """
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name=?
    """, (table_name,))
    return cursor.fetchone() is not None

def load_tsv_to_table(tsv_path, table_name, conn):
    """
    Load data from a TSV file into the corresponding table in the database.
    """
    if not table_exists(conn, table_name):
        print(f"Error: Table {table_name} does not exist in the database.")
        return
    
    try:
        df = pd.read_csv(tsv_path, sep='\t')
        df.to_sql(table_name, conn, if_exists='append', index=False)
        print(f"Loaded data from {tsv_path} into table {table_name}")
    except Exception as e:
        print(f"Error loading {tsv_path} into {table_name}: {e}")

def main():
    # Connect to the SQLite database
    conn = sqlite3.connect(DATABASE_PATH)
    
    # Iterate over all TSV files in the directory
    for filename in os.listdir(TSV_DIR):
        if filename.endswith('.tsv'):
            tsv_path = os.path.join(TSV_DIR, filename)
            table_name = os.path.splitext(filename)[0]  # Remove .tsv extension
            load_tsv_to_table(tsv_path, table_name, conn)
    
    # Commit changes and close the connection
    conn.commit()
    conn.close()
    print("All data loaded successfully.")

if __name__ == '__main__':
    main()
