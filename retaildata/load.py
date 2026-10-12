import pandas as pd
from sqlalchemy import create_engine

# ============================================================
# DATABASE
# ============================================================

DB_USER = "root"
DB_PASSWORD = "S108108w"
DB_HOST = "localhost"
DB_PORT = 3306
DB_NAME = "retail"

engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


# ============================================================
# CSV FILES
# ============================================================

files = {
    "brands": "brands.csv",
    "categories": "categories.csv",
    "customers": "customers.csv",
    "inventory": "inventory.csv",
    "lookup_channel": "lookup_channel.csv",
    "lookup_gender": "lookup_gender.csv",
    "lookup_order_status": "lookup_order_status.csv",
    "lookup_payment_mode": "lookup_payment_mode.csv",
    "product_suppliers": "product_suppliers_fixed.csv",
    "products": "products.csv",
    "sales_order_items": "sales_order_items_generated.csv",
    "sales_orders": "sales_orders_corrected.csv",
    "sales_return_items": "sales_return_items.csv",
    "sales_returns": "sales_returns.csv",
    "stores": "stores.csv",
    "suppliers": "suppliers.csv"
}


# ============================================================
# LOAD ALL CSV FILES
# ============================================================

for table_name, file_name in files.items():

    print(f"Loading {file_name} -> {table_name}")

    df = pd.read_csv(file_name)

    df.to_sql(
        name=table_name,
        con=engine,
        if_exists="append",
        index=False,
        chunksize=5000,
        method="multi"
    )

    print(
        f"Inserted {len(df):,} records into {table_name}"
    )


print("\nAll tables loaded successfully.")