-- ============================================================================
-- AWS Quick Suite POC - Redshift COPY Commands
-- Load data from S3 to qspoc schema
-- ============================================================================
-- 
-- INSTRUCTIONS:
-- 1. Replace dxl-quicksuite-poc with your actual S3 bucket name
-- 2. Replace YOUR_IAM_ROLE_ARN with your Redshift IAM role ARN
-- 3. Ensure CSV files are uploaded to S3 first
-- 4. Run these commands in Redshift Query Editor
-- ============================================================================

-- Set variables (replace these values)
-- BUCKET: dxl-quicksuite-poc
-- IAM_ROLE: arn:aws:iam::YOUR_ACCOUNT:role/RedshiftRole
-- REGION: us-east-1

-- ============================================================================
-- FITMAP/SIZESTREAM DATA (5 tables)
-- ============================================================================

-- Load size_users
COPY qspoc.size_users
FROM 's3://dxl-quicksuite-poc/fitmap/size_users/size_users.csv'
IAM_ROLE 'arn:aws:iam::047002548151:role/service-role/AmazonRedshift-CommandsAccessRole-20251209T105125'
CSV
IGNOREHEADER 1
REGION 'us-east-1'
DATEFORMAT 'auto'
TIMEFORMAT 'auto'
TRUNCATECOLUMNS
BLANKSASNULL
EMPTYASNULL;

-- Load size_scans
COPY qspoc.size_scans
FROM 's3://dxl-quicksuite-poc/fitmap/size_scans/size_scans.csv'
IAM_ROLE 'arn:aws:iam::047002548151:role/service-role/AmazonRedshift-CommandsAccessRole-20251209T105125'
CSV
IGNOREHEADER 1
REGION 'us-east-1'
DATEFORMAT 'auto'
TIMEFORMAT 'auto'
TRUNCATECOLUMNS
BLANKSASNULL
EMPTYASNULL;

-- Load size_app_measures
COPY qspoc.size_app_measures
FROM 's3://dxl-quicksuite-poc/fitmap/size_app_measures/size_app_measures.csv'
IAM_ROLE 'arn:aws:iam::047002548151:role/service-role/AmazonRedshift-CommandsAccessRole-20251209T105125'
CSV
IGNOREHEADER 1
REGION 'us-east-1'
DATEFORMAT 'auto'
TIMEFORMAT 'auto'
TRUNCATECOLUMNS
BLANKSASNULL
EMPTYASNULL;

-- Load size_dxl_custom_measures
COPY qspoc.size_dxl_custom_measures
FROM 's3://dxl-quicksuite-poc/fitmap/size_dxl_custom_measures/size_dxl_custom_measures.csv'
IAM_ROLE 'arn:aws:iam::047002548151:role/service-role/AmazonRedshift-CommandsAccessRole-20251209T105125'
CSV
IGNOREHEADER 1
REGION 'us-east-1'
DATEFORMAT 'auto'
TIMEFORMAT 'auto'
TRUNCATECOLUMNS
BLANKSASNULL
EMPTYASNULL;

-- Load size_core_measures
COPY qspoc.size_core_measures
FROM 's3://dxl-quicksuite-poc/fitmap/size_core_measures/size_core_measures.csv'
IAM_ROLE 'arn:aws:iam::047002548151:role/service-role/AmazonRedshift-CommandsAccessRole-20251209T105125'
CSV
IGNOREHEADER 1
REGION 'us-east-1'
DATEFORMAT 'auto'
TIMEFORMAT 'auto'
TRUNCATECOLUMNS
BLANKSASNULL
EMPTYASNULL;

-- ============================================================================
-- CUSTOMER/CRM DATA (8 tables)
-- ============================================================================

-- Load customer
COPY qspoc.customer
FROM 's3://dxl-quicksuite-poc/customer/customer/customer.csv'
IAM_ROLE 'arn:aws:iam::047002548151:role/service-role/AmazonRedshift-CommandsAccessRole-20251209T105125'
CSV
IGNOREHEADER 1
REGION 'us-east-1'
DATEFORMAT 'auto'
TIMEFORMAT 'auto'
TRUNCATECOLUMNS
BLANKSASNULL
EMPTYASNULL;

-- Load address
COPY qspoc.address
FROM 's3://dxl-quicksuite-poc/customer/address/address.csv'
IAM_ROLE 'arn:aws:iam::047002548151:role/service-role/AmazonRedshift-CommandsAccessRole-20251209T105125'
CSV
IGNOREHEADER 1
REGION 'us-east-1'
DATEFORMAT 'auto'
TIMEFORMAT 'auto'
TRUNCATECOLUMNS
BLANKSASNULL
EMPTYASNULL;

