# Knowledge Base Excel Files Guide

## 📚 Overview

These Excel files contain **business policies, procedures, and reference information** that Quick Suite can use to answer questions about your business operations, policies, and best practices.

---

## 📁 Files Generated

### 1. **Business_Policies_Rules.xlsx** (5 sheets)

**Purpose:** Core business policies that govern operations

**Sheets:**
- **Return Policy** - Return rules, conditions, refund types
- **Discount Policy** - All discount programs and eligibility
- **Shipping Policy** - Shipping options, costs, delivery times
- **Price Match** - Price matching rules and conditions
- **Loyalty Program** - Rewards tiers and benefits

**Sample Questions Quick Suite Can Answer:**
- "What's our return policy for FitMap purchases?"
- "Can VIP customers stack discounts?"
- "What's the free shipping threshold?"
- "Do we price match competitors?"
- "What benefits do Gold members get?"

---

### 2. **Product_Specifications_Care.xlsx** (4 sheets)

**Purpose:** Product care, fit guidance, and quality standards

**Sheets:**
- **Fabric Care** - Washing, drying, ironing instructions by fabric
- **Fit Guide** - Fit types and recommendations
- **Alteration Services** - Available alterations, pricing, turnaround
- **Quality Standards** - Quality control specifications

**Sample Questions Quick Suite Can Answer:**
- "How do I care for wool garments?"
- "What's the difference between slim fit and regular fit?"
- "How much does hemming pants cost?"
- "What quality standards do we have for shirts?"
- "Can I machine wash silk?"

---

### 3. **FitMap_Guidelines_Best_Practices.xlsx** (4 sheets)

**Purpose:** FitMap scanning procedures and troubleshooting

**Sheets:**
- **Scanning Best Practices** - How to prepare for accurate scans
- **Accuracy Guidelines** - Expected accuracy by measurement
- **Recommendation Logic** - How size recommendations work
- **Troubleshooting** - Common issues and solutions

**Sample Questions Quick Suite Can Answer:**
- "How should customers prepare for a FitMap scan?"
- "What's the expected accuracy for waist measurements?"
- "How does FitMap recommend dress shirt sizes?"
- "What should I do if a scan fails?"
- "Why might a FitMap recommendation not fit?"

---

### 4. **Employee_Training_Procedures.xlsx** (3 sheets)

**Purpose:** Employee training, scripts, and procedures

**Sheets:**
- **Customer Service Scripts** - Greeting, FitMap intro, handling returns
- **Sales Techniques** - Upselling, cross-selling, conversion tactics
- **Store Procedures** - Opening/closing checklists

**Sample Questions Quick Suite Can Answer:**
- "How should I greet customers?"
- "What's the script for introducing FitMap?"
- "What are effective upselling techniques?"
- "What's the store opening procedure?"
- "How do I handle a return?"

---

## 🚀 Setup Instructions

### Step 1: Generate Excel Files

```bash
cd poc_data_generators
python generate_knowledge_base_excel.py
```

**Output:** 4 Excel files with 16 total sheets

---

### Step 2: Upload to Quick Suite

1. **Open Quick Suite Console**
2. **Navigate to Knowledge Base** (or Spaces)
3. **Create a new Space** (or use existing):
   - Name: `Business Knowledge Base`
   - Description: `Policies, procedures, and guidelines`

4. **Upload Files:**
   - Click "Upload Documents"
   - Select all 4 Excel files
   - Wait for processing (Quick Suite will extract all sheets)

5. **Verify Upload:**
   - Check that all sheets are indexed
   - Test with sample questions

---

### Step 3: Configure Access

1. **Add Users:**
   - Add employees who need policy information
   - Add managers who need training materials

2. **Set Permissions:**
   - Read-only for most users
   - Edit access for policy managers

---

## 🔍 Sample Queries

### Policy Questions

```
"What's our return policy?"
→ Returns Business_Policies_Rules.xlsx > Return Policy sheet

"Can military members get a discount?"
→ Returns Business_Policies_Rules.xlsx > Discount Policy sheet

"How much is express shipping?"
→ Returns Business_Policies_Rules.xlsx > Shipping Policy sheet

"What are the loyalty program tiers?"
→ Returns Business_Policies_Rules.xlsx > Loyalty Program sheet
```

---

### Product Care Questions

```
"How do I wash a cotton shirt?"
→ Returns Product_Specifications_Care.xlsx > Fabric Care sheet

"What fit type is best for athletic builds?"
→ Returns Product_Specifications_Care.xlsx > Fit Guide sheet

"How much does sleeve hemming cost?"
→ Returns Product_Specifications_Care.xlsx > Alteration Services sheet
```

---

### FitMap Questions

```
"How should customers prepare for FitMap scanning?"
→ Returns FitMap_Guidelines_Best_Practices.xlsx > Scanning Best Practices

"What's the accuracy of chest measurements?"
→ Returns FitMap_Guidelines_Best_Practices.xlsx > Accuracy Guidelines

"Why did a scan fail?"
→ Returns FitMap_Guidelines_Best_Practices.xlsx > Troubleshooting
```

---

### Training Questions

```
"How should I greet customers?"
→ Returns Employee_Training_Procedures.xlsx > Customer Service Scripts

"What's an effective cross-selling technique?"
→ Returns Employee_Training_Procedures.xlsx > Sales Techniques

"What's the store opening checklist?"
→ Returns Employee_Training_Procedures.xlsx > Store Procedures
```

---

## 💡 Use Cases

### 1. **Customer Service Agent**
**Scenario:** Customer asks about return policy

