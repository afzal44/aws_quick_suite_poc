# AWS Quick Suite Pricing Breakdown for DXL
## Two-Phase Deployment Pricing

---

## Pricing Calculation Methodology

### Phase 1: 30-Day POC (Proof of Concept)
- **Users**: 3-5 users (pilot team)
- **Duration**: 30 days
- **Custom Chat Agents**: 5 agents
- **SPICE Storage**: 100 GB (pilot data)

### Phase 2: Full Production Deployment
- **Users**: 20 users (full deployment)
- **Custom Chat Agents**: 5 agents
- **SPICE Storage**: 200 GB (production data)

---

## PHASE 1: 30-DAY POC PRICING

### 1. AWS Quick Suite Core Platform (POC)

| Component | Quantity | Unit Price | Monthly Cost |
|-----------|----------|------------|--------------|
| Quick Suite Enterprise Users | 5 users | $50/user/month | $250 |
| Quick Research Agent | Included | - | - |
| Quick Automate & Flows | Included | - | - |
| Custom Chat Agents | 5 agents | $500/agent/month | $2,500 |

**POC Platform Subtotal: $2,750/month**

---

### 2. Quick Sight BI Capabilities (POC)

#### Author Licenses (Dashboard Creators)
- **Users**: 2 analysts/developers
- **Price**: $24/user/month
- **Monthly Cost**: 2 × $24 = **$48**

#### Reader Licenses (Business Users)
- **Users**: 3 business users (view-only)
- **Price**: $5/user/month
- **Monthly Cost**: 3 × $5 = **$15**

#### SPICE Storage
- **Data Volume**: 100 GB (pilot datasets)
- **Price**: $0.38/GB/month
- **Monthly Cost**: 100 × $0.38 = **$38**

#### Pixel-Perfect Reports
- **Report Units**: 500 units/month (minimum)
- **Price**: $1/report unit/month
- **Monthly Cost**: **$500**

#### Alerts & Anomaly Detection
- **Metrics Evaluated**: 20 metrics/month
- **Price**: ~$0.50/metric/month (estimated)
- **Monthly Cost**: **$10**

**POC Quick Sight Subtotal: $611/month**

---

### 3. AWS Foundation Services (POC)

#### Amazon Bedrock (LLM/Gen AI)
- **Usage**: 50,000 tokens/day for 5 chat agents
- **Model**: Claude 3 Sonnet (estimated)
- **Price**: ~$0.003/1K input tokens, $0.015/1K output tokens
- **Monthly Cost**: **$300**

#### AWS Lambda (Serverless Functions)
- **Invocations**: 500,000/month (automation triggers)
- **Price**: $0.20/1M requests + compute time
- **Monthly Cost**: **$20**

#### Amazon EventBridge
- **Events**: 200,000 events/month (workflow triggers)
- **Price**: $1.00/million events
- **Monthly Cost**: **$1**

**POC AWS Services Subtotal: $321/month**

---

### **TOTAL POC COST (30 DAYS): $3,682**

---

## PHASE 2: FULL PRODUCTION DEPLOYMENT PRICING

### 1. AWS Quick Suite Core Platform (Production)

| Component | Quantity | Unit Price | Monthly Cost | Annual Cost |
|-----------|----------|------------|--------------|-------------|
| Quick Suite Enterprise Users | 20 users | $50/user/month | $1,000 | $12,000 |
| Quick Research Agent | Included | - | - | - |
| Quick Automate & Flows | Included | - | - | - |
| Custom Chat Agents | 5 agents | $500/agent/month | $2,500 | $30,000 |

**Production Platform Subtotal: $3,500/month = $42,000/year**

---

### 2. Quick Sight BI Capabilities (Production)

#### Author Licenses (Dashboard Creators)
- **Users**: 5 analysts/developers
- **Price**: $24/user/month
- **Monthly Cost**: 5 × $24 = $120
- **Annual Cost**: **$1,440**

#### Reader Licenses (Business Users)
- **Users**: 15 business users (view-only)
- **Price**: $5/user/month
- **Monthly Cost**: 15 × $5 = $75
- **Annual Cost**: **$900**

#### SPICE Storage
- **Data Volume**: 200 GB (production datasets)
- **Price**: $0.38/GB/month
- **Monthly Cost**: 200 × $0.38 = $76
- **Annual Cost**: **$912**

#### Pixel-Perfect Reports
- **Report Units**: 500 units/month (minimum)
- **Price**: $1/report unit/month
- **Monthly Cost**: $500
- **Annual Cost**: **$6,000**

