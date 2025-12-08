@echo off
REM AWS Quick Suite POC - S3 Upload Script for Windows
REM Replace YOUR_BUCKET_NAME with your actual S3 bucket name

SET BUCKET_NAME=dxl-quicksuite-poc-data
SET REGION=us-east-1

echo ============================================================
echo AWS Quick Suite POC - S3 Upload Script
echo ============================================================
echo.
echo Bucket: %BUCKET_NAME%
echo Region: %REGION%
echo.
echo ============================================================

REM Check if AWS CLI is installed
aws --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: AWS CLI is not installed or not in PATH
    echo Please install AWS CLI: https://aws.amazon.com/cli/
    pause
    exit /b 1
)

echo Step 1: Creating S3 bucket...
aws s3 mb s3://%BUCKET_NAME% --region %REGION% 2>nul
if errorlevel 1 (
    echo Bucket already exists or error creating bucket
) else (
    echo Bucket created successfully
)
echo.

echo Step 2: Uploading FitMap data...
aws s3 cp size_users.csv s3://%BUCKET_NAME%/fitmap/size_users/size_users.csv
aws s3 cp size_scans.csv s3://%BUCKET_NAME%/fitmap/size_scans/size_scans.csv
aws s3 cp size_app_measures.csv s3://%BUCKET_NAME%/fitmap/size_app_measures/size_app_measures.csv
aws s3 cp size_dxl_custom_measures.csv s3://%BUCKET_NAME%/fitmap/size_dxl_custom_measures/size_dxl_custom_measures.csv
echo FitMap data uploaded
echo.

echo Step 3: Uploading Customer data...
aws s3 cp customer.csv s3://%BUCKET_NAME%/customer/customer/customer.csv
aws s3 cp address.csv s3://%BUCKET_NAME%/customer/address/address.csv
aws s3 cp email.csv s3://%BUCKET_NAME%/customer/email/email.csv
aws s3 cp store.csv s3://%BUCKET_NAME%/customer/store/store.csv
aws s3 cp transaction_header.csv s3://%BUCKET_NAME%/customer/transaction_header/transaction_header.csv
aws s3 cp transaction_detail.csv s3://%BUCKET_NAME%/customer/transaction_detail/transaction_detail.csv
aws s3 cp reward_detail.csv s3://%BUCKET_NAME%/customer/reward_detail/reward_detail.csv
aws s3 cp household.csv s3://%BUCKET_NAME%/customer/household/household.csv
echo Customer data uploaded
echo.

echo Step 4: Uploading Order data...
aws s3 cp orderheader.csv s3://%BUCKET_NAME%/orders/orderheader/orderheader.csv
aws s3 cp orderline.csv s3://%BUCKET_NAME%/orders/orderline/orderline.csv
aws s3 cp orderline_items.csv s3://%BUCKET_NAME%/orders/orderline_items/orderline_items.csv
aws s3 cp orderchargedetail.csv s3://%BUCKET_NAME%/orders/orderchargedetail/orderchargedetail.csv
aws s3 cp invoice.csv s3://%BUCKET_NAME%/orders/invoice/invoice.csv
aws s3 cp payment.csv s3://%BUCKET_NAME%/orders/payment/payment.csv
aws s3 cp quantitydetail.csv s3://%BUCKET_NAME%/orders/quantitydetail/quantitydetail.csv
echo Order data uploaded
echo.

echo ============================================================
echo Step 5: Verifying upload...
echo ============================================================
aws s3 ls s3://%BUCKET_NAME%/ --recursive --human-readable --summarize

echo.
echo ============================================================
echo Upload Complete!
echo ============================================================
echo.
echo Next Steps:
echo 1. Load data to Redshift using COPY commands
echo 2. Or create Athena tables pointing to S3
echo 3. Configure AWS Quick Suite data sources
echo.
echo See QUICK_START.md for detailed instructions
echo ============================================================

pause
