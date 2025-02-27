import pandas as pd
import sqlite3

# File paths
db_file = "../results/m4efad.db"

# Load data
xls = pd.read_csv()

# Connect to SQLite database (creates it if not exists)
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Create tables (fixed schema)
cursor.executescript("""
DROP TABLE IF EXISTS funders;
DROP TABLE IF EXISTS scheme;
DROP TABLE IF EXISTS timeline;

CREATE TABLE funders (
    name TEXT PRIMARY KEY,
    full_name TEXT,
    website TEXT,
    focus TEXT,
    description TEXT
);

CREATE TABLE scheme (
    scheme TEXT PRIMARY KEY,
    funder TEXT,
    website TEXT,
    lead TEXT,
    scheme_type TEXT,
    description TEXT,
    interested TEXT,
    FOREIGN KEY (funder) REFERENCES funders(name)
);

CREATE TABLE timeline (
    scheme TEXT,
    registration TEXT,
    EOI TEXT,
    submission TEXT,
    PRIMARY KEY (scheme, registration, EOI, submission),
    FOREIGN KEY (scheme) REFERENCES scheme(scheme)
);
""")

# Insert data
df_funders.to_sql("funders", conn, if_exists="append", index=False)
df_scheme.to_sql("scheme", conn, if_exists="append", index=False)
df_timeline.to_sql("timeline", conn, if_exists="append", index=False)

# Commit and close
conn.commit()
conn.close()

print("Data imported successfully into SQLite database!")
