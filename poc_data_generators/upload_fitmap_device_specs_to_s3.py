#!/usr/bin/env python3
"""
AWS Quick Suite POC - Upload FitMap Device Specs to S3 (Individual Files)
This script extracts devices from fitmap_device_specs.json array and uploads each as a separate file to S3
This format is compatible with Athena table queries
"""

import json
import boto3
from botocore.exceptions import ClientError
import sys
from pathlib import Path

# Configuration from upload_dimensions_to_s3.ps1
BUCKET_NAME = "dxl-quicksuite-poc-data"
REGION = "us-east-1"
S3_FOLDER = "dimensions/fitmap_devices"

def main():
    print("=" * 60)
    print("AWS Quick Suite POC - FitMap Device Specs S3 Upload")
    print("=" * 60)
    print(f"\nBucket: {BUCKET_NAME}")
    print(f"Region: {REGION}")
    print(f"S3 Folder: {S3_FOLDER}")
    print("=" * 60)

    # Read device specs
    catalog_file = Path("fitmap_device_specs.json")
    if not catalog_file.exists():
        print(f"\nERROR: {catalog_file} not found!")
        print("Please run this script from the poc_data_generators directory")
        sys.exit(1)

    print(f"\nReading {catalog_file}...")
    try:
        with open(catalog_file, 'r') as f:
            devices = json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON format - {e}")
        sys.exit(1)

    if not isinstance(devices, list):
        print("ERROR: Expected JSON array format")
        sys.exit(1)

    print(f"Loaded {len(devices)} devices")

    # Initialize S3 client
    print(f"\nConnecting to AWS S3 (region: {REGION})...")
    try:
        s3_client = boto3.client('s3', region_name=REGION)
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
        print("  1. AWS CLI is configured (run: aws configure)")
        print("  2. You have valid AWS credentials")
        print("  3. You have S3 access permissions")
        sys.exit(1)

    # Upload devices
    print(f"\nUploading {len(devices)} devices to S3...")
    print(f"Target: s3://{BUCKET_NAME}/{S3_FOLDER}/")
    print()

    success_count = 0
    fail_count = 0

    for i, device in enumerate(devices, 1):
        device_id = device.get('device_id', f'unknown_{i}')
        # Sanitize device_id for filename (replace special characters)
        safe_device_id = device_id.replace('/', '_').replace(',', '_')
        filename = f"device_{safe_device_id}.json"
        s3_key = f"{S3_FOLDER}/{filename}"

        try:
            # Convert device to JSON string (single line for Athena compatibility)
            device_json = json.dumps(device)

            # Upload to S3
            s3_client.put_object(
                Bucket=BUCKET_NAME,
                Key=s3_key,
                Body=device_json,
                ContentType='application/json'
            )

            success_count += 1

            # Progress indicator
            if i % 10 == 0 or i == len(devices):
                print(f"  Uploaded {i}/{len(devices)} devices...")

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
    print(f"""CREATE EXTERNAL TABLE fitmap_device_specs (
  device_id STRING,
  device_name STRING,
  manufacturer STRING,
  os STRING,
  camera_resolution STRING,
  scan_accuracy STRING,
  recommended BOOLEAN,
  deployment_date STRING
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
LOCATION 's3://{BUCKET_NAME}/{S3_FOLDER}/'
""")
    print("\n3. Query your data:")
    print("   SELECT manufacturer, COUNT(*) as device_count FROM fitmap_device_specs WHERE recommended = true GROUP BY manufacturer;")
    print("=" * 60)

if __name__ == "__main__":
    main()
