# AWS Quick Suite POC - Complete Setup Guide

## 🎯 POC Objective
Demonstrate AWS Quick Suite's ability to provide conversational analytics across FitMap body measurement data, customer data, and order data - accessible directly from Microsoft Teams.

---

## 📋 Phase 1: Data Preparation (COMPLETED ✓)

You now have Python scripts that generate realistic sample data:

### Generated Data
- **FitMap/SizeStream**: 1,000 users, 2,500 scans, body measurements
- **Customer/CRM**: 5,000 customers, 15,000 transactions
- **Orders**: 3,000 orders with line items

### Next Action
```bash
cd poc_data_generators
pip install -r requirements.txt
python run_all_generators.py
```

This creates 19 CSV files ready for upload.

---

## 📋 Phase 2: AWS Infrastructure Setup (Days 1-3)

### Step 1: Create S3 Bucket for Data

```bash
# Create S3 bucket
aws s3 mb s3://dxl-quicksuite-poc-data --region us-east-1

# Create folder structure
aws s3api put-object --bucket dxl-quicksuite-poc-data --key fitmap/
aws s3api put-object --bucket dxl-quicksuite-poc-data --key customer/
aws s3api put-object --bucket dxl-quicksuite-poc-data --key orders/
```

### Step 2: Upload CSV Files to S3

```bash
# Upload FitMap data
aws s3 cp size_users.csv s3://dxl-quicksuite-poc-data/fitmap/size_users/
aws s3 cp size_scans.csv s3://dxl-quicksuite-poc-data/fitmap/size_scans/
aws s3 cp size_app_measures.csv s3://dxl-quicksuite-poc-data/fitmap/size_app_measures/
aws s3 cp size_dxl_custom_measures.csv s3://dxl-quicksuite-poc-data/fitmap/size_dxl_custom_measures/

# Upload Customer data
aws s3 cp customer.csv s3://dxl-quicksuite-poc-data/customer/customer/
aws s3 cp address.csv s3://dxl-quicksuite-poc-data/customer/address/
aws s3 cp email.csv s3://dxl-quicksuite-poc-data/customer/email/
aws s3 cp store.csv s3://dxl-quicksuite-poc-data/customer/store/
aws s3 cp transaction_header.csv s3://dxl-quicksuite-poc-data/customer/transaction_header/
aws s3 cp transaction_detail.csv s3://dxl-quicksuite-poc-data/customer/transaction_detail/
aws s3 cp reward_detail.csv s3://dxl-quicksuite-poc-data/customer/reward_detail/
aws s3 cp household.csv s3://dxl-quicksuite-poc-data/customer/household/

# Upload Order data
aws s3 cp orderheader.csv s3://dxl-quicksuite-poc-data/orders/orderheader/
aws s3 cp orderline.csv s3://dxl-quicksuite-poc-data/orders/orderline/
aws s3 cp orderline_items.csv s3://dxl-quicksuite-poc-data/orders/orderline_items/
aws s3 cp orderchargedetail.csv s3://dxl-quicksuite-poc-data/orders/orderchargedetail/
aws s3 cp invoice.csv s3://dxl-quicksuite-poc-data/orders/invoice/
aws s3 cp payment.csv s3://dxl-quicksuite-poc-data/orders/payment/
aws s3 cp quantitydetail.csv s3://dxl-quicksuite-poc-data/orders/quantitydetail/
```

### Step 3: Option A - Load to Existing Redshift (Recommended)

If you already have Redshift cluster:

```sql
-- Create schemas if they don't exist
CREATE SCHEMA IF NOT EXISTS dxlg_size_stream;
CREATE SCHEMA IF NOT EXISTS cimb_repl;
CREATE SCHEMA IF NOT EXISTS dxlg_olap_orders;

-- Load data using COPY command (example for one table)
COPY dxlg_size_stream.size_users
FROM 's3://dxl-quicksuite-poc-data/fitmap/size_users/'
IAM_ROLE 'arn:aws:iam::YOUR_ACCOUNT:role/RedshiftRole'
CSV IGNOREHEADER 1
REGION 'us-east-1';

-- Repeat for all tables
```

