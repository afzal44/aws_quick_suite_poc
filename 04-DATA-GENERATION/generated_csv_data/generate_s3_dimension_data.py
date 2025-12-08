"""
Generate Dimensional/Reference Data for S3
These files complement Redshift data and provide lookup/reference information
"""

import pandas as pd
import json
import random
from datetime import datetime, timedelta

# Set random seed
random.seed(42)

# ============================================================================
# 1. PRODUCT CATALOG (JSON)
# ============================================================================
def generate_product_catalog():
    print("Generating product_catalog.json...")
    
    categories = {
        "Shirts": ["Dress Shirt", "Casual Shirt", "Polo Shirt", "T-Shirt", "Henley"],
        "Pants": ["Dress Pants", "Casual Pants", "Jeans", "Chinos", "Cargo Pants"],
        "Outerwear": ["Jacket", "Blazer", "Coat", "Vest", "Windbreaker"],
        "Footwear": ["Dress Shoes", "Casual Shoes", "Sneakers", "Boots", "Loafers"],
        "Accessories": ["Belt", "Tie", "Wallet", "Hat", "Socks"]
    }
    
    brands = ["Polo Ralph Lauren", "Tommy Hilfiger", "Calvin Klein", "Brooks Brothers", 
              "Nautica", "Levi's", "Dockers", "Nike", "Adidas", "Under Armour"]
    
    products = []
    product_id = 1000
    
    for category, subcategories in categories.items():
        for subcategory in subcategories:
            for brand in brands:
                for size in ["XL", "2XL", "3XL", "4XL", "5XL", "6XL"]:
                    products.append({
                        "product_id": product_id,
                        "sku": f"SKU{product_id}",
                        "product_name": f"{brand} {subcategory}",
                        "brand": brand,
                        "category": category,
                        "subcategory": subcategory,
                        "size": size,
                        "color": random.choice(["Navy", "Black", "White", "Grey", "Blue", "Khaki"]),
                        "price": round(random.uniform(29.99, 199.99), 2),
                        "cost": round(random.uniform(15.00, 100.00), 2),
                        "in_stock": random.choice([True, False]),
                        "stock_quantity": random.randint(0, 500),
                        "reorder_point": random.randint(10, 50),
                        "supplier": random.choice(["Supplier A", "Supplier B", "Supplier C"]),
                        "season": random.choice(["Spring", "Summer", "Fall", "Winter", "Year Round"]),
                        "material": random.choice(["Cotton", "Polyester", "Wool", "Blend", "Denim"]),
                        "care_instructions": "Machine wash cold, tumble dry low",
                        "country_of_origin": random.choice(["USA", "China", "Vietnam", "Bangladesh", "Mexico"]),
                        "last_updated": datetime.now().strftime("%Y-%m-%d")
                    })
                    product_id += 1
    
    with open('product_catalog.json', 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2)
    
    return len(products)

# ============================================================================
# 2. STORE LOCATIONS (CSV)
# ============================================================================
def generate_store_locations():
    print("Generating store_locations.csv...")
    
    stores = [
        {"store_id": 5011, "store_name": "DXL Store 5011", "city": "New York", "state": "NY", "region": "Northeast", "district": "Metro", "store_type": "Flagship", "square_footage": 15000, "opened_date": "2010-03-15"},
        {"store_id": 9330, "store_name": "DXL Store 9330", "city": "Los Angeles", "state": "CA", "region": "West", "district": "Pacific", "store_type": "Standard", "square_footage": 12000, "opened_date": "2012-06-20"},
        {"store_id": 9422, "store_name": "DXL Store 9422", "city": "Chicago", "state": "IL", "region": "Midwest", "district": "Central", "store_type": "Standard", "square_footage": 11000, "opened_date": "2013-09-10"},
        {"store_id": 9588, "store_name": "DXL Store 9588", "city": "Houston", "state": "TX", "region": "South", "district": "Southwest", "store_type": "Standard", "square_footage": 10500, "opened_date": "2014-02-28"},
        {"store_id": 9451, "store_name": "DXL Store 9451", "city": "Phoenix", "state": "AZ", "region": "West", "district": "Southwest", "store_type": "Standard", "square_footage": 9500, "opened_date": "2015-05-12"},
        {"store_id": 9851, "store_name": "DXL Store 9851", "city": "Philadelphia", "state": "PA", "region": "Northeast", "district": "Mid-Atlantic", "store_type": "Standard", "square_footage": 11500, "opened_date": "2016-08-22"},
        {"store_id": 9200, "store_name": "DXL Store 9200", "city": "San Antonio", "state": "TX", "region": "South", "district": "Southwest", "store_type": "Outlet", "square_footage": 8000, "opened_date": "2017-11-05"},
        {"store_id": 9100, "store_name": "DXL Store 9100", "city": "San Diego", "state": "CA", "region": "West", "district": "Pacific", "store_type": "Standard", "square_footage": 10000, "opened_date": "2018-01-18"},
        {"store_id": 9500, "store_name": "DXL Store 9500", "city": "Dallas", "state": "TX", "region": "South", "district": "Southwest", "store_type": "Flagship", "square_footage": 14000, "opened_date": "2019-04-30"},
        {"store_id": 9600, "store_name": "DXL Store 9600", "city": "Miami", "state": "FL", "region": "South", "district": "Southeast", "store_type": "Standard", "square_footage": 9000, "opened_date": "2020-07-15"},
    ]
    
    # Add additional details
    for store in stores:
        store["manager_name"] = random.choice(["John Smith", "Mary Johnson", "Robert Williams", "Patricia Brown", "Michael Jones"])
        store["phone"] = f"({random.randint(200, 999)}) {random.randint(200, 999)}-{random.randint(1000, 9999)}"
        store["email"] = f"store{store['store_id']}@dxl.com"
        store["has_fitmap"] = random.choice([True, True, True, False])  # 75% have FitMap
        store["parking_spaces"] = random.randint(50, 200)
        store["avg_daily_traffic"] = random.randint(100, 500)
        store["employee_count"] = random.randint(15, 50)
    
    df = pd.DataFrame(stores)
    df.to_csv('store_locations.csv', index=False, encoding='utf-8-sig')
    
    return len(stores)

