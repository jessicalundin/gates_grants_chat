# Ask questions of committed grants by Gates Foundation
Demo to query committed grants of Gates Foundation using streamlit, langchain, llamaIndex, and chat-gpt

Download committed grants from gates foundation
```
wget https://www.gatesfoundation.org/-/media/files/bmgf-grants.csv
```

Convert csv to sqlite
```
import pandas as pd
import sqlite3

# Load the CSV file into a DataFrame
df = pd.read_csv('bmgf-grants.csv')

# Create a connection to the SQLite database
conn = sqlite3.connect('gates.sqlite')

# Write the DataFrame to the SQLite database
df.to_sql('grants', conn, if_exists='replace', index=False)

# Close the connection
conn.close()
```