#### Alerts & Anomaly Detection
- **Metrics Evaluated**: 50 metrics/month
- **Price**: ~$0.50/metric/month (estimated)
- **Monthly Cost**: $25
- **Annual Cost**: **$300**

**Production Quick Sight Subtotal: $796/month = $9,552/year**

---

### 3. AWS Foundation Services (Production)

#### Amazon Bedrock (LLM/Gen AI)
- **Usage**: 200,000 tokens/day for 5 chat agents
- **Model**: Claude 3 Sonnet (estimated)
- **Price**: ~$0.003/1K input tokens, $0.015/1K output tokens
- **Monthly Cost**: ~$1,200
- **Annual Cost**: **$14,400**

#### AWS Lambda (Serverless Functions)
- **Invocations**: 2 million/month (automation triggers)
- **Price**: $0.20/1M requests + compute time
- **Monthly Cost**: ~$60
- **Annual Cost**: **$720**

#### Amazon EventBridge
- **Events**: 1 million events/month (workflow triggers)
- **Price**: $1.00/million events
- **Monthly Cost**: $1
- **Annual Cost**: **$12**

**Production AWS Services Subtotal: $1,261/month = $15,132/year**

---

## TOTAL COST SUMMARY

### Phase 1: POC (30 Days)
| Category | Cost |
|----------|------|
| Quick Suite Platform (5 users + 5 agents) | $2,750 |
| Quick Sight BI | $611 |
| AWS Services (Bedrock, Lambda, EventBridge) | $321 |
| **TOTAL POC COST (30 DAYS)** | **$3,682** |

---

### Phase 2: Full Production Deployment (Annual)
| Category | Monthly Cost | Annual Cost |
|----------|--------------|-------------|
| **Quick Suite Platform** (20 users + 5 agents) | $3,500 | $42,000 |
| **Quick Sight BI** | $796 | $9,552 |
| **AWS Services** (Bedrock, Lambda, EventBridge) | $1,261 | $15,132 |
| **TOTAL PRODUCTION COST** | **$5,557/month** | **$66,684/year** |

---

## COST BREAKDOWN BY PERCENTAGE (Production)

```
Quick Suite Platform:     63%  ($42,000)
AWS Bedrock (Gen AI):     22%  ($14,400)
Quick Sight BI:          14%  ($9,552)
Lambda & EventBridge:     1%   ($732)
```

---

## YEAR 1 TOTAL INVESTMENT

| Item | Cost |
|------|------|
| **POC (30 Days)** | $3,682 |
| **Production (11 Months)** | $61,127 |
| **QloudX Implementation Services** | $50,000 |
| **Training & Change Management** | $15,000 |
| **TOTAL YEAR 1 INVESTMENT** | **$129,809** |

---

## COST SCALING SCENARIOS

### Year 2: Moderate Growth
- **Users**: 20 → 30 users (+50%)
- **SPICE Storage**: 200GB → 300GB
- **Chat Agents**: 5 agents (same)
- **Estimated Annual Cost**: **$78,000 - $85,000**

### Year 3: Expanded Deployment
- **Users**: 30 → 50 users (+67%)
- **SPICE Storage**: 300GB → 500GB
- **Chat Agents**: 5 → 8 agents
- **Estimated Annual Cost**: **$105,000 - $120,000**

---

## ROI JUSTIFICATION

### Cost Savings (Annual)
| Benefit | Estimated Savings |
|---------|-------------------|
| Analyst time savings (90% reduction) | $120,000 |
| Reduced manual reporting effort | $50,000 |
| Faster decision-making (opportunity cost) | $100,000 |
| Margin optimization (10-15% improvement) | $300,000+ |
| Reduced stockouts/overstock | $150,000 |
| **Total Annual Benefit** | **$720,000+** |

### ROI Calculation
- **Total Year 1 Investment**: $129,809
- **Annual Benefit**: $720,000
- **Net Benefit Year 1**: $590,191
- **ROI**: 455% (4.55x return)
- **Payback Period**: ~2 months

---

## DETAILED PRICING BREAKDOWN TABLE

