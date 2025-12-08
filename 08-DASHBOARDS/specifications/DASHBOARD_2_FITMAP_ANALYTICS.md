# Dashboard 2: DXL FitMap Analytics Dashboard

## Dashboard Overview
**Purpose**: FitMap body measurement analytics and personalized sizing insights
**Target Audience**: Merchandising, Product Development, Store Operations, Marketing
**Refresh Rate**: Real-time (or Daily)
**Data Sources**: Redshift (size_scans, size_users, size_core_measures, size_app_measures, size_dxl_custom_measures), Athena (dimensional data)

---

## Layout Structure (Grid: 12 columns x 8 rows)

```
┌─────────────────────────────────────────────────────────────┐
│  DXL FITMAP ANALYTICS DASHBOARD - BODY MEASUREMENT INSIGHTS │
└─────────────────────────────────────────────────────────────┘
┌──────────┬──────────┬──────────┬──────────┬──────────┬──────┐
│ Total    │ Active   │  Avg     │  Scan    │  Return  │ Fit  │  ROW 1
│ Scans    │ Users    │  Age     │  Rate    │  Rate    │ Score│
├──────────┴──────────┴──────────┴──────────┴──────────┴──────┤
│                                                               │
│         FitMap Scan Volume Trend (Line Chart)                │  ROW 2
│                                                               │
├──────────────────────┬────────────────────────────────────────┤
│                      │                                        │
│  Size Distribution   │   Body Type Distribution               │  ROW 3-4
│  (Histogram)         │   (Treemap)                            │
│                      │                                        │
├──────────────────────┴────────────────────────────────────────┤
│                                                               │
│  Age vs Body Measurements (Scatter Plot with Trend)          │  ROW 5
│                                                               │
├───────────────────────────────┬───────────────────────────────┤
│                               │                               │
│  Top Size Recommendations     │  Measurement Accuracy Heat Map│  ROW 6-7
│  (Table with % confidence)    │  (Chest, Waist, Inseam, etc.) │
│                               │                               │
├───────────────────────────────┴───────────────────────────────┤
│                                                               │
│  Customer Journey: Scan → Purchase → Return Flow (Sankey)    │  ROW 8
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

---

## Widget Details

### ROW 1: FitMap Key Metrics

#### **KPI 1: Total FitMap Scans**
- **Visualization Type**: KPI Card
- **Metric**: `COUNT(DISTINCT scan_id)` from size_scans
- **Comparison**: vs Last Month (MoM%)
- **Icon**: QR code or scanning icon
- **Data Source**: `size_scans.scan_id`

**QuickSight Setup**:
```
Visual Type: KPI
Value: COUNT(DISTINCT scan_id)
Comparison: MoM Change %
Format: Number with commas (12,456)
Conditional Formatting:
  - Green if growth > 10%
  - Yellow if growth 0-10%
  - Red if negative
```

#### **KPI 2: Active FitMap Users**
- **Visualization Type**: KPI Card
- **Metric**: `COUNT(DISTINCT user_id)` from size_users
- **Comparison**: vs Last Quarter
- **Filter**: Users with scan activity in last 90 days
- **Data Source**: `size_users.user_id` WHERE last_scan_date > TODAY() - 90

**QuickSight Setup**:
```
Visual Type: KPI
Value: COUNT(DISTINCT user_id) WHERE active = TRUE
Comparison: vs Last Quarter
Format: Number (8,234)
Show Trend: Mini sparkline
```

#### **KPI 3: Average Customer Age**
- **Visualization Type**: KPI Card
- **Metric**: `AVG(age)` from size_users
- **Comparison**: vs Industry average (45 years)
- **Data Source**: `size_users.age`

**QuickSight Setup**:
```
Visual Type: KPI
Value: AVG(age)
Format: Number (42.5 years)
Comparison: vs Industry Benchmark
Icon: User demographics
```

#### **KPI 4: Scan Completion Rate**
- **Visualization Type**: KPI Card
- **Metric**: `(Completed Scans / Total Scan Attempts) * 100`
- **Comparison**: vs Target (85%)
- **Data Source**: `size_scans.status` (COMPLETED vs STARTED)

**QuickSight Setup**:
```
Visual Type: KPI
Calculated Field:
  (COUNTIF(status = 'COMPLETED') / COUNT(scan_id)) * 100
Format: Percentage (87.3%)
Target: 85%
Conditional Formatting:
  - Green if > 85%
  - Red if < 75%
