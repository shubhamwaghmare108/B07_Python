import pandas as pd
from sqlalchemy import create_engine, text
from pathlib import Path

# Path to dataset
DATASET_PATH = Path(r"C:\Users\SHUBHAM\Desktop\RetailSalesOltp")

# Get CSV file names (without .csv extension)
csv_files = [file.stem for file in DATASET_PATH.glob("*.csv")]
print("CSV files:", csv_files)

# Connect to MySQL
engine = create_engine('mysql+pymysql://root:S108108w@localhost/retail_demo')

with engine.connect() as conn:
    # Fetch tables
    result = conn.execute(text("SHOW TABLES;"))
    tables = [t[0] for t in result.fetchall()]
    print("Existing tables:", tables)

    # Find missing tables
    missing_tables = [file for file in csv_files if file not in tables]
    print("Missing tables:", missing_tables)

    # Disable foreign key checks
    conn.execute(text("SET foreign_key_checks = 0;"))

    # Load CSVs into MySQL
    for csv_file in csv_files:
        table_name = csv_file
        df = pd.read_csv(DATASET_PATH / f"{csv_file}.csv")
        df.to_sql(table_name, con=conn, if_exists="append", index=False)
        print(f"Table '{table_name}' created/updated and data loaded.")

    # Re-enable foreign key checks
    conn.execute(text("SET foreign_key_checks = 1;"))
    conn.commit()
    conn.close()

