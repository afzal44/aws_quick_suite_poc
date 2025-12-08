# S3 Dimensional Data Guide

## 📊 Overview

This guide covers the **dimensional/reference data** stored in S3 that complements your Redshift transactional data. These files provide lookup tables, reference data, and metadata that enrich your Quick Suite analytics.

---

## 🗂️ Files Generated

### 1. **product_catalog.json** (~1,800 products)
**Purpose:** Complete product catalog with pricing, inventory, and specifications

**Structure:**
```json
{
  "product_id": 1000,
  "sku": "SKU1000",
  "product_name": "Polo Ralph Lauren Dress Shirt",
  "brand": "Polo Ralph Lauren",
  "category": "Shirts",
  "subcategory": "Dress Shirt",
  "size": "XL",
  "color": "Navy",
  "price": 89.99,
  "cost": 45.00,
  "in_stock": true,
  "stock_quantity": 250,
  "reorder_point": 25,
  "supplier": "Supplier A",
  "season": "Year Round",
  "material": "Cotton",
  "country_of_origin": "USA"
}
```

**Use Cases:**
- Product recommendations
- Inventory analysis
- Pricing strategies
- Supplier performance

---

### 2. **store_locations.csv** (10 stores)
**Purpose:** Store master data with location, capacity, and operational details

**Columns:**
- store_id, store_name, city, state, region, district
- store_type, square_footage, opened_date
- manager_name, phone, email
- has_fitmap, parking_spaces, avg_daily_traffic, employee_count

**Use Cases:**
- Store performance analysis
- Regional comparisons
- FitMap deployment tracking
- Store capacity planning

---

### 3. **size_chart_reference.csv** (~70 sizes)
**Purpose:** Standard size measurements for all product categories

**Columns:**
- category, size, chest_min, chest_max
- waist_min, waist_max, inseam, hip_min, hip_max, neck

**Use Cases:**
- Size recommendation validation
- FitMap measurement mapping
- Return rate analysis by size
- Inventory planning by size

---

### 4. **marketing_campaigns.json** (5 campaigns)
**Purpose:** Marketing campaign metadata and performance tracking

**Structure:**
```json
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
}
```

**Use Cases:**
- Campaign ROI analysis
- Attribution modeling
- Budget optimization
- Channel performance

---

### 5. **customer_segments.csv** (5 segments)
**Purpose:** Customer segmentation rules and benefits

**Columns:**
- segment_id, segment_name, min_annual_spend, min_transactions
- benefits, priority_level

**Use Cases:**
- Customer segmentation analysis
- Loyalty program tracking
- Personalized marketing
- Revenue by segment

---

### 6. **brand_information.json** (10 brands)
**Purpose:** Brand metadata and positioning

**Structure:**
```json
{
  "brand_id": "POLO",
  "brand_name": "Polo Ralph Lauren",
  "category": "Premium",
  "country": "USA",
  "year_founded": 1967,
  "website": "www.ralphlauren.com",
  "price_range": "High"
}
```

**Use Cases:**
- Brand performance analysis
- Price positioning
- Assortment planning
- Vendor negotiations

---

### 7. **shipping_zones.csv** (~60 zones)
**Purpose:** Shipping costs and delivery times by state

**Columns:**
- zone, state, standard_shipping_days, express_shipping_days
- standard_cost, express_cost, free_shipping_threshold

**Use Cases:**
- Shipping cost analysis
- Delivery time optimization
- Free shipping threshold analysis
- Regional logistics planning

---

### 8. **fitmap_device_specs.json** (4 devices)
**Purpose:** FitMap scanning device specifications

**Structure:**
```json
{
  "device_id": "iPad14,5",
  "device_name": "iPad Pro 11-inch (4th generation)",
  "manufacturer": "Apple",
  "os": "iOS",
  "camera_resolution": "12MP",
  "scan_accuracy": "98%",
  "recommended": true,
  "deployment_date": "2022-10-18"
}
```

**Use Cases:**
- Device performance tracking
- Scan quality analysis
- Device upgrade planning
- Store deployment strategy

---

## 🚀 Setup Instructions

### Step 1: Generate the Files

```bash
cd poc_data_generators
python generate_s3_dimension_data.py
```

**Output:** 8 files (4 JSON, 4 CSV)

---

### Step 2: Upload to S3

```powershell
cd poc_data_generators
.\upload_dimensions_to_s3.ps1
```

**S3 Structure:**
```
s3://dxl-quicksuite-poc-data/
  dimensions/
    products/product_catalog.json
    stores/store_locations.csv
    sizing/size_chart_reference.csv
    marketing/marketing_campaigns.json
    segments/customer_segments.csv
    brands/brand_information.json
    shipping/shipping_zones.csv
    devices/fitmap_device_specs.json
```

---

### Step 3: Configure Quick Suite

1. **Add S3 Data Source:**
   - Open Quick Suite console
   - Navigate to Quick Index
   - Click "Add Data Source"
   - Select "Amazon S3"
   - Connection name: `DXL_Dimensions_S3`
   - Bucket: `dxl-quicksuite-poc-data`
   - Prefix: `dimensions/`

2. **Index the Data:**
   - Quick Suite will automatically detect JSON and CSV files
   - Wait for indexing to complete