### Step 3: Option B - Use Athena (Alternative)

If you don't have Redshift or want to test with Athena:

1. **Open AWS Athena Console**
2. **Create Database:**
```sql
CREATE DATABASE dxl_quicksuite_poc;
```

3. **Create External Tables** (example for size_users):
```sql
CREATE EXTERNAL TABLE dxl_quicksuite_poc.size_users (
    id STRING,
    source_app STRING,
    created STRING,
    modified STRING,
    source_attendant STRING,
    last_name STRING,
    first_name STRING,
    date_of_birth STRING,
    email STRING,
    phone STRING,
    height INT,
    weight INT,
    process_date STRING,
    load_filename STRING,
    load_timestamp STRING,
    gender STRING,
    year INT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION 's3://dxl-quicksuite-poc-data/fitmap/size_users/'
TBLPROPERTIES ('skip.header.line.count'='1');
```

4. **Repeat for all 19 tables**

---

## 📋 Phase 3: AWS Quick Suite Configuration (Days 4-7)

### Step 1: Access Quick Suite

1. Go to AWS Console → **Amazon QuickSight**
2. You should see **Quick Suite** option (trial account)
3. Click **Get Started with Quick Suite**

### Step 2: Set Up Quick Index

Quick Index is the foundation that connects all your data sources.

1. Navigate to **Quick Index** in Quick Suite
2. Click **Add Data Source**
3. Configure connections:

**For Redshift:**
- Data Source Type: **Amazon Redshift**
- Connection Name: `DXL_Redshift_POC`
- Cluster: Select your Redshift cluster
- Database: Your database name
- Schemas: `dxlg_size_stream`, `cimb_repl`, `dxlg_olap_orders`
- Authentication: IAM or username/password

**For Athena:**
- Data Source Type: **Amazon Athena**
- Connection Name: `DXL_Athena_POC`
- Database: `dxl_quicksuite_poc`
- Workgroup: `primary`
- Output Location: `s3://dxl-quicksuite-poc-data/athena-results/`

**For S3 (Documents):**
- Data Source Type: **Amazon S3**
- Connection Name: `DXL_Documents`
- Bucket: `dxl-quicksuite-poc-data`
- Prefix: `documents/` (for any PDFs, docs you want to include)

4. Click **Index Data** - this will crawl and index all your data

### Step 3: Create Spaces

Spaces organize data by context/department.

**Create 3 Spaces:**

1. **FitMap Analytics Space**
   - Name: `FitMap Body Measurements`
   - Description: `Body scan data and size recommendations`
   - Data Sources: 
     - `dxlg_size_stream.size_users`
     - `dxlg_size_stream.size_scans`
     - `dxlg_size_stream.size_app_measures`
     - `dxlg_size_stream.size_dxl_custom_measures`
   - Users: Add your email

2. **Customer Analytics Space**
   - Name: `Customer & Transactions`
   - Description: `Customer data, transactions, and rewards`
   - Data Sources:
     - `cimb_repl.customer`
     - `cimb_repl.address`
     - `cimb_repl.transaction_header`
     - `cimb_repl.transaction_detail`
     - `cimb_repl.store`
   - Users: Add your email

3. **E-commerce Analytics Space**
   - Name: `Online Orders`
   - Description: `E-commerce orders and fulfillment`
   - Data Sources:
     - `dxlg_olap_orders.orderheader`
     - `dxlg_olap_orders.orderline`
     - `dxlg_olap_orders.orderline_items`
   - Users: Add your email

### Step 4: Create Chat Agents

**Agent 1: FitMap Sizing Expert**
- Name: `FitMap Sizing Agent`
- Space: `FitMap Body Measurements`
- Instructions: 
```
You are a body measurement and sizing expert for DXL. 
You help analyze customer body scans and provide size recommendations.
Always reference specific measurements when making recommendations.
Focus on waist, chest, inseam, and height measurements.
```

