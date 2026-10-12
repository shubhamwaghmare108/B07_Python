CREATE DATABASE IF NOT EXISTS retail_demo;
USE retail_demo;

SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS sales_return_items;
DROP TABLE IF EXISTS sales_returns;
DROP TABLE IF EXISTS sales_order_items;
DROP TABLE IF EXISTS sales_orders;
DROP TABLE IF EXISTS inventory;
DROP TABLE IF EXISTS product_suppliers;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS suppliers;
DROP TABLE IF EXISTS stores;
DROP TABLE IF EXISTS customer;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS brands;

DROP TABLE IF EXISTS lookup_return_status;
DROP TABLE IF EXISTS lookup_order_status;
DROP TABLE IF EXISTS lookup_payment_mode;
DROP TABLE IF EXISTS lookup_channel;
DROP TABLE IF EXISTS lookup_gender;

SET FOREIGN_KEY_CHECKS = 1;


-- =========================================================
-- LOOKUP TABLES
-- =========================================================

CREATE TABLE lookup_gender (
    gender_code VARCHAR(10) NOT NULL,
    gender_name VARCHAR(50) NOT NULL,

    PRIMARY KEY (gender_code),
    UNIQUE KEY uk_gender_name (gender_name)
) ENGINE=InnoDB;


CREATE TABLE lookup_channel (
    channel_id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
    channel_name VARCHAR(50) NOT NULL,

    PRIMARY KEY (channel_id),
    UNIQUE KEY uk_channel_name (channel_name)
) ENGINE=InnoDB;


CREATE TABLE lookup_order_status (
    status_id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
    status_name VARCHAR(50) NOT NULL,

    PRIMARY KEY (status_id),
    UNIQUE KEY uk_order_status_name (status_name)
) ENGINE=InnoDB;


CREATE TABLE lookup_payment_mode (
    payment_mode_id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
    payment_mode_name VARCHAR(50) NOT NULL,

    PRIMARY KEY (payment_mode_id),
    UNIQUE KEY uk_payment_mode_name (payment_mode_name)
) ENGINE=InnoDB;


CREATE TABLE lookup_return_status (
    return_status_id SMALLINT UNSIGNED NOT NULL,
    status_name VARCHAR(50) NOT NULL,

    PRIMARY KEY (return_status_id),
    UNIQUE KEY uk_return_status_name (status_name)
) ENGINE=InnoDB;


-- =========================================================
-- BRANDS
-- =========================================================

CREATE TABLE brands (
    brand_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    brand_name VARCHAR(150) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (brand_id),
    UNIQUE KEY uk_brand_name (brand_name)
) ENGINE=InnoDB;


-- =========================================================
-- CATEGORIES
-- Self-referencing hierarchy
-- =========================================================

