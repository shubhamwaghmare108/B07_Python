import pandas as pd
import numpy as np

# ============================================================
# FILES
# ============================================================

ITEMS_FILE = "sales_order_items_generated.csv"
ORDERS_FILE = "sales_orders.csv"

OUTPUT_FILE = "sales_orders_updated.csv"


# ============================================================
# LOAD DATA
# ============================================================

items = pd.read_csv(ITEMS_FILE)
orders = pd.read_csv(ORDERS_FILE)

print(f"Order items : {len(items):,}")
print(f"Orders      : {len(orders):,}")


# ============================================================
# CALCULATE ORDER-LEVEL AMOUNTS FROM ORDER ITEMS
# ============================================================

items["gross_amount"] = (
    items["quantity"] * items["unit_price"]
)

order_totals = (
    items
    .groupby("order_id", as_index=False)
    .agg(
        total_amount=("gross_amount", "sum"),
        discount_amount=("discount_amount", "sum"),
        net_amount=("net_price", "sum")
    )
)


# ============================================================
# ROUND FINANCIAL VALUES
# ============================================================

order_totals["total_amount"] = (
    order_totals["total_amount"].round(2)
)

order_totals["discount_amount"] = (
    order_totals["discount_amount"].round(2)
)

order_totals["net_amount"] = (
    order_totals["net_amount"].round(2)
)


# ============================================================
# REMOVE OLD FINANCIAL COLUMNS
# ============================================================

orders = orders.drop(
    columns=[
        "total_amount",
        "discount_amount",
        "net_amount"
    ]
)


# ============================================================
# MERGE NEW FINANCIAL VALUES
# ============================================================

orders = orders.merge(
    order_totals,
    on="order_id",
    how="left",
    validate="one_to_one"
)


# ============================================================
# VALIDATION
# ============================================================

print("\n========================================")
print("VALIDATION")
print("========================================")

print(
    "Orders without order items:",
    orders["total_amount"].isna().sum()
)

print(
    "NULL total_amount:",
    orders["total_amount"].isna().sum()
)

print(
    "NULL discount_amount:",
    orders["discount_amount"].isna().sum()
)

print(
    "NULL net_amount:",
    orders["net_amount"].isna().sum()
)


# Check financial equation
financial_errors = orders[
    ~np.isclose(
        orders["total_amount"] - orders["discount_amount"],
        orders["net_amount"],
        atol=0.01
    )
]

print(
    "Financial calculation errors:",
    len(financial_errors)
)


# ============================================================
# SAVE
# ============================================================

orders.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\n========================================")
print("COMPLETED")
print("========================================")

print(f"Updated orders : {len(orders):,}")
print(f"Output file    : {OUTPUT_FILE}")


# ============================================================
# SAMPLE
# ============================================================

print("\nSample updated orders:")

print(
    orders[
        [
            "order_id",
            "total_amount",
            "discount_amount",
            "net_amount"
        ]
    ].head(10).to_string(index=False)
)