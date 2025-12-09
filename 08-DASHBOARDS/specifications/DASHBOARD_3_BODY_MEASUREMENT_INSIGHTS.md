# Dashboard 3: Body Measurement & Fit Analytics Dashboard

## Dashboard Overview
**Purpose**: Comprehensive body measurement analytics for garment fit optimization and size recommendation insights
**Target Audience**: Product Development, Merchandising, Quality Assurance, Customer Experience
**Refresh Rate**: Daily
**Data Sources**: Body measurement data (scan records with circumference measurements, garment fit data, brand performance)

---

## Layout Structure (Grid: 12 columns x 8 rows)

```
┌─────────────────────────────────────────────────────────────┐
│  BODY MEASUREMENT & FIT ANALYTICS - SIZE OPTIMIZATION        │
└─────────────────────────────────────────────────────────────┘
┌──────────┬──────────┬──────────┬──────────┬──────────┬──────┐
│ Total    │ Complete │  Error   │  Avg     │  Unique  │ Avg  │  ROW 1
│ Scans    │ Rate %   │  Rate %  │  Age     │  Users   │ Meas.│
├──────────┴──────────┴──────────┴──────────┴──────────┴──────┤
│                                                               │
│         Scan Volume Trend by Status (Area Chart)             │  ROW 2
│                                                               │
├──────────────────────┬────────────────────────────────────────┤
│                      │                                        │
│  Gender Distribution │   Age Distribution                     │  ROW 3-4
│  (Donut Chart)       │   (Histogram)                          │
│                      │                                        │
├──────────────────────┴────────────────────────────────────────┤
│                                                               │
│  Measurement Point Analysis (Box Plot - Circumferences)      │  ROW 5
│                                                               │
├───────────────────────────────┬───────────────────────────────┤
│                               │                               │
│  Top Garment Types & Sizes    │  Brand Performance Matrix     │  ROW 6-7
│  (Stacked Bar Chart)          │  (Heat Map)                   │
│                               │                               │
├───────────────────────────────┴───────────────────────────────┤
│                                                               │
│  Measurement Point Variance by Demographics (Scatter Plot)   │  ROW 8
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

---

## Widget Details

### ROW 1: Key Performance Metrics

#### **KPI 1: Total Scans**
- **Visualization Type**: KPI Card
- **Metric**: `COUNT(DISTINCT scan_id)`
- **Comparison**: vs Last Month (MoM%)
- **Icon**: Measurement icon
- **Data Source**: Scan records

**QuickSight Setup**:
```
Visual Type: KPI
Value: COUNT(DISTINCT scan_id)
Comparison: MoM Change %
Format: Number with commas (15,234)
Conditional Formatting:
  - Green if growth > 5%
  - Yellow if growth 0-5%
  - Red if negative
```

#### **KPI 2: Completion Rate**
- **Visualization Type**: KPI Card
- **Metric**: `(COUNT(status='complete') / COUNT(*)) * 100`
- **Comparison**: vs Target (95%)
- **Data Source**: status field

**QuickSight Setup**:
```
Visual Type: KPI
Calculated Field:
  (COUNTIF(status = 'complete') / COUNT(*)) * 100
Format: Percentage (94.2%)
Target: 95%
Conditional Formatting:
  - Green if >= 95%
  - Yellow if 90-95%
  - Red if < 90%
```

#### **KPI 3: Error Rate**
- **Visualization Type**: KPI Card
- **Metric**: `(COUNT(status='error') / COUNT(*)) * 100`
- **Comparison**: vs Last Month
- **Data Source**: status field

**QuickSight Setup**:
```
Visual Type: KPI
Calculated Field:
  (COUNTIF(status = 'error') / COUNT(*)) * 100
Format: Percentage (5.8%)
Comparison: MoM Change
Conditional Formatting:
  - Red if > 10%
  - Yellow if 5-10%
  - Green if < 5%
