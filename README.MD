# 🏭 Procurement Data Pipeline

**Module:** Fondements Big Data (ENSA Al Hoceima)  
**Academic Year:** 2025-2026  
**Branch:** `data_ing-phase3`

---

## 📌 Project Overview

This project implements a **batch-oriented data pipeline** for a retail procurement system. The system collects daily customer orders from 15 Points of Sale (POS) and warehouse stock levels from 5 warehouses, then calculates net demand and automatically generates supplier replenishment orders.

### 🎯 Business Objective

Transform raw sales and inventory data into actionable procurement decisions:

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   15 Retail     │     │   Data Pipeline │     │   5 Supplier    │
│    Stores       │ ──▶ │   Processing    │ ──▶ │    Orders       │
│  (JSON Orders)  │     │   (Batch ETL)   │     │   (JSON Files)  │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

### ⚠️ Key Constraints

| Constraint | Description |
|------------|-------------|
| **Batch Only** | No streaming technologies (Kafka/Flink/Spark Streaming) allowed |
| **Distributed** | Uses HDFS for storage and Trino for distributed SQL queries |
| **Separation** | Clearly separated OLTP (PostgreSQL) and Analytical (HDFS) layers |
| **Time Window** | Pipeline runs in 22:00 - 00:00 batch window |

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         PROCUREMENT PIPELINE ARCHITECTURE                        │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│   DATA SOURCES                                                                   │
│   ════════════                                                                   │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                      │
│   │   15 POS     │    │  5 Warehouses │    │  PostgreSQL  │                      │
│   │   Stores     │    │    Stock      │    │  Master Data │                      │
│   │  (JSON)      │    │   (CSV)       │    │  (Products,  │                      │
│   │              │    │              │    │  Suppliers)  │                      │
│   └──────┬───────┘    └──────┬───────┘    └──────┬───────┘                      │
│          │                   │                   │                               │
│          ▼                   ▼                   │                               │
│   ┌─────────────────────────────────────┐       │                               │
│   │         HDFS DATA LAKE              │       │                               │
│   │  ┌─────────────┐ ┌─────────────┐   │       │                               │
│   │  │ /raw/orders │ │ /raw/stock  │   │       │                               │
│   │  │  105 files  │ │  35 files   │   │       │                               │
│   │  └─────────────┘ └─────────────┘   │       │                               │
│   └──────────────────┬──────────────────┘       │                               │
│                      │                           │                               │
│                      ▼                           ▼                               │
│   ┌─────────────────────────────────────────────────────────────────┐           │
│   │                      TRINO QUERY ENGINE                          │           │
│   │         (Federated SQL across HDFS + PostgreSQL)                │           │
│   │                                                                  │           │
│   │  ┌─────────────────┐              ┌─────────────────┐          │           │
│   │  │  Hive Catalog   │              │ PostgreSQL      │          │           │
│   │  │  (HDFS Data)    │              │ Catalog         │          │           │
│   │  └─────────────────┘              └─────────────────┘          │           │
│   └──────────────────────────┬──────────────────────────────────────┘           │
│                              │                                                   │
│                              ▼                                                   │
│   ┌─────────────────────────────────────────────────────────────────┐           │
│   │                    PYTHON PROCESSING                             │           │
│   │                                                                  │           │
│   │  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐   │           │
│   │  │ Aggregate  │ │ Calculate  │ │ Apply      │ │ Generate   │   │           │
│   │  │ Demand     │ │ Net Demand │ │ Business   │ │ Reports    │   │           │
│   │  │            │ │            │ │ Rules      │ │            │   │           │
│   │  └────────────┘ └────────────┘ └────────────┘ └────────────┘   │           │
│   └──────────────────────────┬──────────────────────────────────────┘           │
│                              │                                                   │
│                              ▼                                                   │
│   ┌─────────────────────────────────────────────────────────────────┐           │
│   │                      OUTPUT LAYER                                │           │
│   │                                                                  │           │
│   │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │           │
│   │  │ Supplier    │  │ Exception   │  │ Pipeline    │              │           │
│   │  │ Orders      │  │ Reports     │  │ Summary     │              │           │
│   │  │ (5 JSON)    │  │ (JSON+TXT)  │  │ (TXT)       │              │           │
│   │  └─────────────┘  └─────────────┘  └─────────────┘              │           │
│   └─────────────────────────────────────────────────────────────────┘           │
│                                                                                  │
│   ORCHESTRATION                                                                  │
│   ═════════════                                                                  │
│   ┌─────────────────────────────────────────────────────────────────┐           │
│   │                    APACHE AIRFLOW                                │           │
│   │         Schedule: Daily at 22:00 | DAG: procurement_daily       │           │
│   └─────────────────────────────────────────────────────────────────┘           │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 💻 Technical Stack

| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| **Container Platform** | Docker Compose | 3.x | Infrastructure orchestration |
| **Data Lake** | Apache HDFS | 3.2.1 | Distributed file storage |
| **OLTP Database** | PostgreSQL | 13 | Master data storage |
| **Query Engine** | Trino | 479 | Distributed SQL processing |
| **Orchestration** | Apache Airflow | 2.7.3 | Workflow automation |
| **Programming** | Python | 3.10+ | Data processing scripts |
| **Web UI** | pgAdmin | Latest | Database management |

### Python Dependencies

```
pandas>=2.0.0          # Data manipulation
trino>=0.327.0         # Trino Python client
psycopg2-binary>=2.9.0 # PostgreSQL client
faker>=18.0.0          # Test data generation
```

### Why These Technologies?

**HDFS (Hadoop Distributed File System)**
- ✅ Fault tolerance with 3x replication
- ✅ Scalable from GB to PB
- ✅ Industry standard for big data storage
- ✅ Academic requirement: distributed storage

**Trino (formerly PrestoSQL)**
- ✅ Query multiple data sources with one SQL
- ✅ Federates HDFS + PostgreSQL queries
- ✅ Optimized for analytical workloads
- ✅ No data movement required

**PostgreSQL**
- ✅ ACID compliance for master data
- ✅ Rich data types and constraints
- ✅ Battle-tested reliability
- ✅ Perfect for OLTP workloads

**Apache Airflow**
- ✅ Visual DAG representation
- ✅ Retry logic and error handling
- ✅ Monitoring and alerting
- ✅ Industry standard for orchestration

---

## 📊 Business Logic

### 1. Net Demand Formula

The core replenishment calculation:

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│   Net Demand = Total Orders - Available Stock + Safety Stock    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Real-World Example - Step by Step:**