**Query:** "Can I return an item after 60 days?"

**Quick Suite Response:**
- Searches Business_Policies_Rules.xlsx
- Finds Return Policy sheet
- Returns: "Standard returns are accepted within 60 days. After 60 days, returns are not accepted unless the item is defective."

---

### 2. **Store Associate**
**Scenario:** Customer unsure about fabric care

**Query:** "How do I care for this wool sweater?"

**Quick Suite Response:**
- Searches Product_Specifications_Care.xlsx
- Finds Fabric Care sheet
- Returns: "Wool should be hand washed in cold water or dry cleaned. Lay flat to dry. Do not wring or twist. Steam iron only."

---

### 3. **FitMap Technician**
**Scenario:** Scan keeps failing

**Query:** "Customer's scan won't complete, what should I check?"

**Quick Suite Response:**
- Searches FitMap_Guidelines_Best_Practices.xlsx
- Finds Troubleshooting sheet
- Returns: "Common causes: 1) Poor lighting - move to well-lit area, 2) Incorrect distance - adjust to 6 feet, 3) Movement - ask customer to remain still"

---

### 4. **New Employee**
**Scenario:** Learning how to introduce FitMap

**Query:** "What should I say when introducing FitMap to customers?"

**Quick Suite Response:**
- Searches Employee_Training_Procedures.xlsx
- Finds Customer Service Scripts sheet
- Returns: "Have you tried our FitMap body scanning? It takes 30 seconds and ensures perfect fit every time."

---

## 📊 Data Structure

### Excel File Format

Each Excel file contains multiple sheets with structured data:

```
Business_Policies_Rules.xlsx
├── Return Policy (5 policies)
├── Discount Policy (5 discount types)
├── Shipping Policy (5 shipping options)
├── Price Match (2 policies)
└── Loyalty Program (4 tiers)
```

### Column Structure

Each sheet has relevant columns:

**Return Policy:**
- Policy_ID, Policy_Name, Category, Description
- Conditions, Refund_Type, Processing_Days, Exceptions

**Discount Policy:**
- Policy_ID, Policy_Name, Category, Discount_Percent
- Eligibility, Stackable, Exclusions, Valid_Until

---

## 🔧 Updating Knowledge Base

### To Update Policies:

1. **Edit the generator script:**
   ```python
   # Edit: generate_knowledge_base_excel.py
   # Update policy data
   ```

2. **Regenerate files:**
   ```bash
   python generate_knowledge_base_excel.py
   ```

3. **Re-upload to Quick Suite:**
   - Delete old files (optional)
   - Upload new versions
   - Quick Suite will re-index automatically

---

## 🎯 Benefits

### 1. **Consistent Answers**
- All employees get same policy information
- No conflicting answers to customers
- Always up-to-date information

### 2. **Faster Training**
- New employees can query policies instantly
- No need to memorize everything
- Self-service learning

### 3. **Better Customer Service**
- Quick answers to policy questions
- Accurate information every time
- Reduced escalations

### 4. **Compliance**
- Documented policies
- Audit trail of policy versions
- Consistent enforcement

---

## 📈 Advanced Features

### Cross-Reference Queries

Quick Suite can combine information from multiple files:

```
"If a Gold member returns an item, what's the process?"
→ Combines:
   - Business_Policies_Rules.xlsx > Return Policy
   - Business_Policies_Rules.xlsx > Loyalty Program
→ Returns: "Gold members can return items within 60 days with free return shipping. Processing takes 7 days for full refund."
```

---

### Contextual Answers

Quick Suite understands context:

```
"What about wool?"
(After asking about fabric care)
→ Returns wool-specific care instructions
```

---

## ✅ Verification Checklist

- [ ] All 4 Excel files generated
- [ ] Files contain expected number of sheets
- [ ] Data looks correct in Excel
- [ ] Files uploaded to Quick Suite
- [ ] Quick Suite finished indexing
- [ ] Test queries return correct answers
- [ ] Users have appropriate access

---

## 📞 Support

### Common Issues

**Issue:** Quick Suite can't read Excel file
- **Solution:** Ensure file is .xlsx format (not .xls)
- **Solution:** Check file isn't password protected

**Issue:** Answers are incomplete
- **Solution:** Verify all sheets were indexed
- **Solution:** Check column headers are clear

**Issue:** Can't find specific policy
- **Solution:** Use more specific query
- **Solution:** Check policy exists in Excel file

---

## 🎓 Training Users

### Teach employees to ask:

**Good Questions:**
- "What's our return policy for FitMap purchases?"
- "How much does hemming cost for Gold members?"
- "What should I say when greeting customers?"

**Avoid Vague Questions:**
- "Tell me about returns" (too broad)
- "Policy?" (unclear what policy)
- "Help" (no context)

---

## 📝 Content Summary

| File | Sheets | Total Rows | Key Topics |
|------|--------|------------|------------|
| Business_Policies_Rules.xlsx | 5 | 22 | Returns, discounts, shipping, loyalty |
| Product_Specifications_Care.xlsx | 4 | 21 | Fabric care, fit, alterations, quality |
| FitMap_Guidelines_Best_Practices.xlsx | 4 | 26 | Scanning, accuracy, recommendations |
| Employee_Training_Procedures.xlsx | 3 | 20 | Scripts, techniques, procedures |
| **TOTAL** | **16** | **89** | **Complete business knowledge** |

---

**Your Quick Suite Knowledge Base is now ready to answer business policy and procedure questions!**

**Next Step:** Upload files to Quick Suite and start asking questions!
