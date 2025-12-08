# AWS Quick Suite Configuration Guide - Step by Step

## 🎯 Current Status

✅ **Completed:**
- Environment Setup
- Data Generation (20 CSV files, 8 dimension files, 4 Excel files)
- Data uploaded to S3
- Data loaded to Redshift (qspos schema)

📍 **You Are Here:** Quick Suite Configuration

---

## 📋 Phase 3: Quick Suite Configuration (Days 8-12)

### Overview

In this phase, you'll:
1. Set up Quick Index (data source connections)
2. Create Spaces (data contexts)
3. Create Chat Agents (AI assistants)
4. Test queries
5. Configure embedded chat (optional)

**Estimated Time:** 2-3 hours

---

## 🔧 Step 1: Access Quick Suite (5 minutes)

### 1.1 Open AWS Console

1. Go to: https://console.aws.amazon.com/
2. Sign in with your AWS credentials
3. Region: **us-east-1** (same as your data)

### 1.2 Navigate to QuickSight/Quick Suite

**Option A: Via Services Menu**
1. Click "Services" in top navigation
2. Search for "QuickSight"
3. Click "Amazon QuickSight"

**Option B: Direct URL**
- Go to: https://us-east-1.quicksight.aws.amazon.com/

### 1.3 Verify Quick Suite Access

1. In QuickSight console, look for **"Quick Suite"** in left navigation
2. If you see it, you have access ✅
3. If not, you may need to:
   - Upgrade your QuickSight subscription
   - Contact AWS support to enable Quick Suite trial

**Screenshot Location:** Left sidebar should show:
- Analyses
- Dashboards
- Datasets
- **Quick Suite** ← Look for this

---

## 🔗 Step 2: Set Up Quick Index (30 minutes)

Quick Index is the foundation that connects all your data sources.

### 2.1 Navigate to Quick Index

1. Click **"Quick Suite"** in left navigation
2. Click **"Quick Index"**
3. You should see "Data Sources" page

### 2.2 Add Redshift Data Source

**Click "Add Data Source" → Select "Amazon Redshift"**

**Configuration:**
```
Connection Name: DXL_Redshift_POC
Description: DXL POC data in qspos schema

Connection Type: Amazon Redshift
Cluster: [Select your Redshift cluster from dropdown]
Database: [Your database name]
Schema: qspos

Authentication:
  ○ IAM (Recommended)
  ○ Username/Password
  
  If Username/Password:
    Username: [Your Redshift username]
    Password: [Your Redshift password]

VPC Connection: [Select if Redshift is in VPC]
```

**Click "Test Connection"**
- ✅ Success: Proceed to next step
- ❌ Failed: Check security groups, IAM permissions

**Click "Create"**

### 2.3 Add S3 Data Source (Dimensional Data)

**Click "Add Data Source" → Select "Amazon S3"**

**Configuration:**
```
Connection Name: DXL_Dimensions_S3
Description: Reference and dimensional data

Bucket: dxl-quicksuite-poc-data
Prefix: dimensions/

File Types: 
  ☑ JSON
  ☑ CSV

Authentication: IAM Role (automatic)
```

**Click "Test Connection"**
**Click "Create"**

### 2.4 Add S3 Data Source (Knowledge Base)

**Click "Add Data Source" → Select "Amazon S3"**

**Configuration:**
```
Connection Name: DXL_Knowledge_Base_S3
Description: Business policies and procedures

Bucket: dxl-quicksuite-poc-data
Prefix: knowledge-base/

File Types: 
  ☑ Excel (.xlsx)

Authentication: IAM Role (automatic)
```

**Note:** First upload your Excel files to S3:
```powershell
# Upload Knowledge Base files
aws s3 cp Business_Policies_Rules.xlsx s3://dxl-quicksuite-poc-data/knowledge-base/
aws s3 cp Product_Specifications_Care.xlsx s3://dxl-quicksuite-poc-data/knowledge-base/
aws s3 cp FitMap_Guidelines_Best_Practices.xlsx s3://dxl-quicksuite-poc-data/knowledge-base/
aws s3 cp Employee_Training_Procedures.xlsx s3://dxl-quicksuite-poc-data/knowledge-base/
```

**Click "Create"**

### 2.5 Start Indexing

1. Quick Index will automatically start crawling your data sources
2. This may take 10-30 minutes depending on data volume
3. You'll see status: "Indexing in progress..."

