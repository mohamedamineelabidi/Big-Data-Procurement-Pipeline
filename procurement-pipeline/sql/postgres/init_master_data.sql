-- Initialize Master Data

-- 1. Clean up existing tables
DROP TABLE IF EXISTS replenishment_rules;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS suppliers;

-- 2. Create Tables
CREATE TABLE products (
    product_id VARCHAR(50) PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    case_size INT NOT NULL,
    price DECIMAL(10, 2)
);

CREATE TABLE suppliers (
    supplier_id VARCHAR(50) PRIMARY KEY,
    supplier_name VARCHAR(255) NOT NULL,
    contact_email VARCHAR(255),
    lead_time_days INT
);

CREATE TABLE replenishment_rules (
    rule_id SERIAL PRIMARY KEY,
    product_id VARCHAR(50) REFERENCES products(product_id),
    supplier_id VARCHAR(50) REFERENCES suppliers(supplier_id),
    moq INT NOT NULL DEFAULT 1,
    safety_stock_level INT NOT NULL DEFAULT 0,
    UNIQUE(product_id, supplier_id)
);

-- 3. Populate Mock Data
-- Suppliers
INSERT INTO suppliers (supplier_id, supplier_name, contact_email, lead_time_days) VALUES
('SUP-001', 'Acme Corp', 'orders@acme.com', 3),
('SUP-002', 'Global Foods', 'sales@globalfoods.com', 5),
('SUP-003', 'TechParts Inc', 'supply@techparts.com', 7),
('SUP-004', 'FreshMart Wholesale', 'procurement@freshmart.com', 2),
('SUP-005', 'ElectroSupply Co', 'sales@electrosupply.com', 4),
('SUP-006', 'BevCo Distributors', 'orders@bevco.com', 3),
('SUP-007', 'SnackWorld Inc', 'supply@snackworld.com', 6),
('SUP-008', 'DairyFresh LLC', 'orders@dairyfresh.com', 2),
('SUP-009', 'TechGear Plus', 'sales@techgearplus.com', 5),
('SUP-010', 'HomeGoods Supply', 'procurement@homegoods.com', 4);

-- Products (50 items across various categories)
INSERT INTO products (product_id, product_name, category, case_size, price) VALUES
-- Beverages
('SKU-0001', 'Organic Apple Juice', 'Beverages', 24, 15.50),
('SKU-0005', 'Almond Milk', 'Beverages', 12, 4.50),
('SKU-0011', 'Orange Juice 1L', 'Beverages', 12, 5.99),
('SKU-0012', 'Cola 2L', 'Beverages', 6, 2.49),
('SKU-0013', 'Mineral Water 500ml', 'Beverages', 24, 0.99),
('SKU-0014', 'Energy Drink', 'Beverages', 24, 3.99),
('SKU-0015', 'Green Tea', 'Beverages', 20, 4.50),
-- Bakery
('SKU-0002', 'Whole Wheat Bread', 'Bakery', 12, 3.20),
('SKU-0021', 'Croissant Pack', 'Bakery', 6, 8.99),
('SKU-0022', 'Bagels 6pk', 'Bakery', 8, 4.50),
('SKU-0023', 'Muffins Assorted', 'Bakery', 12, 6.99),
('SKU-0024', 'Baguette', 'Bakery', 10, 2.50),
-- Electronics
('SKU-0003', 'Wireless Mouse', 'Electronics', 10, 25.00),
('SKU-0004', 'LED Monitor 24"', 'Electronics', 1, 150.00),
('SKU-0031', 'USB Cable 2m', 'Electronics', 50, 5.99),
('SKU-0032', 'Bluetooth Speaker', 'Electronics', 12, 45.00),
('SKU-0033', 'Webcam HD', 'Electronics', 8, 65.00),
('SKU-0034', 'Keyboard Wireless', 'Electronics', 10, 35.00),
('SKU-0035', 'Headphones', 'Electronics', 15, 29.99),
-- Dairy
('SKU-0041', 'Milk 2%', 'Dairy', 12, 3.99),
('SKU-0042', 'Greek Yogurt', 'Dairy', 16, 1.50),
('SKU-0043', 'Cheddar Cheese', 'Dairy', 10, 5.99),
('SKU-0044', 'Butter', 'Dairy', 20, 4.50),
('SKU-0045', 'Cream Cheese', 'Dairy', 12, 3.50),
-- Snacks
('SKU-0051', 'Potato Chips', 'Snacks', 24, 2.99),
('SKU-0052', 'Chocolate Bar', 'Snacks', 48, 1.50),
('SKU-0053', 'Granola Bar Box', 'Snacks', 12, 5.99),
('SKU-0054', 'Mixed Nuts', 'Snacks', 16, 7.99),
('SKU-0055', 'Popcorn', 'Snacks', 20, 3.50),
-- Fresh Produce
('SKU-0061', 'Bananas', 'Produce', 1, 1.99),
('SKU-0062', 'Apples', 'Produce', 1, 2.50),
('SKU-0063', 'Tomatoes', 'Produce', 1, 3.99),
('SKU-0064', 'Lettuce', 'Produce', 1, 2.50),
('SKU-0065', 'Carrots', 'Produce', 1, 1.99),
-- Frozen Foods
('SKU-0071', 'Frozen Pizza', 'Frozen', 12, 6.99),
('SKU-0072', 'Ice Cream', 'Frozen', 8, 5.50),
('SKU-0073', 'Frozen Vegetables', 'Frozen', 16, 3.99),
('SKU-0074', 'Chicken Nuggets', 'Frozen', 12, 7.99),
('SKU-0075', 'Frozen Fries', 'Frozen', 20, 4.50),
-- Household
('SKU-0081', 'Paper Towels', 'Household', 12, 8.99),
('SKU-0082', 'Toilet Paper 12pk', 'Household', 4, 12.99),
('SKU-0083', 'Dish Soap', 'Household', 24, 3.50),
('SKU-0084', 'Laundry Detergent', 'Household', 6, 14.99),
('SKU-0085', 'Trash Bags', 'Household', 10, 9.99),
-- Personal Care
('SKU-0091', 'Shampoo', 'Personal Care', 12, 6.99),
('SKU-0092', 'Toothpaste', 'Personal Care', 24, 3.50),
('SKU-0093', 'Hand Soap', 'Personal Care', 20, 2.99),
('SKU-0094', 'Deodorant', 'Personal Care', 18, 4.99),
('SKU-0095', 'Body Lotion', 'Personal Care', 12, 7.99);