```
Product: Whole Milk 1L (SKU-0002)
════════════════════════════════════════════════════════════

📅 Step 1: Aggregate Orders (Last 7 Days)
   Day 1 (Dec 28): 65 units
   Day 2 (Dec 29): 72 units
   Day 3 (Dec 30): 68 units
   Day 4 (Dec 31): 80 units  ← Holiday spike
   Day 5 (Jan 01): 85 units  ← Holiday spike
   Day 6 (Jan 02): 70 units
   Day 7 (Jan 03): 80 units
   ────────────────────────
   TOTAL DEMAND: 520 units

📦 Step 2: Check Current Stock
   Warehouse 1: 50 units
   Warehouse 2: 60 units
   Warehouse 3: 40 units
   ────────────────────────
   TOTAL STOCK: 150 units

📋 Step 3: Load Business Rules (PostgreSQL)
   • Supplier: DairyFresh LLC
   • Lead Time: 3 days
   • Safety Stock: 100 units (always keep as buffer)
   • MOQ (Minimum Order): 50 units
   • Case Size: 24 units/case

🧮 Step 4: Calculate Net Demand
   Basic Need = 520 - 150 = 370 units
   Add Safety Buffer = 370 + 100 = 470 units
   
📦 Step 5: Round to Case Size
   Cases Needed = ⌈470 ÷ 24⌉ = 20 cases
   Final Order = 20 × 24 = 480 units ✓

✅ RESULT: Order 480 units (20 cases) from DairyFresh LLC
   Priority: HIGH (stock < 30% of demand)
   Expected Delivery: Jan 06 (3 days)
   Cost: 480 × $4.50 = $2,160.00
```

### 2. Procurement Rules

| Rule | Description | Example |
|------|-------------|---------|
| **MOQ** | Minimum Order Quantity per supplier | Min 50 units |
| **Case Size** | Orders rounded UP to nearest case | 24 units/case → ⌈470÷24⌉ = 20 cases |
| **Priority** | Based on stock coverage | Stock < 30% of demand = HIGH |
| **Lead Time** | Days until delivery | 3 days for dairy products |

**Priority Assignment Logic:**

```python
if current_stock < (demand * 0.10):
    priority = "CRITICAL"     # Less than 10% - Urgent!
elif current_stock < (demand * 0.30):
    priority = "HIGH"         # Less than 30% - Important
elif order_quantity > 5000:
    priority = "HIGH"         # Large order - Plan ahead
else:
    priority = "MEDIUM"       # Standard order
```

### 3. Exception Detection

The system automatically detects anomalies and alerts procurement managers:

| Exception Type | Threshold | Severity | Action Required |
|----------------|-----------|----------|-----------------|
| **HIGH_DEMAND** | > 2,000 units | 🔴 HIGH | Verify with sales team, check for promotions |
| **LOW_STOCK** | Stock < 30% of demand | 🔴 HIGH | Expedite order, consider air freight |
| **CRITICAL_STOCK** | Stock < 10% of demand | 🔴 CRITICAL | Emergency order, notify management |
| **MISSING_SUPPLIER** | No supplier assigned | 🔴 HIGH | Contact procurement to assign supplier |
| **HIGH_VALUE_ORDER** | Order value > $10,000 | 🟡 MEDIUM | Manager approval required |
| **DEMAND_STOCK_GAP** | Demand > 5x stock | 🟡 MEDIUM | Review forecasting model |

**Real Exception Example:**

```json
{
  "exception_id": "EXC-20260103-015",
  "timestamp": "2026-01-03T22:00:45",
  "severity": "HIGH",
  "type": "HIGH_DEMAND",
  "sku": "SKU-0022",
  "product_name": "Bagels 6pk",
  "category": "Bakery",
  "metric_value": 2852,
  "threshold": 2000,
  "percentage_over": 42.6,
  "recommendation": "Unusual demand spike detected. Verify with sales team before ordering. Check for promotions or special events.",
  "context": {
    "normal_weekly_demand": 1400,
    "current_weekly_demand": 2852,
    "variance": "+103.7%"
  }
}
```

---

## 🔄 Pipeline Execution Flow

### Complete Data Journey

```
┌───────────────────────────────────────────────────────────────┐
│  DAY N: Data Collection (09:00 - 21:00)                       │
├───────────────────────────────────────────────────────────────┤
│                                                                │
│  09:00  Stores open, customers start shopping                 │
│         • POS systems record transactions                      │
│         • Each sale creates order items                        │
│                                                                │
│  12:00  Lunch rush - high transaction volume                  │
│         • Average 500 transactions/hour across 15 stores      │
│                                                                │
│  18:00  Evening peak - highest volume                         │
│         • Average 800 transactions/hour                        │
│                                                                │
│  21:00  Stores close                                          │
│         • Daily order files generated                          │
│         • pos_1_2026-01-03.json created (per store)           │
│         • Files contain all day's transactions                 │
│                                                                │
│  21:30  Warehouses complete daily count                       │
│         • Physical inventory verification                      │
│         • warehouse_1_stock_2026-01-03.csv created            │
│         • Contains stock levels for all SKUs                   │
│                                                                │
└───────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────┐
│  DAY N: Pipeline Execution (22:00 - 23:59)                    │
├───────────────────────────────────────────────────────────────┤
│                                                                │
│  22:00:00  🚀 Airflow Triggers Pipeline                       │
│            ├─ Check: All 15 order files present?              │
│            ├─ Check: All 5 stock files present?               │
│            └─ Check: Services healthy?                         │
│                                                                │
│  22:00:05  📊 Stage 1: Data Validation                        │
│            ├─ Validate JSON structure (105 order files)       │
│            ├─ Validate CSV format (35 stock files)            │
│            ├─ Check for missing fields                         │
│            ├─ Validate data types                             │
│            └─ Result: ✅ All files valid                       │
│                                                                │
│  22:00:10  🔍 Stage 2: Demand Calculation                     │
│            │                                                   │
│            ├─ Step 2.1: Load Orders (via Trino)              │
│            │   Query: SELECT * FROM hive.default.orders       │
│            │   WHERE date = '2026-01-03'                      │
│            │   Result: 15,150 order items loaded              │
│            │                                                   │
│            ├─ Step 2.2: Aggregate by SKU                      │
│            │   Query: SELECT sku, SUM(quantity)              │
│            │   GROUP BY sku                                   │
│            │   Result: 50 unique SKUs with totals            │
│            │                                                   │
│            ├─ Step 2.3: Load Stock (via Trino)               │
│            │   Query: SELECT * FROM hive.default.stock       │
│            │   WHERE date = '2026-01-03'                      │
│            │   Result: 250 stock records loaded               │
│            │                                                   │
│            ├─ Step 2.4: Load Master Data (PostgreSQL)        │
│            │   • Products table: 49 products                  │
│            │   • Suppliers table: 10 suppliers                │
│            │   • Rules table: 49 replenishment rules          │
│            │                                                   │
│            ├─ Step 2.5: Calculate Net Demand                  │
│            │   Formula per SKU:                               │
│            │   Net = Total Orders - Stock + Safety Stock     │
│            │   Example: 520 - 150 + 100 = 470 units          │
│            │                                                   │
│            ├─ Step 2.6: Apply Business Rules                  │
│            │   • Round to MOQ multiples                       │
│            │   • Round to case sizes                          │
│            │   • Assign priorities                            │
│            │                                                   │
│            └─ Result: 24 SKUs need 32,748 units               │
│               Output: replenishment_2026-01-03.csv            │
│                                                                │
│  22:00:35  📦 Stage 3: Export Supplier Orders (Parallel)      │
│            ├─ Load replenishment CSV                          │
│            ├─ Group by supplier_name                          │
│            ├─ Generate 5 supplier JSON files:                 │
│            │   ├─ BevCo_Distributors_2026-01-03.json         │
│            │   ├─ DairyFresh_LLC_2026-01-03.json             │
│            │   ├─ ElectroSupply_Co_2026-01-03.json           │
│            │   ├─ FreshMart_Wholesale_2026-01-03.json        │
│            │   └─ TechGear_Plus_2026-01-03.json              │
│            └─ Result: ✅ 5 orders generated                    │
│                                                                │
│  22:00:35  ⚠️  Stage 4: Exception Detection (Parallel)        │
│            ├─ HIGH_DEMAND check: > 2,000 units               │
│            │   Found: 7 SKUs                                  │
│            ├─ LOW_STOCK check: stock < 30% demand            │
│            │   Found: 18 SKUs                                 │
│            ├─ MISSING_SUPPLIER check                          │
│            │   Found: 0 SKUs                                  │
│            ├─ HIGH_VALUE_ORDER check: > $10,000              │
│            │   Found: 3 orders                                │
│            ├─ DEMAND_STOCK_GAP check: demand > 5x stock     │
│            │   Found: 2 SKUs                                  │
│            └─ Result: 30 exceptions detected                  │
│               Output: exception_report_2026-01-03.json        │
│                                                                │
│  22:01:00  📝 Stage 5: Generate Summary                       │
│            ├─ Collect all stage metrics                       │
│            ├─ Format execution report                         │
│            ├─ Calculate performance stats                     │
│            └─ Output: pipeline_run_2026-01-03.txt             │
│                                                                │
│  22:01:06  ✅ Pipeline Complete (Duration: 1.06 seconds)      │
│            └─ Status: SUCCESS                                 │
│                                                                │
└───────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────┐
│  DAY N+1: Business Actions (08:00 - 17:00)                    │
├───────────────────────────────────────────────────────────────┤
│                                                                │
│  08:00  Procurement team reviews reports                      │
│         • Check exception alerts                              │
│         • Review high-value orders                            │
│         • Verify demand spikes                                │
│                                                                │
│  09:00  Send supplier orders                                  │
│         • Email JSON files to suppliers                       │
│         • Confirm order acceptance                            │
│         • Track order status                                  │
│                                                                │
│  10:00  Handle exceptions                                     │
│         • Contact sales for demand spikes                     │
│         • Expedite critical stock items                       │
│         • Resolve missing supplier issues                     │
│                                                                │
│  N+3    Receive supplier deliveries                           │
│         • 3-day lead time typical                             │
│         • Update warehouse stock                              │
│         • Replenish store shelves                             │
│                                                                │
└───────────────────────────────────────────────────────────────┘
```