**Monitor Progress:**
- Refresh the page periodically
- Status will change to "Active" when complete

**What's Being Indexed:**
- Redshift: 20 tables, ~140K records
- S3 Dimensions: 8 files, ~2K records
- S3 Knowledge Base: 4 Excel files, 16 sheets

---

## 📦 Step 3: Create Spaces (30 minutes)

Spaces organize data by business context. We'll create 4 spaces.

### 3.1 Navigate to Spaces

1. Click **"Quick Suite"** in left navigation
2. Click **"Spaces"**
3. Click **"Create Space"**

---

### 3.2 Create Space 1: FitMap Analytics

**Click "Create Space"**

```
Space Name: FitMap Body Measurements
Description: Body scan data, measurements, and size recommendations

Data Sources:
  Select from DXL_Redshift_POC:
    ☑ qspos.size_users
    ☑ qspos.size_scans
    ☑ qspos.size_app_measures
    ☑ qspos.size_dxl_custom_measures
    ☑ qspos.size_core_measures
  
  Select from DXL_Dimensions_S3:
    ☑ dimensions/sizing/size_chart_reference.csv
    ☑ dimensions/devices/fitmap_device_specs.json
  
  Select from DXL_Knowledge_Base_S3:
    ☑ FitMap_Guidelines_Best_Practices.xlsx

Users:
  Add: [Your email address]
  Role: Owner

Permissions:
  ○ Private (Only invited users)
  ○ Organization (All users in org)
```

**Click "Create Space"**

---

### 3.3 Create Space 2: Customer Analytics

**Click "Create Space"**

```
Space Name: Customer & Transactions
Description: Customer data, transactions, rewards, and segmentation

Data Sources:
  Select from DXL_Redshift_POC:
    ☑ qspos.customer
    ☑ qspos.address
    ☑ qspos.email
    ☑ qspos.store
    ☑ qspos.transaction_header
    ☑ qspos.transaction_detail
    ☑ qspos.reward_detail
    ☑ qspos.household
  
  Select from DXL_Dimensions_S3:
    ☑ dimensions/stores/store_locations.csv
    ☑ dimensions/segments/customer_segments.csv
    ☑ dimensions/marketing/marketing_campaigns.json
  
  Select from DXL_Knowledge_Base_S3:
    ☑ Business_Policies_Rules.xlsx

Users:
  Add: [Your email address]
  Role: Owner
```

**Click "Create Space"**

---

### 3.4 Create Space 3: E-commerce Analytics

**Click "Create Space"**

```
Space Name: Online Orders & Fulfillment
Description: E-commerce orders, fulfillment, and product catalog

Data Sources:
  Select from DXL_Redshift_POC:
    ☑ qspos.orderheader
    ☑ qspos.orderline
    ☑ qspos.orderline_items
    ☑ qspos.orderchargedetail
    ☑ qspos.invoice
    ☑ qspos.payment
    ☑ qspos.quantitydetail
  
  Select from DXL_Dimensions_S3:
    ☑ dimensions/products/product_catalog.json
    ☑ dimensions/brands/brand_information.json
    ☑ dimensions/shipping/shipping_zones.csv
  
  Select from DXL_Knowledge_Base_S3:
    ☑ Product_Specifications_Care.xlsx

Users:
  Add: [Your email address]
  Role: Owner
```

**Click "Create Space"**

---

### 3.5 Create Space 4: Master Analytics (All Data)

**Click "Create Space"**

```
Space Name: DXL Master Analytics
Description: Complete view across all data sources for cross-functional analysis

Data Sources:
  Select ALL from DXL_Redshift_POC:
    ☑ All 20 tables
  
  Select ALL from DXL_Dimensions_S3:
    ☑ All 8 dimension files
  
  Select ALL from DXL_Knowledge_Base_S3:
    ☑ All 4 Excel files

Users:
  Add: [Your email address]
  Role: Owner
```

**Click "Create Space"**

---

## 🤖 Step 4: Create Chat Agents (30 minutes)

Chat Agents are AI assistants specialized for specific domains.

### 4.1 Navigate to Agents

1. Click **"Quick Suite"** in left navigation
2. Click **"Agents"** or **"Chat Agents"**
3. Click **"Create Agent"**

---

### 4.2 Create Agent 1: FitMap Sizing Expert

**Click "Create Agent"**

