# AWS Quick Suite POC - Data Generators

This folder contains Python scripts to generate realistic sample data for the AWS Quick Suite POC.

## 📁 Generated Data Schemas

### 1. FitMap/SizeStream Schema (`dxlg_size_stream`)
- **size_users** - Customer body measurement profiles
- **size_scans** - 3D body scan records
- **size_app_measures** - Detailed body measurements
- **size_dxl_custom_measures** - Product-specific size recommendations

### 2. Customer/CRM Schema (`cimb_repl`)
- **customer** - Customer master data
- **address** - Customer addresses
- **email** - Customer email addresses
- **store** - Store locations
- **transaction_header** - Transaction summaries
- **transaction_detail** - Transaction line items
- **reward_detail** - Loyalty rewards
- **household** - Household groupings

### 3. Order/E-commerce Schema (`dxlg_olap_orders`)
- **orderheader** - Order summaries
- **orderline** - Order line items
- **orderline_items** - Product catalog
- **orderchargedetail** - Shipping/charges
- **invoice** - Invoice records
- **payment** - Payment records
- **quantitydetail** - Inventory quantity tracking

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Run All Generators

```bash
python run_all_generators.py
```

Or run individual generators:

```bash
python generate_fitmap_data.py
python generate_customer_data.py
python generate_order_data.py
```

## 📊 Data Volume

- **FitMap Data**: ~5,000 records across 4 tables
- **Customer Data**: ~25,000 records across 8 tables
- **Order Data**: ~10,000 records across 7 tables

**Total**: ~40,000 records, ~50-100 MB of CSV data

## 📝 Generated Files

After running the generators, you'll have these CSV files:

### FitMap Files
- `size_users.csv`
- `size_scans.csv`
- `size_app_measures.csv`
- `size_dxl_custom_measures.csv`

### Customer Files
- `customer.csv`
- `address.csv`
- `email.csv`
- `store.csv`
- `transaction_header.csv`
- `transaction_detail.csv`
- `reward_detail.csv`
- `household.csv`

### Order Files
- `orderheader.csv`
- `orderline.csv`
- `orderline_items.csv`
- `orderchargedetail.csv`
- `invoice.csv`
- `payment.csv`
- `quantitydetail.csv`

## 🔄 Next Steps After Generation

### Step 1: Upload to S3 (Easy Way)

**Windows (PowerShell) - RECOMMENDED:**
```powershell
.\upload_to_s3.ps1
```

**Windows (Command Prompt):**
```cmd
upload_to_s3.bat
```

**Manual Upload (if scripts don't work):**
```bash
aws s3 cp size_users.csv s3://dxl-quicksuite-poc-data/fitmap/size_users/
# ... (see QUICK_START.md for all commands)
```

### Step 2: Choose Your Data Platform

### Option A: Load to Redshift (Recommended)

1. **Create Redshift schemas:**
```sql
CREATE SCHEMA dxlg_size_stream;
CREATE SCHEMA cimb_repl;
CREATE SCHEMA dxlg_olap_orders;
```

2. **Create tables** (use your existing table definitions)

3. **Load CSV data using COPY command:**
```sql
COPY dxlg_size_stream.size_users
FROM 's3://dxl-quicksuite-poc-data/fitmap/size_users/'
IAM_ROLE 'arn:aws:iam::your-account:role/RedshiftRole'
CSV IGNOREHEADER 1 REGION 'us-east-1';
```

See `QUICK_START.md` for all COPY commands.

### Option B: Use Athena (Alternative)

1. **Create Athena database:**
```sql
CREATE DATABASE dxl_quicksuite_poc;
```

2. **Create external tables** pointing to S3 locations

3. **Connect Quick Suite to Athena**

## 🎯 Sample Business Questions for POC

Once data is loaded, test these queries in Quick Suite:

### FitMap Analytics
- "What's the average waist size for customers aged 35-50?"
- "Show me body measurement trends by age group"
- "Which stores have the most body scans this month?"
- "What are the most common size recommendations for denim?"

### Customer Analytics
- "Who are our top 10 customers by total spend?"
- "What's the average transaction value by store?"
- "Show me customer distribution by state"
- "Which customers haven't purchased in 6 months?"

### Order Analytics
- "What are our best-selling products this quarter?"
- "Show me order fulfillment status breakdown"
- "What's the average order value by month?"
- "Which products have the highest return rates?"

### Cross-Schema Analytics (The Power of Quick Suite!)
- "Show me customers with body scans who made purchases"
- "What's the correlation between body measurements and product purchases?"
- "Which size recommendations lead to the lowest return rates?"
- "Analyze customer lifetime value for those who used FitMap vs those who didn't"

## 🛠️ Customization

To adjust data volume, edit these variables in each script:

```python
# In generate_fitmap_data.py
NUM_USERS = 1000
NUM_SCANS = 2500

# In generate_customer_data.py
NUM_CUSTOMERS = 5000
NUM_TRANSACTIONS = 15000

# In generate_order_data.py
NUM_ORDERS = 3000
```

## 📧 Support

For questions or issues, contact: afjal.ahamad@dxl.com

---

**Generated for AWS Quick Suite POC - December 2025**
