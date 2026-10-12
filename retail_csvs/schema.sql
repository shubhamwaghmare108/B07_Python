-- ============================================================
-- Database: retail
-- Character set: utf8mb4
-- Engine: InnoDB (for foreign key support)
-- ============================================================

SET FOREIGN_KEY_CHECKS = 0;

-- ------------------------------------------------------------
-- Lookup tables (reference data)
-- ------------------------------------------------------------

DROP TABLE IF EXISTS `lookup_gender`;
CREATE TABLE `lookup_gender` (
    `gender_code` CHAR(1) NOT NULL,
    `gender_name` VARCHAR(20) NOT NULL,
    PRIMARY KEY (`gender_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `lookup_channel`;
CREATE TABLE `lookup_channel` (
    `channel_id` INT NOT NULL AUTO_INCREMENT,
    `channel_name` VARCHAR(50) NOT NULL,
    PRIMARY KEY (`channel_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `lookup_order_status`;
CREATE TABLE `lookup_order_status` (
    `status_id` INT NOT NULL AUTO_INCREMENT,
    `status_name` VARCHAR(50) NOT NULL,
    PRIMARY KEY (`status_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `lookup_payment_mode`;
CREATE TABLE `lookup_payment_mode` (
    `payment_mode_id` INT NOT NULL AUTO_INCREMENT,
    `payment_mode_name` VARCHAR(50) NOT NULL,
    PRIMARY KEY (`payment_mode_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `lookup_return_status`;
CREATE TABLE `lookup_return_status` (
    `return_status_id` INT NOT NULL AUTO_INCREMENT,
    `status_name` VARCHAR(50) NOT NULL,
    PRIMARY KEY (`return_status_id`),
    UNIQUE KEY `uk_status_name` (`status_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ------------------------------------------------------------
-- Main tables
-- ------------------------------------------------------------

DROP TABLE IF EXISTS `brands`;
CREATE TABLE `brands` (
    `brand_id` BIGINT NOT NULL AUTO_INCREMENT,
    `brand_name` VARCHAR(100) NOT NULL,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`brand_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `categories`;
CREATE TABLE `categories` (
    `category_id` BIGINT NOT NULL AUTO_INCREMENT,
    `category_name` VARCHAR(100) NOT NULL,
    `parent_category_id` BIGINT DEFAULT NULL,
    `level` TINYINT NOT NULL DEFAULT 1, -- assuming level 1 = top
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`category_id`),
    CONSTRAINT `fk_categories_parent` FOREIGN KEY (`parent_category_id`)
        REFERENCES `categories` (`category_id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `stores`;
CREATE TABLE `stores` (
    `store_id` BIGINT NOT NULL AUTO_INCREMENT,
    `store_code` VARCHAR(20) NOT NULL,
    `store_name` VARCHAR(100) NOT NULL,
    `city` VARCHAR(50) NOT NULL,
    `state` VARCHAR(50) NOT NULL,
    `city_tier` TINYINT DEFAULT NULL, -- 1,2,3
    `cluster_zone` VARCHAR(50) DEFAULT NULL,
    `store_type` VARCHAR(50) DEFAULT NULL,
    `store_size_sqft` INT DEFAULT NULL,
    `opening_date` DATE DEFAULT NULL,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`store_id`),
    UNIQUE KEY `uk_store_code` (`store_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `suppliers`;
CREATE TABLE `suppliers` (
    `supplier_id` BIGINT NOT NULL AUTO_INCREMENT,
    `supplier_code` VARCHAR(20) NOT NULL,
    `supplier_name` VARCHAR(100) NOT NULL,
    `supplier_type` VARCHAR(50) DEFAULT NULL,
    `city` VARCHAR(50) DEFAULT NULL,
    `state` VARCHAR(50) DEFAULT NULL,
    `payment_days` INT DEFAULT NULL,
    `lead_time_days` INT DEFAULT NULL,
    `annual_contract_value_lakh` DECIMAL(10,2) DEFAULT NULL,
    `is_preferred_vendor` BOOLEAN DEFAULT FALSE,
    `years_associated` INT DEFAULT NULL,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`supplier_id`),
    UNIQUE KEY `uk_supplier_code` (`supplier_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `customer`;
CREATE TABLE `customer` (
    `customer_id` INT NOT NULL AUTO_INCREMENT,
    `customer_code` VARCHAR(20) NOT NULL,
    `customer_name` VARCHAR(100) NOT NULL,
    `gender` CHAR(1) DEFAULT NULL, -- 'M','F','O'
    `age_group` VARCHAR(20) DEFAULT NULL, -- e.g., '18-24','25-34'
    `city` VARCHAR(50) DEFAULT NULL,
    `state` VARCHAR(50) DEFAULT NULL,
    `city_tier` TINYINT DEFAULT NULL,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`customer_id`),
    UNIQUE KEY `uk_customer_code` (`customer_code`),
    CONSTRAINT `fk_customer_gender` FOREIGN KEY (`gender`)
        REFERENCES `lookup_gender` (`gender_code`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `products`;
CREATE TABLE `products` (
    `product_id` BIGINT NOT NULL AUTO_INCREMENT,
    `product_code` VARCHAR(30) NOT NULL,
    `product_name` VARCHAR(200) NOT NULL,
    `brand_id` BIGINT DEFAULT NULL,
    `category_id` BIGINT DEFAULT NULL,
    `sub_category_id` BIGINT DEFAULT NULL, -- can be FK to categories as well
    `mrp` DECIMAL(10,2) NOT NULL,
    `cost_price` DECIMAL(10,2) NOT NULL,
    `gross_margin_pct` DECIMAL(5,2) GENERATED ALWAYS AS (ROUND((mrp - cost_price) / mrp * 100, 2)) STORED, -- computed, optional
    `is_perishable` BOOLEAN DEFAULT FALSE,
    `veg_nonveg` VARCHAR(10) DEFAULT NULL, -- 'Veg', 'Non-Veg', 'Vegan'
    `max_qty_per_transaction` INT DEFAULT NULL,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`product_id`),
    UNIQUE KEY `uk_product_code` (`product_code`),
    CONSTRAINT `fk_products_brand` FOREIGN KEY (`brand_id`)
        REFERENCES `brands` (`brand_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT `fk_products_category` FOREIGN KEY (`category_id`)
        REFERENCES `categories` (`category_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT `fk_products_sub_category` FOREIGN KEY (`sub_category_id`)
        REFERENCES `categories` (`category_id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `inventory`;
CREATE TABLE `inventory` (
    `inventory_id` BIGINT NOT NULL AUTO_INCREMENT,
    `product_id` BIGINT NOT NULL,
    `store_id` BIGINT NOT NULL,
    `quantity_on_hand` INT NOT NULL DEFAULT 0,
    `quantity_reserved` INT NOT NULL DEFAULT 0,
    `reorder_point` INT DEFAULT NULL,
    `last_updated` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`inventory_id`),
    UNIQUE KEY `uk_product_store` (`product_id`, `store_id`), -- one row per product per store
    CONSTRAINT `fk_inventory_product` FOREIGN KEY (`product_id`)
        REFERENCES `products` (`product_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT `fk_inventory_store` FOREIGN KEY (`store_id`)
        REFERENCES `stores` (`store_id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `sales_orders`;
CREATE TABLE `sales_orders` (
    `order_id` BIGINT NOT NULL AUTO_INCREMENT,
    `order_number` VARCHAR(30) NOT NULL,
    `store_id` BIGINT NOT NULL,
    `order_date` DATE NOT NULL,
    `status_id` INT NOT NULL,
    `payment_mode_id` INT NOT NULL,
    `channel_id` INT NOT NULL,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `total_amount` DECIMAL(12,2) NOT NULL, -- gross total before discounts
    `discount_amount` DECIMAL(12,2) DEFAULT 0.00,
    `net_amount` DECIMAL(12,2) NOT NULL,
    `customer_id` INT DEFAULT NULL, -- NULL for walk-in
    PRIMARY KEY (`order_id`),
    UNIQUE KEY `uk_order_number` (`order_number`),
    CONSTRAINT `fk_orders_store` FOREIGN KEY (`store_id`)
        REFERENCES `stores` (`store_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT `fk_orders_status` FOREIGN KEY (`status_id`)
        REFERENCES `lookup_order_status` (`status_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT `fk_orders_payment` FOREIGN KEY (`payment_mode_id`)
        REFERENCES `lookup_payment_mode` (`payment_mode_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT `fk_orders_channel` FOREIGN KEY (`channel_id`)
        REFERENCES `lookup_channel` (`channel_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT `fk_orders_customer` FOREIGN KEY (`customer_id`)
        REFERENCES `customer` (`customer_id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `sales_order_items`;
CREATE TABLE `sales_order_items` (
    `order_item_id` BIGINT NOT NULL AUTO_INCREMENT,
    `order_id` BIGINT NOT NULL,
    `product_id` BIGINT NOT NULL,
    `quantity` INT NOT NULL,
    `unit_price` DECIMAL(10,2) NOT NULL, -- price per unit at time of order
    `discount_percent` DECIMAL(5,2) DEFAULT 0.00,
    `discount_amount` DECIMAL(12,2) DEFAULT 0.00, -- total discount for this line
    `net_price` DECIMAL(12,2) NOT NULL, -- net line total = quantity * unit_price - discount_amount
    PRIMARY KEY (`order_item_id`),
    CONSTRAINT `fk_orderitems_order` FOREIGN KEY (`order_id`)
        REFERENCES `sales_orders` (`order_id`) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT `fk_orderitems_product` FOREIGN KEY (`product_id`)
        REFERENCES `products` (`product_id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `sales_returns`;
CREATE TABLE `sales_returns` (
    `return_id` BIGINT NOT NULL AUTO_INCREMENT,
    `order_id` BIGINT NOT NULL,
    `return_date` DATE NOT NULL,
    `return_status_id` INT NOT NULL,
    `reason` VARCHAR(255) DEFAULT NULL,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`return_id`),
    CONSTRAINT `fk_returns_order` FOREIGN KEY (`order_id`)
        REFERENCES `sales_orders` (`order_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT `fk_returns_status` FOREIGN KEY (`return_status_id`)
        REFERENCES `lookup_return_status` (`return_status_id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `sales_return_items`;
CREATE TABLE `sales_return_items` (
    `return_item_id` BIGINT NOT NULL AUTO_INCREMENT,
    `return_id` BIGINT NOT NULL,
    `order_item_id` BIGINT NOT NULL,
    `return_quantity` INT NOT NULL,
    `estimated_refund_amount` DECIMAL(12,2) NOT NULL, -- based on original net price * quantity
    `actual_refund` DECIMAL(12,2) DEFAULT NULL,
    PRIMARY KEY (`return_item_id`),
    CONSTRAINT `fk_returnitems_return` FOREIGN KEY (`return_id`)
        REFERENCES `sales_returns` (`return_id`) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT `fk_returnitems_orderitem` FOREIGN KEY (`order_item_id`)
        REFERENCES `sales_order_items` (`order_item_id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `product_suppliers`;
CREATE TABLE `product_suppliers` (
    `product_supplier_id` BIGINT NOT NULL AUTO_INCREMENT,
    `product_id` BIGINT NOT NULL,
    `supplier_id` BIGINT NOT NULL,
    `supplier_cost` DECIMAL(10,2) NOT NULL,
    `is_primary` BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (`product_supplier_id`),
    UNIQUE KEY `uk_product_supplier` (`product_id`, `supplier_id`), -- avoid duplicates
    CONSTRAINT `fk_ps_product` FOREIGN KEY (`product_id`)
        REFERENCES `products` (`product_id`) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT `fk_ps_supplier` FOREIGN KEY (`supplier_id`)
        REFERENCES `suppliers` (`supplier_id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Add indexes on frequently queried foreign keys and date columns for performance
CREATE INDEX idx_inventory_product ON inventory (product_id);
CREATE INDEX idx_inventory_store ON inventory (store_id);
CREATE INDEX idx_sales_orders_store ON sales_orders (store_id);
CREATE INDEX idx_sales_orders_customer ON sales_orders (customer_id);
CREATE INDEX idx_sales_orders_date ON sales_orders (order_date);
CREATE INDEX idx_sales_orders_status ON sales_orders (status_id);
CREATE INDEX idx_sales_order_items_order ON sales_order_items (order_id);
CREATE INDEX idx_sales_order_items_product ON sales_order_items (product_id);
CREATE INDEX idx_sales_returns_order ON sales_returns (order_id);
CREATE INDEX idx_sales_returns_date ON sales_returns (return_date);
CREATE INDEX idx_product_suppliers_product ON product_suppliers (product_id);
CREATE INDEX idx_product_suppliers_supplier ON product_suppliers (supplier_id);
CREATE INDEX idx_products_category ON products (category_id);
CREATE INDEX idx_products_subcategory ON products (sub_category_id);
CREATE INDEX idx_products_brand ON products (brand_id);

SET FOREIGN_KEY_CHECKS = 1;