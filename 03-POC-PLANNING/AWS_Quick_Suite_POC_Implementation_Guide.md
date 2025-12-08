# AWS Quick Suite POC Implementation Guide

**Objective:** Set up a working POC environment to demonstrate Quick Suite capabilities before DXL presentation  
**Timeline:** 5-7 days  
**Environment:** Your AWS Account (Sandbox/Dev)  
**Prepared by:** Senior Data Engineering Team  
**Date:** November 26, 2025

---

## Table of Contents

1. Prerequisites & AWS Permissions
2. Phase 1: Environment Setup (Day 1)
3. Phase 2: Sample Data Preparation (Day 2)
4. Phase 3: Quick Suite Configuration (Day 3-4)
5. Phase 4: Use Case Demonstrations (Day 5-6)
6. Phase 5: Demo Preparation (Day 7)
7. Troubleshooting Guide
8. Cost Estimation
9. Cleanup Instructions

---

## 1. PREREQUISITES & AWS PERMISSIONS

### 1.1 AWS Account Requirements

**Account Type:** AWS account with admin access (or specific permissions below)  
**Region:** us-east-1 (recommended for Quick Suite availability)  
**Budget:** ~$500-800 for 7-day POC

### 1.2 Required IAM Permissions

Create an IAM policy with the following permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "QuickSuiteFullAccess",
      "Effect": "Allow",
      "Action": [
        "quicksuite:*",
        "quicksight:*"
      ],
      "Resource": "*"
    },
    {
      "Sid": "RedshiftAccess",
      "Effect": "Allow",
      "Action": [
        "redshift:DescribeClusters",
        "redshift:GetClusterCredentials",
        "redshift:CreateCluster",
        "redshift:DeleteCluster",
        "redshift:ModifyCluster"
      ],
      "Resource": "*"
    },
    {
      "Sid": "S3Access",
      "Effect": "Allow",
      "Action": [
        "s3:CreateBucket",
        "s3:ListBucket",
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject"
      ],
      "Resource": [
        "arn:aws:s3:::quicksuite-poc-*",
        "arn:aws:s3:::quicksuite-poc-*/*"
      ]
    },
    {
      "Sid": "AthenaAccess",
      "Effect": "Allow",
      "Action": [
        "athena:*"
      ],
      "Resource": "*"
    },
    {
      "Sid": "GlueAccess",
      "Effect": "Allow",
      "Action": [
        "glue:*"
      ],
      "Resource": "*"
    },
    {
      "Sid": "LambdaAccess",
      "Effect": "Allow",
      "Action": [
        "lambda:CreateFunction",
        "lambda:InvokeFunction",
        "lambda:DeleteFunction",
        "lambda:UpdateFunctionCode"
      ],
      "Resource": "*"
    },
    {
      "Sid": "IAMAccess",
      "Effect": "Allow",
      "Action": [
        "iam:CreateRole",
        "iam:AttachRolePolicy",
        "iam:PassRole",
        "iam:GetRole"
      ],
      "Resource": "*"
    },
    {
      "Sid": "VPCAccess",
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeVpcs",
        "ec2:DescribeSubnets",
        "ec2:DescribeSecurityGroups",
        "ec2:CreateSecurityGroup",
        "ec2:AuthorizeSecurityGroupIngress"
      ],
      "Resource": "*"
    },
    {
      "Sid": "CloudWatchAccess",
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents",
        "cloudwatch:PutMetricData"
      ],
      "Resource": "*"
    }
  ]
}
```



### 1.3 Required AWS Resources

| Resource | Purpose | Estimated Cost (7 days) |
|----------|---------|-------------------------|
| Quick Suite Enterprise | Core platform | $0 (30-day trial) |
| Redshift dc2.large (1 node) | Sample data warehouse | $175 |
| S3 Standard Storage (50GB) | Sample data lake | $1.15 |
| Athena Queries | Ad-hoc queries | $5 |
| Lambda Invocations | Automation triggers | $0.20 |
| Glue Crawler | Data catalog | $0.44 |
| CloudWatch Logs | Monitoring | $0.50 |
| **TOTAL ESTIMATED COST** | | **~$182** |

*Note: Quick Suite offers 30-day free trial for POC purposes*

### 1.4 Tools & Software Required

- **AWS CLI** (v2.x): For command-line operations
- **Python 3.9+**: For sample data generation scripts
- **SQL Client**: DBeaver, pgAdmin, or SQL Workbench
- **Text Editor**: VS Code or similar
- **Web Browser**: Chrome, Firefox, or Edge (latest version)

### 1.5 Sample Data Sources

For POC, we'll create synthetic data mimicking DXL's environment:

1. **Sales Transactions** (Redshift table)
2. **Inventory Data** (Redshift table)
3. **FitMap Measurements** (Redshift table - simulated)
4. **Product Catalog** (S3 CSV files)
5. **Customer Reviews** (S3 JSON files)
6. **Store Locations** (S3 CSV file)

---

## 2. PHASE 1: ENVIRONMENT SETUP (Day 1)

### Step 1: Enable Quick Suite in AWS Console

**Time Required:** 30 minutes

```bash
# 1. Log into AWS Console
# Navigate to: https://console.aws.amazon.com/quicksuite/

# 2. Click "Get Started" or "Enable Quick Suite"

# 3. Select Region: us-east-1

# 4. Choose Subscription:
#    - Select "Enterprise Edition" (30-day trial)
#    - Enter billing information (won't be charged during trial)

# 5. Create Admin User:
#    - Username: quicksuite-admin
#    - Email: your-email@company.com
#    - Set password