```

#### **KPI 4: Average Age**
- **Visualization Type**: KPI Card
- **Metric**: `AVG(age)`
- **Comparison**: vs Industry benchmark
- **Data Source**: age field

**QuickSight Setup**:
```
Visual Type: KPI
Value: AVG(age)
Format: Number (45.3 years)
Comparison: vs Benchmark (42 years)
Icon: Demographics
```

#### **KPI 5: Unique Users**
- **Visualization Type**: KPI Card
- **Metric**: `COUNT(DISTINCT user_id)`
- **Comparison**: vs Last Quarter
- **Data Source**: user_id field

**QuickSight Setup**:
```
Visual Type: KPI
Value: COUNT(DISTINCT user_id)
Format: Number (3,456)
Comparison: QoQ Change %
Show Trend: Mini sparkline
```

#### **KPI 6: Average Measurements**
- **Visualization Type**: KPI Card
- **Metric**: `AVG(measurement_value)` across all measurement points
- **Comparison**: By gender
- **Data Source**: circumference fields

**QuickSight Setup**:
```
Visual Type: KPI
Value: AVG(circumference_value)
Format: Number (85.4 cm)
Comparison: Male vs Female
Icon: Ruler
```

---

### ROW 2: Scan Volume Trend

#### **Widget: Scan Volume by Status Over Time**
- **Visualization Type**: Area Chart (Stacked)
- **Dimension**: `scan_date` (Day/Week/Month granularity)
- **Measures**:
  - Complete scans
  - Error scans
  - Total scans
- **Data Source**: scan_date, status fields
- **Time Range**: Last 12 months

**QuickSight Setup**:
```
Visual Type: Area Chart (stacked)
X-axis: scan_date (aggregated by month)
Y-axis: COUNT(scan_id)
Series:
  1. Complete - Green (#4CAF50)
  2. Error - Red (#F44336)
Show Data Labels: On peaks
Annotations:
  - Mark significant dates (system updates, campaigns)
Drill-down: Month → Week → Day
Tooltip:
  - Date
  - Complete Count
  - Error Count
  - Total Count
  - Completion Rate %
```

**Calculated Fields**:
```sql
completion_rate =
  (COUNTIF(status = 'complete') / COUNT(*)) * 100
```

---

### ROW 3-4: Demographics Distribution

#### **Widget 1: Gender Distribution (Left Panel)**
- **Visualization Type**: Donut Chart
- **Dimension**: Gender (male/female)
- **Measure**: `COUNT(DISTINCT user_id)`
- **Data Source**: gender field

**QuickSight Setup**:
```
Visual Type: Donut Chart
Group by: gender
Value: COUNT(DISTINCT user_id)
Colors:
  - Male: Blue (#2196F3)
  - Female: Pink (#E91E63)
Show Percentages: Yes
Show Count: In center
Tooltip:
  - Gender
  - Count
  - Percentage
  - Avg Age
  - Most Common Garment Type
```

#### **Widget 2: Age Distribution (Right Panel)**
- **Visualization Type**: Histogram
- **Dimension**: Age (binned in 5-year groups)
- **Measure**: `COUNT(user_id)`
- **Data Source**: age field

**QuickSight Setup**:
```
Visual Type: Vertical Bar Chart (Histogram)
X-axis: age_group (20-25, 25-30, 30-35, ..., 75-80)
Y-axis: COUNT(user_id)
Colors: Gradient (Light to Dark Blue)
Show Percentages: On bars
Tooltip:
  - Age Range
  - Count
  - % of Total
  - Avg Measurements
  - Gender Split
Sort: By age ascending
```

**Calculated Field - Age Groups**:
```sql
age_group =
  CASE
    WHEN age < 25 THEN '20-25'
    WHEN age BETWEEN 25 AND 29 THEN '25-30'
    WHEN age BETWEEN 30 AND 34 THEN '30-35'
    WHEN age BETWEEN 35 AND 39 THEN '35-40'
    WHEN age BETWEEN 40 AND 44 THEN '40-45'
    WHEN age BETWEEN 45 AND 49 THEN '45-50'
    WHEN age BETWEEN 50 AND 54 THEN '50-55'
    WHEN age BETWEEN 55 AND 59 THEN '55-60'
    WHEN age BETWEEN 60 AND 64 THEN '60-65'
    WHEN age BETWEEN 65 AND 69 THEN '65-70'
    WHEN age BETWEEN 70 AND 74 THEN '70-75'
    ELSE '75+'
  END
```

---

### ROW 5: Measurement Point Analysis

#### **Widget: Circumference Distribution by Measurement Point**
- **Visualization Type**: Box Plot
- **Dimension**: Measurement point names (ChestFront, ChestBack, WaistFront, WaistBack, CrotchPoint, etc.)
- **Measure**: Circumference values
- **Data Source**: measurement_point, circumference fields

**QuickSight Setup**:
```
Visual Type: Box Plot
X-axis: measurement_point_name
Y-axis: circumference_value (cm)
Show:
  - Median (line)
  - Quartiles (box)
  - Min/Max (whiskers)
  - Outliers (dots)
Colors: By measurement category
  - Chest measurements: Blue
  - Waist measurements: Green
  - Hip measurements: Orange
  - Other: Gray
Tooltip:
  - Measurement Point
  - Min, Q1, Median, Q3, Max
  - Std Deviation
  - Sample Size
Filter: Gender selector
```

**Insights**:
- Identifies measurement variance
- Spots outliers for quality control
- Shows typical ranges by body part

---

### ROW 6-7: Garment & Brand Analysis

#### **Widget 1: Top Garment Types & Sizes (Left Panel)**
- **Visualization Type**: Stacked Bar Chart
- **Dimension**: Garment type (Shorts, Dress Pants, Denim)
- **Measure**: Count of scans, grouped by size
- **Data Source**: garment_type, garment_size fields

**QuickSight Setup**:
```
Visual Type: Horizontal Stacked Bar Chart
Y-axis: garment_type
X-axis: COUNT(scan_id)
Stack by: garment_size (parsed waist/inseam)
Colors: Distinct colors per size range
Show Percentages: Yes
Tooltip:
  - Garment Type
  - Size
  - Count
  - % of Garment Type
  - Avg Age
  - Gender Split
Sort: By total count descending
Top N: 10 garment types
```

**Calculated Field - Size Category**:
```sql
waist_category =
  CASE
    WHEN CAST(SPLIT_PART(garment_size, ',', 1) AS INT) < 36 THEN 'Small (< 36)'
    WHEN CAST(SPLIT_PART(garment_size, ',', 1) AS INT) BETWEEN 36 AND 42 THEN 'Medium (36-42)'
    WHEN CAST(SPLIT_PART(garment_size, ',', 1) AS INT) BETWEEN 43 AND 48 THEN 'Large (43-48)'
    WHEN CAST(SPLIT_PART(garment_size, ',', 1) AS INT) BETWEEN 49 AND 54 THEN 'XL (49-54)'
    ELSE 'XXL (55+)'
  END
```

#### **Widget 2: Brand Performance Matrix (Right Panel)**
- **Visualization Type**: Heat Map
- **Rows**: Brand names
- **Columns**: Garment types
- **Color**: Scan count (darker = more popular)
- **Data Source**: brand, garment_type fields

**QuickSight Setup**:
```
Visual Type: Heat Map
Rows: brand
Columns: garment_type
Values: COUNT(scan_id)
Color Scale: White (low) to Dark Blue (high)
Show Values: In cells
Tooltip:
  - Brand
  - Garment Type
  - Scan Count
  - % of Brand Total
  - Avg Completion Rate
  - Most Common Size
Sort Rows: By total scans descending
Sort Columns: Alphabetically
```

**Insights**:
- Shows brand popularity by category
- Identifies brand-garment combinations
- Helps with inventory planning

---

### ROW 8: Measurement Variance Analysis

#### **Widget: Age vs Measurement Variance (Scatter Plot)**
- **Visualization Type**: Scatter Plot with trend lines
- **X-Axis**: Age
- **Y-Axis**: Average circumference (selectable: Chest, Waist, Hip)
- **Size**: Count of measurements
- **Color**: Gender
- **Data Source**: age, measurement values, gender

**QuickSight Setup**:
```
Visual Type: Scatter Plot
X-axis: age
Y-axis: AVG(circumference_value) - Parameter controlled
Bubble Size: COUNT(scan_id)
Color: gender
  - Male: Blue
  - Female: Pink
Trend Lines:
  - Linear regression by gender
  - Show R² value
Tooltip:
  - Age
  - Avg Measurement
  - Count
  - Gender
  - Std Deviation
Filters:
  - Measurement Point selector (dropdown)
  - Gender filter
```

**Parameter - Measurement Selector**:
```
Parameter: selected_measurement
Type: String
Values: ChestFront, ChestBack, WaistFront, WaistBack, CrotchPoint, etc.
Default: ChestFront

Calculated Field:
selected_measurement_value =
  CASE ${selected_measurement}
    WHEN 'ChestFront' THEN chest_front_circumference
    WHEN 'ChestBack' THEN chest_back_circumference
    WHEN 'WaistFront' THEN waist_front_circumference
    WHEN 'WaistBack' THEN waist_back_circumference
    ELSE crotch_point_circumference
  END
```

**Insights**:
- Shows how body measurements change with age
- Identifies demographic patterns
- Helps with size range planning

---

## Additional Widgets (Optional)

### **Widget: Measurement Point Frequency**
- **Visualization Type**: Treemap
- **Dimension**: Measurement point names
- **Measure**: Count of measurements
- **Color**: Average circumference value

**QuickSight Setup**:
```
Visual Type: Treemap
Group by: measurement_point_name
Size: COUNT(*)
Color: AVG(circumference_value) - Gradient
Labels: Show name and count
Tooltip:
  - Measurement Point
  - Count
  - Avg Value
  - Min/Max
  - Std Deviation
```

### **Widget: Size Recommendation Table**
- **Visualization Type**: Pivot Table
- **Rows**: Age group, Gender
- **Columns**: Garment type
- **Values**: Most common size, Average measurements

**QuickSight Setup**:
```
Visual Type: Pivot Table
Rows:
  1. age_group
  2. gender
Columns: garment_type
Values:
  1. Most Common Size - MODE(garment_size)
  2. Avg Chest - AVG(chest_circumference)
  3. Avg Waist - AVG(waist_circumference)
  4. Sample Size - COUNT(*)
Conditional Formatting:
  - Highlight cells with low sample size (< 10)
```

### **Widget: Error Analysis**
- **Visualization Type**: Bar Chart
- **Dimension**: Measurement point (for error scans)
- **Measure**: Error count
- **Data Source**: Filtered to status='error'

**QuickSight Setup**:
```
Visual Type: Horizontal Bar Chart
Filter: status = 'error'
Y-axis: measurement_point_name
X-axis: COUNT(*)
Colors: Red gradient
Show Percentages: Yes
Tooltip:
  - Measurement Point
  - Error Count
  - % of Total Errors
  - Common Error Patterns
Sort: By count descending
```

---

## Filters & Parameters

### Global Filters:
1. **Date Range**: Last 12 months (default), custom range selector
2. **Gender**: Male / Female / All
3. **Age Range**: Slider (18-80 years)
4. **Status**: Complete / Error / All
5. **Garment Type**: Multi-select dropdown
6. **Brand**: Multi-select dropdown

### Parameter Controls:
1. **Measurement Point Selector**: Dropdown for scatter plot
2. **Size Grouping**: Standard / Detailed
3. **Outlier Threshold**: Slider (for filtering extreme values)

---

## QuickSight Setup Instructions

### Step 1: Prepare Dataset
```sql
-- Create unified measurement analytics view
CREATE VIEW body_measurement_analytics AS
SELECT
    scan_id,
    user_id,
    scan_date,
    status,
    age,
    gender,
    measurement_point_name,
    circumference_value,
    measurement_point_x,
    measurement_point_y,
    measurement_point_z,
    garment_type,
    garment_size,
    brand,
    -- Parse waist and inseam from garment_size
    CAST(REGEXP_SUBSTR(garment_size, 'Waist: ([0-9]+)', 1, 1, 'e', 1) AS INT) AS waist_size,
    CAST(REGEXP_SUBSTR(garment_size, 'Inseam: ([0-9]+)', 1, 1, 'e', 1) AS INT) AS inseam_size
FROM measurement_data;
```

### Step 2: Create Calculated Fields
```sql
-- Age Groups
age_group =
  FLOOR(age / 5) * 5 || '-' || (FLOOR(age / 5) * 5 + 5)

-- Size Categories
waist_category =
  CASE
    WHEN waist_size < 36 THEN 'Small'
    WHEN waist_size BETWEEN 36 AND 42 THEN 'Medium'
    WHEN waist_size BETWEEN 43 AND 48 THEN 'Large'
    WHEN waist_size BETWEEN 49 AND 54 THEN 'XL'
    ELSE 'XXL'
  END

-- Completion Rate
completion_rate =
  (COUNTIF(status = 'complete') / COUNT(*)) * 100

-- Error Rate
error_rate =
  (COUNTIF(status = 'error') / COUNT(*)) * 100

-- Measurement Category
measurement_category =
  CASE
    WHEN measurement_point_name LIKE '%Chest%' THEN 'Chest'
    WHEN measurement_point_name LIKE '%Waist%' THEN 'Waist'
    WHEN measurement_point_name LIKE '%Hip%' THEN 'Hip'
    WHEN measurement_point_name LIKE '%Shoulder%' THEN 'Shoulder'
    WHEN measurement_point_name LIKE '%Neck%' THEN 'Neck'
    ELSE 'Other'
  END
```

### Step 3: Build Dashboard
1. Create Analysis: "Body Measurement & Fit Analytics"
2. Add all widgets as specified above
3. Apply global filters
4. Set up drill-downs (Date → Month → Week → Day)
5. Configure tooltips with rich context
6. Add parameter controls
7. Test all interactions
8. Publish dashboard

### Step 4: Set Refresh Schedule
```
Schedule: Daily at 2:00 AM
Incremental Refresh: Yes (last 7 days)
Full Refresh: Weekly (Sunday)
```

---

## Expected Insights

### What This Dashboard Reveals:
1. **Scan Performance**: Completion vs error rates, volume trends
2. **Demographics**: Age and gender distribution of measured customers
3. **Measurement Patterns**: Typical ranges and variance by body part
4. **Garment Preferences**: Most popular types, sizes, and brands
5. **Quality Control**: Outliers and error patterns
6. **Size Trends**: How measurements correlate with demographics

### Questions This Dashboard Answers:
- "What's our scan completion rate and how is it trending?"
- "What's the demographic profile of our measured customers?"
- "Which measurement points have the highest variance?"
- "What are the most popular garment types and sizes?"
- "Which brands are most frequently measured?"
- "How do body measurements vary by age and gender?"
- "Where are we seeing measurement errors?"
- "What size ranges should we prioritize in inventory?"

---

## Integration with Quick Suite

### Upload to Quick Suite:
1. Export dashboard as PDF
2. Upload to Quick Suite Space: "Body Measurement Analytics"
3. Share context with Quick Research

### Sample Questions for Quick Suite Chat:
```
"Analyze the body measurement dashboard. What patterns do you see
in our customer demographics and measurements?"

"Based on the measurement variance data, which body parts show
the most inconsistency? What could be causing this?"

"What's the relationship between age and body measurements?
How should this inform our size range strategy?"

"Compare error rates across different measurement points.
Which areas need quality improvement?"

"What are the top 5 garment type and size combinations?
How should we adjust inventory?"
```

---

**File Reference**: Blueprint for AWS QuickSight Body Measurement Analytics Dashboard
**Created**: December 2024
**Data Source**: Body measurement scan data with circumference measurements
**Purpose**: Fit optimization and size recommendation insights

