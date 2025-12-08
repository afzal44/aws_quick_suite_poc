# Redshift Setup Guide - qspos Schema

## 📋 Overview

This guide provides complete SQL scripts to create and load all 20 tables in the `qspos` schema in Amazon Redshift.

---

## 📁 Files Included

1. **`redshift_create_tables.sql`** - Creates all 20 tables in qspos schema
2. **`redshift_copy_commands.sql`** - Loads data from S3 to Redshift
3. **`REDSHIFT_SETUP_GUIDE.md`** - This file

---

## 🗂️ Schema Structure

### Schema: `qspos`
**Total Tables:** 20
**Total Expected Records:** ~140,000

### Table Categories:

#### 1. FitMap/SizeStream (5 tables)
- `size_users` - 1,000 records
- `size_scans` - 2,500 records
- `size_app_measures` - 2,000 records
- `size_dxl_custom_measures` - ~3,000 records
- `size_core_measures` - ~15,000 records

#### 2. Customer/CRM (8 tables)
- `customer` - 5,000 records
- `address` - ~7,500 records
- `email` - ~6,200 records
- `store` - 8 records
- `transaction_header` - 15,000 records
- `transaction_detail` - ~45,000 records
- `reward_detail` - ~9,000 records
- `household` - 2,500 records

#### 3. Orders/E-commerce (7 tables)
- `orderheader` - 3,000 records
- `orderline` - ~7,400 records
- `orderline_items` - ~50 records
- `orderchargedetail` - 3,000 records
- `invoice` - ~2,700 records
- `payment` - ~2,900 records
- `quantitydetail` - ~7,400 records

---

## 🚀 Step-by-Step Setup

### Step 1: Prerequisites

Before running the SQL scripts, ensure:

✅ **Redshift Cluster is running**
- Cluster endpoint available
- Database created
- User has CREATE SCHEMA and CREATE TABLE permissions

✅ **CSV files uploaded to S3**
- Bucket: `s3://YOUR_BUCKET_NAME/`
- Folder structure:
  ```
  fitmap/
    size_users/size_users.csv
    size_scans/size_scans.csv
    size_app_measures/size_app_measures.csv
    size_dxl_custom_measures/size_dxl_custom_measures.csv
    size_core_measures/size_core_measures.csv
  customer/
    customer/customer.csv
    address/address.csv
    email/email.csv
    store/store.csv
    transaction_header/transaction_header.csv
    transaction_detail/transaction_detail.csv
    reward_detail/reward_detail.csv
    household/household.csv
  orders/
    orderheader/orderheader.csv
    orderline/orderline.csv
    orderline_items/orderline_items.csv
    orderchargedetail/orderchargedetail.csv
    invoice/invoice.csv
    payment/payment.csv
    quantitydetail/quantitydetail.csv
  ```

✅ **IAM Role configured**
- Redshift cluster has IAM role attached
- IAM role has S3 read permissions
- Role ARN: `arn:aws:iam::YOUR_ACCOUNT:role/YOUR_REDSHIFT_ROLE`

---

### Step 2: Create Tables

1. **Open Redshift Query Editor** or connect via SQL client

2. **Run the create tables script:**
   ```sql
   -- Execute: redshift_create_tables.sql
   ```

3. **Verify tables were created:**
   ```sql
   SELECT 
       schemaname,
       tablename,
       tableowner
   FROM pg_tables
   WHERE schemaname = 'qspos'
   ORDER BY tablename;
   ```

   **Expected Output:** 20 tables

---

### Step 3: Update COPY Commands

1. **Open `redshift_copy_commands.sql`**

2. **Replace placeholders:**
   - `YOUR_BUCKET_NAME` → Your S3 bucket name (e.g., `dxl-quicksuite-poc-data`)
   - `YOUR_ACCOUNT` → Your AWS account ID
   - `YOUR_REDSHIFT_ROLE` → Your Redshift IAM role name

   **Example:**
   ```sql
   -- Before:
   FROM 's3://YOUR_BUCKET_NAME/fitmap/size_users/size_users.csv'
   IAM_ROLE 'arn:aws:iam::YOUR_ACCOUNT:role/YOUR_REDSHIFT_ROLE'
   
   -- After:
   FROM 's3://dxl-quicksuite-poc-data/fitmap/size_users/size_users.csv'
   IAM_ROLE 'arn:aws:iam::123456789012:role/RedshiftS3Role'
   ```

3. **Save the updated file**

---

### Step 4: Load Data from S3

1. **Run the COPY commands:**
   ```sql
   -- Execute: redshift_copy_commands.sql
   ```

