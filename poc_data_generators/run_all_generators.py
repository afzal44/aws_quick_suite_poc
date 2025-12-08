"""
Master script to run all data generators for AWS Quick Suite POC
"""

import subprocess
import sys
import os
from datetime import datetime

def run_script(script_name):
    """Run a Python script and capture output"""
    print(f"\n{'='*70}")
    print(f"Running: {script_name}")
    print(f"{'='*70}")
    
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=True,
            text=True,
            check=True
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR running {script_name}:")
        print(e.stderr)
        return False

def clean_old_csv_files():
    """Delete all existing CSV files"""
    csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]
    
    if csv_files:
        print("\nCleaning up old CSV files...")
        print("-" * 70)
        for csv_file in csv_files:
            try:
                os.remove(csv_file)
                print(f"  Deleted: {csv_file}")
            except Exception as e:
                print(f"  Error deleting {csv_file}: {e}")
        print("-" * 70)
        print(f"Removed {len(csv_files)} old CSV files\n")
    else:
        print("\nNo existing CSV files to clean up.\n")

def main():
    start_time = datetime.now()
    
    print("\n" + "="*70)
    print("AWS QUICK SUITE POC - DATA GENERATION")
    print("="*70)
    print(f"Start Time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    # Clean up old CSV files first
    clean_old_csv_files()
    
    # List of scripts to run
    scripts = [
        'generate_fitmap_data.py',
        'generate_customer_data.py',
        'generate_order_data.py'
    ]
    
    results = {}
    
    for script in scripts:
        if os.path.exists(script):
            success = run_script(script)
            results[script] = "✓ SUCCESS" if success else "✗ FAILED"
        else:
            print(f"WARNING: {script} not found!")
            results[script] = "✗ NOT FOUND"
    
    # Summary
    end_time = datetime.now()
    duration = end_time - start_time
    
    print("\n" + "="*70)
    print("GENERATION SUMMARY")
    print("="*70)
    
    for script, status in results.items():
        status_clean = status.replace('✓', '[OK]').replace('✗', '[FAIL]')
        print(f"{status_clean} - {script}")
    
    print("="*70)
    print(f"Total Duration: {duration}")
    print(f"End Time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    # List generated CSV files
    csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]
    
    if csv_files:
        print("\nGenerated CSV Files:")
        print("-" * 70)
        for csv_file in sorted(csv_files):
            file_size = os.path.getsize(csv_file) / (1024 * 1024)  # Size in MB
            print(f"  • {csv_file:<40} ({file_size:.2f} MB)")
        print("-" * 70)
        print(f"\nTotal CSV files: {len(csv_files)}")
    
    print("\n" + "="*70)
    print("NEXT STEPS:")
    print("="*70)
    print("1. Review the generated CSV files")
    print("2. Upload CSV files to S3 bucket")
    print("3. Load data into Redshift tables")
    print("4. Configure AWS Quick Suite data sources")
    print("5. Start testing queries!")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
