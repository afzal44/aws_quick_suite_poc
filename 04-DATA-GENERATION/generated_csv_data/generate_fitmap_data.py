"""
Generate FitMap/SizeStream Sample Data for AWS Quick Suite POC
Generates realistic body measurement and scan data
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import uuid
import json
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Configuration
NUM_USERS = 1000
NUM_SCANS = 2500
START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2025, 12, 5)

# Store numbers for DXL
STORE_NUMBERS = [9330, 9422, 9588, 9451, 5011, 9851, 9200, 9100, 9500, 9600]

# Generate size_users table
def generate_size_users():
    print("Generating size_users data...")
    
    users = []
    for i in range(NUM_USERS):
        user_id = str(uuid.uuid4())
        created = START_DATE + timedelta(days=random.randint(0, (END_DATE - START_DATE).days))
        modified = created + timedelta(days=random.randint(0, 30))
        
        # Realistic demographics for DXL (big & tall customers)
        birth_year = random.randint(1945, 2000)
        age = 2025 - birth_year
        
        # Height in inches (taller than average)
        height = random.randint(68, 84)  # 5'8" to 7'0"
        
        # Weight in lbs (heavier than average for big & tall)
        weight = random.randint(200, 400)
        
        gender = random.choice(['male', 'male', 'male', 'female'])  # 75% male
        
        first_names_male = ['Marcus', 'James', 'Robert', 'Michael', 'David', 'John', 'William', 'Richard', 'Joseph', 'Thomas']
        first_names_female = ['Mary', 'Patricia', 'Jennifer', 'Linda', 'Barbara', 'Elizabeth', 'Susan', 'Jessica', 'Sarah', 'Karen']
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez', 'Allen', 'Cowen']
        
        first_name = random.choice(first_names_male if gender == 'male' else first_names_female)
        last_name = random.choice(last_names)
        
        users.append({
            'id': user_id,
            'source_app': '095e3581-c21b-4abb-9602-8579d32c6c8e',
            'created': created.strftime('%d-%m-%Y %H:%M'),
            'modified': modified.strftime('%d-%m-%Y %H:%M'),
            'source_attendant': f"{random.randint(10000, 99999)}",
            'last_name': last_name,
            'first_name': first_name,
            'date_of_birth': f"{random.randint(1, 28):02d}-{random.randint(1, 12):02d}-{birth_year}",
            'email': f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 999)}@email.com",
            'phone': f"{random.randint(1000000000, 9999999999)}",
            'height': height,
            'weight': weight,
            'process_date': (modified + timedelta(days=1)).strftime('%d-%m-%Y'),
            'load_filename': f"userId-{user_id}_{modified.strftime('%Y_%m_%d_%H_%M_%S')}.json",
            'load_timestamp': f"{random.randint(10, 59)}:{random.randint(10, 59)}.{random.randint(1, 9)}",
            'gender': gender,
            'year': birth_year,
            'age': age,
            'bmi': round(weight / ((height * 0.0254) ** 2), 1),
            'customer_type': random.choice(['NEW', 'RETURNING', 'VIP', 'REGULAR']),
            'scan_count': random.randint(1, 10),
            'last_scan_date': modified.strftime('%d-%m-%Y')
        })
    
    return pd.DataFrame(users)

# Generate size_scans table
def generate_size_scans(users_df):
    print("Generating size_scans data...")
    
    scans = []
    user_ids = users_df['id'].tolist()
    
    for i in range(NUM_SCANS):
        scan_id = str(uuid.uuid4())
        user_id = random.choice(user_ids)
        user_data = users_df[users_df['id'] == user_id].iloc[0]
        
        scan_date = START_DATE + timedelta(days=random.randint(0, (END_DATE - START_DATE).days))
        store_num = random.choice(STORE_NUMBERS)
        
        age = 2025 - user_data['year']
        
        scanning_mode = random.choice(['self', 'assisted'])
        device_type = random.choice(['iPad14,5', 'iPad13,8', 'iPhone14,2', 'Android Tablet'])
        
        scans.append({
            'scan_id': scan_id,
            'user_id': user_id,
            'associate_login_email': f"scan+dxl.sm{store_num}@formcut.us",
            'scanning_mode': scanning_mode,
            'store_num': store_num,
            'app': '095e3581-c21b-4abb-9602-8579d32c6c8e',
            'date': scan_date.strftime('%d-%m-%Y %H:%M'),
            'source_metadata': json.dumps({
                "scanning_mode": scanning_mode, 
                "device": device_type,
                "app_version": f"{random.randint(2, 3)}.{random.randint(0, 5)}.{random.randint(0, 9)}",
                "scan_duration": random.randint(45, 120)
            }),
            'tar': f"s3://prod-tar-upload-5.0.1-616470503709/2d3d-silhouette-2.1.0/{scan_id}/acquired.tar.enc",
            'mesh': f"s3://prod-3did-buckets-1-scans-616470503709/{scan_id}/mesh.drc",
            'measures': f"s3://prod-3did-buckets-1-scans-616470503709/{scan_id}/measure_results_composite.yaml",
            'weight': user_data['weight'],
            'pose_count': random.choice([2, 3, 4]),
            'distance': random.choice([32, 34, 36, 38, 40]),
            'gender': user_data['gender'],
            'age': age,
            'height': user_data['height'],
            'type': random.choice(['2d3d-silhouette-2.1.0', '2d3d-silhouette-2.0.0', '3d-full-body-1.0']),
            'date_partition': random.choice([10, 15, 20, 25, 30]),
            'process_date': (scan_date + timedelta(days=1)).strftime('%d-%m-%Y'),
            'load_filename': f"scanId-{scan_id}_{scan_date.strftime('%Y_%m_%d_%H_%M_%S')}.json",
            'load_timestamp': f"{random.randint(10, 59)}:{random.randint(10, 59)}.{random.randint(1, 9)}",
            'pipeline': random.choice(['dar-measure_3.3.0', 'dar-measure_3.2.0', 'standard-pipeline-1.0']),
            'status': random.choice(['complete', 'complete', 'complete', 'processing', 'error']),
            'year': scan_date.year,
            'month': scan_date.month,
            'multiscan_num': str(random.choice([1, 1, 2, 3])),  # Always has a value
            'pipeline_metadata': json.dumps({
                "version": f"{random.randint(1, 3)}.{random.randint(0, 5)}",
                "quality_score": round(random.uniform(0.85, 0.99), 2)
            }),
            'scan_quality': random.choice(['EXCELLENT', 'GOOD', 'FAIR', 'POOR']),
            'retry_count': random.choice([0, 0, 0, 1, 2]),
            'confidence_score': round(random.uniform(0.75, 0.99), 2)
        })
    
    return pd.DataFrame(scans)

# Generate size_app_measures table
def generate_size_app_measures(scans_df):
    print("Generating size_app_measures data...")
    
    measures = []
    scan_ids = scans_df['scan_id'].tolist()[:2000]  # Subset for measures
    
    for idx, scan_id in enumerate(scan_ids):
        scan_data = scans_df[scans_df['scan_id'] == scan_id].iloc[0]
        weight_kg = scan_data['weight'] * 0.453592  # Convert lbs to kg
        height_cm = scan_data['height'] * 2.54  # Convert inches to cm
        
        # Generate realistic body measurements
        measures.append({
            'inc_id': idx + 1,
            'scan_id': scan_id,
            'bmctotal': round(random.uniform(3500, 5000), 2),
            'bodyfat': round(random.uniform(25, 60), 2),
            'fitness': round(random.uniform(5, 15), 2),
            'leanbodymass': round(random.uniform(150, 250), 2),
            'leanmassarms': round(random.uniform(8000, 15000), 2),
            'leanmasslegs': round(random.uniform(20000, 35000), 2),
            'shoulderwidth': round(random.uniform(19, 25), 2),
            'visceraladiposetissue': round(random.uniform(1500, 4000), 2),
            'weight': round(weight_kg, 2),
            'neck': round(random.uniform(17, 23), 2),
            'chest': round(random.uniform(48, 70), 2),
            'underbust': round(random.uniform(47, 68), 2),
            'overarm': round(random.uniform(52, 70), 2),
            'bicepleft': round(random.uniform(14, 21), 2),
            'bicepright': round(random.uniform(14, 21), 2),
            'forearmleft': round(random.uniform(12, 16), 2),
            'forearmright': round(random.uniform(12, 16), 2),
            'wristleft': round(random.uniform(7, 10), 2),
            'wristright': round(random.uniform(7, 10), 2),
            'stomach': round(random.uniform(45, 70), 2),
            'seat': round(random.uniform(45, 70), 2),
            'thighleft': round(random.uniform(25, 36), 2),
            'thighright': round(random.uniform(25, 36), 2),
            'calfleft': round(random.uniform(16, 22), 2),
            'calfright': round(random.uniform(16, 22), 2),
            'waist': round(random.uniform(42, 68), 2),
            'bodysurfacearea': round(random.uniform(3500, 4500), 2),
            'pantwaist': round(random.uniform(44, 70), 2),
            'backneck2waist': round(random.uniform(18, 22), 2),
            'sleeveleft': round(random.uniform(33, 37), 2),
            'sleeveright': round(random.uniform(33, 37), 2),
            'acrossshoulder': round(random.uniform(20, 24), 2),
            'crotchlength': round(random.uniform(32, 45), 2),
            'inseam': round(random.uniform(28, 36), 2),
            'chestcb': round(random.uniform(48, 70), 2),
            'hipscb': round(random.uniform(46, 68), 2),
            'outseamleft': round(random.uniform(36, 42), 2),
            'outseamright': round(random.uniform(36, 42), 2),
            'process_date': scan_data['process_date'],
            'load_filename': scan_data['load_filename'].replace('scanId-', 'scanId-') + '-app-measures-version-5.0.0',
            'load_timestamp': scan_data['load_timestamp'],
            'version': '5.0.0',
            'year': scan_data['year'],
            'month': scan_data['month']
        })
    
    return pd.DataFrame(measures)

# Generate size_dxl_custom_measures table
def generate_size_dxl_custom_measures(scans_df):
    print("Generating size_dxl_custom_measures data...")
    
    custom_measures = []
    scan_ids = scans_df['scan_id'].tolist()[:1500]
    
    brands = ['7 for All Man Kind', 'Brooks Brothers', 'Polo Ralph Lauren', 'Tommy Hilfiger', 'Calvin Klein']
    product_types = ['Denim', 'Dress Pants', 'Casual Pants', 'Shorts']
    
    for idx, scan_id in enumerate(scan_ids):
        scan_data = scans_df[scans_df['scan_id'] == scan_id].iloc[0]
        
        # Generate 2-3 product recommendations per scan
        for _ in range(random.randint(1, 3)):
            waist = random.choice([38, 40, 42, 44, 46, 48, 50, 52, 54, 56])
            inseam = random.choice([28, 30, 32, 33, 34, 36])
            
            custom_measures.append({
                'inc_id': len(custom_measures) + 1,
                'scan_id': scan_id,
                'producttype': random.choice(product_types),
                'details': f"Waist: {waist} , Inseam: {inseam}",
                'chest': round(random.uniform(48, 60), 2),
                'height': round(random.uniform(68, 80), 2),
                'inseamleft': round(inseam + random.uniform(-0.5, 0.5), 2),
                'inseamright': round(inseam + random.uniform(-0.5, 0.5), 2),
                'neck': round(random.uniform(16, 20), 2),
                'outseamleft': round(random.uniform(38, 46), 2),
                'outseamright': round(random.uniform(38, 46), 2),
                'overarmcircumference': round(random.uniform(52, 62), 2),
                'seatmeasurement': round(random.uniform(46, 56), 2),
                'shirtwaist': round(random.uniform(48, 58), 2),
                'sleeveleft': round(random.uniform(33, 37), 2),
                'sleeveright': round(random.uniform(33, 37), 2),
                'trouserwaist': round(waist + random.uniform(-1, 1), 2),
                'load_filename': f"scanId-{scan_id}-dxl-custom-measures-version-1.5.2_{scan_data['date'][:10].replace('-', '_')}.json",
                'process_date': scan_data['process_date'],
                'load_timestamp': scan_data['load_timestamp'],
                'version': '1.5.2',
                'brand': random.choice(brands),
                'year': scan_data['year'],
                'month': scan_data['month'],
                'thighleft': round(random.uniform(24, 30), 2),
                'wristleft': round(random.uniform(6.5, 8.5), 2),
                'shoulderwidth': round(random.uniform(18, 22), 2),
                'wristright': round(random.uniform(6.5, 8.5), 2),
                'thighright': round(random.uniform(24, 30), 2),
                'overarm': round(random.uniform(50, 60), 2),
                'chestcb': round(random.uniform(42, 52), 2),
                'bicepleft': round(random.uniform(13, 17), 2),
                'hipscb': round(random.uniform(44, 54), 2),
                'bicepright': round(random.uniform(13, 17), 2),
                'waist': round(waist + random.uniform(-1, 1), 2),
                'stomach': round(random.uniform(46, 58), 2)
            })
    
    return pd.DataFrame(custom_measures)

# Generate size_core_measures table
def generate_size_core_measures(scans_df):
    print("Generating size_core_measures data...")
    
    core_measures = []
    scan_ids = scans_df['scan_id'].tolist()[:2000]
    
    landmarks = ['HipWidestBack', 'HeadCircumRight', 'ShoulderLeft', 'ShoulderRight', 'WaistFront', 
                 'WaistBack', 'ChestFront', 'ChestBack', 'NeckBase', 'CrotchPoint']
    
    for scan_id in scan_ids:
        scan_data = scans_df[scans_df['scan_id'] == scan_id].iloc[0]
        
        # Generate 5-10 landmark measurements per scan
        for _ in range(random.randint(5, 10)):
            landmark = random.choice(landmarks)
            
            core_measures.append({
                'scan_id': scan_id,
                'measurement_name': f"{landmark}_circumference",
                'measurement_value': round(random.uniform(30, 120), 2),
                'landmark_name': landmark,
                'landmark_coordinates_x': round(random.uniform(-50, 50), 8),
                'landmark_coordinates_y': round(random.uniform(500, 1800), 8),
                'landmark_coordinates_z': round(random.uniform(-200, 200), 8),
                'process_date': scan_data['process_date'],
                'load_filename': f"scanId-{scan_id}-core-measures-version-2.4.8_{scan_data['date'][:10].replace('-', '_')}.json",
                'load_timestamp': scan_data['load_timestamp'],
                'version': '2.4.8',
                'function_type': random.choice(['landmarks', 'measurements', 'contours']),
                'year': scan_data['year'],
                'month': scan_data['month']
            })
    
    return pd.DataFrame(core_measures)

# Main execution
if __name__ == "__main__":
    print("Starting FitMap/SizeStream data generation...")
    print("=" * 60)
    
    # Generate all tables
    users_df = generate_size_users()
    scans_df = generate_size_scans(users_df)
    app_measures_df = generate_size_app_measures(scans_df)
    custom_measures_df = generate_size_dxl_custom_measures(scans_df)
    core_measures_df = generate_size_core_measures(scans_df)
    
    # Save to CSV
    print("\nSaving CSV files...")
    users_df.to_csv('size_users.csv', index=False, encoding='utf-8-sig')
    scans_df.to_csv('size_scans.csv', index=False, encoding='utf-8-sig')
    app_measures_df.to_csv('size_app_measures.csv', index=False, encoding='utf-8-sig')
    custom_measures_df.to_csv('size_dxl_custom_measures.csv', index=False, encoding='utf-8-sig')
    core_measures_df.to_csv('size_core_measures.csv', index=False, encoding='utf-8-sig')
    
    print("\n" + "=" * 60)
    print("FitMap Data Generation Complete!")
    print("=" * 60)
    print(f"[OK] size_users.csv: {len(users_df)} records")
    print(f"[OK] size_scans.csv: {len(scans_df)} records")
    print(f"[OK] size_app_measures.csv: {len(app_measures_df)} records")
    print(f"[OK] size_dxl_custom_measures.csv: {len(custom_measures_df)} records")
    print(f"[OK] size_core_measures.csv: {len(core_measures_df)} records")
    print("=" * 60)