2. **Monitor progress:**
   - Each COPY command will show rows loaded
   - Watch for any errors

3. **Check for errors:**
   ```sql
   SELECT * FROM stl_load_errors
   WHERE starttime >= CURRENT_DATE - 1
   ORDER BY starttime DESC
   LIMIT 100;
   ```

---

### Step 5: Verify Data Load

1. **Check row counts:**
   ```sql
   SELECT 'size_users' as table_name, COUNT(*) as row_count FROM qspos.size_users
   UNION ALL
   SELECT 'size_scans', COUNT(*) FROM qspos.size_scans
   UNION ALL
   SELECT 'size_app_measures', COUNT(*) FROM qspos.size_app_measures
   UNION ALL
   SELECT 'size_dxl_custom_measures', COUNT(*) FROM qspos.size_dxl_custom_measures
   UNION ALL
   SELECT 'size_core_measures', COUNT(*) FROM qspos.size_core_measures
   UNION ALL
   SELECT 'customer', COUNT(*) FROM qspos.customer
   UNION ALL
   SELECT 'address', COUNT(*) FROM qspos.address
   UNION ALL
   SELECT 'email', COUNT(*) FROM qspos.email
   UNION ALL
   SELECT 'store', COUNT(*) FROM qspos.store
   UNION ALL
   SELECT 'transaction_header', COUNT(*) FROM qspos.transaction_header
   UNION ALL
   SELECT 'transaction_detail', COUNT(*) FROM qspos.transaction_detail
   UNION ALL
   SELECT 'reward_detail', COUNT(*) FROM qspos.reward_detail
   UNION ALL
   SELECT 'household', COUNT(*) FROM qspos.household
   UNION ALL
   SELECT 'orderheader', COUNT(*) FROM qspos.orderheader
   UNION ALL
   SELECT 'orderline', COUNT(*) FROM qspos.orderline
   UNION ALL
   SELECT 'orderline_items', COUNT(*) FROM qspos.orderline_items
   UNION ALL
   SELECT 'orderchargedetail', COUNT(*) FROM qspos.orderchargedetail
   UNION ALL
   SELECT 'invoice', COUNT(*) FROM qspos.invoice
   UNION ALL
   SELECT 'payment', COUNT(*) FROM qspos.payment
   UNION ALL
   SELECT 'quantitydetail', COUNT(*) FROM qspos.quantitydetail
   ORDER BY table_name;
   ```

2. **Sample data from each table:**
   ```sql
   -- FitMap data
   SELECT * FROM qspos.size_users LIMIT 5;
   SELECT * FROM qspos.size_scans LIMIT 5;
   
   -- Customer data
   SELECT * FROM qspos.customer LIMIT 5;
   SELECT * FROM qspos.address LIMIT 5;
   
   -- Order data
   SELECT * FROM qspos.orderheader LIMIT 5;
   SELECT * FROM qspos.orderline LIMIT 5;
   ```

---

## 🔍 Sample Queries for Testing

### FitMap Analytics
```sql
-- Average waist size by gender
SELECT 
    gender,
    AVG(waist) as avg_waist,
    COUNT(*) as scan_count
FROM qspos.size_app_measures m
JOIN qspos.size_scans s ON m.scan_id = s.scan_id
GROUP BY gender;

-- Scans by store
SELECT 
    store_num,
    COUNT(*) as scan_count
FROM qspos.size_scans
GROUP BY store_num
ORDER BY scan_count DESC;
```

### Customer Analytics
```sql
-- Customer distribution by language
SELECT 
    language_code,
    COUNT(*) as customer_count
FROM qspos.customer
GROUP BY language_code
ORDER BY customer_count DESC;

-- Top 10 customers by spend
SELECT 
    c.customer_id,
    c.first_name,
    c.last_name,
    SUM(th.total_net_retail) as total_spend
FROM qspos.customer c
JOIN qspos.transaction_header th ON c.customer_id = th.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY total_spend DESC
LIMIT 10;
```

### Order Analytics
```sql
-- Orders by status
SELECT 
    fulfillmentstatus,
    COUNT(*) as order_count,
    SUM(CASE WHEN iscancelled THEN 1 ELSE 0 END) as cancelled_count
FROM qspos.orderheader
GROUP BY fulfillmentstatus;

-- Top selling products
SELECT 
    i.itemdescription,
    i.itembrand,
    SUM(ol.quantity) as total_quantity,
    COUNT(DISTINCT ol.orderid) as order_count
FROM qspos.orderline ol
JOIN qspos.orderline_items i ON ol.itemid = i.itemid
GROUP BY i.itemdescription, i.itembrand
ORDER BY total_quantity DESC
LIMIT 10;
```

