# AWS Quick Suite POC - Quick Start Commands

## 🚀 Step-by-Step Execution

### Step 1: Generate Sample Data (5 minutes)

```bash
# Navigate to data generators folder
cd poc_data_generators

# Install Python dependencies
pip install -r requirements.txt

# Run all data generators
python run_all_generators.py

# Verify CSV files were created
dir *.csv
```

**Expected Output:** 19 CSV files (~50-100 MB total)

---

### Step 2: Upload to S3 (10 minutes)

```bash
# Create S3 bucket (replace with your bucket name)
aws s3 mb s3://dxl-quicksuite-poc-data --region us-east-1

# Upload all FitMap files
aws s3 cp size_users.csv s3://dxl-quicksuite-poc-data/fitmap/size_users/size_users.csv
aws s3 cp size_scans.csv s3://dxl-quicksuite-poc-data/fitmap/size_scans/size_scans.csv
aws s3 cp size_app_measures.csv s3://dxl-quicksuite-poc-data/fitmap/size_app_measures/size_app_measures.csv
aws s3 cp size_dxl_custom_measures.csv s3://dxl-quicksuite-poc-data/fitmap/size_dxl_custom_measures/size_dxl_custom_measures.csv

# Upload all Customer files
aws s3 cp customer.csv s3://dxl-quicksuite-poc-data/customer/customer/customer.csv
aws s3 cp address.csv s3://dxl-quicksuite-poc-data/customer/address/address.csv
aws s3 cp email.csv s3://dxl-quicksuite-poc-data/customer/email/email.csv
aws s3 cp store.csv s3://dxl-quicksuite-poc-data/customer/store/store.csv
aws s3 cp transaction_header.csv s3://dxl-quicksuite-poc-data/customer/transaction_header/transaction_header.csv
aws s3 cp transaction_detail.csv s3://dxl-quicksuite-poc-data/customer/transaction_detail/transaction_detail.csv
aws s3 cp reward_detail.csv s3://dxl-quicksuite-poc-data/customer/reward_detail/reward_detail.csv
aws s3 cp household.csv s3://dxl-quicksuite-poc-data/customer/household/household.csv

# Upload all Order files
aws s3 cp orderheader.csv s3://dxl-quicksuite-poc-data/orders/orderheader/orderheader.csv
aws s3 cp orderline.csv s3://dxl-quicksuite-poc-data/orders/orderline/orderline.csv
aws s3 cp orderline_items.csv s3://dxl-quicksuite-poc-data/orders/orderline_items/orderline_items.csv
aws s3 cp orderchargedetail.csv s3://dxl-quicksuite-poc-data/orders/orderchargedetail/orderchargedetail.csv
aws s3 cp invoice.csv s3://dxl-quicksuite-poc-data/orders/invoice/invoice.csv
aws s3 cp payment.csv s3://dxl-quicksuite-poc-data/orders/payment/payment.csv
aws s3 cp quantitydetail.csv s3://dxl-quicksuite-poc-data/orders/quantitydetail/quantitydetail.csv

# Verify upload
aws s3 ls s3://dxl-quicksuite-poc-data/ --recursive --human-readable
```

---

### Step 3: Load to Redshift (If using existing Redshift)