-- Replenishment Rules (one rule per product)
INSERT INTO replenishment_rules (product_id, supplier_id, moq, safety_stock_level) VALUES
('SKU-0001', 'SUP-006', 50, 100),
('SKU-0002', 'SUP-004', 20, 50),
('SKU-0003', 'SUP-005', 100, 200),
('SKU-0004', 'SUP-005', 5, 10),
('SKU-0005', 'SUP-006', 40, 80),
('SKU-0011', 'SUP-006', 30, 60),
('SKU-0012', 'SUP-006', 40, 100),
('SKU-0013', 'SUP-006', 50, 150),
('SKU-0014', 'SUP-006', 30, 80),
('SKU-0015', 'SUP-006', 25, 50),
('SKU-0021', 'SUP-004', 15, 30),
('SKU-0022', 'SUP-004', 20, 40),
('SKU-0023', 'SUP-004', 18, 35),
('SKU-0024', 'SUP-004', 25, 50),
('SKU-0031', 'SUP-005', 100, 300),
('SKU-0032', 'SUP-009', 20, 50),
('SKU-0033', 'SUP-009', 15, 30),
('SKU-0034', 'SUP-005', 25, 60),
('SKU-0035', 'SUP-009', 30, 80),
('SKU-0041', 'SUP-008', 40, 100),
('SKU-0042', 'SUP-008', 50, 120),
('SKU-0043', 'SUP-008', 30, 70),
('SKU-0044', 'SUP-008', 35, 80),
('SKU-0045', 'SUP-008', 25, 60),
('SKU-0051', 'SUP-007', 50, 150),
('SKU-0052', 'SUP-007', 100, 250),
('SKU-0053', 'SUP-007', 30, 80),
('SKU-0054', 'SUP-007', 40, 100),
('SKU-0055', 'SUP-007', 45, 120),
('SKU-0061', 'SUP-004', 10, 30),
('SKU-0062', 'SUP-004', 10, 30),
('SKU-0063', 'SUP-004', 10, 25),
('SKU-0064', 'SUP-004', 10, 20),
('SKU-0065', 'SUP-004', 10, 25),
('SKU-0071', 'SUP-004', 25, 60),
('SKU-0072', 'SUP-008', 20, 50),
('SKU-0073', 'SUP-004', 30, 80),
('SKU-0074', 'SUP-004', 25, 70),
('SKU-0075', 'SUP-004', 35, 90),
('SKU-0081', 'SUP-010', 30, 80),
('SKU-0082', 'SUP-010', 20, 50),
('SKU-0083', 'SUP-010', 50, 120),
('SKU-0084', 'SUP-010', 15, 40),
('SKU-0085', 'SUP-010', 25, 60),
('SKU-0091', 'SUP-010', 30, 75),
('SKU-0092', 'SUP-010', 50, 130),
('SKU-0093', 'SUP-010', 40, 100),
('SKU-0094', 'SUP-010', 35, 90),
('SKU-0095', 'SUP-010', 30, 80);