3. **Create a Space:**
   - Name: `Reference Data`
   - Add all S3 dimensional data sources
   - Add users

---

## 🔍 Sample Queries

### Query 1: Product Analysis with Brand Info
```
"Show me total sales by brand category"
```
**Joins:** Redshift transactions + S3 brand_information.json

---

### Query 2: Store Performance with Location Data
```
"Which stores in the West region have the highest sales?"
```
**Joins:** Redshift transactions + S3 store_locations.csv

---

### Query 3: Campaign Attribution
```
"What's the ROI for the Spring 2024 campaign?"
```
**Joins:** Redshift orders + S3 marketing_campaigns.json (via UTM codes)

---

### Query 4: Size Recommendation Accuracy
```
"Compare FitMap size recommendations against our size chart"
```
**Joins:** Redshift size_dxl_custom_measures + S3 size_chart_reference.csv

---

### Query 5: Shipping Cost Analysis
```
"What's the average shipping cost by zone?"
```
**Joins:** Redshift orders + S3 shipping_zones.csv

---

### Query 6: Customer Segmentation
```
"How many customers are in each segment?"
```
**Joins:** Redshift customer + transactions + S3 customer_segments.csv

---

### Query 7: FitMap Device Performance
```
"Which FitMap devices have the highest scan accuracy?"
```
**Joins:** Redshift size_scans + S3 fitmap_device_specs.json

---

### Query 8: Cross-Source Analytics
```
"Show me sales by brand, store region, and customer segment"
```
**Joins:** 
- Redshift: transactions, customers
- S3: brand_information.json, store_locations.csv, customer_segments.csv

---

## 📊 Data Relationships

### Redshift ↔ S3 Join Keys

| Redshift Table | S3 File | Join Key |
|----------------|---------|----------|
| transaction_detail | product_catalog.json | style_id → product_id |
| transaction_header | store_locations.csv | store_no → store_id |
| size_dxl_custom_measures | size_chart_reference.csv | producttype → category |
| orderheader | marketing_campaigns.json | utmcampaign → utm_campaign |
| customer | customer_segments.csv | (calculated) → segment_id |
| orderheader | shipping_zones.csv | (address state) → state |
| size_scans | fitmap_device_specs.json | app → device_id |
| transaction_detail | brand_information.json | (product brand) → brand_id |

---

## 🎯 Advanced Use Cases

### 1. **Dynamic Pricing Analysis**
Combine product catalog pricing with actual transaction prices to identify:
- Discount effectiveness
- Price elasticity
- Margin optimization opportunities

### 2. **Store Clustering**
Use store location data to:
- Group stores by performance
- Identify expansion opportunities
- Optimize inventory distribution

### 3. **Campaign Attribution**
Link marketing campaigns to:
- Order sources (UTM codes)
- Customer acquisition
- Revenue impact

### 4. **Size Recommendation Validation**
Compare FitMap recommendations against:
- Standard size charts
- Actual purchases
- Return rates

### 5. **Shipping Optimization**
Analyze shipping costs by:
- Zone
- Order value
- Delivery speed
- Free shipping threshold impact

---

## 🔧 Maintenance

### Updating Dimensional Data

1. **Modify the generator script:**
   ```python
   # Edit: generate_s3_dimension_data.py
   # Update data as needed
   ```

2. **Regenerate files:**
   ```bash
   python generate_s3_dimension_data.py
   ```

3. **Re-upload to S3:**
   ```powershell
   .\upload_dimensions_to_s3.ps1
   ```

4. **Refresh Quick Suite index:**
   - Quick Suite will automatically detect changes
   - Or manually trigger re-indexing

---

## 📈 Benefits of S3 Dimensional Data

### 1. **Separation of Concerns**
- Transactional data in Redshift (optimized for queries)
- Reference data in S3 (flexible, easy to update)

### 2. **Cost Efficiency**
- S3 storage is cheaper than Redshift
- No need to load reference data into warehouse

### 3. **Flexibility**
- Easy to add new reference files
- Support for JSON and CSV formats
- No schema changes required

### 4. **Quick Suite Integration**
- Seamless joins across Redshift and S3
- Natural language queries work across sources
- Single interface for all data

---

## ✅ Verification Checklist

- [ ] All 8 dimensional files generated
- [ ] Files uploaded to S3 dimensions/ folder
- [ ] S3 data source added to Quick Suite
- [ ] Quick Index completed indexing
- [ ] Reference Data space created
- [ ] Test queries executed successfully
- [ ] Cross-source joins working

---

## 🎓 Training Queries for Quick Suite

Use these to train Quick Suite on your dimensional data:

```
1. "List all brands in the premium category"
2. "Show me stores that have FitMap devices"
3. "What are the active marketing campaigns?"
4. "Which customer segments have the highest benefits?"
5. "Show me shipping costs for Zone 1"
6. "What sizes are available for dress shirts?"
7. "Which products are out of stock?"
8. "Show me store locations in the West region"
```

---

## 📞 Support

For questions about dimensional data:
- Review this guide
- Check S3 bucket structure
- Verify Quick Suite data source configuration
- Test with simple queries first

---

**Your S3 dimensional data is now ready to enrich your Quick Suite analytics!**

**Next Step:** Create queries that combine Redshift transactional data with S3 reference data for powerful cross-source insights.