```sql
-- Connect to your Redshift cluster
-- Replace YOUR_ACCOUNT and YOUR_ROLE with your values

-- Load FitMap tables
COPY dxlg_size_stream.size_users
FROM 's3://dxl-quicksuite-poc-data/fitmap/size_users/'
IAM_ROLE 'arn:aws:iam::YOUR_ACCOUNT:role/YOUR_ROLE'
CSV IGNOREHEADER 1 REGION 'us-east-1';

COPY dxlg_size_stream.size_scans
FROM 's3://dxl-quicksuite-poc-data/fitmap/size_scans/'
IAM_ROLE 'arn:aws:iam::YOUR_ACCOUNT:role/YOUR_ROLE'
CSV IGNOREHEADER 1 REGION 'us-east-1';

COPY dxlg_size_stream.size_app_measures
FROM 's3://dxl-quicksuite-poc-data/fitmap/size_app_measures/'
IAM_ROLE 'arn:aws:iam::YOUR_ACCOUNT:role/YOUR_ROLE'
CSV IGNOREHEADER 1 REGION 'us-east-1';

COPY dxlg_size_stream.size_dxl_custom_measures
FROM 's3://dxl-quicksuite-poc-data/fitmap/size_dxl_custom_measures/'
IAM_ROLE 'arn:aws:iam::YOUR_ACCOUNT:role/YOUR_ROLE'
CSV IGNOREHEADER 1 REGION 'us-east-1';

-- Load Customer tables
COPY cimb_repl.customer
FROM 's3://dxl-quicksuite-poc-data/customer/customer/'
IAM_ROLE 'arn:aws:iam::YOUR_ACCOUNT:role/YOUR_ROLE'
CSV IGNOREHEADER 1 REGION 'us-east-1';

COPY cimb_repl.address
FROM 's3://dxl-quicksuite-poc-data/customer/address/'
IAM_ROLE 'arn:aws:iam::YOUR_ACCOUNT:role/YOUR_ROLE'
CSV IGNOREHEADER 1 REGION 'us-east-1';

COPY cimb_repl.email
FROM 's3://dxl-quicksuite-poc-data/customer/email/'
IAM_ROLE 'arn:aws:iam::YOUR_ACCOUNT:role/YOUR_ROLE'
CSV IGNOREHEADER 1 REGION 'us-east-1';

COPY cimb_repl.store
FROM 's3://dxl-quicksuite-poc-data/customer/store/'
IAM_ROLE 'arn:aws:iam::YOUR_ACCOUNT:role/YOUR_ROLE'
CSV IGNOREHEADER 1 REGION 'us-east-1';

COPY cimb_repl.transaction_header
FROM 's3://dxl-quicksuite-poc-data/customer/transaction_header/'
IAM_ROLE 'arn:aws:iam::YOUR_ACCOUNT:role/YOUR_ROLE'
CSV IGNOREHEADER 1 REGION 'us-east-1';

COPY cimb_repl.transaction_detail
FROM 's3://dxl-quicksuite-poc-data/customer/transaction_detail/'
IAM_ROLE 'arn:aws:iam::YOUR_ACCOUNT:role/YOUR_ROLE'
CSV IGNOREHEADER 1 REGION 'us-east-1';

COPY cimb_repl.reward_detail
FROM 's3://dxl-quicksuite-poc-data/customer/reward_detail/'
IAM_ROLE 'arn:aws:iam::YOUR_ACCOUNT:role/YOUR_ROLE'
CSV IGNOREHEADER 1 REGION 'us-east-1';

COPY cimb_repl.household
FROM 's3://dxl-quicksuite-poc-data/customer/household/'
IAM_ROLE 'arn:aws:iam::YOUR_ACCOUNT:role/YOUR_ROLE'
CSV IGNOREHEADER 1 REGION 'us-east-1';

-- Load Order tables
COPY dxlg_olap_orders.orderheader
FROM 's3://dxl-quicksuite-poc-data/orders/orderheader/'
IAM_ROLE 'arn:aws:iam::YOUR_ACCOUNT:role/YOUR_ROLE'
CSV IGNOREHEADER 1 REGION 'us-east-1';

COPY dxlg_olap_orders.orderline
FROM 's3://dxl-quicksuite-poc-data/orders/orderline/'
IAM_ROLE 'arn:aws:iam::YOUR_ACCOUNT:role/YOUR_ROLE'
CSV IGNOREHEADER 1 REGION 'us-east-1';

COPY dxlg_olap_orders.orderline_items
FROM 's3://dxl-quicksuite-poc-data/orders/orderline_items/'
IAM_ROLE 'arn:aws:iam::YOUR_ACCOUNT:role/YOUR_ROLE'
CSV IGNOREHEADER 1 REGION 'us-east-1';

COPY dxlg_olap_orders.orderchargedetail
FROM 's3://dxl-quicksuite-poc-data/orders/orderchargedetail/'
IAM_ROLE 'arn:aws:iam::YOUR_ACCOUNT:role/YOUR_ROLE'
CSV IGNOREHEADER 1 REGION 'us-east-1';

COPY dxlg_olap_orders.invoice
FROM 's3://dxl-quicksuite-poc-data/orders/invoice/'
IAM_ROLE 'arn:aws:iam::YOUR_ACCOUNT:role/YOUR_ROLE'
CSV IGNOREHEADER 1 REGION 'us-east-1';

COPY dxlg_olap_orders.payment
FROM 's3://dxl-quicksuite-poc-data/orders/payment/'
IAM_ROLE 'arn:aws:iam::YOUR_ACCOUNT:role/YOUR_ROLE'
CSV IGNOREHEADER 1 REGION 'us-east-1';

COPY dxlg_olap_orders.quantitydetail
FROM 's3://dxl-quicksuite-poc-data/orders/quantitydetail/'
IAM_ROLE 'arn:aws:iam::YOUR_ACCOUNT:role/YOUR_ROLE'
CSV IGNOREHEADER 1 REGION 'us-east-1';

-- Verify data loaded
SELECT 'size_users' as table_name, COUNT(*) as row_count FROM dxlg_size_stream.size_users
UNION ALL
SELECT 'size_scans', COUNT(*) FROM dxlg_size_stream.size_scans
UNION ALL
SELECT 'customer', COUNT(*) FROM cimb_repl.customer
UNION ALL
SELECT 'transaction_header', COUNT(*) FROM cimb_repl.transaction_header
UNION ALL
SELECT 'orderheader', COUNT(*) FROM dxlg_olap_orders.orderheader;
```