```

#### **KPI 5: Return Rate (FitMap Users)**
- **Visualization Type**: KPI Card
- **Metric**: `(Returns / Total Orders) * 100` for customers with FitMap scans
- **Comparison**: vs Non-FitMap customers
- **Data Source**: JOIN `orderline.isreturn` with `size_users.user_id`

**QuickSight Setup**:
```
Visual Type: KPI
Calculated Field:
  (COUNTIF(isreturn = TRUE) / COUNT(orderid)) * 100
  WHERE customer_id IN (SELECT user_id FROM size_users)
Format: Percentage (8.2%)
Comparison: vs Non-FitMap (15.4%)
Show Difference: -7.2% (in green)
```

#### **KPI 6: Average Fit Score**
- **Visualization Type**: KPI Card with gauge
- **Metric**: `AVG(fit_confidence_score)` - Calculated field
- **Comparison**: vs Target (90%)
- **Range**: 0-100%
- **Data Source**: Calculated from measurement accuracy

**QuickSight Setup**:
```
Visual Type: KPI (Gauge style)
Value: AVG(fit_confidence_score)
Format: Percentage (92.5%)
Gauge Ranges:
  - Red: 0-70% (Poor fit)
  - Yellow: 70-85% (Good fit)
  - Green: 85-100% (Excellent fit)