---

## 📂 Project Structure

```
Big-data/
├── README.MD                          # This file
├── TODO.MD                            # Project roadmap & task tracking
│
└── procurement-pipeline/
    │
    ├── docker-compose.yml             # Infrastructure definition
    │
    ├── airflow/
    │   ├── dags/
    │   │   └── procurement_dag.py     # Airflow DAG (22:00 schedule)
    │   └── logs/                      # Airflow execution logs
    │
    ├── config/
    │   ├── trino/
    │   │   └── postgresql.properties  # Trino PostgreSQL catalog
    │   └── trino-config/
    │       └── config.properties      # Trino server config
    │
    ├── data/
    │   ├── raw/
    │   │   ├── orders/                # Daily POS order files (JSON)
    │   │   │   ├── pos_1_2025-12-28.json
    │   │   │   ├── pos_1_2025-12-29.json
    │   │   │   └── ... (105 files: 15 POS × 7 days)
    │   │   │
    │   │   └── stock/                 # Daily warehouse snapshots (CSV)
    │   │       ├── warehouse_1_2025-12-28.csv
    │   │       └── ... (35 files: 5 warehouses × 7 days)
    │   │
    │   └── output/
    │       ├── replenishment_2026-01-03.csv
    │       ├── pipeline_run_2026-01-03.txt
    │       │
    │       ├── supplier_orders/       # JSON orders per supplier
    │       │   ├── BevCo_Distributors_2026-01-03.json
    │       │   ├── DairyFresh_LLC_2026-01-03.json
    │       │   ├── ElectroSupply_Co_2026-01-03.json
    │       │   ├── FreshMart_Wholesale_2026-01-03.json
    │       │   └── TechGear_Plus_2026-01-03.json
    │       │
    │       └── exceptions/            # Quality control reports
    │           ├── exception_report_2026-01-03.json
    │           └── exception_summary_2026-01-03.txt
    │
    ├── scripts/
    │   ├── data_gen.py                # Faker-based test data generator
    │   ├── generate_orders.py         # Order generation script
    │   ├── ingest_hdfs.py             # HDFS data ingestion
    │   ├── upload_to_hdfs.ps1         # PowerShell upload script
    │   ├── validate_data_quality.py   # Data quality validation
    │   ├── compute_demand.py          # Main demand calculation
    │   ├── export_orders.py           # Supplier JSON generation
    │   ├── generate_exceptions.py     # Anomaly detection & reporting
    │   ├── run_phase4.py              # Phase 4 orchestration
    │   ├── run_pipeline.py            # Master pipeline orchestrator
    │   ├── test_connection.py         # Infrastructure connectivity test
    │   ├── test_trino_catalog.py      # Trino catalog validation
    │   └── test_system.py             # Full system integration test
    │
    └── sql/
        └── postgres/
            ├── schema.sql             # Database schema
            └── init_master_data.sql   # Seed data (products, suppliers)
```

---

## 🚀 Quick Start Guide

### Prerequisites

- Docker Desktop installed and running
- Python 3.10+ with pip
- Git

### 1. Clone Repository

```bash
git clone https://github.com/mohamedamineelabidi/Big-data.git
cd Big-data/procurement-pipeline
```

### 2. Start Infrastructure

```bash
docker-compose up -d
```

### 3. Install Python Dependencies

```bash
pip install pandas trino psycopg2-binary faker
```

### 4. Verify Services

```bash
python scripts/test_connection.py
```

### 5. Run Full Pipeline

```bash
# Run for specific date
python scripts/run_pipeline.py --date 2026-01-03

# Or run system test
python scripts/test_system.py
```

### 6. Access Web Interfaces

| Service | URL | Credentials |
|---------|-----|-------------|
| **Airflow UI** | http://localhost:8081 | admin / admin |
| **Trino UI** | http://localhost:8080 | admin (no password) |
| **pgAdmin** | http://localhost:5050 | admin@admin.com / admin |
| **HDFS UI** | http://localhost:9870 | No auth required |

---

## 📜 Scripts Documentation

### Core Pipeline Scripts

#### **1. run_pipeline.py** - Master Orchestrator

**Purpose:** Executes the complete procurement pipeline with all stages

**Key Features:**
- Infrastructure validation
- Stage-by-stage execution with error handling
- Performance metrics tracking
- Historical replay capability
- Detailed logging and reporting

**Usage:**
```bash
# Run for specific date
python scripts/run_pipeline.py --date 2026-01-03

# Replay last N days
python scripts/run_pipeline.py --replay 7

# Skip validation stage (faster)
python scripts/run_pipeline.py --skip-validation

# Validation only (no processing)
python scripts/run_pipeline.py --validate-only
```

**Output Files:**
- `data/output/pipeline_run_YYYY-MM-DD.txt` - Execution summary

---

#### **2. compute_demand.py** - Demand Calculation Engine

**Purpose:** Core analytics - calculates what products to reorder