# 6. Configure Initial Settings:
#    - Organization Name: "DXL POC"
#    - Time Zone: Your timezone
#    - Default Language: English
```

**Verification:**
- Quick Suite dashboard should be accessible
- Admin user can log in successfully

---

### Step 2: Create S3 Bucket for Sample Data

**Time Required:** 10 minutes

```bash
# Set variables
export AWS_REGION=us-east-1
export BUCKET_NAME=quicksuite-poc-dxl-$(date +%s)

# Create S3 bucket
aws s3 mb s3://${BUCKET_NAME} --region ${AWS_REGION}

# Create folder structure
aws s3api put-object --bucket ${BUCKET_NAME} --key data/sales/
aws s3api put-object --bucket ${BUCKET_NAME} --key data/inventory/
aws s3api put-object --bucket ${BUCKET_NAME} --key data/fitmap/
aws s3api put-object --bucket ${BUCKET_NAME} --key data/products/
aws s3api put-object --bucket ${BUCKET_NAME} --key data/customers/
aws s3api put-object --bucket ${BUCKET_NAME} --key logs/

# Enable versioning
aws s3api put-bucket-versioning \
  --bucket ${BUCKET_NAME} \
  --versioning-configuration Status=Enabled

echo "S3 Bucket created: ${BUCKET_NAME}"
```

**Verification:**
```bash
aws s3 ls s3://${BUCKET_NAME}/
```

---

### Step 3: Create Redshift Cluster

**Time Required:** 20 minutes (cluster takes 10-15 min to provision)

```bash
# Create Redshift cluster
aws redshift create-cluster \
  --cluster-identifier quicksuite-poc-cluster \
  --node-type dc2.large \
  --master-username admin \
  --master-user-password YourSecurePassword123! \
  --cluster-type single-node \
  --db-name dxl_poc \
  --publicly-accessible \
  --region ${AWS_REGION}

# Wait for cluster to be available
aws redshift wait cluster-available \
  --cluster-identifier quicksuite-poc-cluster \
  --region ${AWS_REGION}

# Get cluster endpoint
aws redshift describe-clusters \
  --cluster-identifier quicksuite-poc-cluster \
  --query 'Clusters[0].Endpoint.Address' \
  --output text
```

**Security Group Configuration:**
```bash
# Get cluster security group
CLUSTER_SG=$(aws redshift describe-clusters \
  --cluster-identifier quicksuite-poc-cluster \
  --query 'Clusters[0].VpcSecurityGroups[0].VpcSecurityGroupId' \
  --output text)

# Allow your IP to access Redshift
YOUR_IP=$(curl -s https://checkip.amazonaws.com)
aws ec2 authorize-security-group-ingress \
  --group-id ${CLUSTER_SG} \
  --protocol tcp \
  --port 5439 \
  --cidr ${YOUR_IP}/32
```

**Verification:**
- Connect to Redshift using SQL client
- Endpoint: [cluster-endpoint]:5439
- Database: dxl_poc
- Username: admin
- Password: YourSecurePassword123!

---

### Step 4: Set Up Athena

**Time Required:** 10 minutes

```bash
# Create Athena results bucket
export ATHENA_RESULTS_BUCKET=quicksuite-poc-athena-results-$(date +%s)
aws s3 mb s3://${ATHENA_RESULTS_BUCKET} --region ${AWS_REGION}

# Create Athena workgroup
aws athena create-work-group \
  --name quicksuite-poc-workgroup \
  --configuration "ResultConfigurationUpdates={OutputLocation=s3://${ATHENA_RESULTS_BUCKET}/}" \
  --region ${AWS_REGION}

# Create Glue database
aws glue create-database \
  --database-input "{\"Name\":\"dxl_poc_db\",\"Description\":\"DXL POC Database\"}" \
  --region ${AWS_REGION}
```

**Verification:**
```bash
aws athena list-work-groups --region ${AWS_REGION}
aws glue get-database --name dxl_poc_db --region ${AWS_REGION}
```

---

### Step 5: Create IAM Roles

**Time Required:** 15 minutes

```bash
# Create trust policy for Quick Suite
cat > quicksuite-trust-policy.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "quicksuite.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF

# Create IAM role for Quick Suite
aws iam create-role \
  --role-name QuickSuiteDataAccessRole \
  --assume-role-policy-document file://quicksuite-trust-policy.json

# Attach policies
aws iam attach-role-policy \
  --role-name QuickSuiteDataAccessRole \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess

aws iam attach-role-policy \
  --role-name QuickSuiteDataAccessRole \
  --policy-arn arn:aws:iam::aws:policy/AmazonRedshiftReadOnlyAccess

aws iam attach-role-policy \
  --role-name QuickSuiteDataAccessRole \
  --policy-arn arn:aws:iam::aws:policy/AmazonAthenaFullAccess

# Create inline policy for Glue
cat > quicksuite-glue-policy.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "glue:GetDatabase",
        "glue:GetTable",
        "glue:GetPartitions"
      ],
      "Resource": "*"
    }
  ]
}
EOF

aws iam put-role-policy \
  --role-name QuickSuiteDataAccessRole \
  --policy-name GlueReadAccess \
  --policy-document file://quicksuite-glue-policy.json
```

**Verification:**
```bash
aws iam get-role --role-name QuickSuiteDataAccessRole
```

---

## 3. PHASE 2: SAMPLE DATA PREPARATION (Day 2)

### Step 1: Generate Sample Data

**Time Required:** 1 hour

Create Python script to generate synthetic DXL data:

```python
# save as: generate_sample_data.py

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import json

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# Configuration
NUM_CUSTOMERS = 1000
NUM_PRODUCTS = 500
NUM_TRANSACTIONS = 5000
NUM_FITMAP_SCANS = 300