**Agent 2: Sales Analytics Agent**
- Name: `Sales Analytics Agent`
- Space: `Customer & Transactions`
- Instructions:
```
You are a retail sales analyst for DXL.
You analyze customer transactions, identify trends, and provide insights.
Always include store performance, product categories, and time-based trends.
Calculate metrics like average transaction value, customer lifetime value.
```

**Agent 3: E-commerce Agent**
- Name: `E-commerce Operations Agent`
- Space: `Online Orders`
- Instructions:
```
You are an e-commerce operations analyst.
You track order fulfillment, identify bottlenecks, and analyze product performance.
Focus on fulfillment status, shipping costs, and product popularity.
```

---

## 📋 Phase 4: Testing & Validation (Days 8-12)

### Test Queries by Space

**FitMap Analytics Space:**
```
1. "What's the average waist size for male customers?"
2. "Show me the distribution of body scans by store"
3. "Which age group has the highest average weight?"
4. "What are the most common size recommendations for denim?"
5. "Compare average measurements between customers aged 30-40 vs 50-60"
```

**Customer Analytics Space:**
```
1. "Who are the top 10 customers by total spend?"
2. "What's the average transaction value by store?"
3. "Show me monthly transaction trends for 2024"
4. "Which stores have the highest sales?"
5. "What's the customer distribution by state?"
```

**E-commerce Analytics Space:**
```
1. "What are the top 5 best-selling products?"
2. "Show me order fulfillment status breakdown"
3. "What's the average order value by month?"
4. "How many orders were cancelled vs fulfilled?"
5. "Which products appear most frequently in orders?"
```

### Cross-Space Analytics (The Real Power!)

Create a **Master Analytics Space** that includes ALL data sources:

```
1. "Show me customers who had body scans and their purchase history"
2. "What's the correlation between waist size and pants purchases?"
3. "Do customers with body scans have higher average order values?"
4. "Which size recommendations lead to the fewest returns?"
5. "Analyze customer lifetime value for FitMap users vs non-users"
```

---

## 📋 Phase 5: Microsoft Teams Integration (Days 13-15)

### Step 1: Enable Quick Suite Bot in Teams

1. In Quick Suite console, go to **Settings** → **Integrations**
2. Click **Microsoft Teams**
3. Click **Enable Teams Integration**
4. Follow OAuth flow to authorize

### Step 2: Add Quick Suite to Teams Channel

1. Open Microsoft Teams
2. Go to your team/channel
3. Click **+** to add an app
4. Search for **AWS Quick Suite**
5. Click **Add**
6. Configure which Spaces are accessible

### Step 3: Test in Teams

In Teams chat, type:
```
@QuickSuite What are our top selling products this month?
@QuickSuite Show me customers with body scans in the last 30 days
@QuickSuite What's the average transaction value by store?
```

---

## 📋 Phase 6: Build Automation (Days 16-20)

### Use Case: Inventory Alert Automation

**Scenario:** When a product size is frequently recommended by FitMap but has low inventory, send alert to Teams.

1. Go to **Quick Automate**
2. Create new workflow: `Low Inventory Alert`
3. **Trigger:** Schedule (daily at 9 AM)
4. **Steps:**
   - Query FitMap recommendations (last 7 days)
   - Query current inventory levels
   - Identify mismatches (high demand, low stock)
   - Send Teams notification with list

### Use Case: Weekly Executive Report

1. Create workflow: `Weekly Executive Summary`
2. **Trigger:** Schedule (Monday 8 AM)
3. **Steps:**
   - Query sales metrics (last week)
   - Query FitMap scan volume
   - Query order fulfillment rates
   - Generate PDF report
   - Email to executives

---

## 📋 Phase 7: POC Validation & Metrics (Days 21-30)

### Success Metrics to Track

**Time Savings:**
- Manual query time: Measure how long it takes to answer questions manually
- Quick Suite query time: Measure response time in Quick Suite
- Target: 90%+ time reduction

**Query Accuracy:**
- Test 20 sample questions
- Verify answers against manual SQL queries
- Target: 95%+ accuracy