**Algorithm:**
```
1. Load orders from HDFS (via Trino Hive catalog)
2. Load stock from HDFS (via Trino Hive catalog)
3. Load master data from PostgreSQL (via Trino PostgreSQL catalog)
4. Aggregate demand per SKU
5. Calculate: Net Demand = Orders - Stock + Safety Stock
6. Apply business rules (MOQ, case size, priorities)
7. Save replenishment CSV
```

**Usage:**
```bash
python scripts/compute_demand.py --date 2026-01-03
```

**Output Files:**
- `data/output/replenishment_YYYY-MM-DD.csv` - Procurement recommendations

**Performance:**
- Processes 15,150 order items in ~500ms
- Handles 50+ unique SKUs
- Memory efficient (< 100 MB)

---

#### **3. export_orders.py** - Supplier Order Generator

**Purpose:** Transforms replenishment CSV into supplier-specific JSON orders

**Logic:**
```python
1. Load replenishment_YYYY-MM-DD.csv
2. Group items by supplier_name
3. For each supplier:
   - Create order JSON structure
   - Calculate totals (items, units, cases, value)
   - Set delivery dates (current_date + lead_time)
   - Assign order priorities
4. Save JSON file per supplier
```

**Usage:**
```bash
python scripts/export_orders.py --date 2026-01-03
```

**Output Files:**
- `data/output/supplier_orders/SupplierName_YYYY-MM-DD.json` (5 files)

---

#### **4. generate_exceptions.py** - Anomaly Detection

**Purpose:** Detect business rule violations and unusual patterns

**Detection Rules:**
```python
HIGH_DEMAND:
  - Threshold: > 2,000 units
  - Check: Compare to historical average
  - Alert: "Unusual spike - verify before ordering"

LOW_STOCK:
  - Threshold: stock < 30% of demand
  - Check: Stock coverage ratio
  - Alert: "Low inventory - risk of stockout"

CRITICAL_STOCK:
  - Threshold: stock < 10% of demand
  - Check: Critical coverage
  - Alert: "URGENT - emergency order required"

MISSING_SUPPLIER:
  - Check: supplier_name IS NULL
  - Alert: "Cannot generate order - assign supplier"

HIGH_VALUE_ORDER:
  - Threshold: order_value > $10,000
  - Check: Total order cost
  - Alert: "Manager approval required"

DEMAND_STOCK_GAP:
  - Threshold: demand > 5x stock
  - Check: Demand-to-stock ratio
  - Alert: "Large gap - review forecasting"
```

**Usage:**
```bash
python scripts/generate_exceptions.py --date 2026-01-03
```

**Output Files:**
- `data/output/exceptions/exception_report_YYYY-MM-DD.json` - Detailed exceptions
- `data/output/exceptions/exception_summary_YYYY-MM-DD.txt` - Human-readable report

---

### Testing & Validation Scripts

#### **5. test_system.py** - Comprehensive Integration Tests

**Purpose:** Validates entire system with 37 automated tests

**Test Coverage:**
```
Docker Services (5 tests)
├─ Container health checks
├─ Port availability
└─ Network connectivity

Database Layer (6 tests)
├─ PostgreSQL connection
├─ Table structure validation
├─ Data integrity checks
├─ Trino connectivity
├─ Catalog availability
└─ Query execution

Data Files (3 tests)
├─ Order file count (105 expected)
├─ Stock file count (35 expected)
└─ File format validation

Processing Modules (12 tests)
├─ compute_demand.py functionality
├─ export_orders.py execution
├─ generate_exceptions.py rules
└─ Data transformation accuracy

Orchestration (7 tests)
├─ run_pipeline.py execution
├─ Airflow DAG syntax
├─ Task dependencies
└─ Schedule configuration

End-to-End (4 tests)
├─ Full pipeline execution
├─ Output file generation
├─ Data consistency
└─ Performance benchmarks
```

**Usage:**
```bash
python scripts/test_system.py

# Expected output:
# ✅ 37/37 tests passed (100%)
# ⏱️  Total time: ~15 seconds
```

---

#### **6. test_trino_catalog.py** - Trino Connectivity Tests

**Purpose:** Validates Trino query engine and data access

**Test Categories:**
```
1. Version Check
   - Verify Trino 479 running

2. Catalog Discovery
   - List available catalogs (postgresql, hive, system)

3. Schema Exploration
   - List schemas in each catalog

4. Table Queries
   - Simple SELECT queries
   - COUNT aggregations
   - GROUP BY operations

5. JOIN Operations
   - Cross-catalog joins (PostgreSQL + Hive)
   - Multi-table joins

6. Complex Analytics
   - Subqueries
   - Window functions
   - Aggregations with filters
```

**Usage:**
```bash
python scripts/test_trino_catalog.py

# Expected: 10/10 tests passed
```

---

#### **7. test_connection.py** - Infrastructure Health Check

**Purpose:** Quick connectivity test for all services

**Checks:**
```
✓ PostgreSQL: Connection + query execution
✓ HDFS: Namenode accessibility + file system operations
✓ Trino: Query engine + catalog availability
```

**Usage:**
```bash
python scripts/test_connection.py

# Expected output:
# ✅ PostgreSQL Connected
# ✅ HDFS Connected
# ✅ Trino Connected
```

---

### Data Generation Scripts

#### **8. data_gen.py** - Test Data Generator

**Purpose:** Create realistic test data using Faker library

**Generated Data:**
```
Orders (JSON files):
├─ 15 POS locations (pos_1 to pos_15)
├─ 7 days of history (Dec 28 - Jan 03)
├─ 100-150 orders per store per day
├─ 10-15 items per order
├─ Realistic product distributions
└─ Total: 105 files, ~15,150 items

Stock (CSV files):
├─ 5 warehouses (WH-001 to WH-005)
├─ 7 days of snapshots
├─ 50 SKUs per warehouse
├─ Random stock levels (0-500 units)
└─ Total: 35 files, ~250 records/file
```

**Usage:**
```bash
# Generate 7 days of data
python scripts/data_gen.py --days 7 --start-date 2025-12-28

# Generate with custom stores/warehouses
python scripts/data_gen.py --stores 20 --warehouses 10
```

---

#### **9. validate_data_quality.py** - Data Quality Validator

**Purpose:** Ensure data integrity before processing

**Validation Rules:**
```
JSON Orders:
✓ Valid JSON structure
✓ Required fields present (order_id, pos_id, items)
✓ Data types correct (quantity = integer, price = decimal)
✓ Logical constraints (quantity > 0, price > 0)
✓ Date format validation

CSV Stock:
✓ Valid CSV format
✓ Required columns present
✓ Numeric fields are numeric
✓ No negative quantities
✓ SKU references valid products
```

**Usage:**
```bash
python scripts/validate_data_quality.py --date 2026-01-03
```

---

### Utility Scripts

#### **10. ingest_hdfs.py** - HDFS Upload

**Purpose:** Upload data files to HDFS

**Usage:**
```bash
python scripts/ingest_hdfs.py --source data/raw --hdfs-path /procurement
```

---

### CLI Options Reference

| Script | Option | Description |
|--------|--------|-------------|
| run_pipeline.py | `--date YYYY-MM-DD` | Process specific date |
| | `--replay N` | Replay last N days |
| | `--skip-validation` | Skip data validation stage |
| | `--validate-only` | Only run validation |
| | `--output PATH` | Custom output directory |
| compute_demand.py | `--date YYYY-MM-DD` | Calculation date |
| | `--base-path PATH` | Data directory path |
| export_orders.py | `--date YYYY-MM-DD` | Order generation date |
| | `--supplier NAME` | Generate for specific supplier |
| data_gen.py | `--days N` | Number of days to generate |
| | `--start-date YYYY-MM-DD` | Start date for generation |
| | `--stores N` | Number of POS locations |
| | `--warehouses N` | Number of warehouses |