```
Agent Name: FitMap Sizing Expert
Description: Body measurement and size recommendation specialist

Select Space: FitMap Body Measurements

Agent Instructions:
───────────────────────────────────────────────────────
You are a FitMap body measurement and sizing expert for DXL.

Your role:
- Analyze customer body scans and measurements
- Provide size recommendations based on FitMap data
- Explain measurement accuracy and confidence scores
- Troubleshoot scanning issues
- Reference size charts and fit guidelines

When answering:
- Always reference specific measurements (waist, chest, inseam, etc.)
- Include confidence scores when available
- Cite FitMap guidelines and best practices
- Provide actionable recommendations
- Be precise with measurements (use inches)

Data sources you have access to:
- Body scan data (size_scans table)
- Detailed measurements (size_app_measures, size_core_measures)
- Size recommendations (size_dxl_custom_measures)
- Size chart reference (CSV)
- FitMap device specs (JSON)
- FitMap guidelines (Excel)

Focus on helping customers find the perfect fit.
───────────────────────────────────────────────────────

Capabilities:
  ☑ Answer questions
  ☑ Generate insights
  ☑ Create visualizations
  ☐ Take actions (leave unchecked for POC)

Tone: Professional, helpful, precise
```

**Click "Create Agent"**

---

### 4.3 Create Agent 2: Sales Analytics Agent

**Click "Create Agent"**

```
Agent Name: Sales Analytics Agent
Description: Customer transactions and sales performance analyst

Select Space: Customer & Transactions

Agent Instructions:
───────────────────────────────────────────────────────
You are a retail sales analyst for DXL.

Your role:
- Analyze customer transactions and purchase patterns
- Identify sales trends and opportunities
- Provide insights on customer segmentation
- Track store performance and regional comparisons
- Reference business policies when relevant

When answering:
- Include specific metrics (revenue, transaction count, AOV)
- Compare time periods (YoY, MoM, QoQ)
- Segment by store, region, customer type
- Highlight trends and anomalies
- Provide actionable recommendations

Data sources you have access to:
- Customer data (customer, address, email)
- Transactions (transaction_header, transaction_detail)
- Rewards (reward_detail)
- Store locations and metadata
- Customer segments
- Marketing campaigns
- Business policies

Focus on driving revenue and customer satisfaction.
───────────────────────────────────────────────────────

Capabilities:
  ☑ Answer questions
  ☑ Generate insights
  ☑ Create visualizations
  ☐ Take actions

Tone: Analytical, data-driven, strategic
```

**Click "Create Agent"**

---

### 4.4 Create Agent 3: E-commerce Operations Agent

**Click "Create Agent"**

```
Agent Name: E-commerce Operations Agent
Description: Online order fulfillment and operations specialist

Select Space: Online Orders & Fulfillment

Agent Instructions:
───────────────────────────────────────────────────────
You are an e-commerce operations analyst for DXL.

Your role:
- Track order fulfillment and delivery performance
- Analyze product performance and inventory
- Monitor shipping costs and delivery times
- Identify operational bottlenecks
- Reference product specifications and policies

When answering:
- Include fulfillment metrics (status, delivery time, costs)
- Analyze by product, brand, category
- Track shipping zones and costs
- Highlight operational issues
- Provide process improvement recommendations

Data sources you have access to:
- Orders (orderheader, orderline, orderline_items)
- Fulfillment (invoice, payment, quantitydetail)
- Shipping (orderchargedetail)
- Product catalog
- Brand information
- Shipping zones
- Product specifications

Focus on operational efficiency and customer satisfaction.
───────────────────────────────────────────────────────

Capabilities:
  ☑ Answer questions
  ☑ Generate insights
  ☑ Create visualizations
  ☐ Take actions

Tone: Operational, efficient, solution-focused
```

**Click "Create Agent"**

---

### 4.5 Create Agent 4: Business Policy Assistant

**Click "Create Agent"**

