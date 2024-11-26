# Ask questions of committed grants by Gates Foundation
Demo to query committed grants of Gates Foundation using streamlit, langchain, llamaIndex, and chat-gpt

Download committed grants from gates foundation
```
wget https://www.gatesfoundation.org/-/media/files/bmgf-grants.csv
```

Convert csv to sqlite
```
import sqlite3
import pandas as pd

# Load CSV file into a DataFrame
csv_file = 'bmgf-grants.csv'
df = pd.read_csv(csv_file,header=2)

# Define SQLite database and table name
sqlite_file = 'gates.sqlite'
table_name = 'grants'

# Create a connection to the SQLite database
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

# Create table with appropriate data types
c.execute(f'''
    CREATE TABLE IF NOT EXISTS {table_name} (
        "GRANT ID" INTEGER PRIMARY KEY,
        "GRANTEE" TEXT,
        "PURPOSE" TEXT,
        "DIVISION" TEXT,
        "DATE COMMITTED" DATE,
        "DURATION (MONTHS)" INTEGER,
        "AMOUNT COMMITTED" REAL,
        "GRANTEE WEBSITE" TEXT,
        "GRANTEE CITY" TEXT,
        "GRANTEE STATE" TEXT,
        "GRANTEE COUNTRY" TEXT,
        "REGION SERVED" TEXT,
        "TOPIC" TEXT
    )
''')

# Insert DataFrame into SQLite table
df.to_sql(table_name, conn, if_exists='replace', index=False)

# Commit changes and close the connection
conn.commit()

# Close the connection
conn.close()
```
