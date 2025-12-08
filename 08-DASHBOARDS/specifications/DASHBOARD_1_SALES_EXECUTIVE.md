# Dashboard 1: DXL Sales Executive Dashboard

## Dashboard Overview
**Purpose**: Executive-level sales performance monitoring and strategic insights
**Target Audience**: C-Suite, VP Sales, Finance Leadership
**Refresh Rate**: Daily
**Data Sources**: Redshift (transaction_header, transaction_detail, orderheader, orderline), Athena (dimensional data)

---

## Layout Structure (Grid: 12 columns x 8 rows)

```
┌─────────────────────────────────────────────────────────────┐
│  DXL SALES EXECUTIVE DASHBOARD - 2024 PERFORMANCE          │
└─────────────────────────────────────────────────────────────┘
┌──────────┬──────────┬──────────┬──────────┬──────────┬──────┐
│  KPI 1   │  KPI 2   │  KPI 3   │  KPI 4   │  KPI 5   │ KPI 6│  ROW 1
├──────────┴──────────┴──────────┴──────────┴──────────┴──────┤
│                                                               │
│              Revenue Trend Chart                             │  ROW 2-3
│                                                               │
├───────────────────────┬───────────────────────────────────────┤
│                       │                                       │
│  Channel Mix          │   Customer Segmentation               │  ROW 4-5
│  (Pie Chart)          │   (Donut Chart)                       │
│                       │                                       │
├───────────────────────┴───────────────────────────────────────┤
│                                                               │
│              Top 10 Products Performance Table                │  ROW 6
│                                                               │
├──────────────────────────────┬────────────────────────────────┤
│                              │                                │
│  Store Performance Map       │  Campaign ROI Table            │  ROW 7-8
│                              │                                │
└──────────────────────────────┴────────────────────────────────┘
```

---

## Widget Details

### ROW 1: Key Performance Indicators (KPIs)

#### **KPI 1: Total Revenue**
- **Visualization Type**: KPI Card
- **Metric**: `SUM(total_net_retail)` from transaction_header
- **Comparison**: vs Last Year (YoY%)
- **Color Coding**: Green if >0%, Red if <0%
- **Format**: Currency ($2,456,789)
- **Data Source**: `transaction_header.total_net_retail` WHERE year = 2024
- **Filter**: Date range selector

**QuickSight Setup**:
```
Visual Type: KPI
Value: SUM(total_net_retail)
Comparison: {SUM(total_net_retail) - Previous Year} / Previous Year * 100
Format: Currency, 0 decimals
Conditional Formatting:
  - Green if Comparison > 0
  - Red if Comparison < 0
```

#### **KPI 2: Total Transactions**
- **Visualization Type**: KPI Card
- **Metric**: `COUNT(DISTINCT transaction_id)`
- **Comparison**: vs Last Month (MoM%)
- **Icon**: Shopping cart
- **Data Source**: `transaction_header.transaction_id`

**QuickSight Setup**:
```
Visual Type: KPI
Value: COUNT(DISTINCT transaction_id)
Comparison: MoM Change %
Format: Number with commas (15,234)
```

#### **KPI 3: Average Order Value (AOV)**
- **Visualization Type**: KPI Card
- **Metric**: `AVG(total_net_retail)`
- **Comparison**: vs Target ($350)
- **Data Source**: `transaction_header.total_net_retail`

**QuickSight Setup**:
```
Visual Type: KPI
Value: AVG(total_net_retail)
Comparison: vs Target ($350)
Format: Currency ($342.50)
Target Line: $350
```

#### **KPI 4: Gross Margin %**
- **Visualization Type**: KPI Card
- **Metric**: `(SUM(net_retail) - SUM(cost)) / SUM(net_retail) * 100`
- **Comparison**: vs Last Quarter
- **Data Source**: `transaction_detail.net_retail`, `transaction_detail.cost`

**QuickSight Setup**:
```
Visual Type: KPI
Calculated Field:
  (SUM(net_retail) - SUM(cost)) / SUM(net_retail) * 100
Format: Percentage (45.2%)
Conditional Formatting:
  - Green if > 40%
  - Yellow if 35-40%
  - Red if < 35%
```