---

## 📦 Data Models

### Input: Order JSON Schema

```json
{
  "pos_id": "POS-001",
  "date": "2026-01-03",
  "items": [
    {
      "sku": "SKU-0012",
      "quantity": 24,
      "unit_price": 2.99
    }
  ]
}
```

### Input: Stock CSV Schema

| Column | Type | Description |
|--------|------|-------------|
| warehouse_id | string | Warehouse identifier |
| sku | string | Product SKU |
| available_stock | integer | Units available |
| reserved_stock | integer | Units reserved |
| date | date | Snapshot date |

### Output: Supplier Order JSON

```json
{
  "order_id": "ORD-20260103-006-001",
  "supplier_id": "SUP-006",
  "supplier_name": "BevCo Distributors",
  "order_date": "2026-01-03",
  "requested_delivery_date": "2026-01-05",
  "status": "PENDING",
  "priority": "HIGH",
  "items": [
    {
      "line_number": 1,
      "sku": "SKU-0001",
      "product_name": "Organic Apple Juice",
      "category": "Beverages",
      "quantity_ordered": 1344,
      "cases": 56,
      "case_size": 24,
      "net_demand": 1333.0
    }
  ],
  "summary": {
    "total_line_items": 7,
    "total_units": 10494,
    "total_cases": 874
  },
  "metadata": {
    "generated_by": "procurement_pipeline",
    "generation_timestamp": "2026-01-04T03:52:28",
    "pipeline_version": "1.0"
  }
}
```

### Output: Exception Report

```json
{
  "report_date": "2026-01-03",
  "generated_at": "2026-01-04T02:58:07",
  "summary": {
    "total_skus_analyzed": 24,
    "total_exceptions": 30,
    "by_severity": {
      "CRITICAL": 0,
      "HIGH": 28,
      "MEDIUM": 2
    }
  },
  "exceptions": [
    {
      "type": "HIGH_DEMAND",
      "severity": "HIGH",
      "sku": "SKU-0022",
      "product_name": "Bagels 6pk",
      "metric_value": 2852,
      "threshold": 2000,
      "recommendation": "Consider expedited supplier contact"
    }
  ]
}
```

---

## 📈 Pipeline Results

### Latest Execution (2026-01-03)

```
╔════════════════════════════════════════════════════════════════════╗
║                    PIPELINE EXECUTION SUMMARY                       ║
╠════════════════════════════════════════════════════════════════════╣
║  📅 Processing Date:     2026-01-03                                 ║
║  ⏱️  Execution Time:      1.06 seconds                              ║
║  📊 Status:              ✅ SUCCESS                                 ║
╠════════════════════════════════════════════════════════════════════╣
║  📦 INPUT DATA                                                      ║
║     • Order Files:        105 JSON files                            ║
║     • Stock Files:        35 CSV files                              ║
║     • Order Items:        15,150 items                              ║
║     • Stock Records:      250 records                               ║
║     • POS Locations:      15 stores                                 ║
║     • Warehouses:         5 locations                               ║
╠════════════════════════════════════════════════════════════════════╣
║  📊 PROCESSING                                                      ║
║     • Total Demand:       121,840 units                             ║
║     • Total Stock:        58,401 units                              ║
║     • Unique SKUs:        50 products                               ║
║     • Products (Master):  49 in database                            ║
╠════════════════════════════════════════════════════════════════════╣
║  📤 OUTPUT DATA                                                     ║
║     • SKUs to Reorder:    24 products                               ║
║     • Total Units:        32,748 units                              ║
║     • Suppliers:          5 orders generated                        ║
║     • Exceptions:         30 (0 critical)                           ║
╚════════════════════════════════════════════════════════════════════╝
```

### Supplier Orders Generated

| Supplier | SKUs | Units | Cases | Priority |
|----------|------|-------|-------|----------|
| BevCo Distributors | 7 | 10,494 | 874 | 🔴 HIGH |
| FreshMart Wholesale | 5 | 6,744 | 562 | 🔴 HIGH |
| DairyFresh LLC | 5 | 6,594 | 549 | 🔴 HIGH |
| ElectroSupply Co | 4 | 5,461 | 455 | 🔴 HIGH |
| TechGear Plus | 3 | 3,455 | 288 | 🟡 MEDIUM |
| **TOTAL** | **24** | **32,748** | **2,728** | |

### Top 10 Items to Reorder

| Rank | SKU | Product | Category | Order Qty | Supplier |
|------|-----|---------|----------|-----------|----------|
| 1 | SKU-0031 | USB Cable 2m | Electronics | 2,200 | ElectroSupply Co |
| 2 | SKU-0021 | Croissant Pack | Bakery | 2,040 | FreshMart Wholesale |
| 3 | SKU-0012 | Cola 2L | Beverages | 1,974 | BevCo Distributors |
| 4 | SKU-0005 | Almond Milk | Beverages | 1,728 | BevCo Distributors |
| 5 | SKU-0045 | Cream Cheese | Dairy | 1,692 | DairyFresh LLC |
| 6 | SKU-0024 | Baguette | Bakery | 1,540 | FreshMart Wholesale |
| 7 | SKU-0043 | Cheddar Cheese | Dairy | 1,510 | DairyFresh LLC |
| 8 | SKU-0003 | Wireless Mouse | Electronics | 1,440 | ElectroSupply Co |
| 9 | SKU-0022 | Bagels 6pk | Bakery | 1,424 | FreshMart Wholesale |
| 10 | SKU-0011 | Orange Juice 1L | Beverages | 1,416 | BevCo Distributors |

---

## ✅ Project Phases Completed

### Phase 1: Infrastructure Setup ✅

- [x] Docker Compose with PostgreSQL, HDFS, Trino, pgAdmin, Airflow
- [x] PostgreSQL schema with products, suppliers, replenishment_rules
- [x] Master data: 49 products, 10 suppliers, 49 rules
- [x] All services verified and running

### Phase 2: Data Ingestion ✅

- [x] HDFS directory hierarchy (`/raw/orders/`, `/raw/stock/`)
- [x] 7 days of test data generated (Dec 28 - Jan 3)
- [x] 105 order files (15 POS × 7 days)
- [x] 35 stock files (5 warehouses × 7 days)
- [x] Data quality validation implemented

### Phase 3: Analytical Processing ✅

- [x] Trino connectors: PostgreSQL catalog, Hive catalog
- [x] Demand aggregation: 121,840 units across 50 SKUs
- [x] Net demand computation with safety stock
- [x] Business rules: MOQ and case size rounding
- [x] Result: 24 SKUs require 32,748 units

### Phase 4: Output Generation ✅

- [x] Supplier order export (5 JSON files)
- [x] Exception reporting (30 exceptions detected)
- [x] Order priorities assigned (4 HIGH, 1 MEDIUM)
- [x] Human-readable reports generated

### Phase 5: Orchestration ✅

