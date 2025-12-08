# DXL Sales Report Generator - README

## What Was Created

A comprehensive Python script that generates a professional 10-page PDF sales report for DXL, optimized for **AWS Quick Suite Quick Research** analysis.

---

## Files Created

### 1. `generate_dxl_sales_report.py` (Main Script)
**Purpose**: Generates comprehensive PDF sales report from your CSV data

**Data Sources Used**:
- `orderheader.csv` - 3,000 orders
- `orderline.csv` - Order line items
- `transaction_header.csv` - 15,000 transactions
- `transaction_detail.csv` - Transaction line items
- `customer.csv` - 5,000 customers
- `store.csv` - 8 store locations

**Output**: `DXL_Sales_Report_2024.pdf` (10 pages, ~95KB)

### 2. `DXL_Sales_Report_2024.pdf` (Generated Report)
**Contents**:
- Page 1: Professional cover page with DXL branding
- Page 2: Executive summary with 6 key metrics
- Page 3: Revenue analysis (monthly trends, quarterly breakdown)
- Page 4: Sales channel performance (mobile, web, in-store)
- Page 5: Customer analytics (segmentation, demographics)
- Page 6: Product performance (sizes, markdowns, promotions)
- Page 7: Store performance (top stores, transaction volumes)
- Page 8: Payment & fulfillment analysis
- Page 9: Trends & seasonality (growth rates, forecasts)
- Page 10: Strategic recommendations for 2025

### 3. `AWS_QUICK_SUITE_USAGE_GUIDE.md` (Instructions)
Complete guide for using the PDF with AWS Quick Suite

---

## Quick Start

### Step 1: Generate the Report
```bash
cd "c:\Users\afjal.ahamad\Desktop\Office Work\aiML-pURPOSAL\Quick SUite Analysis"
python generate_dxl_sales_report.py
```

### Step 2: Upload to AWS Quick Suite
1. Log in to AWS Quick Suite console
2. Create a new Space: "DXL Sales Analysis 2024"
3. Upload `DXL_Sales_Report_2024.pdf`
4. Wait for Quick Index to process (~2-3 minutes)

### Step 3: Ask Quick Research
**Example Questions**:
```
"Analyze the DXL sales report and provide top 3 growth opportunities for 2025"

"What are the revenue trends by quarter and which customer segments drive the most value?"

"Analyze the markdown strategy - how can we optimize pricing to improve margins?"

"Which sales channels show the most growth potential and what investments are needed?"
```

---

## Key Metrics in Report

### 2024 Performance Summary:
- **Total Revenue**: Calculated from 1,137 transactions in 2024
- **Total Transactions**: 1,137 (from 15,000 total dataset)
- **Total Orders**: 511 (from 3,000 total dataset)
- **Active Customers**: Unique customer count from 2024 data
- **Average Transaction Value**: Mean revenue per transaction
- **Gross Margin**: (Revenue - Cost) / Revenue %
- **Active Stores**: 8 DXL locations + 2 web channels

### Analysis Included:
✅ Monthly revenue trends with growth rates
✅ Quarterly performance comparison
✅ Payment method distribution (VISA, AMEX, CASH, etc.)
✅ Sales channel breakdown (in-store, mobile, web, call center)
✅ Customer segmentation (VIP, GOLD, PREMIUM, STANDARD)
✅ Top-selling product sizes
✅ Markdown impact analysis
✅ Store performance rankings
✅ Fulfillment status tracking
✅ Marketing campaign effectiveness

---

## Customization Options

### Modify Report Year
Edit line 17 in `generate_dxl_sales_report.py`:
```python
self.report_year = 2024  # Change to desired year
```

### Change Data Path
Edit line 16:
```python
self.data_path = "poc_data_generators"  # Change to your data folder
```

### Customize Output File
Run with custom filename:
```python
generator.run("Custom_Report_Name.pdf")
```

### Add/Remove Pages
Edit the `generate_pdf()` method (lines 120-155) to add or remove page sections

---

## Dependencies

**Required Python Packages**:
```bash
pip install pandas matplotlib seaborn numpy
```

All packages should already be installed in your `menv` virtual environment.

---

## AWS Quick Suite Integration

### What is AWS Quick Suite?
**AWS Quick Suite** is Amazon's new agentic AI platform (launched Oct 2025) that includes:

- **Quick Research**: AI research agent that analyzes documents and data
- **Quick Sight**: Conversational business intelligence
- **Quick Automate**: Enterprise workflow automation
- **Quick Flows**: User-friendly automation builder
- **Quick Index**: Unified knowledge base foundation

### Why This Report is Optimized for Quick Suite:

1. **Structured Data**: Clear sections, headings, and metrics
2. **Visual Analytics**: Charts and graphs for pattern recognition
3. **Executive Summary**: Key highlights for quick scanning
4. **Strategic Recommendations**: Actionable insights for decision-making
5. **Comprehensive Coverage**: Revenue, customers, products, operations
6. **Citation-Friendly**: Clear page structure for Quick Research references