# ============================================================================
# 3. SIZE CHART REFERENCE (CSV)
# ============================================================================
def generate_size_chart():
    print("Generating size_chart_reference.csv...")
    
    size_chart = []
    
    # Shirt sizes
    shirt_sizes = [
        {"category": "Shirts", "size": "XL", "chest_min": 46, "chest_max": 48, "waist_min": 40, "waist_max": 42, "neck": 17.5},
        {"category": "Shirts", "size": "2XL", "chest_min": 48, "chest_max": 50, "waist_min": 42, "waist_max": 44, "neck": 18},
        {"category": "Shirts", "size": "3XL", "chest_min": 50, "chest_max": 52, "waist_min": 44, "waist_max": 46, "neck": 18.5},
        {"category": "Shirts", "size": "4XL", "chest_min": 52, "chest_max": 54, "waist_min": 46, "waist_max": 48, "neck": 19},
        {"category": "Shirts", "size": "5XL", "chest_min": 54, "chest_max": 56, "waist_min": 48, "waist_max": 50, "neck": 19.5},
        {"category": "Shirts", "size": "6XL", "chest_min": 56, "chest_max": 58, "waist_min": 50, "waist_max": 52, "neck": 20},
    ]
    
    # Pants sizes
    for waist in range(38, 60, 2):
        for inseam in [28, 30, 32, 34, 36]:
            size_chart.append({
                "category": "Pants",
                "size": f"{waist}W{inseam}L",
                "waist_min": waist - 0.5,
                "waist_max": waist + 0.5,
                "inseam": inseam,
                "hip_min": waist + 8,
                "hip_max": waist + 10,
                "neck": None
            })
    
    size_chart.extend(shirt_sizes)
    
    df = pd.DataFrame(size_chart)
    df.to_csv('size_chart_reference.csv', index=False, encoding='utf-8-sig')
    
    return len(size_chart)