### Cross-Schema Analytics
```sql
-- Customers with body scans and their purchase history
SELECT 
    c.customer_id,
    c.first_name,
    c.last_name,
    COUNT(DISTINCT s.scan_id) as scan_count,
    COUNT(DISTINCT th.transaction_id) as transaction_count,
    SUM(th.total_net_retail) as total_spend
FROM qspos.customer c
LEFT JOIN qspos.size_users u ON c.email = u.email
LEFT JOIN qspos.size_scans s ON u.id = s.user_id
LEFT JOIN qspos.transaction_header th ON c.customer_id = th.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
HAVING COUNT(DISTINCT s.scan_id) > 0
ORDER BY total_spend DESC
LIMIT 20;
```

---

## 🛠️ Troubleshooting

### Issue: COPY command fails with "Access Denied"

**Solution:**
1. Verify IAM role has S3 read permissions
2. Check bucket policy allows Redshift access
3. Verify IAM role is attached to Redshift cluster

```sql
-- Check cluster IAM roles
SELECT * FROM svv_iam_roles;
```

### Issue: COPY command fails with "File not found"

**Solution:**
1. Verify S3 path is correct
2. Check file exists in S3:
   ```bash
   aws s3 ls s3://YOUR_BUCKET_NAME/fitmap/size_users/
   ```
3. Ensure file name matches exactly (case-sensitive)

### Issue: Data type mismatch errors

**Solution:**
1. Check CSV file encoding (should be UTF-8)
2. Verify column order matches table definition
3. Use `TRUNCATECOLUMNS` option to handle long strings

### Issue: Some columns have NULL values

**Solution:**
- This is expected for optional fields
- Use `BLANKSASNULL` and `EMPTYASNULL` options
- Check original CSV for empty values

---

## 📊 Performance Optimization

### Analyze Tables
After loading data, run ANALYZE to update statistics:

```sql
ANALYZE qspos.size_users;
ANALYZE qspos.size_scans;
ANALYZE qspos.customer;
ANALYZE qspos.transaction_header;
ANALYZE qspos.orderheader;
-- ... repeat for all tables
```

### Vacuum Tables
Reclaim space and sort data:

```sql
VACUUM qspos.size_users;
VACUUM qspos.size_scans;
VACUUM qspos.customer;
-- ... repeat for all tables
```

### Check Table Statistics
```sql
SELECT 
    "table",
    size,
    tbl_rows,
    unsorted
FROM svv_table_info
WHERE schema = 'qspos'
ORDER BY size DESC;
```

---

## 🔐 Security Best Practices

1. **Limit Schema Access:**
   ```sql
   REVOKE ALL ON SCHEMA qspos FROM PUBLIC;
   GRANT USAGE ON SCHEMA qspos TO quicksuite_user;
   GRANT SELECT ON ALL TABLES IN SCHEMA qspos TO quicksuite_user;
   ```

2. **Create Read-Only User:**
   ```sql
   CREATE USER quicksuite_readonly WITH PASSWORD 'SecurePassword123!';
   GRANT USAGE ON SCHEMA qspos TO quicksuite_readonly;
   GRANT SELECT ON ALL TABLES IN SCHEMA qspos TO quicksuite_readonly;
   ```

3. **Enable Audit Logging:**
   - Enable CloudWatch Logs for Redshift
   - Monitor query patterns
   - Track data access

---

## 📞 Support

### AWS Documentation
- Redshift COPY: https://docs.aws.amazon.com/redshift/latest/dg/r_COPY.html
- Redshift Best Practices: https://docs.aws.amazon.com/redshift/latest/dg/best-practices.html

### Quick Suite Integration
- After loading data, configure Quick Suite to connect to Redshift
- Use schema: `qspos`
- Test connection with sample queries

---

## ✅ Checklist

- [ ] Redshift cluster is running
- [ ] CSV files uploaded to S3
- [ ] IAM role configured with S3 access
- [ ] IAM role attached to Redshift cluster
- [ ] Schema `qspos` created
- [ ] All 20 tables created
- [ ] COPY commands updated with correct S3 paths
- [ ] Data loaded successfully
- [ ] Row counts verified
- [ ] Sample queries tested
- [ ] ANALYZE run on all tables
- [ ] Quick Suite connected to Redshift

---

**Setup Complete! Your Redshift database is ready for AWS Quick Suite POC.**

**Next Step:** Configure AWS Quick Suite to connect to the `qspos` schema and start testing queries!