#### **KPI 5: Conversion Rate**
- **Visualization Type**: KPI Card
- **Metric**: `(Confirmed Orders / Total Orders) * 100`
- **Comparison**: vs Industry Benchmark (65%)
- **Data Source**: `orderheader.isconfirmed`

**QuickSight Setup**:
```
Visual Type: KPI
Calculated Field:
  (COUNTIF(isconfirmed = TRUE) / COUNT(orderid)) * 100
Format: Percentage (72.3%)
Comparison: vs Benchmark (65%)
```

#### **KPI 6: Customer Lifetime Value (CLV)**
- **Visualization Type**: KPI Card
- **Metric**: `Total Revenue / Unique Customers`
- **Comparison**: vs Last Year
- **Data Source**: `transaction_header.total_net_retail`, `transaction_header.customer_id`

**QuickSight Setup**:
```
Visual Type: KPI
Calculated Field:
  SUM(total_net_retail) / COUNT(DISTINCT customer_id)
Format: Currency ($1,234)
```

---

### ROW 2-3: Revenue Trend Analysis

#### **Widget: Monthly Revenue Trend with Forecast**
- **Visualization Type**: Combo Chart (Line + Bar)
- **Primary Axis**: Monthly Revenue (Bar)
- **Secondary Axis**: Revenue Target (Line), Forecast (Dotted Line)
- **Dimensions**: `transaction_date` (Month)
- **Measures**:
  - `SUM(total_net_retail)` - Actual Revenue
  - `Target Revenue` - Static or from target table
  - `Forecast` - ML-powered forecast (QuickSight ML Insights)
- **Filters**: Year selector, Quarter selector

**QuickSight Setup**:
```
Visual Type: Combo Chart
X-axis: transaction_date (Month granularity)
Bars: SUM(total_net_retail)
Lines:
  - Target Revenue (dashed)
  - ML Forecast (dotted, enable ML Insights)
Colors:
  - Actual: Blue (#1565C0)
  - Target: Orange (#F57C00)
  - Forecast: Green (#2E7D32)
Show Data Labels: On bars
Legend: Top right
Add Annotations: Q4 Holiday Season, Summer Sale
```

**Additional Features**:
- Drill down: Month → Week → Day
- Tooltip: Show YoY comparison, variance from target
- Conditional formatting: Highlight months below target in red

---

### ROW 4-5: Channel & Customer Analysis

#### **Widget 1: Sales Channel Mix (Left Panel)**
- **Visualization Type**: Pie Chart or Donut Chart
- **Dimension**: `order_source` (IN_STORE, WEBSITE, MOBILE_APP, CALL_CENTER)
- **Measure**: `SUM(orderlinetotal)`
- **Data Source**: `orderheader.order_source`, `orderline.orderlinetotal`

**QuickSight Setup**:
```
Visual Type: Donut Chart
Slices: order_source
Values: SUM(orderlinetotal)
Colors: Custom palette
  - IN_STORE: #1565C0 (Blue)
  - WEBSITE: #2E7D32 (Green)
  - MOBILE_APP: #F57C00 (Orange)
  - CALL_CENTER: #C62828 (Red)
Show Percentages: Yes
Show Values: Yes (Currency format)
Legend: Right side
```

**Interaction**:
- Click slice to filter entire dashboard
- Tooltip shows: Revenue, % of total, transaction count

#### **Widget 2: Customer Segmentation (Right Panel)**
- **Visualization Type**: Donut Chart
- **Dimension**: `customer.segmentation_value_a` (VIP, GOLD, PREMIUM, STANDARD)
- **Measure**: `SUM(total_net_retail)`
- **Data Source**: JOIN `transaction_header.customer_id` with `customer.customer_id`

**QuickSight Setup**:
```
Visual Type: Donut Chart
Slices: segmentation_value_a
Values: SUM(total_net_retail)
Colors: Gradient (Gold theme)
  - VIP: #FFD700 (Gold)
  - GOLD: #DAA520 (Golden Rod)
  - PREMIUM: #C0C0C0 (Silver)
  - STANDARD: #CD7F32 (Bronze)
Show Percentages: Yes
Center Label: "Total Customers"
```

**Calculated Fields**:
```sql
-- Average Revenue per Segment
segmented_avg_revenue = SUM(total_net_retail) / COUNT(DISTINCT customer_id)
```