# ============================================================================
# 4. MARKETING CAMPAIGNS (JSON)
# ============================================================================
def generate_marketing_campaigns():
    print("Generating marketing_campaigns.json...")
    
    campaigns = [
        {
            "campaign_id": "SPRING2024",
            "campaign_name": "Spring Sale 2024",
            "start_date": "2024-03-01",
            "end_date": "2024-04-30",
            "discount_percent": 20,
            "budget": 50000,
            "target_audience": "All Customers",
            "channels": ["Email", "Social Media", "In-Store"],
            "utm_campaign": "spring_sale",
            "utm_medium": "email",
            "utm_source": "newsletter"
        },
        {
            "campaign_id": "SUMMER2024",
            "campaign_name": "Summer Clearance 2024",
            "start_date": "2024-06-01",
            "end_date": "2024-07-31",
            "discount_percent": 30,
            "budget": 75000,
            "target_audience": "Loyalty Members",
            "channels": ["Email", "SMS", "Social Media"],
            "utm_campaign": "summer_promo",
            "utm_medium": "social",
            "utm_source": "facebook"
        },
        {
            "campaign_id": "FALL2024",
            "campaign_name": "Fall Collection Launch",
            "start_date": "2024-09-01",
            "end_date": "2024-10-31",
            "discount_percent": 15,
            "budget": 60000,
            "target_audience": "New Customers",
            "channels": ["Google Ads", "Social Media", "In-Store"],
            "utm_campaign": "fall_clearance",
            "utm_medium": "cpc",
            "utm_source": "google"
        },
        {
            "campaign_id": "HOLIDAY2024",
            "campaign_name": "Holiday Sale 2024",
            "start_date": "2024-11-15",
            "end_date": "2024-12-31",
            "discount_percent": 25,
            "budget": 100000,
            "target_audience": "All Customers",
            "channels": ["Email", "Social Media", "TV", "In-Store"],
            "utm_campaign": "holiday_2024",
            "utm_medium": "email",
            "utm_source": "newsletter"
        },
        {
            "campaign_id": "BLACKFRI2024",
            "campaign_name": "Black Friday 2024",
            "start_date": "2024-11-29",
            "end_date": "2024-11-29",
            "discount_percent": 40,
            "budget": 150000,
            "target_audience": "All Customers",
            "channels": ["Email", "Social Media", "Google Ads", "In-Store"],
            "utm_campaign": "black_friday",
            "utm_medium": "email",
            "utm_source": "newsletter"
        }
    ]
    
    with open('marketing_campaigns.json', 'w', encoding='utf-8') as f:
        json.dump(campaigns, f, indent=2)
    
    return len(campaigns)

# ============================================================================
# 5. CUSTOMER SEGMENTS (CSV)
# ============================================================================
def generate_customer_segments():
    print("Generating customer_segments.csv...")
    
    segments = [
        {"segment_id": "VIP", "segment_name": "VIP Customers", "min_annual_spend": 5000, "min_transactions": 20, "benefits": "Free shipping, 20% discount, early access", "priority_level": 1},
        {"segment_id": "PREMIUM", "segment_name": "Premium Customers", "min_annual_spend": 2500, "min_transactions": 10, "benefits": "Free shipping, 15% discount", "priority_level": 2},
        {"segment_id": "STANDARD", "segment_name": "Standard Customers", "min_annual_spend": 1000, "min_transactions": 5, "benefits": "10% discount on select items", "priority_level": 3},
        {"segment_id": "BASIC", "segment_name": "Basic Customers", "min_annual_spend": 0, "min_transactions": 1, "benefits": "Standard pricing", "priority_level": 4},
        {"segment_id": "GOLD", "segment_name": "Gold Members", "min_annual_spend": 3500, "min_transactions": 15, "benefits": "Free shipping, 18% discount, birthday gift", "priority_level": 2},
    ]
    
    df = pd.DataFrame(segments)
    df.to_csv('customer_segments.csv', index=False, encoding='utf-8-sig')
    
    return len(segments)

# ============================================================================
# 6. BRAND INFORMATION (JSON)
# ============================================================================
def generate_brand_info():
    print("Generating brand_information.json...")
    
    brands = [
        {"brand_id": "POLO", "brand_name": "Polo Ralph Lauren", "category": "Premium", "country": "USA", "year_founded": 1967, "website": "www.ralphlauren.com", "price_range": "High"},
        {"brand_id": "TOMMY", "brand_name": "Tommy Hilfiger", "category": "Premium", "country": "USA", "year_founded": 1985, "website": "www.tommy.com", "price_range": "Medium-High"},
        {"brand_id": "CALVIN", "brand_name": "Calvin Klein", "category": "Premium", "country": "USA", "year_founded": 1968, "website": "www.calvinklein.com", "price_range": "Medium-High"},
        {"brand_id": "BROOKS", "brand_name": "Brooks Brothers", "category": "Premium", "country": "USA", "year_founded": 1818, "website": "www.brooksbrothers.com", "price_range": "High"},
        {"brand_id": "NAUTICA", "brand_name": "Nautica", "category": "Mid-Range", "country": "USA", "year_founded": 1983, "website": "www.nautica.com", "price_range": "Medium"},
        {"brand_id": "LEVIS", "brand_name": "Levi's", "category": "Mid-Range", "country": "USA", "year_founded": 1853, "website": "www.levis.com", "price_range": "Medium"},
        {"brand_id": "DOCKERS", "brand_name": "Dockers", "category": "Mid-Range", "country": "USA", "year_founded": 1986, "website": "www.dockers.com", "price_range": "Medium"},
        {"brand_id": "NIKE", "brand_name": "Nike", "category": "Athletic", "country": "USA", "year_founded": 1964, "website": "www.nike.com", "price_range": "Medium-High"},
        {"brand_id": "ADIDAS", "brand_name": "Adidas", "category": "Athletic", "country": "Germany", "year_founded": 1949, "website": "www.adidas.com", "price_range": "Medium-High"},
        {"brand_id": "UNDERARMOUR", "brand_name": "Under Armour", "category": "Athletic", "country": "USA", "year_founded": 1996, "website": "www.underarmour.com", "price_range": "Medium"},
    ]
    
    with open('brand_information.json', 'w', encoding='utf-8') as f:
        json.dump(brands, f, indent=2)
    
    return len(brands)