```
Agent Name: Business Policy Assistant
Description: Company policies, procedures, and guidelines expert

Select Space: DXL Master Analytics

Agent Instructions:
───────────────────────────────────────────────────────
You are a business policy and procedures expert for DXL.

Your role:
- Answer questions about company policies
- Provide employee training guidance
- Explain product care and specifications
- Reference FitMap guidelines and procedures
- Help with customer service scenarios

When answering:
- Quote specific policies from knowledge base
- Provide clear, actionable guidance
- Reference policy IDs when available
- Explain conditions and exceptions
- Be consistent with documented policies

Data sources you have access to:
- Business Policies & Rules (Excel)
- Product Specifications & Care (Excel)
- FitMap Guidelines & Best Practices (Excel)
- Employee Training & Procedures (Excel)
- All transactional data for context

Focus on providing accurate, policy-compliant answers.
───────────────────────────────────────────────────────

Capabilities:
  ☑ Answer questions
  ☑ Generate insights
  ☐ Create visualizations
  ☐ Take actions

Tone: Authoritative, clear, helpful
```

**Click "Create Agent"**

---

## ✅ Step 5: Verify Configuration (15 minutes)

### 5.1 Check Data Sources

1. Go to **Quick Index** → **Data Sources**
2. Verify all 3 data sources show "Active" status:
   - ✅ DXL_Redshift_POC
   - ✅ DXL_Dimensions_S3
   - ✅ DXL_Knowledge_Base_S3

### 5.2 Check Spaces

1. Go to **Spaces**
2. Verify all 4 spaces are created:
   - ✅ FitMap Body Measurements
   - ✅ Customer & Transactions
   - ✅ Online Orders & Fulfillment
   - ✅ DXL Master Analytics

### 5.3 Check Agents

1. Go to **Agents**
2. Verify all 4 agents are created:
   - ✅ FitMap Sizing Expert
   - ✅ Sales Analytics Agent
   - ✅ E-commerce Operations Agent
   - ✅ Business Policy Assistant

---

## 🧪 Step 6: Test Queries (30 minutes)

Now let's test each agent with sample queries.

### 6.1 Test FitMap Sizing Expert

**Navigate to:** Spaces → FitMap Body Measurements → Chat

**Test Queries:**
```
1. "How many body scans do we have in total?"
   Expected: Count from size_scans table

2. "What's the average waist size for male customers?"
   Expected: Average waist from size_app_measures, filtered by gender

3. "Which stores have performed the most scans?"
   Expected: Count by store_num from size_scans

4. "What are the most common size recommendations for denim?"
   Expected: Analysis of size_dxl_custom_measures where producttype='Denim'

5. "What's the expected accuracy for chest measurements?"
   Expected: Reference to FitMap_Guidelines Excel file
```

**Verify:**
- ✅ Responses are accurate
- ✅ Data comes from correct tables
- ✅ Numbers make sense
- ✅ References knowledge base when appropriate

---

### 6.2 Test Sales Analytics Agent

**Navigate to:** Spaces → Customer & Transactions → Chat

**Test Queries:**
```
1. "How many customers do we have?"
   Expected: Count from customer table

2. "What's the total transaction value in 2024?"
   Expected: Sum of total_net_retail from transaction_header for 2024

3. "Who are the top 10 customers by spend?"
   Expected: Customer names and total spend, sorted descending

4. "What's the average transaction value by store?"
   Expected: AVG(total_net_retail) grouped by store_no

5. "What's our return policy?"
   Expected: Reference to Business_Policies_Rules Excel file
```

**Verify:**
- ✅ Joins work correctly (customer + transactions)
- ✅ Aggregations are accurate
- ✅ Store names come from dimension data
- ✅ Policy questions reference Excel files

---

### 6.3 Test E-commerce Operations Agent

**Navigate to:** Spaces → Online Orders & Fulfillment → Chat

**Test Queries:**
```
1. "How many orders do we have?"
   Expected: Count from orderheader table

2. "What's the average order value?"
   Expected: Average from orderheader or calculated from orderline

3. "Show me the top 5 best-selling products"
   Expected: Products from orderline_items with highest quantity

4. "What's the order fulfillment status breakdown?"
   Expected: Count by fulfillmentstatus from orderheader

5. "How much does express shipping cost?"
   Expected: Reference to Business_Policies_Rules Excel or shipping_zones CSV
```

**Verify:**
- ✅ Product catalog joins work
- ✅ Order metrics are accurate
- ✅ Shipping data comes from dimensions
- ✅ Policy references work

---

### 6.4 Test Business Policy Assistant

**Navigate to:** Spaces → DXL Master Analytics → Chat