---

### ROW 6: Top Products Performance

#### **Widget: Top 10 Products/Sizes by Revenue**
- **Visualization Type**: Horizontal Bar Chart with embedded table
- **Dimensions**: `size_description`, `style_id`
- **Measures**:
  - `SUM(net_retail)` - Revenue
  - `SUM(quantity)` - Units Sold
  - `AVG(markdown_percent)` - Avg Discount
  - `Gross Margin %` - Calculated
- **Data Source**: `transaction_detail`
- **Sort**: Descending by Revenue
- **Limit**: Top 10

**QuickSight Setup**:
```
Visual Type: Pivot Table or Horizontal Bar Chart
Rows: size_description (e.g., "2XLT", "3XL", "48W32L")
Values:
  1. SUM(net_retail) - Format: Currency
  2. SUM(quantity) - Format: Number
  3. AVG(markdown_percent) - Format: Percentage
  4. Calculated: (net_retail - cost) / net_retail * 100
Sort: By Revenue (Descending)
Top N: 10
Conditional Formatting:
  - Revenue: Color scale (Green = High, Red = Low)
  - Margin: Red if < 30%, Yellow if 30-40%, Green if > 40%
```

**Alternative**: Heat Map
- Rows: Size categories
- Columns: Color codes
- Values: Revenue (color intensity)

---

### ROW 7-8: Geographic & Campaign Performance

#### **Widget 1: Store Performance Map (Left Panel)**
- **Visualization Type**: Geospatial Map (Points Map)
- **Dimension**: `store_no`, `store_locations` (lat/long)
- **Measures**:
  - `SUM(total_net_retail)` - Size of bubble
  - `COUNT(transaction_id)` - Color intensity
- **Data Source**: `transaction_header` JOIN `store_locations`

**QuickSight Setup**:
```
Visual Type: Points on Map
Geospatial Field:
  - Latitude: store_locations.latitude
  - Longitude: store_locations.longitude
Size: SUM(total_net_retail)
Color: COUNT(transaction_id) - Gradient scale
Tooltip:
  - Store Name
  - Total Revenue
  - Transaction Count
  - Avg Transaction Value
  - YoY Growth %
Legend: Show color scale
```

**Alternative if no lat/long**:
Use **Table** with mini sparklines:
```
Columns:
  - Store Name
  - Revenue (Bar)
  - Transactions (Number)
  - AOV (Currency)
  - Growth % (with up/down arrow)
```

#### **Widget 2: Marketing Campaign ROI (Right Panel)**
- **Visualization Type**: Table with conditional formatting
- **Dimensions**: `utmcampaign`, `utmsource`, `utmmedium`
- **Measures**:
  - Orders generated
  - Revenue
  - Estimated Cost (if available)
  - ROI %
  - Conversion Rate
- **Data Source**: `orderheader.utmcampaign`

**QuickSight Setup**:
```
Visual Type: Table
Rows: utmcampaign
Columns:
  1. Campaign Name (utmcampaign)
  2. Source (utmsource)
  3. Orders - COUNT(orderid)
  4. Revenue - SUM(orderlinetotal)
  5. Conversion % - (confirmed / total) * 100
  6. ROI % - Calculated (if cost data available)
Sort: By Revenue (Descending)
Conditional Formatting:
  - Conversion %: Green if > 70%, Red if < 50%
  - Revenue: Color scale
Top N: Top 8 campaigns
```

**Calculated Fields**:
```sql
campaign_conversion_rate =
  (COUNTIF(isconfirmed = TRUE) / COUNT(orderid)) * 100
```

---

## Filters & Parameters

### Global Filters (Apply to all widgets):
1. **Date Range**: Calendar picker (Default: Last 90 days)
2. **Store Type**: Dropdown (All, Physical Stores, E-Commerce)
3. **Customer Segment**: Multi-select (VIP, GOLD, PREMIUM, STANDARD, ALL)
4. **Order Status**: Multi-select (Fulfilled, Shipped, Cancelled, Pending)

### Parameter Controls:
1. **Target Revenue**: Numeric input (Default: $350)
2. **Year Selector**: Dropdown (2024, 2023, 2022)
3. **Comparison Period**: Dropdown (MoM, QoQ, YoY)