- [x] Master orchestrator (`run_pipeline.py`)
- [x] Airflow DAG scheduled at 22:00 daily
- [x] Historical replay capability (`--replay N`)
- [x] System integration tests (37 tests, 100% pass)

---

## 🧪 System Tests

Run the comprehensive test suite:

```bash
python scripts/test_system.py
```

### Test Categories

| Category | Tests | Description |
|----------|-------|-------------|
| Docker Services | 5 | Container health checks |
| PostgreSQL | 4 | Connection & data validation |
| Trino | 2 | Query engine verification |
| Data Files | 3 | File existence & counts |
| Demand Module | 4 | Data loading & processing |
| Export Module | 4 | JSON generation |
| Exception Module | 4 | Report generation |
| Orchestrator | 3 | Infrastructure validation |
| Airflow DAG | 4 | DAG syntax & configuration |
| End-to-End | 4 | Output file verification |
| **TOTAL** | **37** | **All passing ✅** |

---

## 🐳 Docker Services

```yaml
services:
  postgres:        # Master data storage
  namenode:        # HDFS name node
  datanode:        # HDFS data node
  trino:           # Query engine
  pgadmin:         # Database UI
  airflow:         # Workflow orchestration
```

### Service Ports

| Service | Internal Port | External Port |
|---------|---------------|---------------|
| PostgreSQL | 5432 | 5432 |
| HDFS Namenode | 9000, 9870 | 9000, 9870 |
| Trino | 8080 | 8080 |
| Airflow | 8080 | 8081 |
| pgAdmin | 80 | 5050 |

---

## 🔧 Troubleshooting Guide

### Common Issues & Solutions

---

#### **1. Container Not Starting**

**Symptom:**
```
Error: Container exited with code 1
```

**Diagnosis:**
```bash
# Check container logs
docker logs procurement-trino
docker logs procurement-postgres

# Check port conflicts
netstat -ano | findstr "8080"  # Windows
netstat -tuln | grep 8080      # Linux
```

**Solutions:**
```bash
# 1. Port already in use
docker-compose down
# Kill process using the port
taskkill /PID <PID> /F  # Windows
kill -9 <PID>           # Linux
docker-compose up -d

# 2. Insufficient resources
docker system prune -a  # Free up space
# Increase Docker Desktop resources (RAM to 4GB+)

# 3. Corrupted volumes
docker-compose down -v
docker-compose up -d
```

---

#### **2. Trino Connection Failed**

**Symptom:**
```python
TrinoConnectionError: HTTP 503: Service Unavailable
```

**Diagnosis:**
```bash
# Check Trino health
curl http://localhost:8080/v1/info
docker exec -it procurement-trino trino --version

# Verify catalogs
docker exec -it procurement-trino ls /etc/trino/catalog
```

**Solutions:**
```bash
# 1. Trino not fully started (wait 30 seconds)
python -c "import time; print('Waiting...'); time.sleep(30)"
python scripts/test_connection.py

# 2. Catalog configuration error
# Check config/trino/postgresql.properties:
#   connector.name=postgresql
#   connection-url=jdbc:postgresql://postgres:5432/procurement
#   connection-user=admin
#   connection-password=admin123

# 3. Restart Trino
docker restart procurement-trino
```

---

#### **3. PostgreSQL Connection Error**

**Symptom:**
```
psycopg2.OperationalError: could not connect to server
```

**Diagnosis:**
```bash
# Test PostgreSQL directly
docker exec -it procurement-postgres psql -U admin -d procurement -c "SELECT 1;"

# Check PostgreSQL logs
docker logs procurement-postgres --tail 50
```

**Solutions:**
```bash
# 1. Database not initialized
docker exec -it procurement-postgres psql -U admin -d procurement
# If database doesn't exist:
docker exec -i procurement-postgres psql -U admin < sql/postgres/schema.sql
docker exec -i procurement-postgres psql -U admin -d procurement < sql/postgres/init_master_data.sql

# 2. Wrong credentials
# Update .env file or docker-compose.yml:
#   POSTGRES_USER=admin
#   POSTGRES_PASSWORD=admin123
#   POSTGRES_DB=procurement
```

---

#### **4. HDFS Permission Denied**

**Symptom:**
```
org.apache.hadoop.security.AccessControlException: Permission denied
```

**Diagnosis:**
```bash
# Check HDFS files
docker exec -it procurement-hdfs-namenode hdfs dfs -ls /procurement
docker exec -it procurement-hdfs-namenode hdfs dfs -ls /procurement/orders
```

**Solutions:**
```bash
# 1. Fix directory permissions
docker exec -it procurement-hdfs-namenode hdfs dfs -chmod -R 777 /procurement

# 2. Recreate HDFS directories
docker exec -it procurement-hdfs-namenode hdfs dfs -rm -r /procurement
docker exec -it procurement-hdfs-namenode hdfs dfs -mkdir -p /procurement/orders
docker exec -it procurement-hdfs-namenode hdfs dfs -mkdir -p /procurement/stock

# 3. Re-upload data
python scripts/ingest_hdfs.py --source data/raw --hdfs-path /procurement
```

---

#### **5. Airflow DAG Not Showing**

**Symptom:**
- DAG not visible in Airflow UI
- Import errors in logs

**Diagnosis:**
```bash
# Check DAG syntax
python airflow/dags/procurement_dag.py

# Check Airflow logs
docker logs procurement-airflow --tail 100
docker exec -it procurement-airflow airflow dags list
```

**Solutions:**
```bash
# 1. Python syntax error in DAG
# Fix syntax in airflow/dags/procurement_dag.py

# 2. Missing dependencies
docker exec -it procurement-airflow pip install pandas trino psycopg2-binary

# 3. Airflow database not created
docker exec procurement-postgres psql -U admin -d procurement -c "CREATE DATABASE airflow;"
docker restart procurement-airflow

# 4. Restart Airflow scheduler
docker restart procurement-airflow
```

---

#### **6. Pipeline Execution Failure**

**Symptom:**
```
ERROR: Stage 'compute_demand' failed
```

**Diagnosis:**
```bash
# Check pipeline logs
cat data/output/pipeline_run_2026-01-03.txt

# Check data files
ls data/raw/orders/*.json | wc -l  # Should be 105
ls data/raw/stock/*.csv | wc -l    # Should be 35
```

**Solutions:**
```bash
# 1. Missing data files
python scripts/data_gen.py --days 7 --start-date 2025-12-28
python scripts/ingest_hdfs.py

# 2. Run validation first
python scripts/run_pipeline.py --validate-only

# 3. Check specific stage
python scripts/compute_demand.py --date 2026-01-03
python scripts/export_orders.py --date 2026-01-03
```

---

#### **7. Test Failures**

**Symptom:**
```
❌ Test failed: test_docker_containers
```

**Diagnosis:**
```bash
# Run specific test
python scripts/test_system.py

# Check which containers are down
docker ps -a
```

**Solutions:**
```bash
# 1. Start all containers
docker-compose up -d

# 2. Wait for services to be ready
python scripts/test_connection.py

# 3. Re-run tests
python scripts/test_system.py
```

---

#### **8. Performance Issues**

**Symptom:**
- Pipeline takes > 5 seconds
- High memory usage

**Diagnosis:**
```bash
# Check Docker resource usage
docker stats

# Check Trino query performance
curl http://localhost:8080/v1/query
```

