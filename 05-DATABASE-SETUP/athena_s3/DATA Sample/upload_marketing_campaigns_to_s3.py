#!/usr/bin/env python3
"""
AWS Quick Suite POC - Upload Marketing Campaigns to S3 (Individual Files)
This script extracts campaigns from marketing_campaigns.json array and uploads each as a separate file to S3
This format is compatible with Athena table queries
"""

import json
import boto3
from botocore.exceptions import ClientError
import sys
from pathlib import Path

# Configuration from upload_dimensions_to_s3.ps1
BUCKET_NAME = "dxl-quicksuite-poc"
REGION = "us-east-1"
S3_FOLDER = "dimensions/marketing"

def main():
    print("=" * 60)
    print("AWS Quick Suite POC - Marketing Campaigns S3 Upload")
    print("=" * 60)
    print(f"\nBucket: {BUCKET_NAME}")
    print(f"Region: {REGION}")
    print(f"S3 Folder: {S3_FOLDER}")
    print("=" * 60)
    
    # Read marketing campaigns
    catalog_file = Path("marketing_campaigns.json")
    if not catalog_file.exists():
        print(f"\nERROR: {catalog_file} not found!")
        print("Please run this script from the poc_data_generators directory")
        sys.exit(1)
    
    print(f"\nReading {catalog_file}...")
    try:
        with open(catalog_file, 'r') as f:
            products = json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON format - {e}")
        sys.exit(1)
    
    if not isinstance(products, list):
        print("ERROR: Expected JSON array format")
        sys.exit(1)
    
    print(f"Loaded {len(products)} campaigns")
    
    # Initialize S3 client with qloudx profile
    print(f"\nConnecting to AWS S3 (region: {REGION}) using profile 'qloudx'...")
    try:
        session = boto3.Session(profile_name='qloudx')
        s3_client = session.client('s3', region_name=REGION)
        # Test connection
        s3_client.head_bucket(Bucket=BUCKET_NAME)
        print(f"Connected to bucket: {BUCKET_NAME}")
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == '404':
            print(f"ERROR: Bucket '{BUCKET_NAME}' does not exist")
        elif error_code == '403':
            print(f"ERROR: Access denied to bucket '{BUCKET_NAME}'")
        else:
            print(f"ERROR: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Failed to connect to AWS - {e}")
        print("\nPlease ensure:")
        print("  1. AWS CLI is configured with 'qloudx' profile (run: aws configure --profile qloudx)")
        print("  2. You have valid AWS credentials for the qloudx profile")
        print("  3. You have S3 access permissions")
        sys.exit(1)
    
    # Upload campaigns
    print(f"\nUploading {len(products)} campaigns to S3...")
    print(f"Target: s3://{BUCKET_NAME}/{S3_FOLDER}/")
    print()
    
    success_count = 0
    fail_count = 0
    
    for i, product in enumerate(products, 1):
        campaign_id = product.get('campaign_id', f'unknown_{i}')
        filename = f"campaign_{campaign_id}.json"
        s3_key = f"{S3_FOLDER}/{filename}"
        
        try:
            # Convert campaign to JSON string (single line for Athena compatibility)
            product_json = json.dumps(product)
            
            # Upload to S3
            s3_client.put_object(
                Bucket=BUCKET_NAME,
                Key=s3_key,
                Body=product_json,
                ContentType='application/json'
            )
            
            success_count += 1
            
            # Progress indicator
            if i % 10 == 0:
                print(f"  Uploaded {i}/{len(products)} campaigns...")
        
        except Exception as e:
            print(f"  Failed to upload {filename}: {e}")
            fail_count += 1
    
    print(f"\nUpload complete!")
    
    # Summary
    print("\n" + "=" * 60)
    print("Upload Summary")
    print("=" * 60)
    print(f"Successful uploads: {success_count}")
    print(f"Failed uploads: {fail_count}")
    print("=" * 60)
    
    # Verify upload
    print("\nVerifying S3 upload...")
    try:
        response = s3_client.list_objects_v2(
            Bucket=BUCKET_NAME,
            Prefix=S3_FOLDER + "/",
            MaxKeys=10
        )
        
        if 'Contents' in response:
            print(f"Found {response.get('KeyCount', 0)} files in S3")
            print("\nSample files:")
            for obj in response['Contents'][:5]:
                size_kb = obj['Size'] / 1024
                print(f"  - {obj['Key']} ({size_kb:.2f} KB)")
        else:
            print("No files found in S3")
    except Exception as e:
        print(f"Could not verify: {e}")
    
    # Next steps
    print("\n" + "=" * 60)
    print("Next Steps - Create Athena Table")
    print("=" * 60)
    print("\n1. Open AWS Athena Console")
    print("2. Create a table with this DDL:\n")
    print(f"""CREATE EXTERNAL TABLE marketing_campaigns (
  campaign_id STRING,
  campaign_name STRING,
  start_date STRING,
  end_date STRING,
  discount_percent INT,
  budget DOUBLE,
  target_audience STRING,
  channels ARRAY<STRING>,
  utm_campaign STRING,
  utm_medium STRING,
  utm_source STRING
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
LOCATION 's3://{BUCKET_NAME}/{S3_FOLDER}/'
""")
    print("\n3. Query your data:")
    print("   SELECT campaign_name, discount_percent, budget FROM marketing_campaigns;")
    print("=" * 60)

if __name__ == "__main__":
    main()