---

## QuickSight Setup Instructions

### Step 1: Prepare Data Sources
```sql
-- Create a unified sales dataset in Redshift or Athena
CREATE VIEW sales_dashboard_data AS
SELECT
    th.transaction_id,
    th.transaction_date,
    th.store_no,
    th.customer_id,
    th.tender_type,
    th.total_net_retail,
    td.style_id,
    td.size_description,
    td.quantity,
    td.net_retail,
    td.cost,
    td.markdown_percent,
    c.segmentation_value_a,
    c.segmentation_value_b,
    s.store_name,
    s.sales_channel_code
FROM transaction_header th
LEFT JOIN transaction_detail td ON th.transaction_id = td.transaction_id
LEFT JOIN customer c ON th.customer_id = c.customer_id
LEFT JOIN store s ON th.store_no = s.store_no
WHERE th.transaction_date >= '2023-01-01';

-- Create orders dataset
CREATE VIEW orders_dashboard_data AS
SELECT
    oh.orderid,
    oh.createdtimestamp,
    oh.order_source,
    oh.payment_method,
    oh.fulfillmentstatus,
    oh.utmcampaign,
    oh.utmsource,
    oh.utmmedium,
    oh.customer_type,
    oh.device_type,
    ol.orderlinetotal,
    ol.quantity
FROM orderheader oh
LEFT JOIN orderline ol ON oh.orderid = ol.orderid
WHERE oh.createdtimestamp >= '2023-01-01';
```

### Step 2: Create QuickSight Dataset
1. Go to QuickSight → Datasets → New Dataset
2. Select Data Source: **Redshift** or **Athena**
3. Import both views: `sales_dashboard_data`, `orders_dashboard_data`
4. Configure refresh schedule: **Daily at 6 AM**
5. Enable SPICE for faster performance

### Step 3: Create Calculated Fields
```
Revenue YoY % =
  (SUM(total_net_retail) - sumOver(SUM(total_net_retail), [{transaction_date} ASC], 1, 0)) /
  sumOver(SUM(total_net_retail), [{transaction_date} ASC], 1, 0) * 100

Gross Margin % =
  (SUM(net_retail) - SUM(cost)) / SUM(net_retail) * 100

AOV =
  SUM(total_net_retail) / COUNT(DISTINCT transaction_id)

Conversion Rate =
  (COUNTIF(isconfirmed = TRUE) / COUNT(orderid)) * 100
```

### Step 4: Build Dashboard
1. Create new Analysis → Name: "DXL Sales Executive Dashboard"
2. Add widgets in order listed above
3. Apply filters and parameters
4. Configure interactions (click-to-filter)
5. Publish as Dashboard

### Step 5: Share & Permissions
1. Publish Dashboard
2. Share with executive team
3. Set up email subscriptions (Weekly summary)
4. Enable mobile view optimization

---

## Expected Insights

### What This Dashboard Reveals:
1. **Revenue Performance**: Monthly trends, forecast accuracy, seasonal patterns
2. **Channel Effectiveness**: Which channels drive most revenue and profit
3. **Customer Value**: High-value segments, CLV trends, retention opportunities
4. **Product Insights**: Best sellers, markdown impact, inventory optimization
5. **Geographic Patterns**: Top-performing stores, regional trends
6. **Marketing ROI**: Campaign effectiveness, channel attribution

### Questions This Dashboard Answers:
- "How is 2024 revenue trending vs target and last year?"
- "Which sales channels are growing and which need attention?"
- "Which customer segments drive the most value?"
- "What are our top-selling sizes and products?"
- "Which stores are outperforming and underperforming?"
- "Which marketing campaigns have the best ROI?"
- "What's our average order value and conversion rate?"

---

## Next Steps

1. **Build in QuickSight**: Follow the widget specifications above
2. **Upload to Quick Suite**: Export dashboard image or embed URL
3. **Share with Quick Suite Chat**:
   ```
   "Analyze this sales executive dashboard. What are the top 3 insights
   and what actions should we take based on this data?"
   ```

---

**File Reference**: Use this as blueprint for AWS QuickSight dashboard creation
**Created**: December 2024
**For**: DXL AWS Quick Suite POC