### POC Phase (30 Days)
| Line Item | Quantity | Unit Price | Total |
|-----------|----------|------------|-------|
| Quick Suite User Licenses | 5 users | $50/user/month | $250 |
| Custom Chat Agents | 5 agents | $500/agent/month | $2,500 |
| QuickSight Author Licenses | 2 users | $24/user/month | $48 |
| QuickSight Reader Licenses | 3 users | $5/user/month | $15 |
| SPICE Storage | 100 GB | $0.38/GB/month | $38 |
| Pixel-Perfect Reports | 500 units | $1/unit/month | $500 |
| Alerts & Anomaly Detection | 20 metrics | $0.50/metric/month | $10 |
| Amazon Bedrock (Gen AI) | ~50K tokens/day | Variable | $300 |
| AWS Lambda | 500K invocations | $0.20/1M | $20 |
| Amazon EventBridge | 200K events | $1/1M events | $1 |
| **POC TOTAL (30 DAYS)** | | | **$3,682** |

### Production Phase (Annual)
| Line Item | Quantity | Unit Price | Monthly | Annual |
|-----------|----------|------------|---------|--------|
| Quick Suite User Licenses | 20 users | $50/user/month | $1,000 | $12,000 |
| Custom Chat Agents | 5 agents | $500/agent/month | $2,500 | $30,000 |
| QuickSight Author Licenses | 5 users | $24/user/month | $120 | $1,440 |
| QuickSight Reader Licenses | 15 users | $5/user/month | $75 | $900 |
| SPICE Storage | 200 GB | $0.38/GB/month | $76 | $912 |
| Pixel-Perfect Reports | 500 units | $1/unit/month | $500 | $6,000 |
| Alerts & Anomaly Detection | 50 metrics | $0.50/metric/month | $25 | $300 |
| Amazon Bedrock (Gen AI) | ~200K tokens/day | Variable | $1,200 | $14,400 |
| AWS Lambda | 2M invocations | $0.20/1M | $60 | $720 |
| Amazon EventBridge | 1M events | $1/1M events | $1 | $12 |
| **PRODUCTION TOTAL** | | | **$5,557** | **$66,684** |

---

## PRICING NOTES & ASSUMPTIONS

1. **Quick Suite Platform pricing**: $50/user/month for full platform access (Quick Index, Research, Sight, Automate)

2. **Custom Chat Agents**: $500/agent/month (5 specialized agents: FitMap Assistant, Sales Assistant, Merchandising Intelligence, Customer Service, Financial Reporting)

3. **AWS Bedrock costs**: Based on Claude 3 Sonnet pricing (~$0.003/1K input, $0.015/1K output tokens)
   - POC: ~50,000 tokens/day = ~1.5M tokens/month
   - Production: ~200,000 tokens/day = ~6M tokens/month

4. **SPICE storage**: Optional but recommended for fast dashboard performance
   - POC: 100 GB for pilot datasets
   - Production: 200 GB for production datasets

5. **Pixel-Perfect Reports**: 500-unit minimum ($500/month) for formatted, scheduled reports

6. **Data source costs NOT included**: Assumes existing Redshift, S3, Athena, RDS infrastructure
   - No incremental cost for data sources
   - Only Quick Suite platform and compute costs included

7. **Pricing is subject to change**: AWS updates pricing regularly. Recommend quarterly reviews.

8. **Volume discounts**: May be available for 1-3 year enterprise commitments

---

## COST OPTIMIZATION RECOMMENDATIONS

1. **Start with POC**: 30-day pilot with 3-5 users validates ROI before full commitment
2. **Phased User Rollout**: Start with 20 users, expand to 30-50 based on adoption
3. **SPICE Optimization**: Only cache frequently-accessed datasets to minimize storage costs
4. **Monitor Bedrock Usage**: Track token consumption and optimize prompts for efficiency
5. **Right-size Chat Agents**: Start with 5 agents, add more only as needed
6. **Annual Commitment**: Consider 1-year reserved capacity for potential 20-30% savings

---

## COMPARISON TO ALTERNATIVES

| Solution | Year 1 Cost | Users | Implementation | Notes |
|----------|-------------|-------|----------------|-------|
| **AWS Quick Suite** | **$129,809** | 20 | 30-60 days | Recommended - Fast ROI |
| Custom Build | $400,000+ | Unlimited | 12-18 months | High risk, maintenance burden |
| Microsoft Power BI + Azure | $150,000+ | 20 | 6-9 months | Requires Azure migration |
| Tableau + Einstein | $120,000+ | 20 | 4-6 months | Limited agentic AI capabilities |

---

*Pricing calculated: December 3, 2025*  
*Based on AWS Quick Suite pricing page: https://aws.amazon.com/quicksuite/pricing/*  
*Actual costs may vary based on usage patterns and AWS pricing updates*
