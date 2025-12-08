"""
Generate Order/E-commerce Sample Data for AWS Quick Suite POC
Generates realistic online order data
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import uuid
import json
import random

# Set random seed
np.random.seed(42)
random.seed(42)

# Configuration
NUM_ORDERS = 3000
START_DATE = datetime(2020, 1, 1)
END_DATE = datetime(2025, 12, 5)

# Product catalog
PRODUCTS = [
    {'itemid': 1009608, 'brand': 'DEERSTAGS', 'description': 'Deer Stags Sailor Slip-Ons', 'dept': 'Footwear', 'price': 49.50},
    {'itemid': 775376, 'brand': 'POLO', 'description': 'Polo Ralph Lauren Dress Shirt', 'dept': 'Dress Shirts', 'price': 98.00},
    {'itemid': 676596, 'brand': 'LEVIS', 'description': 'Levi\'s 501 Original Fit Jeans', 'dept': 'Denim', 'price': 69.50},
    {'itemid': 1222483, 'brand': 'NAUTICA', 'description': 'Nautica Casual Pants', 'dept': 'Casual Pants', 'price': 79.00},
    {'itemid': 1222647, 'brand': 'TOMMY', 'description': 'Tommy Hilfiger Polo Shirt', 'dept': 'Casual Shirts', 'price': 59.50},
    {'itemid': 800123, 'brand': 'CALVIN', 'description': 'Calvin Klein Dress Pants', 'dept': 'Dress Pants', 'price': 89.00},
    {'itemid': 800456, 'brand': 'BROOKS', 'description': 'Brooks Brothers Sport Coat', 'dept': 'Outerwear', 'price': 249.00},
    {'itemid': 900789, 'brand': 'DOCKERS', 'description': 'Dockers Khaki Pants', 'dept': 'Casual Pants', 'price': 54.50},
    {'itemid': 901234, 'brand': 'NIKE', 'description': 'Nike Athletic Shorts', 'dept': 'Activewear', 'price': 39.99},
    {'itemid': 902345, 'brand': 'ADIDAS', 'description': 'Adidas Track Jacket', 'dept': 'Activewear', 'price': 74.99}
]

SIZES = ['XL', '2XL', '3XL', '4XL', '5XL', '6XL', 'LT', 'XLT', '2XLT', '3XLT', 
         '38W30L', '40W30L', '42W32L', '44W32L', '46W34L', '48W34L', '50W36L', '110 W', '120 W', '130 W']

COLORS = ['Navy', 'Black', 'Khaki', 'Grey', 'Blue', 'White', 'Brown', 'Olive', 'Burgundy', 'Charcoal']

# Generate orderheader table
def generate_order_headers():
    print("Generating orderheader data...")
    
    orders = []
    
    for i in range(NUM_ORDERS):
        order_id = 122000000 + i
        created_timestamp = START_DATE + timedelta(days=random.randint(0, (END_DATE - START_DATE).days))
        
        is_cancelled = random.choice([True, False]) if random.random() > 0.95 else False
        fulfillment_status_id = random.choice([3000, 3000, 3000, 2000, 4000, 5000])
        
        orders.append({
            'orderid': order_id,
            'createdtimestamp': created_timestamp.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3],
            'iscancelled': is_cancelled,
            'isconfirmed': not is_cancelled,
            'maxfulfillmentstatusid': fulfillment_status_id,
            'minfulfillmentstatusid': fulfillment_status_id,
            'ordertypeid': random.choice(['WEB', 'MOBILE', 'PHONE', 'STORE']),
            'orgid': 'dxlg-us',
            'sellinglocationid': f"LOC{random.randint(1000, 9999)}",
            'messageid': str(uuid.uuid4()),
            'utmcampaign': random.choice(['spring_sale', 'summer_promo', 'fall_clearance', 'holiday_2024', 'black_friday', 'cyber_monday', 'new_year']),
            'utmmedium': random.choice(['email', 'social', 'cpc', 'organic', 'direct', 'referral']),
            'utmsource': random.choice(['google', 'facebook', 'instagram', 'newsletter', 'bing', 'twitter', 'affiliate']),
            'customeremail': f"customer{random.randint(1000, 9999)}@email.com",
            'fulfillmentstatus': random.choice(['Fulfilled', 'Fulfilled', 'Fulfilled', 'Pending', 'Shipped', 'Processing', 'Cancelled']),
            'alternateorderid': f"ALT{random.randint(100000, 999999)}",
            'order_source': random.choice(['WEBSITE', 'MOBILE_APP', 'CALL_CENTER', 'IN_STORE']),
            'payment_method': random.choice(['CREDIT_CARD', 'DEBIT_CARD', 'PAYPAL', 'GIFT_CARD', 'APPLE_PAY']),
            'shipping_method': random.choice(['STANDARD', 'EXPRESS', 'OVERNIGHT', 'PICKUP', 'SAME_DAY']),
            'customer_type': random.choice(['NEW', 'RETURNING', 'VIP', 'LOYALTY']),
            'device_type': random.choice(['DESKTOP', 'MOBILE', 'TABLET', 'APP']),
            'browser': random.choice(['Chrome', 'Safari', 'Firefox', 'Edge', 'Mobile Safari'])
        })
    
    return pd.DataFrame(orders)

# Generate orderline table
def generate_order_lines(order_headers_df):
    print("Generating orderline data...")
    
    order_lines = []
    
    for _, order in order_headers_df.iterrows():
        num_lines = random.randint(1, 4)  # 1-4 items per order
        
        for line_no in range(1, num_lines + 1):
            product = random.choice(PRODUCTS)
            quantity = random.randint(1, 3)
            unit_price = product['price']
            discount = round(unit_price * random.choice([0, 0, 0, 0.1, 0.15, 0.2, 0.25]), 2)
            subtotal = round(unit_price * quantity, 2)
            total = round(subtotal - (discount * quantity), 2)
            
            order_lines.append({
                'orderlineid': line_no,
                'orderid': order['orderid'],
                'itemid': product['itemid'],
                'cancelledtotaldiscounts': round(discount * quantity, 2) if order['iscancelled'] else 0,
                'maxappeasementamount': round(random.uniform(0, 50), 2),
                'orderlinesubtotal': subtotal,
                'orderlinetotal': total,
                'quantity': quantity,
                'refundprice': total if order['iscancelled'] else 0,
                'returnlinetotalwithoutfees': total if order['iscancelled'] else 0,
                'returnablelinetotal': total,
                'returnablequantity': 0 if not order['iscancelled'] else quantity,
                'taxoverridevalue': round(random.uniform(0, 5), 2),
                'taxableamount': total,
                'totalcharges': round(random.uniform(5, 15), 2),
                'totaldiscountonitem': round(discount * quantity, 2),
                'totaldiscounts': round(discount * quantity, 2),
                'totaltaxes': round(total * 0.08, 2),
                'unitprice': unit_price,
                'messageid': str(uuid.uuid4()),
                'maxfulfillmentstatusid': order['maxfulfillmentstatusid'],
                'minfulfillmentstatusid': order['minfulfillmentstatusid'],
                'fulfillmentstatus': order['fulfillmentstatus'],
                'isonhold': random.choice([True, False]),
                'isreturn': order['iscancelled'],
                'isevenexchange': random.choice([True, False]) if random.random() > 0.9 else False,
                'iscancelled': order['iscancelled'],
                'parentorderlineid': f"{random.randint(1, 1000)}" if random.random() > 0.95 else 'NONE',
                'parentorderid': f"{random.randint(100000000, 199999999)}" if random.random() > 0.95 else 'NONE',
                'createdtimestamp': order['createdtimestamp'],
                'orderline_pk': f"{random.randint(6000000000000000000, 6999999999999999999)}"
            })
    
    return pd.DataFrame(order_lines)

# Generate orderline_items table
def generate_order_line_items():
    print("Generating orderline_items data...")
    
    items = []
    
    for product in PRODUCTS:
        # Generate multiple size/color variants
        for _ in range(random.randint(3, 8)):
            items.append({
                'itemid': product['itemid'],
                'itembarcode': f"{product['itemid']}{random.randint(1000, 9999)}",
                'itembrand': product['brand'],
                'itemcolordescription': random.choice(COLORS),
                'itemdepartmentname': product['dept'],
                'itemdepartmentnumber': '',
                'itemdescription': product['description'],
                'itemseason': random.choice(['Spring', 'Summer', 'Fall', 'Winter', 'Year Round']),
                'itemsize': random.choice(SIZES),
                'itemstyle': f"M{random.randint(1000, 9999)}",
                'itemtaxcode': 'A_CLTH_GEN',
                'originalunitprice': product['price'],
                'itemshortdescription': product['description']
            })
    
    return pd.DataFrame(items)

# Generate orderchargedetail table
def generate_order_charge_details(order_headers_df):
    print("Generating orderchargedetail data...")
    
    charges = []
    
    for _, order in order_headers_df.iterrows():
        # Shipping charge
        shipping_cost = random.choice([0, 0, 5.99, 7.99, 10.00, 12.99])  # Free shipping often
        
        charges.append({
            'orderid': order['orderid'],
            'taxcode': 'Shipping',
            'chargetotal': shipping_cost,
            'istaxincluded': False,
            'isoverridden': False,
            'originalchargeamount': shipping_cost,
            'isinformational': False,
            'isprorated': True,
            'fulfillmentgroupid': f"FG{random.randint(1000, 9999)}",
            'isorderdiscount': False,
            'isreturncharge': False,
            'isproratedatsamelevel': False,
            'chargetypeid': 'Shipping',
            'chargedisplayname': 'Shipping'
        })
    
    return pd.DataFrame(charges)

# Generate invoice table
def generate_invoices(order_headers_df):
    print("Generating invoice data...")
    
    invoices = []
    
    for _, order in order_headers_df.iterrows():
        if random.random() > 0.1:  # 90% of orders have invoices
            invoice_id = order['orderid'] + 1000000
            
            invoice_total = round(random.uniform(50, 500), 2)
            invoice_date = datetime.strptime(order['createdtimestamp'], '%Y-%m-%dT%H:%M:%S.%f')
            
            invoices.append({
                'invoiceid': invoice_id,
                'invoice_pk': f"{random.randint(6000000000000000000, 6999999999999999999)}",
                'orderid': order['orderid'],
                'orderpk': f"{random.randint(6000000000000000000, 6999999999999999999)}",
                'createdtimestamp': order['createdtimestamp'],
                'cleanuptaskid': f"TASK{random.randint(1000, 9999)}",
                'errordescription': random.choice(['NONE', 'SUCCESS', 'COMPLETED']),
                'iserror': False,
                'publishcount': random.randint(1, 3),
                'process': random.choice(['COMPLETED', 'PROCESSED', 'FINALIZED']),
                'failedamount': 0,
                'fulfillmentdate': (invoice_date + timedelta(days=random.randint(1, 5))).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3],
                'sellinglocationid': order['sellinglocationid'],
                'updatedby': f"user{random.randint(1000, 9999)}@dxlg.com",
                'amountprocessed': invoice_total,
                'totalcharges': round(random.uniform(5, 15), 2),
                'invoicesubtotal': round(invoice_total * 0.92, 2),
                'parentorderid': f"{random.randint(100000000, 199999999)}" if random.random() > 0.95 else 'NONE',
                'taxexemptid': random.choice(['NONE', 'TAX001', 'TAX002']),
                'totaltaxes': round(invoice_total * 0.08, 2),
                'totaldiscounts': round(invoice_total * 0.05, 2),
                'publishstatusid': random.choice([1000, 2000, 3000]),
                'statusid': random.choice([100, 200, 300]),
                'updatedtimestamp': (invoice_date + timedelta(hours=random.randint(1, 24))).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3],
                'createdby': f"system@dxlg.com",
                'invoicetypeid': random.choice(['STANDARD', 'CREDIT', 'DEBIT']),
                'customerid': f"CUST{random.randint(10000, 99999)}",
                'orgid': order['orgid'],
                'contextid': str(uuid.uuid4()),
                'packageid': f"PKG{random.randint(10000, 99999)}",
                'invoicetotal': invoice_total,
                'unique_identifier': str(uuid.uuid4()),
                'invoiceadditional': json.dumps({"notes": "Standard invoice", "type": "retail"}),
                'messageid': order['messageid'],
                'load_date': datetime.now().strftime('%Y-%m-%d'),
                'update_date': datetime.now().strftime('%Y-%m-%d')
            })
    
    return pd.DataFrame(invoices)

# Generate payment table
def generate_payments(order_headers_df):
    print("Generating payment data...")
    
    payments = []
    
    for _, order in order_headers_df.iterrows():
        if not order['iscancelled']:
            payment_date = datetime.strptime(order['createdtimestamp'], '%Y-%m-%dT%H:%M:%S.%f')
            
            payments.append({
                'payment_pk': f"{random.randint(6000000000000000000, 6999999999999999999)}",
                'orderid': order['orderid'],
                'orderpk': f"{random.randint(6000000000000000000, 6999999999999999999)}",
                'createdby': order['customeremail'],
                'createdtimestamp': order['createdtimestamp'],
                'updatedby': f"system@dxlg.com",
                'updatedtimestamp': (payment_date + timedelta(minutes=random.randint(1, 60))).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3],
                'messages': json.dumps({"status": "success", "message": "Payment processed"}),
                'orgid': order['orgid'],
                'paymentgroupid': str(uuid.uuid4()),
                'customerid': f"CUST{random.randint(10000, 99999)}",
                'iscancelled': order['iscancelled'],
                'statusid': random.choice([1000, 2000, 3000]),
                'messageid': order['messageid'],
                'load_date': datetime.now().strftime('%Y-%m-%d'),
                'update_date': datetime.now().strftime('%Y-%m-%d')
            })
    
    return pd.DataFrame(payments)

# Generate quantitydetail table
def generate_quantity_details(order_lines_df):
    print("Generating quantitydetail data...")
    
    quantity_details = []
    
    for _, line in order_lines_df.iterrows():
        quantity_details.append({
            'quantitydetail_pk': f"{random.randint(6000000000000000000, 6999999999999999999)}",
            'quantitydetailid': f"{random.randint(6000000000000000000, 6999999999999999999)}",
            'orderid': line['orderid'],
            'orderline_pk': f"{random.randint(6000000000000000000, 6999999999999999999)}",
            'statusid': random.choice([1000, 2000, 3000, 3600]),
            'updatedtimestamp': datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3],
            'createdby': 'Ability_API@dxlg.com',
            'createdtimestamp': datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3],
            'quantity': line['quantity'],
            'itemid': line['itemid'],
            'orgid': 'dxlg-us',
            'updatedby': 'Ability_API@dxlg.com',
            'uom': 'EA',
            'contextid': str(uuid.uuid4()),
            'messageid': str(uuid.uuid4()),
            'load_date': datetime.now().strftime('%d:%M.%S'),
            'update_date': datetime.now().strftime('%d:%M.%S')
        })
    
    return pd.DataFrame(quantity_details)

# Main execution
if __name__ == "__main__":
    print("Starting Order/E-commerce data generation...")
    print("=" * 60)
    
    # Generate all tables
    order_headers_df = generate_order_headers()
    order_lines_df = generate_order_lines(order_headers_df)
    order_line_items_df = generate_order_line_items()
    order_charge_details_df = generate_order_charge_details(order_headers_df)
    invoices_df = generate_invoices(order_headers_df)
    payments_df = generate_payments(order_headers_df)
    quantity_details_df = generate_quantity_details(order_lines_df)
    
    # Save to CSV
    print("\nSaving CSV files...")
    order_headers_df.to_csv('orderheader.csv', index=False, encoding='utf-8-sig')
    order_lines_df.to_csv('orderline.csv', index=False, encoding='utf-8-sig')
    order_line_items_df.to_csv('orderline_items.csv', index=False, encoding='utf-8-sig')
    order_charge_details_df.to_csv('orderchargedetail.csv', index=False, encoding='utf-8-sig')
    invoices_df.to_csv('invoice.csv', index=False, encoding='utf-8-sig')
    payments_df.to_csv('payment.csv', index=False, encoding='utf-8-sig')
    quantity_details_df.to_csv('quantitydetail.csv', index=False, encoding='utf-8-sig')
    
    print("\n" + "=" * 60)
    print("Order/E-commerce Data Generation Complete!")
    print("=" * 60)
    print(f"[OK] orderheader.csv: {len(order_headers_df)} records")
    print(f"[OK] orderline.csv: {len(order_lines_df)} records")
    print(f"[OK] orderline_items.csv: {len(order_line_items_df)} records")
    print(f"[OK] orderchargedetail.csv: {len(order_charge_details_df)} records")
    print(f"[OK] invoice.csv: {len(invoices_df)} records")
    print(f"[OK] payment.csv: {len(payments_df)} records")
    print(f"[OK] quantitydetail.csv: {len(quantity_details_df)} records")
    print("=" * 60)