-- Load email
COPY qspoc.email
FROM 's3://dxl-quicksuite-poc/customer/email/email.csv'
IAM_ROLE 'arn:aws:iam::047002548151:role/service-role/AmazonRedshift-CommandsAccessRole-20251209T105125'
CSV
IGNOREHEADER 1
REGION 'us-east-1'
DATEFORMAT 'auto'
TIMEFORMAT 'auto'
TRUNCATECOLUMNS
BLANKSASNULL
EMPTYASNULL;

-- Load store
COPY qspoc.store
FROM 's3://dxl-quicksuite-poc/customer/store/store.csv'
IAM_ROLE 'arn:aws:iam::047002548151:role/service-role/AmazonRedshift-CommandsAccessRole-20251209T105125'
CSV
IGNOREHEADER 1
REGION 'us-east-1'
DATEFORMAT 'auto'
TIMEFORMAT 'auto'
TRUNCATECOLUMNS
BLANKSASNULL
EMPTYASNULL;

-- Load transaction_header
COPY qspoc.transaction_header
FROM 's3://dxl-quicksuite-poc/customer/transaction_header/transaction_header.csv'
IAM_ROLE 'arn:aws:iam::047002548151:role/service-role/AmazonRedshift-CommandsAccessRole-20251209T105125'
CSV
IGNOREHEADER 1
REGION 'us-east-1'
DATEFORMAT 'auto'
TIMEFORMAT 'auto'
TRUNCATECOLUMNS
BLANKSASNULL
EMPTYASNULL;

-- Load transaction_detail
COPY qspoc.transaction_detail
FROM 's3://dxl-quicksuite-poc/customer/transaction_detail/transaction_detail.csv'
IAM_ROLE 'arn:aws:iam::047002548151:role/service-role/AmazonRedshift-CommandsAccessRole-20251209T105125'
CSV
IGNOREHEADER 1
REGION 'us-east-1'
DATEFORMAT 'auto'
TIMEFORMAT 'auto'
TRUNCATECOLUMNS
BLANKSASNULL
EMPTYASNULL;

-- Load reward_detail
COPY qspoc.reward_detail
FROM 's3://dxl-quicksuite-poc/customer/reward_detail/reward_detail.csv'
IAM_ROLE 'arn:aws:iam::047002548151:role/service-role/AmazonRedshift-CommandsAccessRole-20251209T105125'
CSV
IGNOREHEADER 1
REGION 'us-east-1'
DATEFORMAT 'auto'
TIMEFORMAT 'auto'
TRUNCATECOLUMNS
BLANKSASNULL
EMPTYASNULL;

-- Load household
COPY qspoc.household
FROM 's3://dxl-quicksuite-poc/customer/household/household.csv'
IAM_ROLE 'arn:aws:iam::047002548151:role/service-role/AmazonRedshift-CommandsAccessRole-20251209T105125'
CSV
IGNOREHEADER 1
REGION 'us-east-1'
DATEFORMAT 'auto'
TIMEFORMAT 'auto'
TRUNCATECOLUMNS
BLANKSASNULL
EMPTYASNULL;

-- ============================================================================
-- ORDER/E-COMMERCE DATA (7 tables)
-- ============================================================================

-- Load orderheader
COPY qspoc.orderheader
FROM 's3://dxl-quicksuite-poc/orders/orderheader/orderheader.csv'
IAM_ROLE 'arn:aws:iam::047002548151:role/service-role/AmazonRedshift-CommandsAccessRole-20251209T105125'
CSV
IGNOREHEADER 1
REGION 'us-east-1'
DATEFORMAT 'auto'
TIMEFORMAT 'auto'
TRUNCATECOLUMNS
BLANKSASNULL
EMPTYASNULL;

-- Load orderline
COPY qspoc.orderline
FROM 's3://dxl-quicksuite-poc/orders/orderline/orderline.csv'
IAM_ROLE 'arn:aws:iam::047002548151:role/service-role/AmazonRedshift-CommandsAccessRole-20251209T105125'
CSV
IGNOREHEADER 1
REGION 'us-east-1'
DATEFORMAT 'auto'
TIMEFORMAT 'auto'
TRUNCATECOLUMNS
BLANKSASNULL
EMPTYASNULL;

-- Load orderline_items
COPY qspoc.orderline_items
FROM 's3://dxl-quicksuite-poc/orders/orderline_items/orderline_items.csv'
IAM_ROLE 'arn:aws:iam::047002548151:role/service-role/AmazonRedshift-CommandsAccessRole-20251209T105125'
CSV
IGNOREHEADER 1
REGION 'us-east-1'
DATEFORMAT 'auto'
TIMEFORMAT 'auto'
TRUNCATECOLUMNS
BLANKSASNULL
EMPTYASNULL;