CREATE TABLE categories (
    category_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    category_name VARCHAR(150) NOT NULL,
    parent_category_id BIGINT UNSIGNED NULL,
    level TINYINT UNSIGNED NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (category_id),

    UNIQUE KEY uk_category_parent_name
        (parent_category_id, category_name),

    CONSTRAINT fk_category_parent
        FOREIGN KEY (parent_category_id)
        REFERENCES categories(category_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT chk_category_level
        CHECK (level >= 1)
) ENGINE=InnoDB;


-- =========================================================
-- CUSTOMERS
-- =========================================================

CREATE TABLE customer (
    customer_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    customer_code VARCHAR(30) NOT NULL,
    customer_name VARCHAR(150) NOT NULL,
    gender_code VARCHAR(10) NULL,
    age_group VARCHAR(30) NULL,
    city VARCHAR(100) NULL,
    state VARCHAR(100) NULL,
    city_tier TINYINT UNSIGNED NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (customer_id),

    UNIQUE KEY uk_customer_code (customer_code),

    KEY idx_customer_gender (gender_code),
    KEY idx_customer_city (city),
    KEY idx_customer_state (state),

    CONSTRAINT fk_customer_gender
        FOREIGN KEY (gender_code)
        REFERENCES lookup_gender(gender_code)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT chk_customer_city_tier
        CHECK (city_tier IS NULL OR city_tier BETWEEN 1 AND 5)
) ENGINE=InnoDB;


-- =========================================================
-- STORES
-- =========================================================

CREATE TABLE stores (
    store_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    store_code VARCHAR(30) NOT NULL,
    store_name VARCHAR(150) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    city_tier TINYINT UNSIGNED NULL,
    cluster_zone VARCHAR(100) NULL,
    store_type VARCHAR(50) NULL,
    store_size_sqft INT UNSIGNED NULL,
    opening_date DATE NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (store_id),

    UNIQUE KEY uk_store_code (store_code),

    KEY idx_store_city (city),
    KEY idx_store_state (state),

    CONSTRAINT chk_store_city_tier
        CHECK (city_tier IS NULL OR city_tier BETWEEN 1 AND 5),

    CONSTRAINT chk_store_size
        CHECK (store_size_sqft IS NULL OR store_size_sqft > 0)
) ENGINE=InnoDB;


-- =========================================================
-- SUPPLIERS
-- =========================================================

CREATE TABLE suppliers (
    supplier_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    supplier_code VARCHAR(30) NOT NULL,
    supplier_name VARCHAR(150) NOT NULL,
    supplier_type VARCHAR(50) NULL,
    city VARCHAR(100) NULL,
    state VARCHAR(100) NULL,
    payment_days SMALLINT UNSIGNED NULL,
    lead_time_days SMALLINT UNSIGNED NULL,
    annual_contract_value_lakh DECIMAL(15,2) NULL,
    is_preferred_vendor BOOLEAN NOT NULL DEFAULT FALSE,
    years_associated SMALLINT UNSIGNED NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (supplier_id),

    UNIQUE KEY uk_supplier_code (supplier_code),

    KEY idx_supplier_name (supplier_name),

    CONSTRAINT chk_supplier_payment_days
        CHECK (payment_days IS NULL OR payment_days >= 0),

    CONSTRAINT chk_supplier_lead_time
        CHECK (lead_time_days IS NULL OR lead_time_days >= 0),

    CONSTRAINT chk_supplier_contract_value
        CHECK (
            annual_contract_value_lakh IS NULL
            OR annual_contract_value_lakh >= 0
        )
) ENGINE=InnoDB;


-- =========================================================
-- PRODUCTS
-- =========================================================

CREATE TABLE products (
    product_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    product_code VARCHAR(50) NOT NULL,
    product_name VARCHAR(200) NOT NULL,
    brand_id BIGINT UNSIGNED NULL,
    category_id BIGINT UNSIGNED NOT NULL,

    mrp DECIMAL(12,2) NOT NULL,
    cost_price DECIMAL(12,2) NOT NULL,
    gross_margin_pct DECIMAL(5,2) NULL,

    is_perishable BOOLEAN NOT NULL DEFAULT FALSE,
    veg_nonveg VARCHAR(20) NULL,
    max_qty_per_transaction INT UNSIGNED NULL,

    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (product_id),

    UNIQUE KEY uk_product_code (product_code),

    KEY idx_product_brand (brand_id),
    KEY idx_product_category (category_id),

    CONSTRAINT fk_product_brand
        FOREIGN KEY (brand_id)
        REFERENCES brands(brand_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_product_category
        FOREIGN KEY (category_id)
        REFERENCES categories(category_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT chk_product_mrp
        CHECK (mrp >= 0),

    CONSTRAINT chk_product_cost
        CHECK (cost_price >= 0),

    CONSTRAINT chk_product_margin
        CHECK (
            gross_margin_pct IS NULL
            OR gross_margin_pct BETWEEN 0 AND 100
        ),

    CONSTRAINT chk_product_max_qty
        CHECK (
            max_qty_per_transaction IS NULL
            OR max_qty_per_transaction > 0
        )
) ENGINE=InnoDB;


-- =========================================================
-- PRODUCT SUPPLIERS
-- Many-to-many relationship
-- =========================================================

CREATE TABLE product_suppliers (
    product_supplier_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    product_id BIGINT UNSIGNED NOT NULL,
    supplier_id BIGINT UNSIGNED NOT NULL,
    supplier_cost DECIMAL(12,2) NOT NULL,
    supplier_date DATE NULL,
    is_primary BOOLEAN NOT NULL DEFAULT FALSE,

    PRIMARY KEY (product_supplier_id),

    UNIQUE KEY uk_product_supplier
        (product_id, supplier_id),

    KEY idx_ps_supplier (supplier_id),

    CONSTRAINT fk_ps_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_ps_supplier
        FOREIGN KEY (supplier_id)
        REFERENCES suppliers(supplier_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT chk_supplier_cost
        CHECK (supplier_cost >= 0)
) ENGINE=InnoDB;


-- =========================================================
-- INVENTORY
-- Product x Store
-- =========================================================

CREATE TABLE inventory (
    inventory_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    product_id BIGINT UNSIGNED NOT NULL,
    store_id BIGINT UNSIGNED NOT NULL,

    quantity_on_hand INT UNSIGNED NOT NULL DEFAULT 0,
    quantity_reserved INT UNSIGNED NOT NULL DEFAULT 0,
    reorder_point INT UNSIGNED NOT NULL DEFAULT 0,

    last_updated DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (inventory_id),

    UNIQUE KEY uk_inventory_product_store
        (product_id, store_id),

    KEY idx_inventory_store (store_id),

    CONSTRAINT fk_inventory_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_inventory_store
        FOREIGN KEY (store_id)
        REFERENCES stores(store_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT chk_inventory_reserved
        CHECK (quantity_reserved <= quantity_on_hand)
) ENGINE=InnoDB;


-- =========================================================
-- SALES ORDERS
-- =========================================================

CREATE TABLE sales_orders (
    order_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    order_number VARCHAR(40) NOT NULL,

    customer_id BIGINT UNSIGNED NULL,
    store_id BIGINT UNSIGNED NOT NULL,

    order_date DATETIME NOT NULL,
    status_id SMALLINT UNSIGNED NOT NULL,
    payment_mode_id SMALLINT UNSIGNED NOT NULL,
    channel_id SMALLINT UNSIGNED NOT NULL,

    total_amount DECIMAL(14,2) NOT NULL DEFAULT 0.00,
    discount_amount DECIMAL(14,2) NOT NULL DEFAULT 0.00,
    net_amount DECIMAL(14,2) NOT NULL DEFAULT 0.00,

    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (order_id),

    UNIQUE KEY uk_order_number (order_number),

    KEY idx_order_customer (customer_id),
    KEY idx_order_store (store_id),
    KEY idx_order_date (order_date),
    KEY idx_order_status (status_id),
    KEY idx_order_payment (payment_mode_id),
    KEY idx_order_channel (channel_id),

    CONSTRAINT fk_order_customer
        FOREIGN KEY (customer_id)
        REFERENCES customer(customer_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE,

    CONSTRAINT fk_order_store
        FOREIGN KEY (store_id)
        REFERENCES stores(store_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_order_status
        FOREIGN KEY (status_id)
        REFERENCES lookup_order_status(status_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_order_payment
        FOREIGN KEY (payment_mode_id)
        REFERENCES lookup_payment_mode(payment_mode_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_order_channel
        FOREIGN KEY (channel_id)
        REFERENCES lookup_channel(channel_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT chk_order_total
        CHECK (total_amount >= 0),

    CONSTRAINT chk_order_discount
        CHECK (discount_amount >= 0),

    CONSTRAINT chk_order_net
        CHECK (net_amount >= 0),

    CONSTRAINT chk_order_amounts
        CHECK (net_amount <= total_amount)
) ENGINE=InnoDB;


-- =========================================================
-- SALES ORDER ITEMS
-- =========================================================

CREATE TABLE sales_order_items (
    order_item_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    order_id BIGINT UNSIGNED NOT NULL,
    product_id BIGINT UNSIGNED NOT NULL,

    quantity INT UNSIGNED NOT NULL,
    unit_price DECIMAL(12,2) NOT NULL,

    discount_percent DECIMAL(5,2) NOT NULL DEFAULT 0.00,
    discount_amount DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    net_price DECIMAL(14,2) NOT NULL,

    PRIMARY KEY (order_item_id),

    UNIQUE KEY uk_order_product
        (order_id, product_id),

    KEY idx_order_item_product (product_id),

    CONSTRAINT fk_order_item_order
        FOREIGN KEY (order_id)
        REFERENCES sales_orders(order_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_order_item_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT chk_order_item_quantity
        CHECK (quantity > 0),

    CONSTRAINT chk_order_item_price
        CHECK (unit_price >= 0),

    CONSTRAINT chk_order_item_discount_pct
        CHECK (discount_percent BETWEEN 0 AND 100),

    CONSTRAINT chk_order_item_discount_amount
        CHECK (discount_amount >= 0),

    CONSTRAINT chk_order_item_net
        CHECK (net_price >= 0)
) ENGINE=InnoDB;


-- =========================================================
-- SALES RETURNS
-- =========================================================

CREATE TABLE sales_returns (
    return_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    order_id BIGINT UNSIGNED NOT NULL,

    return_date DATETIME NOT NULL,
    return_status_id SMALLINT UNSIGNED NOT NULL,
    reason VARCHAR(500) NULL,

    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (return_id),

    KEY idx_return_order (order_id),
    KEY idx_return_status (return_status_id),
    KEY idx_return_date (return_date),

    CONSTRAINT fk_return_order
        FOREIGN KEY (order_id)
        REFERENCES sales_orders(order_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_return_status
        FOREIGN KEY (return_status_id)
        REFERENCES lookup_return_status(return_status_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE=InnoDB;


-- =========================================================
-- SALES RETURN ITEMS
-- =========================================================

CREATE TABLE sales_return_items (
    return_item_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    return_id BIGINT UNSIGNED NOT NULL,
    order_item_id BIGINT UNSIGNED NOT NULL,

    return_quantity INT UNSIGNED NOT NULL,

    estimated_refund_amount DECIMAL(14,2) NOT NULL DEFAULT 0.00,
    actual_refund DECIMAL(14,2) NULL,

    PRIMARY KEY (return_item_id),

    UNIQUE KEY uk_return_order_item
        (return_id, order_item_id),

    KEY idx_return_item_order_item (order_item_id),

    CONSTRAINT fk_return_item_return
        FOREIGN KEY (return_id)
        REFERENCES sales_returns(return_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_return_item_order_item
        FOREIGN KEY (order_item_id)
        REFERENCES sales_order_items(order_item_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT chk_return_quantity
        CHECK (return_quantity > 0),

    CONSTRAINT chk_estimated_refund
        CHECK (estimated_refund_amount >= 0),

    CONSTRAINT chk_actual_refund
        CHECK (
            actual_refund IS NULL
            OR actual_refund >= 0
        )
) ENGINE=InnoDB;