"""
Generate Customer/CRM Sample Data for AWS Quick Suite POC
Generates realistic customer, address, transaction data
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed
np.random.seed(42)
random.seed(42)

# Configuration
NUM_CUSTOMERS = 5000
NUM_TRANSACTIONS = 15000
START_DATE = datetime(2012, 1, 1)
END_DATE = datetime(2025, 12, 5)

# Store configuration
STORES = [
    (1, 'REPP CATALOG', 'Repp Catalog'),
    (2, 'REPP E-COMME', 'Repp E-Commerce'),
    (5011, 'DXL STORE 5011', 'DXL Store 5011'),
    (9330, 'DXL STORE 9330', 'DXL Store 9330'),
    (9422, 'DXL STORE 9422', 'DXL Store 9422'),
    (9588, 'DXL STORE 9588', 'DXL Store 9588'),
    (9451, 'DXL STORE 9451', 'DXL Store 9451'),
    (9851, 'DXL STORE 9851', 'DXL Store 9851')
]

# Language codes
LANGUAGE_CODES = ['ENG', 'SPA', 'FRE', 'GER', 'ITA', 'POR', 'CHI', 'JPN']

# Country codes
COUNTRY_CODES = ['USA', 'CAN', 'MEX', 'GBR', 'FRA', 'DEU', 'ITA', 'ESP', 'AUS', 'JPN']

# Email types
EMAIL_TYPES = ['PRIMARY', 'SECONDARY', 'WORK', 'PERSONAL', 'BUSINESS']

# Generate customer table
def generate_customers():
    print("Generating customer data...")
    
    customers = []
    first_names = ['John', 'Michael', 'David', 'James', 'Robert', 'William', 'Richard', 'Joseph', 'Thomas', 'Charles',
                   'Mary', 'Patricia', 'Jennifer', 'Linda', 'Barbara', 'Elizabeth', 'Susan', 'Jessica', 'Sarah', 'Karen']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez',
                  'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin']
    
    for i in range(NUM_CUSTOMERS):
        customer_id = i + 1
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        gender = random.choice(['M', 'M', 'M', 'F'])  # 75% male for DXL
        birth_year = random.randint(1945, 2000)
        birth_month = random.randint(1, 12)
        birth_day = random.randint(1, 28)
        birth_date = f"{birth_day:02d}-{birth_month:02d}-{birth_year}"
        
        # Generate company name for some customers
        company_names = ['', '', '', 'ABC Corp', 'XYZ Industries', 'Tech Solutions', 'Global Enterprises', 'Retail Group']
        job_titles = ['', '', '', 'Manager', 'Director', 'VP Sales', 'CEO', 'Consultant', 'Engineer']
        
        created_date = START_DATE + timedelta(days=random.randint(0, (END_DATE - START_DATE).days))
        
        customers.append({
            'customer_id': customer_id,
            'language_code': random.choice(LANGUAGE_CODES),
            'alpha_key': f"{last_name.upper()[:4].ljust(8)}{first_name.upper()[:4]}",
            'phonetic_key': f"{last_name.upper()[:4]}{first_name.upper()[:2]}",
            'customer_no': f"{random.randint(10000000000, 99999999999)}",
            'title': random.choice(['Mr', 'Mrs', 'Ms', 'Dr', 'Prof']),
            'first_name': first_name,
            'last_name': last_name,
            'gender': gender,
            'marital_status': random.choice(['M', 'S', 'D', 'W', 'U']),
            'next_address_id': random.randint(1, 3),
            'distribution_status': random.choice([0, 1]),
            'landmark_date_a': created_date.strftime('%d-%m-%Y'),
            'landmark_date_b': (created_date + timedelta(days=random.randint(30, 365))).strftime('%d-%m-%Y'),
            'segmentation_value_a': random.choice(['PREMIUM', 'STANDARD', 'BASIC', 'VIP', 'GOLD']),
            'segmentation_value_b': random.choice(['HIGH', 'MEDIUM', 'LOW', 'VERY_HIGH']),
            'segmentation_value_c': random.choice(['ACTIVE', 'INACTIVE', 'DORMANT', 'ENGAGED']),
            'segmentation_value_d': random.choice(['RETAIL', 'ONLINE', 'BOTH', 'HYBRID']),
            'segmentation_code_a': random.choice(['A', 'B', 'C', 'D', 'E']),
            'segmentation_code_b': random.choice(['1', '2', '3', '4', '5']),
            'segmentation_code_c': random.choice(['X', 'Y', 'Z', 'W']),
            'segmentation_code_d': random.choice(['P', 'Q', 'R', 'S']),
            'segmentation_flag_a': random.choice([0, 1]),
            'segmentation_flag_b': random.choice([0, 1]),
            'segmentation_flag_c': random.choice([0, 1]),
            'segmentation_flag_d': random.choice([0, 1]),
            'segmentation_flag_e': random.choice([0, 1]),
            'segmentation_flag_f': random.choice([0, 1]),
            'status': random.choice(['A', 'A', 'A', 'I', 'P']),  # Mostly Active
            'salutation': f"{random.choice(['Mr', 'Mrs', 'Ms', 'Dr'])} {first_name} {last_name}",
            'head_of_household_flag': random.choice([0, 1]),
            'timestamp': f"{random.randint(1, 999999999):016X}",
            'original_division_id': random.choice([1, 2, 3]),
            'company_name': random.choice(['ABC Corp', 'XYZ Industries', 'Tech Solutions', 'Global Enterprises', 'Retail Group', 'Services Inc', 'Consulting LLC']),
            'job_title': random.choice(['Manager', 'Director', 'VP Sales', 'CEO', 'Consultant', 'Engineer', 'Analyst', 'Specialist']),
            'birth_date': birth_date,
            'birth_day': birth_day,
            'is_complete': random.choice([0, 1]),
            'complete_date': created_date.strftime('%d-%m-%Y %H:%M'),
            'complete_modify_date': (created_date + timedelta(days=random.randint(1, 100))).strftime('%d-%m-%Y %H:%M'),
            'system_modify_date': (created_date + timedelta(days=random.randint(0, 500))).strftime('%d-%m-%Y %H:%M')
        })
    
    return pd.DataFrame(customers)

# Generate address table
def generate_addresses(customers_df):
    print("Generating address data...")
    
    addresses = []
    
    cities_states = [
        ('New York', 'NY', '10001'), ('Los Angeles', 'CA', '90001'), ('Chicago', 'IL', '60601'),
        ('Houston', 'TX', '77001'), ('Phoenix', 'AZ', '85001'), ('Philadelphia', 'PA', '19019'),
        ('San Antonio', 'TX', '78201'), ('San Diego', 'CA', '92101'), ('Dallas', 'TX', '75201'),
        ('San Jose', 'CA', '95101'), ('Austin', 'TX', '78701'), ('Jacksonville', 'FL', '32099'),
        ('Fort Worth', 'TX', '76101'), ('Columbus', 'OH', '43004'), ('Charlotte', 'NC', '28201'),
        ('Freeville', 'NY', '13068'), ('Lady Lake', 'FL', '32159'), ('Miami', 'FL', '33101')
    ]
    
    for _, customer in customers_df.iterrows():
        # Each customer gets 1-2 addresses
        for addr_id in range(1, random.randint(2, 3)):
            city, state, base_zip = random.choice(cities_states)
            street_num = random.randint(1, 9999)
            street_names = ['Main St', 'Oak Ave', 'Maple Dr', 'Park Ln', 'Cedar Rd', 'Elm St', 'Pine Ave', 'Leisure Ln', 'Salido Ave', 
                           'Broadway', 'Washington Ave', 'Market St', 'Church Rd', 'Lake Dr', 'Hill St']
            
            country_code = random.choice(COUNTRY_CODES)
            created_date = START_DATE + timedelta(days=random.randint(0, 1000))
            modified_date = created_date + timedelta(days=random.randint(0, (END_DATE - created_date).days))
            
            addresses.append({
                'customer_id': customer['customer_id'],
                'address_id': addr_id,
                'country_code': country_code,
                'address_match_key': f"{base_zip}{random.randint(1000, 9999)}    {random.choice(['HOME', 'WORK', 'MAIL', 'SHIP', 'BILL'])}",
                'address_type_code': random.choice(['HOME', 'WORK', 'MAIL', 'SHIP', 'BILL', 'OTHER']),
                'mail_indicator': random.choice([0, 1]),
                'carrier_route': f"C{random.randint(1000, 9999)}" if random.random() > 0.5 else f"R{random.randint(100, 999)}",
                'address_ncoa_date': modified_date.strftime('%d-%m-%Y'),
                'address_1': f"{street_num} {random.choice(street_names)}",
                'address_2': random.choice([f"Apt {random.randint(1, 999)}", f"Suite {random.randint(100, 999)}", f"Unit {random.randint(1, 50)}", f"#{random.randint(1, 999)}"]),
                'address_3': city,
                'address_4': state,
                'address_5': random.choice(['Building A', 'Building B', 'North Wing', 'South Wing', 'East Tower', 'West Tower']),
                'address_6': random.choice(['Floor 1', 'Floor 2', 'Floor 3', 'Ground Floor', 'Mezzanine']),
                'post_code': f"{base_zip}-{random.randint(1000, 9999)}",
                'date_last_modified': modified_date.strftime('%d-%m-%Y %H:%M'),
                'address_error': random.choice(['VALID', 'R913', 'R914', 'R915', 'VERIFIED']),
                'address_longitude': round(random.uniform(-125, -65), 6),
                'address_latitude': round(random.uniform(25, 50), 6),
                'timestamp': f"{random.randint(1, 999999999):016X}",
                'create_store_no': random.choice([s[0] for s in STORES]),
                'modify_store_no': random.choice([s[0] for s in STORES]),
                'create_user_id': random.choice([-2, -1, 1000, 2000, 3000]),
                'create_date': created_date.strftime('%d-%m-%Y %H:%M'),
                'modify_user_id': random.choice([-2, -1, 1000, 2000, 3000]),
                'create_source_id': random.choice([1, 2, 3, 4]),
                'create_comment': random.choice(['Initial load', 'Customer update', 'Address verification', 'System migration', 'Data import']),
                'modify_source_id': random.choice([0, 1, 2, 3]),
                'modify_comment': random.choice(['Updated by customer', 'NCOA update', 'Verified', 'System update', 'Manual correction']),
                'posted_date': modified_date.strftime('%d-%m-%Y %H:%M'),
                'old_customer_id': f"OLD{random.randint(100000, 999999)}",
                'temp_old_cust_no': f"{random.randint(1000000, 9999999)}"
            })
    
    return pd.DataFrame(addresses)

# Generate email table
def generate_emails(customers_df):
    print("Generating email data...")
    
    emails = []
    domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'aol.com', 'icloud.com']
    
    for _, customer in customers_df.iterrows():
        # 90% have at least one email, some have multiple
        num_emails = random.choices([0, 1, 2, 3], weights=[10, 60, 25, 5])[0]
        
        for email_id in range(1, num_emails + 1):
            email_addr = f"{customer['first_name'].lower()}.{customer['last_name'].lower()}{random.randint(1, 999)}@{random.choice(domains)}"
            created_date = START_DATE + timedelta(days=random.randint(0, 1000))
            modified_date = created_date + timedelta(days=random.randint(0, (END_DATE - created_date).days))
            
            emails.append({
                'customer_id': customer['customer_id'],
                'email_id': email_id,
                'email_address': email_addr,
                'email_type': random.choice(EMAIL_TYPES),
                'is_valid': random.choice([1, 1, 1, 0]),  # 75% valid
                'opt_in': random.choice([0, 1]),
                'opt_in_date': created_date.strftime('%d-%m-%Y %H:%M'),
                'bounce_count': random.choice([0, 0, 0, 1, 2, 3]),
                'last_verified': modified_date.strftime('%d-%m-%Y %H:%M'),
                'create_date': created_date.strftime('%d-%m-%Y %H:%M'),
                'modify_date': modified_date.strftime('%d-%m-%Y %H:%M'),
                'create_user_id': random.choice([-2, -1, 1000, 2000]),
                'modify_user_id': random.choice([-2, -1, 1000, 2000])
            })
    
    return pd.DataFrame(emails)

# Generate store table
def generate_stores():
    print("Generating store data...")
    
    stores = []
    for store_no, short_name, full_name in STORES:
        stores.append({
            'store_no': store_no,
            'division_id': 2,
            'store_short_name': short_name,
            'store_name': full_name,
            'next_customer_no': store_no * 1000000 + 1,
            'sales_associate_no_default': 9999,
            'store_country_code': 'USA',
            'reward_redemption_flag': 0,
            'real_time_rewards_flag': 1,
            'timestamp': f"{random.randint(1, 999999999):016X}",
            'sales_channel_code': 'STR' if store_no > 10 else 'WEB',
            'division_set_id': 1,
            'eom_id': ''
        })
    
    return pd.DataFrame(stores)

# Generate transaction_header table
def generate_transaction_headers(customers_df):
    print("Generating transaction_header data...")
    
    transactions = []
    customer_ids = customers_df['customer_id'].tolist()
    
    for i in range(NUM_TRANSACTIONS):
        transaction_id = 58477061 + i
        transaction_date = START_DATE + timedelta(days=random.randint(0, (END_DATE - START_DATE).days))
        
        transactions.append({
            'transaction_id': transaction_id,
            'sales_module_transaction_id': 0,
            'transaction_source': 1,
            'tender_type': random.choice(['AMEX', 'VISA', 'MAST', 'DISC', 'CASH', 'CHECK', 'GIFT']),
            'store_no': random.choice([s[0] for s in STORES]),
            'customer_id': random.choice(customer_ids),
            'sales_associate_no': random.randint(10000, 99999),
            'transaction_type': random.choice(['S', 'S', 'S', 'R']),  # 75% sales, 25% returns
            'transaction_date': transaction_date.strftime('%d-%m-%Y %H:%M'),
            'pos_transaction_no': random.randint(10000, 99999),
            'register_no': random.randint(1, 10),
            'segmentation_flag_a': 0,
            'segmentation_flag_b': 0,
            'segmentation_flag_c': 0,
            'segmentation_flag_d': 0,
            'segmentation_flag_e': 0,
            'segmentation_flag_f': 0,
            'segmentation_flag_g': 0,
            'segmentation_flag_h': 0,
            'customer_no_flag': 1,
            'total_net_retail': round(random.uniform(50, 500), 2),
            'no_transaction_lines': random.randint(1, 5),
            'reward_points_flag': 1,
            'total_net_retail_central': 0,  # Will be same as total_net_retail
            'exchange_rate': 1,
            'currency_code': 'USD',
            'posted_date': (transaction_date + timedelta(days=1)).strftime('%d-%m-%Y %H:%M'),
            'transaction_time': transaction_date.strftime('%d-%m-%Y %H:%M'),
            'tender_amount_total': 0,  # Will be calculated
            'tender_amount_total_central': 0,
            'no_tender_lines': 1
        })
    
    df = pd.DataFrame(transactions)
    df['total_net_retail_central'] = df['total_net_retail']
    df['tender_amount_total'] = df['total_net_retail']
    df['tender_amount_total_central'] = df['total_net_retail']
    
    return df

# Generate transaction_detail table
def generate_transaction_details(transaction_headers_df):
    print("Generating transaction_detail data...")
    
    details = []
    
    for _, transaction in transaction_headers_df.iterrows():
        num_lines = transaction['no_transaction_lines']
        
        for line_no in range(1, num_lines + 1):
            unit_price = round(random.uniform(30, 150), 2)
            quantity = random.randint(1, 3)
            markdown_percent = random.choice([0, 0, 0, 10, 15, 20, 25, 30, 50])
            markdown_amount = round(unit_price * quantity * markdown_percent / 100, 2)
            net_retail = round(unit_price * quantity - markdown_amount, 2)
            cost = round(net_retail * random.uniform(0.4, 0.6), 2)
            
            details.append({
                'transaction_id': transaction['transaction_id'],
                'transaction_line_no': line_no,
                'sale_or_return_indicator': 'S' if transaction['transaction_type'] == 'S' else 'R',
                'sales_associate_no': transaction['sales_associate_no'],
                'style_id': random.randint(100000, 999999),
                'color_code': random.randint(1001, 9999),
                'size_description': random.choice(['38W30L', '40W32L', '42W30L', '44W32L', '46W30L', '48W32L', '50W34L', 
                                                   'XL', '2XL', '3XL', '4XL', '5XL', 'LT', 'XLT', '2XLT', '3XLT']),
                'quantity': quantity,
                'net_retail': net_retail,
                'cost': cost,
                'markdown_percent': markdown_percent,
                'comments': random.choice(['Regular purchase', 'Sale item', 'Clearance', 'Promotional', 'Standard']),
                'promotion_flag': 1 if markdown_percent > 0 else 0,
                'class_code': random.randint(1000000, 99999999),
                'net_retail_central': net_retail,
                'cost_central': cost,
                'markdown_amount': markdown_amount,
                'markdown_amount_central': markdown_amount
            })
    
    return pd.DataFrame(details)

# Generate reward_detail table
def generate_reward_details(transaction_headers_df):
    print("Generating reward_detail data...")
    
    rewards = []
    
    # Sample 30% of transactions for rewards
    reward_transactions = transaction_headers_df.sample(frac=0.3)
    
    for _, transaction in reward_transactions.iterrows():
        num_lines = random.randint(1, 3)
        
        for line_no in range(1, num_lines + 1):
            net_retail = round(random.uniform(50, 200), 2)
            regular_points = int(net_retail)  # 1 point per dollar
            bonus_points = random.choice([0, 0, 0, 10, 20, 50])
            
            rewards.append({
                'reward_transaction_id': transaction['transaction_id'],
                'line_no': line_no,
                'class_code': random.randint(100000000, 999999999),
                'style_id': random.randint(100000, 999999),
                'quantity': random.randint(1, 2),
                'net_retail': net_retail,
                'markdown_percent': random.choice([0, 10, 15, 20, 25]),
                'coupon_code': random.choice(['SAVE10', 'SAVE20', 'WELCOME', 'LOYALTY', 'SPRING25', 'NONE']),
                'regular_points': regular_points,
                'bonus_points': bonus_points,
                'net_retail_central': net_retail,
                'header_bonus_points': 0,
                'tender_bonus_points': 0,
                'return_flag': 0,
                'original_reward_tran_id': f"{random.randint(80000000, 89999999)}" if random.random() > 0.8 else 'NONE',
                'original_reward_line_no': str(random.randint(1, 5)) if random.random() > 0.8 else 'NONE',
                'returned_quantity': random.choice([0, 0, 0, 1]),
                'exchange_for_line_no': str(random.randint(1, 10)) if random.random() > 0.9 else 'NONE'
            })
    
    return pd.DataFrame(rewards)

# Generate household table
def generate_households(customers_df):
    print("Generating household data...")
    
    households = []
    num_households = len(customers_df) // 2  # Average 2 customers per household
    
    for i in range(num_households):
        households.append({
            'household_id': i + 1,
            'household_match_key': f"{random.randint(10000000, 99999999)}{random.choice(['HCBOX', 'POBOX', 'ADDR '])}{random.choice(['SMITH', 'JONES', 'BROWN', 'DAVIS'])}"
        })
    
    return pd.DataFrame(households)

# Main execution
if __name__ == "__main__":
    print("Starting Customer/CRM data generation...")
    print("=" * 60)
    
    # Generate all tables
    customers_df = generate_customers()
    addresses_df = generate_addresses(customers_df)
    emails_df = generate_emails(customers_df)
    stores_df = generate_stores()
    transaction_headers_df = generate_transaction_headers(customers_df)
    transaction_details_df = generate_transaction_details(transaction_headers_df)
    reward_details_df = generate_reward_details(transaction_headers_df)
    households_df = generate_households(customers_df)
    
    # Save to CSV
    print("\nSaving CSV files...")
    customers_df.to_csv('customer.csv', index=False, encoding='utf-8-sig')
    addresses_df.to_csv('address.csv', index=False, encoding='utf-8-sig')
    emails_df.to_csv('email.csv', index=False, encoding='utf-8-sig')
    stores_df.to_csv('store.csv', index=False, encoding='utf-8-sig')
    transaction_headers_df.to_csv('transaction_header.csv', index=False, encoding='utf-8-sig')
    transaction_details_df.to_csv('transaction_detail.csv', index=False, encoding='utf-8-sig')
    reward_details_df.to_csv('reward_detail.csv', index=False, encoding='utf-8-sig')
    households_df.to_csv('household.csv', index=False, encoding='utf-8-sig')
    
    print("\n" + "=" * 60)
    print("Customer/CRM Data Generation Complete!")
    print("=" * 60)
    print(f"[OK] customer.csv: {len(customers_df)} records")
    print(f"[OK] address.csv: {len(addresses_df)} records")
    print(f"[OK] email.csv: {len(emails_df)} records")
    print(f"[OK] store.csv: {len(stores_df)} records")
    print(f"[OK] transaction_header.csv: {len(transaction_headers_df)} records")
    print(f"[OK] transaction_detail.csv: {len(transaction_details_df)} records")
    print(f"[OK] reward_detail.csv: {len(reward_details_df)} records")
    print(f"[OK] household.csv: {len(households_df)} records")
    print("=" * 60)
