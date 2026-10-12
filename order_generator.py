import pandas as pd
import numpy as np
from pathlib import Path

# ============================================================
# CONFIGURATION
# ============================================================
root = Path(__file__).parent /'retail_csvs'
PRODUCT_FILE = root/"products.csv"
ORDER_FILE = root/"sales_orders.csv"
OUTPUT_FILE = root/"sales_order_items_generated.csv"

# Minimum and maximum number of products in an order
MIN_ITEMS_PER_ORDER = 1
MAX_ITEMS_PER_ORDER = 5

# Probability distribution for number of items
# You can modify this to create more realistic orders.
ITEM_COUNT_PROBABILITIES = {
    1: 0.20,
    2: 0.25,
    3: 0.20,
    4: 0.15,
    5: 0.10,
    6: 0.05,
    7: 0.03,
    8: 0.02
}

# Discount range
MIN_DISCOUNT = 0.00
MAX_DISCOUNT = 0.25

# Random seed for reproducibility
RANDOM_SEED = 42

np.random.seed(RANDOM_SEED)


# ============================================================
# LOAD DATA
# ============================================================

products = pd.read_csv(PRODUCT_FILE)
orders = pd.read_csv(ORDER_FILE)

print(f"Products loaded : {len(products):,}")
print(f"Orders loaded   : {len(orders):,}")


# ============================================================
# CLEAN PRODUCT DATA
# ============================================================

products["mrp"] = pd.to_numeric(products["mrp"], errors="coerce")
products["cost_price"] = pd.to_numeric(
    products["cost_price"],
    errors="coerce"
)

products["max_qty_per_transaction"] = pd.to_numeric(
    products["max_qty_per_transaction"],
    errors="coerce"
).fillna(1)

# Remove products without valid price
products = products[
    products["mrp"].notna() &
    (products["mrp"] > 0)
].copy()

products["max_qty_per_transaction"] = (
    products["max_qty_per_transaction"]
    .clip(lower=1)
    .astype(int)
)

products = products.reset_index(drop=True)


# ============================================================
# ITEM COUNT DISTRIBUTION
# ============================================================

item_counts = list(ITEM_COUNT_PROBABILITIES.keys())
item_probabilities = list(ITEM_COUNT_PROBABILITIES.values())

# Normalize probabilities
item_probabilities = np.array(item_probabilities)
item_probabilities = item_probabilities / item_probabilities.sum()


# ============================================================
# GENERATE SALES ORDER ITEMS
# ============================================================

sales_order_items = []

order_item_id = 1

for _, order in orders.iterrows():

    order_id = int(order["order_id"])

    # --------------------------------------------------------
    # Decide how many products this order contains
    # --------------------------------------------------------

    number_of_items = np.random.choice(
        item_counts,
        p=item_probabilities
    )

    # Cannot have more unique products than available products
    number_of_items = min(
        number_of_items,
        len(products)
    )

    # --------------------------------------------------------
    # Select unique products for this order
    # --------------------------------------------------------

    selected_products = products.sample(
        n=number_of_items,
        replace=False
    )

    # --------------------------------------------------------
    # Generate each order item
    # --------------------------------------------------------

    for _, product in selected_products.iterrows():

        product_id = int(product["product_id"])
        unit_price = float(product["mrp"])

        max_quantity = int(
            product["max_qty_per_transaction"]
        )

        # Quantity between 1 and product's allowed maximum
        quantity = np.random.randint(
            1,
            max_quantity + 1
        )

        # ----------------------------------------------------
        # Discount
        # ----------------------------------------------------

        discount_percent = round(
            np.random.uniform(
                MIN_DISCOUNT,
                MAX_DISCOUNT
            ),
            4
        )

        # ----------------------------------------------------
        # Gross amount
        # ----------------------------------------------------

        gross_amount = unit_price * quantity

        # ----------------------------------------------------
        # Discount amount
        # ----------------------------------------------------

        discount_amount = (
            gross_amount * discount_percent
        )

        discount_amount = round(
            discount_amount,
            2
        )

        # ----------------------------------------------------
        # Net price
        # ----------------------------------------------------

        net_price = (
            gross_amount - discount_amount
        )

        net_price = round(
            net_price,
            2
        )

        # ----------------------------------------------------
        # Add item
        # ----------------------------------------------------

        sales_order_items.append({
            "order_item_id": order_item_id,
            "order_id": order_id,
            "product_id": product_id,
            "quantity": quantity,
            "unit_price": round(unit_price, 2),
            "discount_percent": discount_percent,
            "discount_amount": discount_amount,
            "net_price": net_price
        })

        order_item_id += 1


# ============================================================
# CREATE DATAFRAME
# ============================================================

sales_order_items_df = pd.DataFrame(
    sales_order_items
)


# ============================================================
# SAVE
# ============================================================

sales_order_items_df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# VALIDATION
# ============================================================

print("\n========================================")
print("SALES ORDER ITEM GENERATION COMPLETED")
print("========================================")

print(
    f"Orders             : "
    f"{sales_order_items_df['order_id'].nunique():,}"
)

print(
    f"Order items        : "
    f"{len(sales_order_items_df):,}"
)

print(
    f"Average items/order: "
    f"{sales_order_items_df.groupby('order_id').size().mean():.2f}"
)

print(
    f"Minimum items/order: "
    f"{sales_order_items_df.groupby('order_id').size().min()}"
)

print(
    f"Maximum items/order: "
    f"{sales_order_items_df.groupby('order_id').size().max()}"
)

print("\nSample:")
print(
    sales_order_items_df.head(15).to_string(
        index=False
    )
)

print(f"\nSaved to: {OUTPUT_FILE}")