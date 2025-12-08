-- ============================================================================
-- AWS Quick Suite POC - Redshift COPY Commands
-- Load data from S3 to qspos schema
-- ============================================================================
-- 
-- INSTRUCTIONS:
-- 1. Replace dxl-quicksuite-poc-data with your actual S3 bucket name
-- 2. Replace YOUR_IAM_ROLE_ARN with your Redshift IAM role ARN
-- 3. Ensure CSV files are uploaded to S3 first
-- 4. Run these commands in Redshift Query Editor
-- ============================================================================

-- Set variables (replace these values)
-- BUCKET: dxl-quicksuite-poc-data
-- IAM_ROLE: arn:aws:iam::YOUR_ACCOUNT:role/RedshiftRole
-- REGION: us-east-1

-- ============================================================================
-- FITMAP/SIZESTREAM DATA (5 tables)
-- ============================================================================

-- Load size_users
COPY qspos.size_users
FROM 's3://dxl-quicksuite-poc-data/fitmap/size_users/size_users.csv'
IAM_ROLE 'arn:aws:iam::565393035923:role/service-role/AmazonRedshift-CommandsAccessRole-20251205T112603'
CSV
IGNOREHEADER 1
REGION 'us-east-1'
DATEFORMAT 'auto'
TIMEFORMAT 'auto'
TRUNCATECOLUMNS
BLANKSASNULL
EMPTYASNULL;

-- Load size_scans
COPY qspos.size_scans
FROM 's3://dxl-quicksuite-poc-data/fitmap/size_scans/size_scans.csv'
IAM_ROLE 'arn:aws:iam::565393035923:role/service-role/AmazonRedshift-CommandsAccessRole-20251205T112603'
CSV
IGNOREHEADER 1
REGION 'us-east-1'
DATEFORMAT 'auto'
TIMEFORMAT 'auto'
TRUNCATECOLUMNS
BLANKSASNULL
EMPTYASNULL;

-- Load size_app_measures
COPY qspos.size_app_measures
FROM 's3://dxl-quicksuite-poc-data/fitmap/size_app_measures/size_app_measures.csv'
IAM_ROLE 'arn:aws:iam::565393035923:role/service-role/AmazonRedshift-CommandsAccessRole-20251205T112603'
CSV
IGNOREHEADER 1
REGION 'us-east-1'
DATEFORMAT 'auto'
TIMEFORMAT 'auto'
TRUNCATECOLUMNS
BLANKSASNULL
EMPTYASNULL;

-- Load size_dxl_custom_measures
COPY qspos.size_dxl_custom_measures
FROM 's3://dxl-quicksuite-poc-data/fitmap/size_dxl_custom_measures/size_dxl_custom_measures.csv'
IAM_ROLE 'arn:aws:iam::565393035923:role/service-role/AmazonRedshift-CommandsAccessRole-20251205T112603'
CSV
IGNOREHEADER 1
REGION 'us-east-1'
DATEFORMAT 'auto'
TIMEFORMAT 'auto'
TRUNCATECOLUMNS
BLANKSASNULL
EMPTYASNULL;

-- Load size_core_measures
COPY qspos.size_core_measures
FROM 's3://dxl-quicksuite-poc-data/fitmap/size_core_measures/size_core_measures.csv'
IAM_ROLE 'arn:aws:iam::565393035923:role/service-role/AmazonRedshift-CommandsAccessRole-20251205T112603'
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
COPY qspos.customer
FROM 's3://dxl-quicksuite-poc-data/customer/customer/customer.csv'
IAM_ROLE 'arn:aws:iam::565393035923:role/service-role/AmazonRedshift-CommandsAccessRole-20251205T112603'
CSV
IGNOREHEADER 1
REGION 'us-east-1'
DATEFORMAT 'auto'
TIMEFORMAT 'auto'
TRUNCATECOLUMNS
BLANKSASNULL
EMPTYASNULL;

-- Load address
COPY qspos.address
FROM 's3://dxl-quicksuite-poc-data/customer/address/address.csv'
IAM_ROLE 'arn:aws:iam::565393035923:role/service-role/AmazonRedshift-CommandsAccessRole-20251205T112603'
CSV
IGNOREHEADER 1
REGION 'us-east-1'
DATEFORMAT 'auto'
TIMEFORMAT 'auto'
TRUNCATECOLUMNS
BLANKSASNULL
EMPTYASNULL;

-- Load email
COPY qspos.email
FROM 's3://dxl-quicksuite-poc-data/customer/email/email.csv'
IAM_ROLE 'arn:aws:iam::565393035923:role/service-role/AmazonRedshift-CommandsAccessRole-20251205T112603'
CSV
IGNOREHEADER 1
REGION 'us-east-1'
DATEFORMAT 'auto'
TIMEFORMAT 'auto'
TRUNCATECOLUMNS
BLANKSASNULL
EMPTYASNULL;

-- Load store
COPY qspos.store
FROM 's3://dxl-quicksuite-poc-data/customer/store/store.csv'
IAM_ROLE 'arn:aws:iam::565393035923:role/service-role/AmazonRedshift-CommandsAccessRole-20251205T112603'
CSV
IGNOREHEADER 1
REGION 'us-east-1'
DATEFORMAT 'auto'
TIMEFORMAT 'auto'
TRUNCATECOLUMNS
BLANKSASNULL
EMPTYASNULL;