```

---

### ROW 2: Scan Volume Trend

#### **Widget: FitMap Scan Volume Over Time**
- **Visualization Type**: Area Chart or Line Chart
- **Dimension**: `scan_date` (Day/Week/Month granularity)
- **Measures**:
  - Total Scans
  - Unique Users
  - Scan Completion Rate
- **Data Source**: `size_scans.scan_date`
- **Time Range**: Last 12 months

**QuickSight Setup**:
```
Visual Type: Area Chart (stacked)
X-axis: scan_date (Month granularity)
Y-axis (Primary): COUNT(scan_id)
Y-axis (Secondary): COUNT(DISTINCT user_id)
Lines:
  1. Total Scans - Blue (#1565C0)
  2. Unique Users - Green (#2E7D32)
  3. Completion Rate - Orange (#F57C00) (Line only, no fill)
Show Data Labels: On peaks/valleys
Annotations:
  - "In-store FitMap launch" (specific date)
  - "Mobile app integration" (specific date)
Drill-down: Month → Week → Day
```

**Calculated Fields**:
```sql
scan_completion_rate =
  (COUNTIF(status = 'COMPLETED') / COUNT(scan_id)) * 100
```

---

### ROW 3-4: Size & Body Type Distribution

#### **Widget 1: Size Distribution (Left Panel)**
- **Visualization Type**: Histogram or Vertical Bar Chart
- **Dimension**: Size categories (S, M, L, XL, 2XL, 3XL, 4XL, 5XL, etc.)
- **Measure**: `COUNT(user_id)` or `COUNT(scan_id)`
- **Data Source**: `size_core_measures` (chest, waist measurements converted to size)

**QuickSight Setup**:
```
Visual Type: Vertical Bar Chart
X-axis: size_category (Ordered: XS, S, M, L, XL, 2XL, 3XL, 4XL, 5XL)
Y-axis: COUNT(DISTINCT user_id)
Colors: Gradient (Light to Dark Blue)
Show Percentages: On bars
Tooltip:
  - Size
  - Customer Count
  - % of Total
  - Avg Age for this size
  - Avg Revenue per customer
Sort: By size order (not alphabetical)
```

**Calculated Field - Size Category**:
```sql
size_category =
  CASE
    WHEN chest_circumference < 38 THEN 'S'
    WHEN chest_circumference BETWEEN 38 AND 42 THEN 'M'
    WHEN chest_circumference BETWEEN 42 AND 46 THEN 'L'
    WHEN chest_circumference BETWEEN 46 AND 50 THEN 'XL'
    WHEN chest_circumference BETWEEN 50 AND 54 THEN '2XL'
    WHEN chest_circumference BETWEEN 54 AND 58 THEN '3XL'
    WHEN chest_circumference BETWEEN 58 AND 62 THEN '4XL'
    ELSE '5XL+'
  END
```

#### **Widget 2: Body Type Distribution (Right Panel)**
- **Visualization Type**: Treemap
- **Dimension**: Body type segments (Athletic, Regular, Husky, Big & Tall, etc.)
- **Measure**: `COUNT(user_id)`, `AVG(revenue_per_customer)`
- **Data Source**: Calculated from `size_core_measures` and `size_dxl_custom_measures`

**QuickSight Setup**:
```
Visual Type: Treemap
Group by: body_type_segment
Size: COUNT(DISTINCT user_id)
Color: AVG(revenue_per_customer) - Gradient (Red to Green)
Tooltip:
  - Body Type
  - Customer Count
  - % of Total
  - Avg Revenue
  - Avg Order Frequency
  - Top Selling Category
Labels: Show count and percentage
```

**Calculated Field - Body Type Segment**:
```sql
body_type_segment =
  CASE
    WHEN height > 74 AND chest_circumference > 46 THEN 'Big & Tall'
    WHEN height > 74 AND chest_circumference <= 46 THEN 'Tall'
    WHEN chest_circumference > 50 THEN 'Big'
    WHEN (waist_circumference / chest_circumference) < 0.85 THEN 'Athletic'
    WHEN (waist_circumference / chest_circumference) > 0.95 THEN 'Husky'
    ELSE 'Regular'
  END
```

---

### ROW 5: Age vs Body Measurements

#### **Widget: Age vs Key Measurements Correlation**
- **Visualization Type**: Scatter Plot with trend lines
- **X-Axis**: Age (from size_users)
- **Y-Axis**: Chest Circumference, Waist Circumference (dual metrics)
- **Size**: Count of customers at that data point
- **Color**: Body type segment
- **Data Source**: `size_users.age` + `size_core_measures`

**QuickSight Setup**:
```
Visual Type: Scatter Plot
X-axis: age (binned in 5-year groups: 25-30, 30-35, etc.)
Y-axis: chest_circumference (Primary), waist_circumference (Secondary)
Bubble Size: COUNT(user_id)
Color: body_type_segment
Trend Lines:
  - Linear regression for chest (Blue)
  - Linear regression for waist (Red)
Tooltip:
  - Age Range
  - Avg Chest
  - Avg Waist
  - Customer Count
  - Recommended Size Range
Filters: Gender selector (Male/Female)
```

**Insights**:
- Shows how measurements change with age
- Identifies size trends by demographic
- Helps with inventory planning

---

### ROW 6-7: Size Recommendations & Measurement Accuracy

#### **Widget 1: Top Size Recommendations (Left Panel)**
- **Visualization Type**: Table with confidence scores
- **Dimensions**: Recommended Size, Body Type, Purchase Category
- **Measures**:
  - Count of recommendations
  - Confidence %
  - Purchase rate
  - Return rate
- **Data Source**: `size_scans` + historical orders

**QuickSight Setup**:
```
Visual Type: Table (Pivot Table)
Rows:
  1. recommended_size (e.g., "2XLT", "48W32L")
  2. product_category (Shirts, Pants, Suits)
Columns:
  1. Recommendations - COUNT(scan_id)
  2. Confidence % - AVG(confidence_score)
  3. Purchase Rate % - (Purchases / Recommendations) * 100
  4. Return Rate % - (Returns / Purchases) * 100
  5. Accuracy Score - Calculated
Sort: By Recommendations (Descending)
Conditional Formatting:
  - Confidence: Green if > 90%, Yellow 80-90%, Red < 80%
  - Return Rate: Red if > 10%, Green if < 5%
Top N: 15 size recommendations
```

**Calculated Fields**:
```sql
recommendation_accuracy =
  ((100 - return_rate) + confidence_score) / 2

purchase_conversion =
  (COUNT(orderid) / COUNT(scan_id)) * 100
  WHERE scan_id IS NOT NULL
```

#### **Widget 2: Measurement Accuracy Heat Map (Right Panel)**
- **Visualization Type**: Heat Map
- **Rows**: Measurement Types (Chest, Waist, Inseam, Sleeve, Neck, Shoulder)
- **Columns**: Accuracy Ranges (±0.5", ±1", ±2", >2")
- **Color**: Frequency (darker = more common)
- **Data Source**: `size_core_measures` vs actual product measurements

**QuickSight Setup**:
```
Visual Type: Heat Map
Rows: measurement_type
Columns: accuracy_bucket
  - ±0.5 inch (Excellent)
  - ±1 inch (Good)
  - ±2 inch (Fair)
  - >2 inch (Poor)
Values: COUNT(user_id)
Color Scale: Green (High accuracy) to Red (Low accuracy)
Tooltip:
  - Measurement Type
  - Accuracy Range
  - Count
  - % of Total
  - Avg Deviation
```

**Calculated Field - Accuracy Bucket**:
```sql
measurement_accuracy_bucket =
  CASE
    WHEN ABS(measured_value - actual_value) <= 0.5 THEN '±0.5"'
    WHEN ABS(measured_value - actual_value) <= 1 THEN '±1"'
    WHEN ABS(measured_value - actual_value) <= 2 THEN '±2"'
    ELSE '>2"'
  END
```

---

### ROW 8: Customer Journey Flow

#### **Widget: Scan → Purchase → Return Flow (Sankey Diagram)**
- **Visualization Type**: Sankey Diagram (Flow Chart)
- **Flow Stages**:
  1. FitMap Scan (Start)
  2. Recommendation Made
  3. Purchase (Yes/No)
  4. Kept / Returned
- **Measure**: Count of customers at each stage
- **Data Source**: `size_scans` → `orderheader` → `orderline.isreturn`

**QuickSight Setup**:
```
Visual Type: Sankey Diagram
Source → Target Flow:
  1. "FitMap Scan" → "Recommendation Made" (100%)
  2. "Recommendation Made" → "Purchased" (X%)
  3. "Recommendation Made" → "Did Not Purchase" (Y%)
  4. "Purchased" → "Kept Item" (Z%)
  5. "Purchased" → "Returned" (W%)

Colors:
  - Green: Positive flow (Scan → Purchase → Kept)
  - Red: Negative flow (Did Not Purchase, Returned)
  - Yellow: Neutral (Recommendation stage)

Show Values: On each flow (count and %)
Tooltip: Conversion rate at each stage
```

**Alternative: Funnel Chart**:
```
Visual Type: Funnel Chart
Stages:
  1. Total FitMap Scans - 100%
  2. Recommendations Generated - 95%
  3. Purchases Made - 68%
  4. Items Kept - 92%
  5. Repeat Purchases - 45%
Show Drop-off %: Between each stage
Colors: Blue gradient
```

**Calculated Field - Conversion Metrics**:
```sql
scan_to_purchase_rate =
  (COUNT(DISTINCT orderid) / COUNT(DISTINCT scan_id)) * 100
  WHERE customer_id IN (SELECT user_id FROM size_scans)

fitmap_return_rate =
  (COUNTIF(isreturn = TRUE) / COUNT(orderid)) * 100
  WHERE customer_id IN (SELECT user_id FROM size_scans)

non_fitmap_return_rate =
  (COUNTIF(isreturn = TRUE) / COUNT(orderid)) * 100
  WHERE customer_id NOT IN (SELECT user_id FROM size_scans)
```

---

## Additional Widgets (Optional - Add if Space Available)

### **Widget: FitMap vs Non-FitMap Comparison**
- **Visualization Type**: Side-by-side KPI cards or Table
- **Metrics**:
  - Average Order Value
  - Return Rate
  - Customer Satisfaction
  - Repeat Purchase Rate
- **Comparison**: FitMap users vs Non-FitMap users

**QuickSight Setup**:
```
Visual Type: Comparison Table
Rows:
  1. Average Order Value
  2. Return Rate
  3. Items per Order
  4. Repeat Purchase Rate
  5. Customer Lifetime Value
Columns:
  1. FitMap Users
  2. Non-FitMap Users
  3. Difference (%)
  4. Impact ($)
Conditional Formatting:
  - Green if FitMap is better
  - Red if FitMap is worse
```

### **Widget: Size Scan Location Heat Map**
- **Visualization Type**: Geographic Map (if location data available)
- **Dimension**: Store location
- **Measure**: Scan volume, conversion rate
- **Data Source**: `size_scans.location_id` + `store_locations`

---

## Filters & Parameters

### Global Filters:
1. **Date Range**: Last 12 months (default)
2. **Gender**: Male / Female / All
3. **Age Range**: Slider (18-80 years)
4. **Body Type**: Multi-select dropdown
5. **Scan Location**: Store / Mobile App / All
6. **Customer Segment**: VIP, GOLD, PREMIUM, STANDARD

### Parameter Controls:
1. **Target Return Rate**: 10% (benchmark)
2. **Minimum Confidence Score**: 85%
3. **Size Category Grouping**: Standard / Extended

---

## QuickSight Setup Instructions

### Step 1: Prepare FitMap Dataset
```sql
-- Create unified FitMap analytics view
CREATE VIEW fitmap_analytics AS
SELECT
    ss.scan_id,
    ss.user_id,
    ss.scan_date,
    ss.status,
    su.age,
    su.gender,
    su.height,
    scm.chest_circumference,
    scm.waist_circumference,
    scm.inseam,
    scm.neck_circumference,
    scm.sleeve_length,
    scm.shoulder_width,
    sdcm.shirt_size_recommendation,
    sdcm.pants_size_recommendation,
    sdcm.fit_confidence_score,
    o.orderid,
    o.createdtimestamp AS purchase_date,
    ol.isreturn,
    ol.orderlinetotal
FROM size_scans ss
LEFT JOIN size_users su ON ss.user_id = su.user_id
LEFT JOIN size_core_measures scm ON ss.scan_id = scm.scan_id
LEFT JOIN size_dxl_custom_measures sdcm ON ss.scan_id = sdcm.scan_id
LEFT JOIN orderheader o ON ss.user_id = o.customerid
    AND o.createdtimestamp >= ss.scan_date
    AND o.createdtimestamp <= ss.scan_date + INTERVAL '30 days'
LEFT JOIN orderline ol ON o.orderid = ol.orderid;
```

### Step 2: Create Calculated Fields
```sql
-- Body Type Segmentation
body_type =
  CASE
    WHEN height > 74 AND chest_circumference > 46 THEN 'Big & Tall'
    WHEN height > 74 THEN 'Tall'
    WHEN chest_circumference > 50 THEN 'Big'
    WHEN (waist_circumference / chest_circumference) < 0.85 THEN 'Athletic'
    WHEN (waist_circumference / chest_circumference) > 0.95 THEN 'Husky'
    ELSE 'Regular'
  END

-- Size Category
size_category =
  CASE
    WHEN chest_circumference < 38 THEN 'S'
    WHEN chest_circumference BETWEEN 38 AND 42 THEN 'M'
    WHEN chest_circumference BETWEEN 42 AND 46 THEN 'L'
    WHEN chest_circumference BETWEEN 46 AND 50 THEN 'XL'
    WHEN chest_circumference BETWEEN 50 AND 54 THEN '2XL'
    WHEN chest_circumference > 54 THEN '3XL+'
  END

-- Conversion Metrics
scan_to_purchase =
  COUNTIF(orderid IS NOT NULL) / COUNT(scan_id) * 100

return_rate_fitmap =
  COUNTIF(isreturn = TRUE) / COUNTIF(orderid IS NOT NULL) * 100
```

### Step 3: Build Dashboard
1. Create Analysis: "DXL FitMap Analytics"
2. Add all widgets as specified above
3. Apply global filters
4. Set up drill-downs
5. Configure tooltips
6. Publish dashboard

---

## Expected Insights

### What This Dashboard Reveals:
1. **FitMap Adoption**: Scan volume, user growth, completion rates
2. **Size Trends**: Distribution of sizes, body types in customer base
3. **Measurement Accuracy**: How well FitMap predicts correct sizes
4. **Return Reduction**: Impact of FitMap on return rates
5. **Customer Journey**: Flow from scan to purchase to satisfaction
6. **Demographic Patterns**: Age/size correlations, segment preferences

### Questions This Dashboard Answers:
- "How many customers are using FitMap and is it growing?"
- "What's the most common size/body type in our customer base?"
- "Does FitMap reduce return rates? By how much?"
- "Which measurements are most accurate vs least accurate?"
- "What's the conversion rate from FitMap scan to purchase?"
- "How do FitMap users compare to non-FitMap users in value?"
- "What size recommendations should we stock more of?"

---

## Integration with Quick Suite

### Upload to Quick Suite:
1. Export dashboard as image/PDF
2. Upload to Quick Suite Space: "FitMap Analytics"
3. Share context with Quick Research

### Sample Questions for Quick Suite Chat:
```
"Analyze the FitMap dashboard. What are the biggest opportunities
to improve fit accuracy and reduce returns?"

"Based on the body type distribution, what inventory adjustments
should we make for next quarter?"

"Compare FitMap users vs non-FitMap users. What's the ROI of
expanding FitMap to all stores?"

"Which age groups have the highest scan-to-purchase conversion?
How should we target marketing?"
```

---

**File Reference**: Use as blueprint for AWS QuickSight FitMap dashboard
**Created**: December 2024
**For**: DXL AWS Quick Suite POC