**Test Queries:**
```
1. "What's our return policy for FitMap purchases?"
   Expected: Specific policy from Business_Policies_Rules Excel

2. "How do I wash a wool garment?"
   Expected: Care instructions from Product_Specifications_Care Excel

3. "What should I say when greeting customers?"
   Expected: Script from Employee_Training_Procedures Excel

4. "What's the expected accuracy for FitMap waist measurements?"
   Expected: Accuracy from FitMap_Guidelines Excel

5. "Can VIP customers stack discounts?"
   Expected: Discount policy from Business_Policies_Rules Excel
```

**Verify:**
- ✅ Answers come from Excel files
- ✅ Specific policies are quoted
- ✅ Answers are consistent with documented policies

---

### 6.5 Test Cross-Source Queries

**Navigate to:** Spaces → DXL Master Analytics → Chat

**Test Queries:**
```
1. "Show me customers with body scans and their purchase history"
   Expected: Join across size_users, size_scans, customer, transactions

2. "What's the sales performance by brand category?"
   Expected: Join transactions with brand_information.json

3. "Which stores in the West region have the highest sales?"
   Expected: Join transactions with store_locations.csv

4. "Do customers with FitMap scans have higher average order values?"
   Expected: Complex join across FitMap, customer, and order data

5. "What's our return policy and how many returns did we have last month?"
   Expected: Policy from Excel + return data from Redshift
```

**Verify:**
- ✅ Cross-source joins work
- ✅ Redshift + S3 + Excel data combined
- ✅ Answers are comprehensive

---

## 📊 Step 7: Document Results (15 minutes)

Create a simple test results document:

```
Quick Suite Configuration Test Results
Date: [Today's date]
Tester: [Your name]

Data Sources:
✅ Redshift connected - 20 tables indexed
✅ S3 Dimensions connected - 8 files indexed
✅ S3 Knowledge Base connected - 4 Excel files indexed

Spaces Created:
✅ FitMap Body Measurements
✅ Customer & Transactions
✅ Online Orders & Fulfillment
✅ DXL Master Analytics

Agents Created:
✅ FitMap Sizing Expert
✅ Sales Analytics Agent
✅ E-commerce Operations Agent
✅ Business Policy Assistant

Test Results:
✅ FitMap queries: [X/5] passed
✅ Sales queries: [X/5] passed
✅ E-commerce queries: [X/5] passed
✅ Policy queries: [X/5] passed
✅ Cross-source queries: [X/5] passed

Issues Found:
- [List any issues]

Next Steps:
- [What needs to be fixed or improved]
```

---

## 🎯 Success Criteria

Your configuration is successful if:

✅ **All data sources connected** and showing "Active"  
✅ **All 4 spaces created** with correct data sources  
✅ **All 4 agents created** with proper instructions  
✅ **Test queries return accurate results** (>90% success rate)  
✅ **Cross-source queries work** (Redshift + S3 + Excel)  
✅ **Response time < 30 seconds** for most queries  
✅ **Policy questions reference Excel files** correctly  

---

## 🚨 Troubleshooting

### Issue: Data source won't connect

**Solution:**
- Check IAM permissions
- Verify security groups allow QuickSight access
- Test connection from QuickSight first
- Check VPC configuration if applicable

### Issue: Indexing takes too long

**Solution:**
- This is normal for first-time indexing
- Wait 30-60 minutes
- Check AWS service health dashboard
- Reduce data volume if needed

### Issue: Queries return no results

**Solution:**
- Verify data was loaded to Redshift
- Check table names match exactly (case-sensitive)
- Verify Space has correct data sources selected
- Test with simpler queries first

### Issue: Agent gives wrong answers

**Solution:**
- Review agent instructions
- Make instructions more specific
- Add examples to instructions
- Verify data sources are correct for that Space

### Issue: Excel files not indexed

**Solution:**
- Verify files uploaded to S3
- Check file format is .xlsx (not .xls)
- Ensure files aren't password protected
- Wait for indexing to complete

---

## 📞 Next Steps

Once configuration is complete:

1. ✅ **Phase 3 Complete:** Quick Suite Configuration
2. ➡️ **Phase 4:** Testing & Validation (Days 13-20)
3. ➡️ **Phase 5:** Teams Integration (Optional)
4. ➡️ **Phase 6:** Automation & Workflows (Optional)

---

**Congratulations! Your Quick Suite POC is now configured and ready for testing! 🎉**

**You can now:**
- Ask questions in natural language
- Get insights from 140K+ records
- Reference business policies
- Combine data from multiple sources
- Demonstrate to stakeholders

**Next:** Start comprehensive testing and collect metrics for your POC report.