**Solutions:**
```bash
# 1. Increase Docker resources
# Docker Desktop → Settings → Resources
# - CPUs: 4+
# - Memory: 4GB+
# - Swap: 2GB+

# 2. Optimize Trino queries
# Add indexes in PostgreSQL:
CREATE INDEX idx_products_sku ON products(product_id);
CREATE INDEX idx_suppliers_name ON suppliers(supplier_name);

# 3. Process in batches
python scripts/run_pipeline.py --date 2026-01-03  # One day at a time
```

---

#### **9. Data Quality Issues**

**Symptom:**
```
WARNING: Invalid data detected in pos_1_2026-01-03.json
```

**Diagnosis:**
```bash
# Validate data files
python scripts/validate_data_quality.py --date 2026-01-03

# Check file contents
cat data/raw/orders/pos_1_2026-01-03.json | python -m json.tool
```

**Solutions:**
```bash
# 1. Regenerate corrupt files
python scripts/data_gen.py --days 1 --start-date 2026-01-03

# 2. Manual fix
# Edit JSON file to ensure valid structure:
# - All brackets closed
# - No trailing commas
# - Valid date formats

# 3. Skip validation (not recommended)
python scripts/run_pipeline.py --skip-validation
```

---

### Error Code Reference

| Error Code | Meaning | Action |
|------------|---------|--------|
| **HTTP 503** | Service Unavailable | Wait 30 seconds, check container health |
| **HTTP 404** | Catalog Not Found | Verify Trino catalog config files |
| **Exit Code 1** | Container Startup Failed | Check logs: `docker logs <container>` |
| **Exit Code 137** | Out of Memory | Increase Docker memory limit |
| **ECONNREFUSED** | Connection Refused | Check if service is running |
| **ETIMEDOUT** | Connection Timeout | Check network, increase timeout |

---

### Quick Diagnostics Commands

```bash
# System Health Check
python scripts/test_connection.py

# Container Status
docker-compose ps

# View All Logs
docker-compose logs --tail=50

# Resource Usage
docker stats --no-stream

# Database Connectivity
docker exec -it procurement-postgres psql -U admin -d procurement -c "\dt"

# HDFS Status
docker exec -it procurement-hdfs-namenode hdfs dfsadmin -report

# Trino Catalogs
docker exec -it procurement-trino trino --execute "SHOW CATALOGS"

# Full System Test
python scripts/test_system.py
```

---

### Support & Resources

**Official Documentation:**
- Trino: https://trino.io/docs/current/
- HDFS: https://hadoop.apache.org/docs/stable/
- Airflow: https://airflow.apache.org/docs/
- PostgreSQL: https://www.postgresql.org/docs/

**Project Resources:**
- Check logs in `airflow/logs/`
- Check pipeline output in `data/output/`
- Review test results from `test_system.py`

**Contact:**
- Project Repository: https://github.com/mohamedamineelabidi/Big-data
- Report bugs via GitHub Issues

---

## 🤖 AI Development Context (GitHub Copilot)

### Project Understanding for AI Assistants

When providing assistance for this codebase, AI tools should understand:

---

#### **Domain Context:**

**Business Domain:** Retail Supply Chain Management & Procurement Automation

**Problem Statement:**
- Retail chain with 15 stores generates 15,150 daily transactions
- 5 warehouses manage inventory across 50 SKUs
- Need automated daily procurement to prevent stockouts
- Must consider: demand volatility, supplier lead times, MOQ constraints, case pack sizes

**Key Stakeholders:**
- **Store Managers:** Need consistent stock availability
- **Procurement Team:** Need accurate daily orders
- **Warehouse Managers:** Need optimal stock levels
- **Finance:** Need cost-effective ordering (MOQ compliance)

---

#### **Technical Architecture:**

**Data Engineering Pattern:** Batch-oriented ELT (Extract-Load-Transform)

**Technology Stack Rationale:**
```
HDFS (Data Lake)
  ↓ Stores: Raw JSON orders + CSV stock snapshots
  ↓ Why: Fault-tolerant, scalable for growing data volumes

Trino (Query Engine)
  ↓ Federates: PostgreSQL (master data) + Hive (HDFS data)
  ↓ Why: Single SQL interface for heterogeneous sources

PostgreSQL (Operational Database)
  ↓ Stores: Products, suppliers, business rules
  ↓ Why: ACID compliance for master data integrity

Airflow (Orchestrator)
  ↓ Schedules: Daily 22:00 execution
  ↓ Why: Visual DAG monitoring + error handling
```

**Not Used (Anti-patterns):**
- ❌ No Spark - Data volume too small (<1GB)
- ❌ No Kafka - Batch processing, not streaming
- ❌ No Cassandra - No high-write throughput needs
- ❌ No MongoDB - Structured data with relationships

---

#### **Code Conventions:**

**Variable Naming Patterns:**
```python
# Business Terms (Preferred)
sku, moq, safety_stock, net_demand, lead_time

# Data Sources
orders_df, stock_df, products_df, suppliers_df

# Processing Stages
raw_demand, adjusted_demand, rounded_demand

# Avoid Generic Names
data, temp, result, output
```

**Module Organization:**
```
scripts/
├── run_pipeline.py      # Orchestrator only - no business logic
├── compute_demand.py    # Core analytics - demand calculation
├── export_orders.py     # Output formatting - JSON generation
├── generate_exceptions.py  # Quality checks - anomaly detection
└── test_*.py            # Testing modules
```

**SQL Query Patterns:**
```sql
-- Always use explicit catalog.schema.table
SELECT * FROM postgresql.procurement.products

-- Always qualify joins
FROM postgresql.procurement.products p
JOIN hive.default.orders o ON p.product_id = o.sku

-- Always use meaningful aliases
SELECT p.product_name AS product, s.supplier_name AS supplier
```

---

#### **Common Development Tasks:**

**Adding a New Business Rule:**
```python
# 1. Update PostgreSQL schema
ALTER TABLE replenishment_rules ADD COLUMN new_rule_column INT;

# 2. Update init_master_data.sql
INSERT INTO replenishment_rules (product_id, new_rule_column) VALUES ...

# 3. Modify compute_demand.py
df['calculated_value'] = df.apply(lambda x: x['demand'] * x['new_rule_column'], axis=1)

# 4. Add test in test_system.py
def test_new_rule():
    assert calculated_value > 0
```

**Adding a New Exception Type:**
```python
# In generate_exceptions.py
if condition_met:
    exceptions.append({
        "exception_type": "NEW_EXCEPTION_TYPE",
        "severity": "HIGH",
        "sku": sku,
        "message": "Descriptive message",
        "action_required": "What to do"
    })
```

**Modifying Data Schema:**
```python
# 1. Update JSON schema in data_gen.py
order_data = {
    "pos_id": pos_id,
    "date": date,
    "new_field": value,  # Add here
    "items": [...]
}

# 2. Update compute_demand.py to handle new field
orders_df['new_field'] = orders_df['metadata'].apply(lambda x: x.get('new_field'))

# 3. Update test_system.py
def test_new_field_exists():
    with open('data/raw/orders/pos_1_2026-01-03.json') as f:
        data = json.load(f)
        assert 'new_field' in data
```

---

#### **Debugging Strategies:**