---

### Step 4: Configure Quick Suite (AWS Console)

**Manual Steps in AWS Console:**

1. **Open QuickSight/Quick Suite:**
   - Go to: https://us-east-1.quicksight.aws.amazon.com/
   - Click "Quick Suite" in left navigation

2. **Set Up Quick Index:**
   - Click "Quick Index" → "Add Data Source"
   - Select "Amazon Redshift"
   - Connection name: `DXL_POC_Redshift`
   - Select your Redshift cluster
   - Test connection
   - Click "Index Data"

3. **Create Spaces:**
   - Click "Spaces" → "Create Space"
   - Name: `FitMap Analytics`
   - Add data sources: All `dxlg_size_stream` tables
   - Add your email as user
   - Repeat for Customer and Orders spaces

4. **Create Chat Agent:**
   - Click "Agents" → "Create Agent"
   - Name: `FitMap Sizing Expert`
   - Select Space: `FitMap Analytics`
   - Add instructions (see setup guide)
   - Save

---

### Step 5: Test Queries

**In Quick Suite Chat Interface:**

```
Test Query 1:
"How many body scans do we have in total?"

Test Query 2:
"What's the average waist size for male customers?"

Test Query 3:
"Show me the top 5 stores by number of scans"

Test Query 4:
"What are the most common size recommendations?"

Test Query 5:
"How many customers do we have?"

Test Query 6:
"What's the total transaction value in 2024?"

Test Query 7:
"Show me the top 10 products by order frequency"

Test Query 8:
"What's the average order value?"
```

---

## 📊 Verification Checklist

After each step, verify:

**After Data Generation:**
```bash
# Should see 19 CSV files
dir *.csv | measure-object -line
# Expected: 19 files
```

**After S3 Upload:**
```bash
aws s3 ls s3://dxl-quicksuite-poc-data/ --recursive | measure-object -line
# Expected: 19 files
```

**After Redshift Load:**
```sql
-- Should see row counts
SELECT COUNT(*) FROM dxlg_size_stream.size_users; -- ~1000
SELECT COUNT(*) FROM dxlg_size_stream.size_scans; -- ~2500
SELECT COUNT(*) FROM cimb_repl.customer; -- ~5000
SELECT COUNT(*) FROM cimb_repl.transaction_header; -- ~15000
SELECT COUNT(*) FROM dxlg_olap_orders.orderheader; -- ~3000
```

**After Quick Suite Setup:**
- [ ] Quick Index shows "Connected" status
- [ ] 3 Spaces created
- [ ] 3 Chat Agents created
- [ ] Test query returns results

---

## 🆘 Troubleshooting

**Python script fails:**
```bash
# Check Python version (need 3.8+)
python --version

# Reinstall dependencies
pip install --upgrade pandas numpy
```

**S3 upload fails:**
```bash
# Check AWS credentials
aws sts get-caller-identity

# Check bucket exists
aws s3 ls s3://dxl-quicksuite-poc-data/
```

**Redshift COPY fails:**
```sql
-- Check for errors
SELECT * FROM stl_load_errors ORDER BY starttime DESC LIMIT 10;

-- Verify IAM role has S3 access
-- Check security group allows Redshift access
```

**Quick Suite connection fails:**
- Verify Redshift security group allows QuickSight IP ranges
- Check IAM permissions for QuickSight
- Test connection from QuickSight first

---

## 📞 Need Help?

**AWS Support:**
- Open AWS Support case
- Category: QuickSight/Quick Suite

**Internal:**
- POC Lead: Afjal Ahamad
- Email: afjal.ahamad@dxl.com

---

## ⏱️ Time Estimates

- **Data Generation:** 5 minutes
- **S3 Upload:** 10 minutes
- **Redshift Load:** 15 minutes
- **Quick Suite Setup:** 30 minutes
- **Testing:** 30 minutes

**Total: ~90 minutes to fully operational POC**

---

**You're now ready to demonstrate AWS Quick Suite! 🚀**
