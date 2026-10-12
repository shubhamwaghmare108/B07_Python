from sqlalchemy import create_engine,text
from pathlib import Path    
import pandas as pd
import time

# Path where CSVs will be dumped
csv_dump_path = Path(r"C:\Users\SHUBHAM\Desktop\RetailSalesOltp")

# Connect to MySQL
engine = create_engine('mysql+pymysql://root:S108108w@localhost/retail')
conn = engine.connect()

# Get list of tables
result = conn.execute(text("SHOW TABLES;"))
tables = [row[0] for row in result.fetchall()]  # flatten tuples

# Dump each table to CSV
timestart = time.time()
for table in tables:
    print(f"Dumping table: {table}")
    df = pd.read_sql_table(table, con=engine)   # use engine, not conn
    df.to_csv(csv_dump_path / f"{table}.csv", index=False)
print(f"CSV files are located in: {csv_dump_path.resolve()}")
timeend = time.time()
print(f"Dumped {len(tables)} tables to CSV in {timeend - timestart:.2f} seconds.")
print("Done.")
conn.close()