**User Adoption:**
- Number of queries per day
- Number of unique users
- Most common questions
- Target: 10+ queries/day

**Business Value:**
- Number of insights discovered
- Decisions made faster
- Actions taken based on insights

### POC Report Template

```markdown
# AWS Quick Suite POC Results

## Executive Summary
- POC Duration: 30 days
- Users: 2 pilot users
- Data Sources: 3 schemas, 19 tables, 40K+ records
- Queries Tested: 50+

## Key Findings

### Time Savings
- Average manual query time: 2-3 hours
- Average Quick Suite query time: 30 seconds
- Time savings: 95%

### Accuracy
- Queries tested: 50
- Accurate responses: 48
- Accuracy rate: 96%

### User Feedback
- Ease of use: 9/10
- Response quality: 8/10
- Would recommend: Yes

## Sample Insights Discovered
1. Customers with body scans have 35% higher AOV
2. Store 9330 has highest scan volume but lowest conversion
3. Size recommendations for waist 44-48 most common
4. Return rate 15% lower for FitMap-assisted purchases

## Recommendations
✓ Proceed with full deployment
✓ Expand to 20 users across departments
✓ Add more data sources (CRM, POS, inventory)
✓ Build automated workflows for alerts

## ROI Projection
- Annual cost: $67,000
- Time saved: 1,000 hours/year
- Value of time: $150,000
- Additional insights value: $200,000
- **Total ROI: 405%**
```

---

## 🎯 Quick Reference: Sample Questions for Demo

### For Executive Demo (5 minutes)
```
1. "What are our top 5 products by revenue this quarter?"
2. "Show me customer distribution by state"
3. "How many body scans did we perform last month?"
4. "What's the average order value for online orders?"
5. "Which stores have the highest transaction volume?"
```

### For Technical Demo (15 minutes)
```
1. "Analyze body measurement trends by age group"
2. "Show me customers who had scans but didn't purchase"
3. "What's the correlation between waist size and product purchases?"
4. "Compare transaction values: FitMap users vs non-users"
5. "Which size recommendations have the lowest return rates?"
6. "Show me monthly sales trends with year-over-year comparison"
7. "What's the average fulfillment time by product category?"
```

### For Teams Integration Demo (5 minutes)
```
In Teams channel:
@QuickSuite What were yesterday's sales?
@QuickSuite How many body scans this week?
@QuickSuite Show top 3 stores by revenue
```

---

## 📞 Support & Resources

### AWS Documentation
- Quick Suite Docs: https://docs.aws.amazon.com/quicksuite/
- Quick Suite Getting Started: https://aws.amazon.com/quicksuite/getting-started/

### Internal Contacts
- POC Lead: Afjal Ahamad
- AWS Account Manager: [Your AWS Rep]
- Technical Support: AWS Support Portal

### Troubleshooting

**Issue: Data source connection fails**
- Check IAM permissions
- Verify security group rules
- Test connection from AWS Console

**Issue: Queries return no results**
- Verify data was loaded correctly
- Check table names and schemas
- Test with simple query first

**Issue: Slow query performance**
- Check data volume
- Verify indexes exist
- Consider data partitioning

---

## ✅ POC Checklist

- [ ] Generate sample data (run Python scripts)
- [ ] Upload CSV files to S3
- [ ] Load data to Redshift or create Athena tables
- [ ] Configure Quick Suite account
- [ ] Set up Quick Index with data sources
- [ ] Create 3 Spaces (FitMap, Customer, Orders)
- [ ] Create 3 Chat Agents
- [ ] Test 20+ sample queries
- [ ] Integrate with Microsoft Teams
- [ ] Build 1-2 automated workflows
- [ ] Document results and metrics
- [ ] Prepare executive presentation
- [ ] Make Go/No-Go recommendation

---

**POC Timeline: 30 Days**
**Investment: $100 (trial period)**
**Expected Outcome: Clear ROI demonstration for full deployment**

Good luck with your POC! 🚀
