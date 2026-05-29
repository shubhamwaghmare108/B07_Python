-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: retail_dw
-- ------------------------------------------------------
-- Server version	8.0.41

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `dim_customer`
--

DROP TABLE IF EXISTS `dim_customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dim_customer` (
  `customer_id` varchar(20) NOT NULL,
  `customer_name` varchar(255) DEFAULT NULL,
  `gender` varchar(20) DEFAULT NULL,
  `age_group` varchar(50) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `state` varchar(100) DEFAULT NULL,
  `city_tier` int DEFAULT NULL,
  `is_registered` varchar(10) DEFAULT NULL,
  `loyalty_member` varchar(10) DEFAULT NULL,
  `store_id` varchar(20) DEFAULT NULL,
  `avg_monthly_spend_inr` decimal(12,2) DEFAULT NULL,
  `visit_frequency_per_month` int DEFAULT NULL,
  PRIMARY KEY (`customer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dim_date`
--

DROP TABLE IF EXISTS `dim_date`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dim_date` (
  `date_id` int NOT NULL,
  `full_date` date DEFAULT NULL,
  `year` int DEFAULT NULL,
  `quarter` int DEFAULT NULL,
  `quarter_label` varchar(20) DEFAULT NULL,
  `month` int DEFAULT NULL,
  `month_name` varchar(20) DEFAULT NULL,
  `day` int DEFAULT NULL,
  `day_of_week` int DEFAULT NULL,
  `weekday_name` varchar(20) DEFAULT NULL,
  `is_weekend` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`date_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dim_product`
--

DROP TABLE IF EXISTS `dim_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dim_product` (
  `product_id` varchar(20) NOT NULL,
  `product_name` varchar(255) DEFAULT NULL,
  `brand` varchar(100) DEFAULT NULL,
  `category` varchar(100) DEFAULT NULL,
  `sub_category` varchar(100) DEFAULT NULL,
  `sub_sub_category` varchar(100) DEFAULT NULL,
  `variant_name` varchar(100) DEFAULT NULL,
  `mrp` decimal(10,2) DEFAULT NULL,
  `cost_price` decimal(10,2) DEFAULT NULL,
  `gross_margin_pct` decimal(10,4) DEFAULT NULL,
  `is_perishable` varchar(10) DEFAULT NULL,
  `veg_nonveg` varchar(20) DEFAULT NULL,
  `max_qty_per_transaction` int DEFAULT NULL,
  PRIMARY KEY (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dim_store`
--

DROP TABLE IF EXISTS `dim_store`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dim_store` (
  `store_id` varchar(20) NOT NULL,
  `store_name` varchar(255) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `state` varchar(100) DEFAULT NULL,
  `city_tier` int DEFAULT NULL,
  `cluster_zone` varchar(50) DEFAULT NULL,
  `store_type` varchar(50) DEFAULT NULL,
  `store_size_sqft` int DEFAULT NULL,
  `owned_or_leased` varchar(20) DEFAULT NULL,
  `opening_date` date DEFAULT NULL,
  `total_checkouts` int DEFAULT NULL,
  `parking_capacity` int DEFAULT NULL,
  `distribution_center` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`store_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dim_supplier`
--

DROP TABLE IF EXISTS `dim_supplier`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dim_supplier` (
  `supplier_id` varchar(20) NOT NULL,
  `supplier_name` varchar(255) DEFAULT NULL,
  `supplier_type` varchar(100) DEFAULT NULL,
  `category` varchar(100) DEFAULT NULL,
  `state` varchar(100) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `payment_days` int DEFAULT NULL,
  `lead_time_days` int DEFAULT NULL,
  `annual_contract_value_lakh` decimal(12,2) DEFAULT NULL,
  `is_preferred_vendor` varchar(10) DEFAULT NULL,
  `years_associated` int DEFAULT NULL,
  PRIMARY KEY (`supplier_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `fact_inventory`
--

DROP TABLE IF EXISTS `fact_inventory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fact_inventory` (
  `inventory_key` bigint NOT NULL AUTO_INCREMENT,
  `store_id` varchar(20) DEFAULT NULL,
  `product_id` varchar(20) DEFAULT NULL,
  `week_start_date` date DEFAULT NULL,
  `opening_stock_units` int DEFAULT NULL,
  `units_sold` int DEFAULT NULL,
  `units_received` int DEFAULT NULL,
  `closing_stock_units` int DEFAULT NULL,
  `stockout_flag` tinyint(1) DEFAULT NULL,
  `reorder_triggered` tinyint(1) DEFAULT NULL,
  `days_of_stock_remaining` decimal(10,2) DEFAULT NULL,
  `inventory_value_inr` decimal(14,2) DEFAULT NULL,
  `week_start_date_key` int DEFAULT NULL,
  PRIMARY KEY (`inventory_key`),
  KEY `fk_inventory_date` (`week_start_date_key`),
  KEY `idx_inventory_product` (`product_id`),
  KEY `idx_inventory_store` (`store_id`),
  CONSTRAINT `fk_inventory_date` FOREIGN KEY (`week_start_date_key`) REFERENCES `dim_date` (`date_id`),
  CONSTRAINT `fk_inventory_product` FOREIGN KEY (`product_id`) REFERENCES `dim_product` (`product_id`),
  CONSTRAINT `fk_inventory_store` FOREIGN KEY (`store_id`) REFERENCES `dim_store` (`store_id`)
) ENGINE=InnoDB AUTO_INCREMENT=65536 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `fact_transaction`
--

DROP TABLE IF EXISTS `fact_transaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fact_transaction` (
  `transaction_key` bigint NOT NULL AUTO_INCREMENT,
  `transaction_id` varchar(30) DEFAULT NULL,
  `bill_date` date DEFAULT NULL,
  `store_id` varchar(20) DEFAULT NULL,
  `customer_id` varchar(20) DEFAULT NULL,
  `product_id` varchar(20) DEFAULT NULL,
  `supplier_id` varchar(20) DEFAULT NULL,
  `channel` varchar(50) DEFAULT NULL,
  `quantity` int DEFAULT NULL,
  `mrp` decimal(10,2) DEFAULT NULL,
  `discount_pct` decimal(8,4) DEFAULT NULL,
  `discount_amount` decimal(10,2) DEFAULT NULL,
  `sale_price` decimal(10,2) DEFAULT NULL,
  `total_sale_amount` decimal(14,2) DEFAULT NULL,
  `total_cost` decimal(14,2) DEFAULT NULL,
  `gross_profit` decimal(14,4) DEFAULT NULL,
  `gross_margin_pct` decimal(8,4) DEFAULT NULL,
  `payment_mode` varchar(50) DEFAULT NULL,
  `is_festive_period` varchar(10) DEFAULT NULL,
  `festival_name` varchar(100) DEFAULT NULL,
  `return_flag` varchar(10) DEFAULT NULL,
  `date_id` int DEFAULT NULL,
  PRIMARY KEY (`transaction_key`),
  KEY `fk_transaction_supplier` (`supplier_id`),
  KEY `fk_transaction_date` (`date_id`),
  KEY `idx_transaction_product` (`product_id`),
  KEY `idx_transaction_customer` (`customer_id`),
  KEY `idx_transaction_store` (`store_id`),
  CONSTRAINT `fk_transaction_customer` FOREIGN KEY (`customer_id`) REFERENCES `dim_customer` (`customer_id`),
  CONSTRAINT `fk_transaction_date` FOREIGN KEY (`date_id`) REFERENCES `dim_date` (`date_id`),
  CONSTRAINT `fk_transaction_product` FOREIGN KEY (`product_id`) REFERENCES `dim_product` (`product_id`),
  CONSTRAINT `fk_transaction_store` FOREIGN KEY (`store_id`) REFERENCES `dim_store` (`store_id`),
  CONSTRAINT `fk_transaction_supplier` FOREIGN KEY (`supplier_id`) REFERENCES `dim_supplier` (`supplier_id`)
) ENGINE=InnoDB AUTO_INCREMENT=65536 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-05-29 11:56:32
