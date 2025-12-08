# AWS Quick Suite POC - S3 Upload Script (PowerShell)
# Replace YOUR_BUCKET_NAME with your actual S3 bucket name

$BUCKET_NAME = "dxl-quicksuite-poc-data"
$REGION = "us-east-1"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "AWS Quick Suite POC - S3 Upload Script" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Bucket: $BUCKET_NAME"
Write-Host "Region: $REGION"
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan

# Check if AWS CLI is installed
try {
    $awsVersion = aws --version 2>&1
    Write-Host "AWS CLI detected: $awsVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: AWS CLI is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install AWS CLI: https://aws.amazon.com/cli/" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Step 1: Creating S3 bucket..." -ForegroundColor Yellow
aws s3 mb s3://$BUCKET_NAME --region $REGION 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Bucket already exists or error creating bucket (this is OK)" -ForegroundColor Yellow
} else {
    Write-Host "Bucket created successfully" -ForegroundColor Green
}

Write-Host ""
Write-Host "Step 2: Uploading FitMap data..." -ForegroundColor Yellow
$fitMapFiles = @(
    "size_users.csv",
    "size_scans.csv",
    "size_app_measures.csv",
    "size_dxl_custom_measures.csv",
    "size_core_measures.csv"
)

foreach ($file in $fitMapFiles) {
    if (Test-Path $file) {
        $tableName = $file -replace '.csv', ''
        Write-Host "  Uploading $file..." -NoNewline
        aws s3 cp $file s3://$BUCKET_NAME/fitmap/$tableName/$file --quiet
        if ($LASTEXITCODE -eq 0) {
            Write-Host " [OK]" -ForegroundColor Green
        } else {
            Write-Host " [FAIL]" -ForegroundColor Red
        }
    } else {
        Write-Host "  WARNING: $file not found" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Step 3: Uploading Customer data..." -ForegroundColor Yellow
$customerFiles = @(
    "customer.csv",
    "address.csv",
    "email.csv",
    "store.csv",
    "transaction_header.csv",
    "transaction_detail.csv",
    "reward_detail.csv",
    "household.csv"
)

foreach ($file in $customerFiles) {
    if (Test-Path $file) {
        $tableName = $file -replace '.csv', ''
        Write-Host "  Uploading $file..." -NoNewline
        aws s3 cp $file s3://$BUCKET_NAME/customer/$tableName/$file --quiet
        if ($LASTEXITCODE -eq 0) {
            Write-Host " [OK]" -ForegroundColor Green
        } else {
            Write-Host " [FAIL]" -ForegroundColor Red
        }
    } else {
        Write-Host "  WARNING: $file not found" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Step 4: Uploading Order data..." -ForegroundColor Yellow
$orderFiles = @(
    "orderheader.csv",
    "orderline.csv",
    "orderline_items.csv",
    "orderchargedetail.csv",
    "invoice.csv",
    "payment.csv",
    "quantitydetail.csv"
)

foreach ($file in $orderFiles) {
    if (Test-Path $file) {
        $tableName = $file -replace '.csv', ''
        Write-Host "  Uploading $file..." -NoNewline
        aws s3 cp $file s3://$BUCKET_NAME/orders/$tableName/$file --quiet
        if ($LASTEXITCODE -eq 0) {
            Write-Host " [OK]" -ForegroundColor Green
        } else {
            Write-Host " [FAIL]" -ForegroundColor Red
        }
    } else {
        Write-Host "  WARNING: $file not found" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Step 5: Verifying upload..." -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan
aws s3 ls s3://$BUCKET_NAME/ --recursive --human-readable --summarize

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Upload Complete!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Load data to Redshift using COPY commands"
Write-Host "2. Or create Athena tables pointing to S3"
Write-Host "3. Configure AWS Quick Suite data sources"
Write-Host ""
Write-Host "See QUICK_START.md for detailed instructions"
Write-Host "============================================================" -ForegroundColor Cyan

Read-Host "Press Enter to exit"