# Generate Customers
def generate_customers(n):
    customers = []
    for i in range(1, n+1):
        customers.append({
            'customer_id': i,
            'first_name': f'Customer{i}',
            'last_name': f'LastName{i}',
            'email': f'customer{i}@email.com',
            'age': random.randint(25, 65),
            'state': random.choice(['CA', 'TX', 'FL', 'NY', 'IL', 'PA']),
            'signup_date': (datetime.now() - timedelta(days=random.randint(1, 730))).strftime('%Y-%m-%d'),
            'loyalty_tier': random.choice(['Bronze', 'Silver', 'Gold', 'Platinum'])
        })
    return pd.DataFrame(customers)

# Generate Products
def generate_products(n):
    categories = ['Shirts', 'Pants', 'Outerwear', 'Activewear', 'Suits', 'Shoes', 'Accessories']
    sizes = ['XL', '2XL', '3XL', '4XL', '5XL', 'LT', 'XLT', '2XLT', '3XLT']
    
    products = []
    for i in range(1, n+1):
        category = random.choice(categories)
        products.append({
            'product_id': i,
            'product_name': f'{category} Item {i}',
            'category': category,
            'size': random.choice(sizes),
            'color': random.choice(['Navy', 'Black', 'Gray', 'Blue', 'White', 'Red']),
            'price': round(random.uniform(29.99, 199.99), 2),
            'cost': round(random.uniform(15.00, 100.00), 2),
            'brand': random.choice(['DXL', 'Harbor Bay', 'Oak Hill', 'Synrgy'])
        })
    return pd.DataFrame(products)

# Generate Sales Transactions
def generate_transactions(n, customers_df, products_df):
    transactions = []
    for i in range(1, n+1):
        customer = customers_df.sample(1).iloc[0]
        product = products_df.sample(1).iloc[0]
        quantity = random.randint(1, 3)
        
        transactions.append({
            'transaction_id': i,
            'customer_id': customer['customer_id'],
            'product_id': product['product_id'],
            'quantity': quantity,
            'unit_price': product['price'],
            'total_amount': round(quantity * product['price'], 2),
            'transaction_date': (datetime.now() - timedelta(days=random.randint(1, 180))).strftime('%Y-%m-%d'),
            'channel': random.choice(['Online', 'Store', 'Mobile']),
            'store_id': random.randint(1, 50) if random.random() > 0.3 else None
        })
    return pd.DataFrame(transactions)

