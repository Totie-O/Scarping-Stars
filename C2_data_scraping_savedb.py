from pathlib import Path
import sqlite3
import pandas as pd

db = 'assets/stars.db'
p = Path(db)
if p.exists(): p.unlink()

conn = sqlite3.connect(db)

df = pd.read_csv('assets/cons.csv')
df.to_sql('cons', conn, index=False)

df = pd.read_csv('assets/stars.csv')
df.to_sql('stars', conn, index=False)



conn.close()
