# AWS Quick Suite POC - Upload Dimensional Data to S3
# This script uploads reference/dimensional data files to S3

$BUCKET_NAME = "dxl-quicksuite-poc-data"
$REGION = "us-east-1"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "AWS Quick Suite POC - S3 Dimensional Data Upload" -ForegroundColor Cyan
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
Write-Host "Uploading Dimensional/Reference Data..." -ForegroundColor Yellow
Write-Host ""

# List of dimensional data files
$dimensionFiles = @(
    @{File="product_catalog.json"; Folder="dimensions/products"},
    @{File="store_locations.csv"; Folder="dimensions/stores"},
    @{File="size_chart_reference.csv"; Folder="dimensions/sizing"},
    @{File="marketing_campaigns.json"; Folder="dimensions/marketing"},
    @{File="customer_segments.csv"; Folder="dimensions/segments"},
    @{File="brand_information.json"; Folder="dimensions/brands"},
    @{File="shipping_zones.csv"; Folder="dimensions/shipping"},
    @{File="fitmap_device_specs.json"; Folder="dimensions/devices"}
)

$successCount = 0
$failCount = 0

foreach ($item in $dimensionFiles) {
    $file = $item.File
    $folder = $item.Folder
    
    if (Test-Path $file) {
        Write-Host "  Uploading $file to $folder..." -NoNewline
        aws s3 cp $file s3://$BUCKET_NAME/$folder/$file --quiet
        if ($LASTEXITCODE -eq 0) {
            Write-Host " [OK]" -ForegroundColor Green
            $successCount++
        } else {
            Write-Host " [FAIL]" -ForegroundColor Red
            $failCount++
        }
    } else {
        Write-Host "  WARNING: $file not found" -ForegroundColor Red
        $failCount++
    }
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Verifying upload..." -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Files in dimensions folder:" -ForegroundColor Yellow
aws s3 ls s3://$BUCKET_NAME/dimensions/ --recursive --human-readable

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Upload Summary" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Successful uploads: $successCount" -ForegroundColor Green
Write-Host "Failed uploads: $failCount" -ForegroundColor $(if ($failCount -gt 0) { "Red" } else { "Green" })
Write-Host "============================================================" -ForegroundColor Cyan

Write-Host ""
Write-Host "S3 Folder Structure:" -ForegroundColor Yellow
Write-Host "  s3://$BUCKET_NAME/dimensions/products/    - Product catalog"
Write-Host "  s3://$BUCKET_NAME/dimensions/stores/      - Store locations"
Write-Host "  s3://$BUCKET_NAME/dimensions/sizing/      - Size charts"
Write-Host "  s3://$BUCKET_NAME/dimensions/marketing/   - Marketing campaigns"
Write-Host "  s3://$BUCKET_NAME/dimensions/segments/    - Customer segments"
Write-Host "  s3://$BUCKET_NAME/dimensions/brands/      - Brand information"
Write-Host "  s3://$BUCKET_NAME/dimensions/shipping/    - Shipping zones"
Write-Host "  s3://$BUCKET_NAME/dimensions/devices/     - FitMap devices"

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "1. Configure AWS Quick Suite to connect to S3"
Write-Host "2. Add S3 as a data source in Quick Index"
Write-Host "3. Create queries that join Redshift + S3 data"
Write-Host "4. Test cross-source analytics"
Write-Host ""
Write-Host "Example Query:"
Write-Host '  "Show me sales by brand category from brand_information.json"'
Write-Host '  "Which stores have FitMap devices based on store_locations.csv?"'
Write-Host "============================================================" -ForegroundColor Cyan

Read-Host "Press Enter to exit"