-- Load orderchargedetail
COPY qspoc.orderchargedetail
FROM 's3://dxl-quicksuite-poc/orders/orderchargedetail/orderchargedetail.csv'
IAM_ROLE 'arn:aws:iam::047002548151:role/service-role/AmazonRedshift-CommandsAccessRole-20251209T105125'
CSV
IGNOREHEADER 1
REGION 'us-east-1'
DATEFORMAT 'auto'
TIMEFORMAT 'auto'
TRUNCATECOLUMNS
BLANKSASNULL
EMPTYASNULL;

-- Load invoice
COPY qspoc.invoice
FROM 's3://dxl-quicksuite-poc/orders/invoice/invoice.csv'
IAM_ROLE 'arn:aws:iam::047002548151:role/service-role/AmazonRedshift-CommandsAccessRole-20251209T105125'
CSV
IGNOREHEADER 1
REGION 'us-east-1'
DATEFORMAT 'auto'
TIMEFORMAT 'auto'
TRUNCATECOLUMNS
BLANKSASNULL
EMPTYASNULL;

-- Load payment
COPY qspoc.payment
FROM 's3://dxl-quicksuite-poc/orders/payment/payment.csv'
IAM_ROLE 'arn:aws:iam::047002548151:role/service-role/AmazonRedshift-CommandsAccessRole-20251209T105125'
CSV
IGNOREHEADER 1
REGION 'us-east-1'
DATEFORMAT 'auto'
TIMEFORMAT 'auto'
TRUNCATECOLUMNS
BLANKSASNULL
EMPTYASNULL;

-- Load quantitydetail
COPY qspoc.quantitydetail
FROM 's3://dxl-quicksuite-poc/orders/quantitydetail/quantitydetail.csv'
IAM_ROLE 'arn:aws:iam::047002548151:role/service-role/AmazonRedshift-CommandsAccessRole-20251209T105125'
CSV
IGNOREHEADER 1
REGION 'us-east-1'
DATEFORMAT 'auto'
TIMEFORMAT 'auto'
TRUNCATECOLUMNS
BLANKSASNULL
EMPTYASNULL;

-- ============================================================================
-- VERIFICATION QUERIES
-- ============================================================================

-- Check row counts for all tables
SELECT 'size_users' as table_name, COUNT(*) as row_count FROM qspoc.size_users
UNION ALL
SELECT 'size_scans', COUNT(*) FROM qspoc.size_scans
UNION ALL
SELECT 'size_app_measures', COUNT(*) FROM qspoc.size_app_measures
UNION ALL
SELECT 'size_dxl_custom_measures', COUNT(*) FROM qspoc.size_dxl_custom_measures
UNION ALL
SELECT 'size_core_measures', COUNT(*) FROM qspoc.size_core_measures
UNION ALL
SELECT 'customer', COUNT(*) FROM qspoc.customer
UNION ALL
SELECT 'address', COUNT(*) FROM qspoc.address
UNION ALL
SELECT 'email', COUNT(*) FROM qspoc.email
UNION ALL
SELECT 'store', COUNT(*) FROM qspoc.store
UNION ALL
SELECT 'transaction_header', COUNT(*) FROM qspoc.transaction_header
UNION ALL
SELECT 'transaction_detail', COUNT(*) FROM qspoc.transaction_detail
UNION ALL
SELECT 'reward_detail', COUNT(*) FROM qspoc.reward_detail
UNION ALL
SELECT 'household', COUNT(*) FROM qspoc.household
UNION ALL
SELECT 'orderheader', COUNT(*) FROM qspoc.orderheader
UNION ALL
SELECT 'orderline', COUNT(*) FROM qspoc.orderline
UNION ALL
SELECT 'orderline_items', COUNT(*) FROM qspoc.orderline_items
UNION ALL
SELECT 'orderchargedetail', COUNT(*) FROM qspoc.orderchargedetail
UNION ALL
SELECT 'invoice', COUNT(*) FROM qspoc.invoice
UNION ALL
SELECT 'payment', COUNT(*) FROM qspoc.payment
UNION ALL
SELECT 'quantitydetail', COUNT(*) FROM qspoc.quantitydetail
ORDER BY table_name;

-- Check for any load errors
SELECT * FROM stl_load_errors
WHERE starttime >= CURRENT_DATE - 1
ORDER BY starttime DESC
LIMIT 100;

-- Sample data from each table
SELECT 'size_users' as table_name, * FROM qspoc.size_users LIMIT 5;
SELECT 'customer' as table_name, * FROM qspoc.customer LIMIT 5;
SELECT 'orderheader' as table_name, * FROM qspoc.orderheader LIMIT 5;

-- ============================================================================
-- END OF SCRIPT
-- ============================================================================