# ============================================================================
# 7. SHIPPING ZONES (CSV)
# ============================================================================
def generate_shipping_zones():
    print("Generating shipping_zones.csv...")
    
    zones = []
    states = {
        "Zone 1": ["NY", "NJ", "PA", "CT", "MA", "RI", "VT", "NH", "ME"],
        "Zone 2": ["OH", "MI", "IN", "IL", "WI", "MN", "IA", "MO"],
        "Zone 3": ["TX", "OK", "AR", "LA", "MS", "AL", "TN", "KY"],
        "Zone 4": ["CA", "OR", "WA", "NV", "AZ", "UT", "ID", "MT"],
        "Zone 5": ["FL", "GA", "SC", "NC", "VA", "WV", "MD", "DE"],
        "Zone 6": ["CO", "NM", "WY", "ND", "SD", "NE", "KS"],
        "Zone 7": ["AK", "HI"]
    }
    
    for zone, state_list in states.items():
        for state in state_list:
            zones.append({
                "zone": zone,
                "state": state,
                "standard_shipping_days": random.randint(3, 7),
                "express_shipping_days": random.randint(1, 2),
                "standard_cost": round(random.uniform(5.99, 12.99), 2),
                "express_cost": round(random.uniform(15.99, 29.99), 2),
                "free_shipping_threshold": 75.00
            })
    
    df = pd.DataFrame(zones)
    df.to_csv('shipping_zones.csv', index=False, encoding='utf-8-sig')
    
    return len(zones)

# ============================================================================
# 8. FITMAP DEVICE SPECIFICATIONS (JSON)
# ============================================================================
def generate_fitmap_devices():
    print("Generating fitmap_device_specs.json...")
    
    devices = [
        {
            "device_id": "iPad14,5",
            "device_name": "iPad Pro 11-inch (4th generation)",
            "manufacturer": "Apple",
            "os": "iOS",
            "camera_resolution": "12MP",
            "scan_accuracy": "98%",
            "recommended": True,
            "deployment_date": "2022-10-18"
        },
        {
            "device_id": "iPad13,8",
            "device_name": "iPad Pro 12.9-inch (5th generation)",
            "manufacturer": "Apple",
            "os": "iOS",
            "camera_resolution": "12MP",
            "scan_accuracy": "99%",
            "recommended": True,
            "deployment_date": "2021-05-21"
        },
        {
            "device_id": "iPhone14,2",
            "device_name": "iPhone 13 Pro",
            "manufacturer": "Apple",
            "os": "iOS",
            "camera_resolution": "12MP",
            "scan_accuracy": "95%",
            "recommended": False,
            "deployment_date": "2021-09-24"
        },
        {
            "device_id": "Android Tablet",
            "device_name": "Samsung Galaxy Tab S8",
            "manufacturer": "Samsung",
            "os": "Android",
            "camera_resolution": "13MP",
            "scan_accuracy": "96%",
            "recommended": True,
            "deployment_date": "2022-02-25"
        }
    ]
    
    with open('fitmap_device_specs.json', 'w', encoding='utf-8') as f:
        json.dump(devices, f, indent=2)
    
    return len(devices)

# ============================================================================
# MAIN EXECUTION
# ============================================================================
if __name__ == "__main__":
    print("\n" + "="*70)
    print("GENERATING S3 DIMENSIONAL DATA")
    print("="*70)
    
    results = {}
    
    results['product_catalog.json'] = generate_product_catalog()
    results['store_locations.csv'] = generate_store_locations()
    results['size_chart_reference.csv'] = generate_size_chart()
    results['marketing_campaigns.json'] = generate_marketing_campaigns()
    results['customer_segments.csv'] = generate_customer_segments()
    results['brand_information.json'] = generate_brand_info()
    results['shipping_zones.csv'] = generate_shipping_zones()
    results['fitmap_device_specs.json'] = generate_fitmap_devices()
    
    print("\n" + "="*70)
    print("S3 DIMENSIONAL DATA GENERATION COMPLETE")
    print("="*70)
    
    for filename, count in results.items():
        print(f"[OK] {filename}: {count} records")
    
    print("="*70)
    print(f"\nTotal files: {len(results)}")
    print("\nThese files can be uploaded to S3 and used as reference data")
    print("in AWS Quick Suite alongside your Redshift data.")
    print("="*70 + "\n")