**For Query Errors:**
```python
# 1. Test Trino connectivity first
python scripts/test_connection.py

# 2. Run query directly in Trino CLI
docker exec -it procurement-trino trino --execute "SELECT * FROM postgresql.procurement.products LIMIT 5"

# 3. Check catalog configuration
cat config/trino/postgresql.properties

# 4. Verify table exists in PostgreSQL
docker exec -it procurement-postgres psql -U admin -d procurement -c "\dt"
```

**For Pipeline Failures:**
```python
# 1. Run validation only
python scripts/run_pipeline.py --validate-only

# 2. Run individual stages
python scripts/compute_demand.py --date 2026-01-03
python scripts/export_orders.py --date 2026-01-03

# 3. Check output logs
cat data/output/pipeline_run_2026-01-03.txt

# 4. Validate data quality
python scripts/validate_data_quality.py --date 2026-01-03
```

**For Test Failures:**
```python
# 1. Check container health
docker ps -a
docker-compose logs --tail=50

# 2. Verify data files exist
ls data/raw/orders/*.json | wc -l  # Should be 105
ls data/raw/stock/*.csv | wc -l    # Should be 35

# 3. Run individual test categories
python scripts/test_system.py  # See which tests fail

# 4. Check service accessibility
curl http://localhost:8080/v1/info  # Trino
docker exec -it procurement-postgres psql -U admin -d procurement -c "SELECT 1"  # PostgreSQL
```

---

#### **Performance Optimization Guidelines:**

**Query Optimization:**
```sql
-- ✅ Good: Use filters early
SELECT * FROM hive.default.orders 
WHERE order_date = '2026-01-03'  -- Filter first
  AND quantity > 0

-- ❌ Bad: Filter after full table scan
SELECT * FROM hive.default.orders 
WHERE quantity > 0 AND order_date = '2026-01-03'
```

**DataFrame Operations:**
```python
# ✅ Good: Vectorized operations
df['net_demand'] = df['demand'] - df['stock'] + df['safety_stock']

# ❌ Bad: Row-by-row iteration
for index, row in df.iterrows():
    df.at[index, 'net_demand'] = row['demand'] - row['stock'] + row['safety_stock']
```

**Memory Management:**
```python
# ✅ Good: Process in chunks
for chunk in pd.read_csv('large_file.csv', chunksize=10000):
    process(chunk)

# ❌ Bad: Load entire file
df = pd.read_csv('large_file.csv')  # May cause OOM
```

---

#### **Data Validation Rules:**

**Order Files (JSON):**
```python
# Required fields
["pos_id", "date", "items"]

# Item structure
{
    "sku": "SKU-XXXX",      # Must match products table
    "quantity": int,         # Must be > 0
    "unit_price": float      # Must be > 0
}

# Date format
"YYYY-MM-DD"

# File naming
"pos_{1-15}_YYYY-MM-DD.json"
```

**Stock Files (CSV):**
```python
# Required columns
["warehouse_id", "sku", "date", "quantity"]

# Constraints
warehouse_id: "WH-001" to "WH-005"
sku: Must exist in products table
quantity: >= 0 (can be zero for out-of-stock)
date: YYYY-MM-DD format

# File naming
"stock_WH-XXX_YYYY-MM-DD.csv"
```

**Master Data (PostgreSQL):**
```sql
-- Products table
product_id: PRIMARY KEY, format "SKU-XXXX"
category: NOT NULL
supplier_name: FOREIGN KEY to suppliers

-- Replenishment Rules
moq: > 0 (Minimum Order Quantity)
case_size: > 0 (Units per case)
safety_stock: >= 0 (Can be zero)
lead_time: > 0 (Days)
```

---

#### **Testing Philosophy:**

**Unit Tests:** Individual module functionality
```python
# Test compute_demand.py in isolation
def test_demand_calculation():
    result = compute_demand(date='2026-01-03')
    assert len(result) > 0
    assert result['net_demand'].sum() > 0
```

**Integration Tests:** Module interactions
```python
# Test compute_demand → export_orders pipeline
def test_full_chain():
    compute_demand(date='2026-01-03')
    export_orders(date='2026-01-03')
    assert os.path.exists('data/output/supplier_orders/BevCo_Distributors_2026-01-03.json')
```

**End-to-End Tests:** Full system validation
```python
# Test complete pipeline execution
def test_pipeline_execution():
    result = subprocess.run(['python', 'scripts/run_pipeline.py', '--date', '2026-01-03'])
    assert result.returncode == 0
    assert os.path.exists('data/output/replenishment_2026-01-03.csv')
```

---

#### **Deployment Considerations:**

**Environment Variables:**
```bash
# Development
POSTGRES_HOST=localhost
TRINO_HOST=localhost

# Production (would use)
POSTGRES_HOST=postgres.internal.company.com
TRINO_HOST=trino-cluster.internal.company.com
```

**Scaling Strategy:**
```
Current: 15 stores, 5 warehouses, 50 SKUs
↓ 
Scale to: 100 stores, 20 warehouses, 500 SKUs
↓
Changes needed:
1. Increase HDFS datanodes (3 → 10)
2. Add Trino workers (single node → cluster)
3. Partition HDFS data by date (improve query performance)
4. Add caching layer (Redis) for master data
```

**Monitoring Metrics:**
```python
# Pipeline health
- Execution time (target: < 2 seconds)
- Success rate (target: 99.9%)
- Data freshness (target: < 24 hours old)

# Data quality
- Order file count (expected: 105)
- SKU coverage (expected: 50)
- Exception rate (target: < 5%)

# Resource usage
- Trino query time (target: < 500ms)
- PostgreSQL connections (max: 100)
- HDFS disk usage (target: < 80%)
```

---

#### **Common Pitfalls:**

**Trino Catalog Confusion:**
```sql
-- ❌ Wrong: Assuming catalog
SELECT * FROM products

-- ✅ Correct: Explicit catalog
SELECT * FROM postgresql.procurement.products
```

**Date Handling:**
```python
# ❌ Wrong: String comparison
if date > "2026-01-03":

# ✅ Correct: Date objects
from datetime import datetime
if datetime.strptime(date, '%Y-%m-%d') > datetime(2026, 1, 3):
```

**File Path Issues:**
```python
# ❌ Wrong: Hardcoded paths
file_path = "C:/Users/hp/Desktop/data/orders/..."

# ✅ Correct: Relative paths
import os
base_path = os.path.dirname(__file__)
file_path = os.path.join(base_path, "../data/orders/...")
```

**Docker Container Names:**
```bash
# ❌ Wrong: Auto-generated names
docker logs big-data_postgres_1

# ✅ Correct: Explicit names in docker-compose.yml
docker logs procurement-postgres
```

---

### Key Takeaways for AI Assistance:

1. **This is a DATA ENGINEERING project, not a web application**
2. **Batch processing only - no real-time/streaming requirements**
3. **Always use `trino` Python client, never `prestodb`**
4. **Explicit catalog names in all Trino queries**
5. **Business terminology over generic variable names**
6. **Test changes with `test_system.py` before committing**
7. **Master data lives in PostgreSQL, raw data in HDFS**
8. **Pipeline runs daily at 22:00, processing previous day's data**

---

## 👥 Team

**Project:** Big Data Fundamentals (Fondements Big Data)  
**Institution:** ENSA Al Hoceima  
**Academic Year:** 2025-2026

---

## 📄 License

Academic project - ENSA Al Hoceima © 2025-2026