# Generate FitMap Measurements
def generate_fitmap_data(n, customers_df):
    measurements = []
    for i in range(1, n+1):
        customer = customers_df.sample(1).iloc[0]
        
        measurements.append({
            'scan_id': i,
            'customer_id': customer['customer_id'],
            'scan_date': (datetime.now() - timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d'),
            'height_inches': round(random.uniform(68, 78), 1),
            'chest_inches': round(random.uniform(44, 60), 1),
            'waist_inches': round(random.uniform(38, 56), 1),
            'hip_inches': round(random.uniform(42, 58), 1),
            'inseam_inches': round(random.uniform(28, 36), 1),
            'shoulder_width_inches': round(random.uniform(18, 24), 1),
            'arm_length_inches': round(random.uniform(32, 38), 1),
            'confidence_score': round(random.uniform(0.75, 0.98), 2),
            'device_type': random.choice(['iPhone', 'Android', 'iPad']),
            'recommended_size': random.choice(['XL', '2XL', '3XL', '4XL', 'XLT', '2XLT'])
        })
    return pd.DataFrame(measurements)

# Generate Inventory
def generate_inventory(products_df):
    inventory = []
    for _, product in products_df.iterrows():
        inventory.append({
            'product_id': product['product_id'],
            'warehouse_qty': random.randint(0, 200),
            'store_qty': random.randint(0, 50),
            'reorder_point': 20,
            'last_restock_date': (datetime.now() - timedelta(days=random.randint(1, 90))).strftime('%Y-%m-%d')
        })
    return pd.DataFrame(inventory)

# Generate all data
print("Generating sample data...")
customers_df = generate_customers(NUM_CUSTOMERS)
products_df = generate_products(NUM_PRODUCTS)
transactions_df = generate_transactions(NUM_TRANSACTIONS, customers_df, products_df)
fitmap_df = generate_fitmap_data(NUM_FITMAP_SCANS, customers_df)
inventory_df = generate_inventory(products_df)

# Save to CSV
customers_df.to_csv('customers.csv', index=False)
products_df.to_csv('products.csv', index=False)
transactions_df.to_csv('transactions.csv', index=False)
fitmap_df.to_csv('fitmap_measurements.csv', index=False)
inventory_df.to_csv('inventory.csv', index=False)

print("Sample data generated successfully!")
print(f"Customers: {len(customers_df)}")
print(f"Products: {len(products_df)}")
print(f"Transactions: {len(transactions_df)}")
print(f"FitMap Scans: {len(fitmap_df)}")
print(f"Inventory Records: {len(inventory_df)}")
```

**Run the script:**
```bash
python generate_sample_data.py
```



### Step 2: Upload Data to S3

**Time Required:** 15 minutes

```bash
# Upload CSV files to S3
aws s3 cp customers.csv s3://${BUCKET_NAME}/data/customers/
aws s3 cp products.csv s3://${BUCKET_NAME}/data/products/
aws s3 cp transactions.csv s3://${BUCKET_NAME}/data/sales/
aws s3 cp fitmap_measurements.csv s3://${BUCKET_NAME}/data/fitmap/
aws s3 cp inventory.csv s3://${BUCKET_NAME}/data/inventory/

# Verify uploads
aws s3 ls s3://${BUCKET_NAME}/data/ --recursive
```

---

### Step 3: Load Data into Redshift

**Time Required:** 30 minutes

Create SQL script to load data:

```sql
-- save as: load_redshift_data.sql

-- Create schema
CREATE SCHEMA IF NOT EXISTS dxl;

-- Create customers table
CREATE TABLE dxl.customers (
    customer_id INTEGER PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(200),
    age INTEGER,
    state VARCHAR(2),
    signup_date DATE,
    loyalty_tier VARCHAR(20)
);

-- Create products table
CREATE TABLE dxl.products (
    product_id INTEGER PRIMARY KEY,
    product_name VARCHAR(200),
    category VARCHAR(50),
    size VARCHAR(10),
    color VARCHAR(50),
    price DECIMAL(10,2),
    cost DECIMAL(10,2),
    brand VARCHAR(100)
);

-- Create transactions table
CREATE TABLE dxl.transactions (
    transaction_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    unit_price DECIMAL(10,2),
    total_amount DECIMAL(10,2),
    transaction_date DATE,
    channel VARCHAR(20),
    store_id INTEGER
);

-- Create fitmap_measurements table
CREATE TABLE dxl.fitmap_measurements (
    scan_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    scan_date DATE,
    height_inches DECIMAL(5,1),
    chest_inches DECIMAL(5,1),
    waist_inches DECIMAL(5,1),
    hip_inches DECIMAL(5,1),
    inseam_inches DECIMAL(5,1),
    shoulder_width_inches DECIMAL(5,1),
    arm_length_inches DECIMAL(5,1),
    confidence_score DECIMAL(4,2),
    device_type VARCHAR(50),
    recommended_size VARCHAR(10)
);

-- Create inventory table
CREATE TABLE dxl.inventory (
    product_id INTEGER PRIMARY KEY,
    warehouse_qty INTEGER,
    store_qty INTEGER,
    reorder_point INTEGER,
    last_restock_date DATE
);

-- Load data from S3 (replace BUCKET_NAME with your actual bucket)
COPY dxl.customers
FROM 's3://BUCKET_NAME/data/customers/customers.csv'
IAM_ROLE 'arn:aws:iam::ACCOUNT_ID:role/QuickSuiteDataAccessRole'
CSV
IGNOREHEADER 1;

COPY dxl.products
FROM 's3://BUCKET_NAME/data/products/products.csv'
IAM_ROLE 'arn:aws:iam::ACCOUNT_ID:role/QuickSuiteDataAccessRole'
CSV
IGNOREHEADER 1;

COPY dxl.transactions
FROM 's3://BUCKET_NAME/data/sales/transactions.csv'
IAM_ROLE 'arn:aws:iam::ACCOUNT_ID:role/QuickSuiteDataAccessRole'
CSV
IGNOREHEADER 1;

COPY dxl.fitmap_measurements
FROM 's3://BUCKET_NAME/data/fitmap/fitmap_measurements.csv'
IAM_ROLE 'arn:aws:iam::ACCOUNT_ID:role/QuickSuiteDataAccessRole'
CSV
IGNOREHEADER 1;

COPY dxl.inventory
FROM 's3://BUCKET_NAME/data/inventory/inventory.csv'
IAM_ROLE 'arn:aws:iam::ACCOUNT_ID:role/QuickSuiteDataAccessRole'
CSV
IGNOREHEADER 1;

-- Verify data loaded
SELECT 'customers' as table_name, COUNT(*) as row_count FROM dxl.customers
UNION ALL
SELECT 'products', COUNT(*) FROM dxl.products
UNION ALL
SELECT 'transactions', COUNT(*) FROM dxl.transactions
UNION ALL
SELECT 'fitmap_measurements', COUNT(*) FROM dxl.fitmap_measurements
UNION ALL
SELECT 'inventory', COUNT(*) FROM dxl.inventory;
```

**Execute the script:**
```bash
# Replace placeholders
sed -i "s/BUCKET_NAME/${BUCKET_NAME}/g" load_redshift_data.sql
sed -i "s/ACCOUNT_ID/$(aws sts get-caller-identity --query Account --output text)/g" load_redshift_data.sql

# Execute SQL (using psql or your SQL client)
psql -h [REDSHIFT_ENDPOINT] -U admin -d dxl_poc -p 5439 -f load_redshift_data.sql
```

---

### Step 4: Create Athena Tables

**Time Required:** 15 minutes

```sql
-- Create external tables in Athena

-- Customers table
CREATE EXTERNAL TABLE IF NOT EXISTS dxl_poc_db.customers_s3 (
    customer_id INT,
    first_name STRING,
    last_name STRING,
    email STRING,
    age INT,
    state STRING,
    signup_date STRING,
    loyalty_tier STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION 's3://BUCKET_NAME/data/customers/'
TBLPROPERTIES ('skip.header.line.count'='1');

-- Products table
CREATE EXTERNAL TABLE IF NOT EXISTS dxl_poc_db.products_s3 (
    product_id INT,
    product_name STRING,
    category STRING,
    size STRING,
    color STRING,
    price DOUBLE,
    cost DOUBLE,
    brand STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION 's3://BUCKET_NAME/data/products/'
TBLPROPERTIES ('skip.header.line.count'='1');
```

---

## 4. PHASE 3: QUICK SUITE CONFIGURATION (Day 3-4)

### Step 1: Connect Data Sources to Quick Index

**Time Required:** 1 hour

**In Quick Suite Console:**

1. **Navigate to Quick Index**
   - Go to: Quick Suite Console → Quick Index → Data Sources

2. **Add Redshift Connection**
   ```
   Connection Name: DXL_Redshift_POC
   Connection Type: Amazon Redshift
   Cluster Identifier: quicksuite-poc-cluster
   Database: dxl_poc
   Schema: dxl
   Authentication: IAM Role
   IAM Role ARN: arn:aws:iam::ACCOUNT_ID:role/QuickSuiteDataAccessRole
   
   Tables to Index:
   ✓ customers
   ✓ products
   ✓ transactions
   ✓ fitmap_measurements
   ✓ inventory
   
   Refresh Schedule: Every 1 hour
   ```

3. **Add S3 Connection**
   ```
   Connection Name: DXL_S3_DataLake
   Connection Type: Amazon S3
   Bucket: quicksuite-poc-dxl-XXXXX
   Prefix: data/
   File Types: CSV, JSON
   IAM Role ARN: arn:aws:iam::ACCOUNT_ID:role/QuickSuiteDataAccessRole
   
   Refresh Schedule: Every 4 hours
   ```

4. **Add Athena Connection**
   ```
   Connection Name: DXL_Athena_POC
   Connection Type: Amazon Athena
   Database: dxl_poc_db
   Workgroup: quicksuite-poc-workgroup
   IAM Role ARN: arn:aws:iam::ACCOUNT_ID:role/QuickSuiteDataAccessRole
   ```

5. **Verify Indexing**
   - Wait 10-15 minutes for initial indexing
   - Check: Quick Index → Data Catalog
   - Confirm all tables are visible and searchable

---

### Step 2: Create Spaces

**Time Required:** 30 minutes

**Create FitMap Analytics Space:**

1. Navigate to: Quick Suite → Spaces → Create New Space
2. Configuration:
   ```
   Space Name: FitMap Analytics
   Description: Body measurement analysis and sizing insights
   
   Connected Data Sources:
   ✓ dxl.fitmap_measurements (Redshift)
   ✓ dxl.customers (Redshift)
   ✓ dxl.products (Redshift)
   
   Access Control:
   - Owner: You
   - Viewers: All users (for POC)
   
   Refresh Schedule: Hourly
   ```

3. **Upload Documents:**
   - Create a simple PDF: "FitMap_Sizing_Standards.pdf" with sizing guidelines
   - Upload to the Space

**Create Merchandising Space:**

1. Create New Space:
   ```
   Space Name: Merchandising Intelligence
   Description: Sales, inventory, and product performance
   
   Connected Data Sources:
   ✓ dxl.transactions (Redshift)
   ✓ dxl.products (Redshift)
   ✓ dxl.inventory (Redshift)
   ✓ dxl.customers (Redshift)
   ```

---

### Step 3: Configure Chat Agents

**Time Required:** 45 minutes

**Create FitMap Insights Agent:**

1. Navigate to: Quick Suite → Chat Agents → Create Agent
2. Configuration:
   ```
   Agent Name: FitMap Insights Assistant
   Description: Analyzes body measurements and provides sizing recommendations
   
   Knowledge Sources:
   - Space: FitMap Analytics
   - Tables: fitmap_measurements, customers, products
   - Documents: FitMap_Sizing_Standards.pdf
   
   Instructions:
   "You are a FitMap sizing expert. Help users analyze body measurement data,
   identify sizing trends, and provide fit recommendations. Always cite
   confidence scores and measurement sources. Be precise with numbers."
   
   Capabilities:
   ✓ Query measurements by date range
   ✓ Calculate statistics (averages, distributions)
   ✓ Analyze confidence scores
   ✓ Recommend sizes based on measurements
   
   Permissions:
   - Read: All FitMap data
   - Write: None
   ```

3. **Test the Agent:**
   - Query: "What's the average chest measurement for customers in the last 30 days?"
   - Query: "Show me scans with confidence score below 0.80"
   - Query: "What's the most common recommended size?"

**Create Sales Assistant Agent:**

1. Create Agent:
   ```
   Agent Name: Sales Assistant
   Description: Helps with product information and customer inquiries
   
   Knowledge Sources:
   - Space: Merchandising Intelligence
   - Tables: products, inventory, customers
   
   Instructions:
   "You are a DXL sales assistant. Help with product availability,
   pricing, and customer information. Be friendly and helpful."
   
   Capabilities:
   ✓ Check product availability
   ✓ Provide pricing information
   ✓ Look up customer history
   ```

---

### Step 4: Create Quick Sight Dashboards

**Time Required:** 1 hour

**Create Sales Performance Dashboard:**

1. Navigate to: Quick Suite → Quick Sight → Create Dashboard
2. Use natural language:
   ```
   "Create a dashboard showing:
   - Total sales by month for the last 6 months
   - Top 10 products by revenue
   - Sales by channel (Online, Store, Mobile)
   - Average transaction value
   - Sales by category"
   ```

3. Quick Sight will generate the dashboard automatically
4. Customize colors and layout as needed
5. Save as: "Sales Performance Dashboard"

**Create FitMap Analytics Dashboard:**

1. Create new dashboard with prompt:
   ```
   "Create a FitMap analytics dashboard showing:
   - Total scans by month
   - Average confidence score trend
   - Distribution of recommended sizes
   - Scans by device type
   - Top 5 most common measurements"
   ```

2. Save as: "FitMap Analytics Dashboard"

---

### Step 5: Build Quick Flows

**Time Required:** 1 hour

**Flow 1: Weekly FitMap Summary Report**

1. Navigate to: Quick Suite → Quick Flows → Create Flow
2. Use natural language:
   ```
   "Create a flow that runs every Monday at 8 AM and:
   1. Counts total FitMap scans from the past week
   2. Calculates average confidence score
   3. Identifies the most common recommended size
   4. Generates a summary report
   5. Sends the report via email to me"
   ```

3. Quick Flows will generate the workflow
4. Review and adjust:
   - Input: Date range (last 7 days)
   - Process: Query fitmap_measurements table
   - Output: Email with summary
5. Test the flow manually
6. Save and activate

**Flow 2: Low Inventory Alert**

1. Create new flow:
   ```
   "Create a flow that runs every 4 hours and:
   1. Checks inventory levels for all products
   2. Identifies products with warehouse_qty < 20
   3. Lists the low-stock products
   4. Sends an alert email if any products are low"
   ```

2. Test and activate



---

## 5. PHASE 4: USE CASE DEMONSTRATIONS (Day 5-6)

### Demo 1: FitMap Measurement Intelligence

**Objective:** Show how Quick Suite accelerates FitMap analysis

**Preparation:**
1. Open FitMap Insights Assistant
2. Prepare 5-6 sample queries
3. Document response times

**Demo Script:**

```
Query 1: "What are the top 5 most common chest measurements in the last 90 days?"
Expected: Table with measurements and counts

Query 2: "Show me the average confidence score by device type"
Expected: Statistics showing iPhone vs Android vs iPad scores

Query 3: "How many scans have a waist measurement between 40 and 45 inches?"
Expected: Count and percentage

Query 4: "What's the distribution of recommended sizes for customers aged 35-50?"
Expected: Chart or table showing size distribution

Query 5: "Identify scans with confidence score below 0.80 in the last 30 days"
Expected: List of low-confidence scans with details

Query 6: "Generate a report on sizing trends for Q4"
Expected: Comprehensive analysis with charts
```

**Key Talking Points:**
- ✅ No SQL required - business users can query directly
- ✅ Instant results (vs. 2-3 weeks manual analysis)
- ✅ Natural language understanding
- ✅ Automatic visualization
- ✅ Source citations for trust

---

### Demo 2: Quick Research - Competitive Analysis

**Objective:** Demonstrate AI-powered research capabilities

**Demo Script:**

1. Navigate to: Quick Suite → Quick Research
2. Enter research query:
   ```
   "Analyze our product pricing compared to industry standards for big & tall
   men's clothing. Focus on shirts and pants categories. Include recommendations
   for pricing optimization."
   ```

3. Quick Research will:
   - Generate research plan
   - Gather data from internal sources (products table)
   - Synthesize findings
   - Provide recommendations with citations

4. Show the generated report (PDF export)

**Key Talking Points:**
- ✅ Comprehensive analysis in minutes
- ✅ Combines internal and external data
- ✅ Source verification
- ✅ Actionable recommendations
- ✅ Professional report format

---

### Demo 3: Automated Reporting with Quick Flows

**Objective:** Show workflow automation capabilities

**Demo Script:**

1. Navigate to: Quick Suite → Quick Flows
2. Show the "Weekly FitMap Summary Report" flow
3. Manually trigger the flow
4. Show execution progress
5. Display the generated email report

**Key Talking Points:**
- ✅ No-code automation
- ✅ Scheduled execution
- ✅ Eliminates manual reporting
- ✅ Consistent format
- ✅ Time savings (12 hours → 15 minutes)

---

### Demo 4: Interactive Dashboards with Quick Sight

**Objective:** Demonstrate conversational BI

**Demo Script:**

1. Open "Sales Performance Dashboard"
2. Use natural language queries:
   ```
   "Show me sales for the Shirts category in the last 30 days"
   "Compare online vs store sales for Q4"
   "What's the average transaction value by loyalty tier?"
   "Which products have the highest profit margin?"
   ```

3. Show one-click actions:
   - Click on low-performing product
   - Create Jira ticket for merchandising review
   - Send alert to team via email

**Key Talking Points:**
- ✅ Conversational interface
- ✅ No dashboard building required
- ✅ Real-time data
- ✅ Action from insights
- ✅ Mobile accessible

---

### Demo 5: Embedded Chat in Application

**Objective:** Show how Quick Suite integrates into existing apps

**Demo Script:**

1. Create simple HTML page with embedded chat:

```html
<!DOCTYPE html>
<html>
<head>
    <title>DXL Sales Portal - POC</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        #chat-container { 
            width: 400px; 
            height: 600px; 
            border: 1px solid #ccc; 
            border-radius: 8px;
        }
    </style>
</head>
<body>
    <h1>DXL Sales Portal</h1>
    <p>Ask the Sales Assistant about products, inventory, or customers:</p>
    
    <div id="chat-container">
        <!-- Quick Suite Embedded Chat -->
        <iframe 
            src="https://quicksuite.aws.amazon.com/embed/chat/AGENT_ID"
            width="100%" 
            height="100%"
            frameborder="0">
        </iframe>
    </div>
</body>
</html>
```

2. Open in browser
3. Interact with embedded agent:
   ```
   "Is product ID 123 in stock?"
   "What's the price of Navy 3XL dress shirts?"
   "Show me customer 456's recent purchases"
   ```

**Key Talking Points:**
- ✅ Seamless integration
- ✅ No app rebuild required
- ✅ Contextual intelligence
- ✅ Consistent experience
- ✅ Works in POS, CRM, custom apps

---

## 6. PHASE 5: DEMO PREPARATION (Day 7)

### Step 1: Create Demo Presentation

**Time Required:** 2 hours

**Presentation Structure:**

```
Slide 1: Title
- AWS Quick Suite POC for DXL
- Your Name, Date

Slide 2: Agenda
- Current Challenges
- Quick Suite Overview
- Live Demonstrations
- Business Impact
- Next Steps

Slide 3: Current Challenges
- Manual reporting (36 hrs/week)
- FitMap insights delayed (2-3 weeks)
- Limited self-service (15% adoption)
- Pricing decision lag (3-5 days)

Slide 4: Quick Suite Solution
- Unified AI platform
- Natural language queries
- Automated workflows
- Real-time insights

Slide 5-9: Live Demos
- [Screen recordings or live demos]

Slide 10: Business Impact
- 98% faster FitMap analysis
- 405% ROI
- $1M+ annual benefit

Slide 11: POC Results
- 5 use cases demonstrated
- All data sources connected
- 2 chat agents configured
- 2 automated workflows
- 2 interactive dashboards

Slide 12: Next Steps
- Pilot with 10 users (4 weeks)
- Full implementation (12 weeks)
- Budget approval ($243K Year 1)
```

---

### Step 2: Record Demo Videos

**Time Required:** 1 hour

Use screen recording software (OBS, Loom, or QuickTime) to record:

1. **Video 1: FitMap Analysis (3 min)**
   - Show natural language queries
   - Highlight instant results
   - Compare to "old way" (SQL, Excel)

2. **Video 2: Automated Reporting (2 min)**
   - Show flow execution
   - Display generated report
   - Emphasize time savings

3. **Video 3: Interactive Dashboard (2 min)**
   - Conversational queries
   - One-click actions
   - Mobile view

**Backup Plan:**
- Have videos ready in case live demo fails
- Screenshots as additional backup

---

### Step 3: Prepare Demo Script

**Time Required:** 30 minutes

```markdown
# Demo Script for DXL Leadership

## Introduction (2 min)
"Good morning. Today I'll demonstrate AWS Quick Suite, a unified AI platform
that addresses our data analytics challenges. We've set up a working POC
environment with sample DXL data to show real capabilities."

## Demo 1: FitMap Intelligence (5 min)
"Let's start with our FitMap investment. Currently, analyzing body measurement
data takes 2-3 weeks. Watch this..."

[Open FitMap Insights Assistant]

"I'll ask: 'What are the top 5 chest measurements in the last 90 days?'"

[Show instant results]

"Notice: No SQL, instant results, automatic visualization. This is what
business users can do themselves."

[Run 2-3 more queries]

## Demo 2: Automated Reporting (3 min)
"Next, our manual reporting challenge. 36 hours per week compiling reports.
Here's the automated solution..."

[Show Quick Flow]
[Trigger flow]
[Show generated report]

"This runs automatically every Monday. Time savings: 12 hours to 15 minutes."

## Demo 3: Interactive Dashboards (4 min)
"Now, conversational business intelligence..."

[Open Sales Dashboard]
[Run natural language queries]
[Show one-click actions]

"Any business user can do this. No training required."

## Business Impact (3 min)
"Based on this POC and industry benchmarks:
- 405% Year 1 ROI
- $1M+ annual benefit
- 2.2 month payback
- Low risk, AWS-native solution"

## Next Steps (2 min)
"Recommended path:
1. Pilot with 10 users - 4 weeks
2. Full implementation - 12 weeks
3. Investment: $243K Year 1

Questions?"
```

---

### Step 4: Test Everything

**Time Required:** 1 hour

**Pre-Demo Checklist:**

```
□ Quick Suite console accessible
□ All data sources connected and indexed
□ FitMap Insights Assistant responding correctly
□ Sales Assistant responding correctly
□ Dashboards loading properly
□ Quick Flows executing successfully
□ Embedded chat demo page working
□ Internet connection stable
□ Backup videos ready
□ Screenshots prepared
□ Demo script printed
□ Presentation loaded
□ Screen sharing tested
□ Audio/video tested (if virtual)
```

**Test Queries:**

Run through all demo queries to ensure:
- Responses are accurate
- Response time is acceptable (<5 seconds)
- Visualizations render correctly
- No error messages

---

## 7. TROUBLESHOOTING GUIDE

### Issue 1: Quick Suite Not Accessible

**Symptoms:** Cannot access Quick Suite console

**Solutions:**
```bash
# Check if Quick Suite is enabled in your region
aws quicksuite describe-account-settings --region us-east-1

# Verify IAM permissions
aws iam get-user

# Check browser console for errors (F12)
```

---

### Issue 2: Data Sources Not Connecting

**Symptoms:** Redshift/S3 connection fails

**Solutions:**
```bash
# Verify IAM role exists
aws iam get-role --role-name QuickSuiteDataAccessRole

# Check Redshift cluster status
aws redshift describe-clusters --cluster-identifier quicksuite-poc-cluster

# Test S3 access
aws s3 ls s3://${BUCKET_NAME}/

# Verify security group allows Quick Suite IP ranges
# Add Quick Suite service IP ranges to security group
```

---

### Issue 3: Slow Query Performance

**Symptoms:** Queries take >10 seconds

**Solutions:**
```sql
-- Analyze Redshift tables
ANALYZE dxl.customers;
ANALYZE dxl.products;
ANALYZE dxl.transactions;
ANALYZE dxl.fitmap_measurements;

-- Vacuum tables
VACUUM dxl.transactions;

-- Check query execution
SELECT * FROM svl_qlog ORDER BY starttime DESC LIMIT 10;
```

---

### Issue 4: Chat Agent Not Responding

**Symptoms:** Agent returns errors or no response

**Solutions:**
1. Check agent configuration
2. Verify knowledge sources are indexed
3. Test with simpler queries
4. Check CloudWatch logs for errors
5. Restart agent (disable/enable)

---

### Issue 5: Quick Flows Failing

**Symptoms:** Workflow execution fails

**Solutions:**
1. Check execution logs in Quick Flows console
2. Verify data source connectivity
3. Test each step individually
4. Check IAM permissions for actions
5. Simplify workflow and add steps incrementally

---

## 8. COST ESTIMATION

### Daily Costs (7-day POC)

| Service | Daily Cost | 7-Day Total |
|---------|-----------|-------------|
| Quick Suite (Trial) | $0 | $0 |
| Redshift dc2.large | $25 | $175 |
| S3 Storage (50GB) | $0.16 | $1.15 |
| S3 Requests | $0.05 | $0.35 |
| Athena Queries | $0.71 | $5.00 |
| Glue Crawler | $0.06 | $0.44 |
| Lambda | $0.03 | $0.20 |
| CloudWatch | $0.07 | $0.50 |
| Data Transfer | $0.14 | $1.00 |
| **TOTAL** | **$26** | **$183.64** |

### Cost Optimization Tips:

1. **Pause Redshift when not in use:**
   ```bash
   aws redshift pause-cluster --cluster-identifier quicksuite-poc-cluster
   aws redshift resume-cluster --cluster-identifier quicksuite-poc-cluster
   ```

2. **Use S3 Intelligent-Tiering:**
   ```bash
   aws s3api put-bucket-intelligent-tiering-configuration \
     --bucket ${BUCKET_NAME} \
     --id poc-tiering \
     --intelligent-tiering-configuration file://tiering-config.json
   ```

3. **Limit Athena query data scanned:**
   - Use partitioned tables
   - Specify columns in SELECT
   - Use LIMIT clause

---

## 9. CLEANUP INSTRUCTIONS

### After Demo (to avoid ongoing costs)

**Time Required:** 20 minutes

```bash
# 1. Delete Redshift cluster
aws redshift delete-cluster \
  --cluster-identifier quicksuite-poc-cluster \
  --skip-final-cluster-snapshot \
  --region ${AWS_REGION}

# 2. Delete S3 buckets
aws s3 rb s3://${BUCKET_NAME} --force
aws s3 rb s3://${ATHENA_RESULTS_BUCKET} --force

# 3. Delete Glue database
aws glue delete-database --name dxl_poc_db

# 4. Delete Athena workgroup
aws athena delete-work-group \
  --work-group quicksuite-poc-workgroup \
  --recursive-delete-option

# 5. Delete IAM role
aws iam detach-role-policy \
  --role-name QuickSuiteDataAccessRole \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess

aws iam detach-role-policy \
  --role-name QuickSuiteDataAccessRole \
  --policy-arn arn:aws:iam::aws:policy/AmazonRedshiftReadOnlyAccess

aws iam detach-role-policy \
  --role-name QuickSuiteDataAccessRole \
  --policy-arn arn:aws:iam::aws:policy/AmazonAthenaFullAccess

aws iam delete-role-policy \
  --role-name QuickSuiteDataAccessRole \
  --policy-name GlueReadAccess

aws iam delete-role --role-name QuickSuiteDataAccessRole

# 6. Disable Quick Suite (if not continuing)
# Go to Quick Suite Console → Settings → Disable Account

# 7. Verify cleanup
aws redshift describe-clusters --region ${AWS_REGION}
aws s3 ls
aws glue get-databases
```

### Keep for Future Use

If you want to keep the POC for future demos:
- Pause Redshift cluster (saves 90% of cost)
- Keep S3 data (minimal cost)
- Keep Quick Suite configuration
- Document access credentials

---

## 10. SUCCESS CRITERIA

### POC is Successful If:

✅ **Technical:**
- All 5 data sources connected and indexed
- 2 chat agents responding accurately
- 2 dashboards displaying data correctly
- 2 automated workflows executing successfully
- Query response time <5 seconds
- System uptime >99%

✅ **Functional:**
- FitMap analysis queries work as expected
- Natural language understanding is accurate
- Automated reports generate correctly
- Embedded chat integrates properly
- One-click actions execute successfully

✅ **Business:**
- Demonstrates 90%+ time savings for analysis
- Shows clear ROI potential
- Addresses all identified pain points
- Impresses DXL leadership
- Generates approval for pilot phase

---

## 11. NEXT STEPS AFTER SUCCESSFUL POC

### Immediate (Week 1):
1. Present POC results to DXL leadership
2. Gather feedback and questions
3. Refine business case based on feedback
4. Secure budget approval

### Short-term (Weeks 2-4):
1. Plan pilot with 10 DXL users
2. Identify pilot participants
3. Set up production-grade environment
4. Develop training materials

### Medium-term (Weeks 5-16):
1. Execute 4-week pilot
2. Gather user feedback
3. Measure success metrics
4. Plan full rollout (12 weeks)

---

## APPENDIX A: Quick Reference Commands

```bash
# Check Redshift status
aws redshift describe-clusters --cluster-identifier quicksuite-poc-cluster

# List S3 contents
aws s3 ls s3://${BUCKET_NAME}/ --recursive

# Test Athena query
aws athena start-query-execution \
  --query-string "SELECT COUNT(*) FROM dxl_poc_db.customers_s3" \
  --result-configuration "OutputLocation=s3://${ATHENA_RESULTS_BUCKET}/"

# Check IAM role
aws iam get-role --role-name QuickSuiteDataAccessRole

# View CloudWatch logs
aws logs tail /aws/quicksuite/poc --follow
```

---

## APPENDIX B: Sample Queries for Testing

```sql
-- FitMap Analysis Queries
SELECT 
    recommended_size,
    COUNT(*) as scan_count,
    AVG(confidence_score) as avg_confidence
FROM dxl.fitmap_measurements
WHERE scan_date >= CURRENT_DATE - 90
GROUP BY recommended_size
ORDER BY scan_count DESC;

-- Sales Performance
SELECT 
    DATE_TRUNC('month', transaction_date) as month,
    SUM(total_amount) as revenue,
    COUNT(*) as transaction_count
FROM dxl.transactions
GROUP BY month
ORDER BY month DESC;

-- Low Inventory Alert
SELECT 
    p.product_name,
    p.category,
    p.size,
    i.warehouse_qty,
    i.store_qty
FROM dxl.inventory i
JOIN dxl.products p ON i.product_id = p.product_id
WHERE i.warehouse_qty < 20
ORDER BY i.warehouse_qty ASC;
```

---

**Document Version:** 1.0  
**Last Updated:** November 26, 2025  
**Author:** Senior Data Engineering Team  
**Status:** Ready for Implementation

---

**For questions or support during POC implementation, contact:**
- AWS Support: https://console.aws.amazon.com/support/
- Quick Suite Documentation: https://docs.aws.amazon.com/quicksuite/
- Internal Team: [Your contact info]

**Good luck with your POC! 🚀**