-- Load transaction_header
COPY qspos.transaction_header
FROM 's3://dxl-quicksuite-poc-data/customer/transaction_header/transaction_header.csv'
IAM_ROLE 'arn:aws:iam::565393035923:role/service-role/AmazonRedshift-CommandsAccessRole-20251205T112603'
CSV
IGNOREHEADER 1
REGION 'us-east-1'
DATEFORMAT 'auto'
TIMEFORMAT 'auto'
TRUNCATECOLUMNS
BLANKSASNULL
EMPTYASNULL;

-- Load transaction_detail
COPY qspos.transaction_detail
FROM 's3://dxl-quicksuite-poc-data/customer/transaction_detail/transaction_detail.csv'
IAM_ROLE 'arn:aws:iam::565393035923:role/service-role/AmazonRedshift-CommandsAccessRole-20251205T112603'
CSV
IGNOREHEADER 1
REGION 'us-east-1'
DATEFORMAT 'auto'
TIMEFORMAT 'auto'
TRUNCATECOLUMNS
BLANKSASNULL
EMPTYASNULL;

-- Load reward_detail
COPY qspos.reward_detail
FROM 's3://dxl-quicksuite-poc-data/customer/reward_detail/reward_detail.csv'
IAM_ROLE 'arn:aws:iam::565393035923:role/service-role/AmazonRedshift-CommandsAccessRole-20251205T112603'
CSV
IGNOREHEADER 1
REGION 'us-east-1'
DATEFORMAT 'auto'
TIMEFORMAT 'auto'
TRUNCATECOLUMNS
BLANKSASNULL
EMPTYASNULL;

-- Load household
COPY qspos.household
FROM 's3://dxl-quicksuite-poc-data/customer/household/household.csv'
IAM_ROLE 'arn:aws:iam::565393035923:role/service-role/AmazonRedshift-CommandsAccessRole-20251205T112603'
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
COPY qspos.orderheader
FROM 's3://dxl-quicksuite-poc-data/orders/orderheader/orderheader.csv'
IAM_ROLE 'arn:aws:iam::565393035923:role/service-role/AmazonRedshift-CommandsAccessRole-20251205T112603'
CSV
IGNOREHEADER 1
REGION 'us-east-1'
DATEFORMAT 'auto'
TIMEFORMAT 'auto'
TRUNCATECOLUMNS
BLANKSASNULL
EMPTYASNULL;

-- Load orderline
COPY qspos.orderline
FROM 's3://dxl-quicksuite-poc-data/orders/orderline/orderline.csv'
IAM_ROLE 'arn:aws:iam::565393035923:role/service-role/AmazonRedshift-CommandsAccessRole-20251205T112603'
CSV
IGNOREHEADER 1
REGION 'us-east-1'
DATEFORMAT 'auto'
TIMEFORMAT 'auto'
TRUNCATECOLUMNS
BLANKSASNULL
EMPTYASNULL;

-- Load orderline_items
COPY qspos.orderline_items
FROM 's3://dxl-quicksuite-poc-data/orders/orderline_items/orderline_items.csv'
IAM_ROLE 'arn:aws:iam::565393035923:role/service-role/AmazonRedshift-CommandsAccessRole-20251205T112603'
CSV
IGNOREHEADER 1
REGION 'us-east-1'
DATEFORMAT 'auto'
TIMEFORMAT 'auto'
TRUNCATECOLUMNS
BLANKSASNULL
EMPTYASNULL;

-- Load orderchargedetail
COPY qspos.orderchargedetail
FROM 's3://dxl-quicksuite-poc-data/orders/orderchargedetail/orderchargedetail.csv'
IAM_ROLE 'arn:aws:iam::565393035923:role/service-role/AmazonRedshift-CommandsAccessRole-20251205T112603'
CSV
IGNOREHEADER 1
REGION 'us-east-1'
DATEFORMAT 'auto'
TIMEFORMAT 'auto'
TRUNCATECOLUMNS
BLANKSASNULL
EMPTYASNULL;

-- Load invoice
COPY qspos.invoice
FROM 's3://dxl-quicksuite-poc-data/orders/invoice/invoice.csv'
IAM_ROLE 'arn:aws:iam::565393035923:role/service-role/AmazonRedshift-CommandsAccessRole-20251205T112603'
CSV
IGNOREHEADER 1
REGION 'us-east-1'
DATEFORMAT 'auto'
TIMEFORMAT 'auto'
TRUNCATECOLUMNS
BLANKSASNULL
EMPTYASNULL;

-- Load payment
COPY qspos.payment
FROM 's3://dxl-quicksuite-poc-data/orders/payment/payment.csv'
IAM_ROLE 'arn:aws:iam::565393035923:role/service-role/AmazonRedshift-CommandsAccessRole-20251205T112603'
CSV
IGNOREHEADER 1
REGION 'us-east-1'
DATEFORMAT 'auto'
TIMEFORMAT 'auto'
TRUNCATECOLUMNS
BLANKSASNULL
EMPTYASNULL;

-- Load quantitydetail
COPY qspos.quantitydetail
FROM 's3://dxl-quicksuite-poc-data/orders/quantitydetail/quantitydetail.csv'
IAM_ROLE 'arn:aws:iam::565393035923:role/service-role/AmazonRedshift-CommandsAccessRole-20251205T112603'
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

-- Check for any load errors
SELECT * FROM stl_load_errors
WHERE starttime >= CURRENT_DATE - 1
ORDER BY starttime DESC
LIMIT 100;

-- Sample data from each table
SELECT 'size_users' as table_name, * FROM qspos.size_users LIMIT 5;
SELECT 'customer' as table_name, * FROM qspos.customer LIMIT 5;
SELECT 'orderheader' as table_name, * FROM qspos.orderheader LIMIT 5;

-- ============================================================================
-- END OF SCRIPT
-- ============================================================================