---

## Use Cases with Quick Research

### 1. Executive Strategic Planning
**Question**: "Based on 2024 performance, what should be our top 3 strategic priorities for 2025?"

**Quick Research Will**:
- Analyze all 10 pages of the report
- Identify high-impact opportunities
- Cross-reference revenue, customer, and product data
- Provide data-backed recommendations with citations

### 2. Marketing Campaign Optimization
**Question**: "Which marketing campaigns performed best and how should we allocate 2025 budget?"

**Quick Research Will**:
- Extract campaign performance data
- Compare ROI across channels
- Identify customer segments with highest response
- Recommend budget allocation strategy

### 3. Inventory & Merchandising
**Question**: "Analyze the size distribution and markdown patterns. How can we optimize inventory?"

**Quick Research Will**:
- Identify top-selling vs slow-moving sizes
- Analyze markdown effectiveness
- Recommend stock level adjustments
- Suggest dynamic pricing strategies

### 4. Customer Retention
**Question**: "What insights about customer behavior can help reduce churn and increase loyalty?"

**Quick Research Will**:
- Segment customers by value and activity
- Identify at-risk customer patterns
- Recommend retention programs
- Estimate revenue impact

---

## Advanced Workflows

### Automated Monthly Reporting
Create a Quick Flow:
```
Trigger: 1st day of each month
→ Run generate_dxl_sales_report.py with last month's data
→ Upload PDF to Quick Suite Space
→ Quick Research analyzes report
→ Email executive summary to leadership
→ Post highlights to Slack #sales-updates channel
```

### Real-Time Sales Monitoring
Create a Quick Automate workflow:
```
Monitor: Redshift sales data (hourly)
→ If revenue <90% of forecast: Trigger alert
→ Quick Research analyzes anomaly
→ Generate diagnostic report
→ Notify sales leadership with recommended actions
```

### Embedded Sales Assistant
Create Custom Chat Agent:
```
Name: "DXL Sales Advisor"
Knowledge: DXL_Sales_Report_2024.pdf + Live Redshift data
Deploy: Embed in sales portal for instant insights
```

---

## Regenerating for Different Time Periods

### For Previous Years:
```python
# Edit the script to filter by different year
self.report_year = 2023  # or 2022, 2021, etc.
```

### For Specific Quarters:
```python
# Add quarter filter in prepare_data() method
self.transactions_2024 = self.transactions[
    (self.transactions['year'] == 2024) &
    (self.transactions['quarter'] == 4)  # Q4 only
].copy()
```

### For Month-over-Month Comparison:
```python
# Generate separate reports for each month
for month in range(1, 13):
    generator.report_month = month
    generator.run(f"DXL_Sales_Report_2024_Month_{month:02d}.pdf")
```

---

## Troubleshooting

### Issue: Script fails with encoding error
**Solution**: Already fixed in current version (uses `encoding='utf-8-sig'`)

### Issue: Empty charts or missing data
**Solution**: Check that CSV files are in `poc_data_generators` folder and properly formatted

### Issue: PDF too large
**Solution**: Reduce DPI in matplotlib settings or filter data to specific time period

### Issue: Out of memory
**Solution**: Process data in chunks or filter to smaller date range

---

## Next Steps

### Immediate (Next 30 Minutes):
1. ✅ Report generated successfully
2. ⬜ Upload to AWS Quick Suite
3. ⬜ Ask 3 sample questions to Quick Research
4. ⬜ Review insights and share with team

### This Week:
- Connect Redshift and Athena data sources to Quick Suite
- Create custom chat agent for ongoing analysis
- Set up automated monthly report generation
- Build dashboard of key metrics in Quick Sight

### This Month:
- Expand to full organization (10-20 users)
- Create Quick Flows for operational workflows
- Implement real-time alerting
- Measure ROI and business impact

---

## Support & Resources

**Project Files**:
- `generate_dxl_sales_report.py` - Main script
- `DXL_Sales_Report_2024.pdf` - Generated report
- `AWS_QUICK_SUITE_USAGE_GUIDE.md` - Detailed usage guide
- `SALES_REPORT_README.md` - This file

**AWS Quick Suite Resources**:
- Documentation: https://docs.aws.amazon.com/quicksuite/
- Quick Research: https://aws.amazon.com/quicksuite/research/
- Community: AWS Quick Suite User Forum

**DXL POC Documentation**:
- Email_Senior_Leadership_POC_Proposal.md
- AWS_Quick_Suite_Knowledge_Base.md
- AWS_Quick_Suite_Blog_Post.md
- DXL_AWS_Quick_Suite_Proposal.md

---

## Contact

**Created by**: Afjal Ahamad
**Date**: December 2024
**Purpose**: DXL AWS Quick Suite POC

For questions or support with the report generation or AWS Quick Suite integration, refer to the documentation or reach out to the project team.

---

**Remember**: AWS Quick Suite is different from Amazon QuickSight. Quick Suite is the new agentic AI platform that includes Quick Research for intelligent document analysis and strategic insights!
