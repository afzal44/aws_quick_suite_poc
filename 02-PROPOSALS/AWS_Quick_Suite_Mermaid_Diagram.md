# AWS Quick Suite Architecture - Mermaid Diagrams

## Main Architecture Diagram

```mermaid
graph TB
    subgraph AQS["AWS QUICK SUITE PLATFORM<br/>(DXL AWS Tenancy - Secure & Governed)"]
        QI[Quick Index<br/>Unified Knowledge<br/>Foundation]
        QR[Quick Research<br/>AI Analysis Agent]
        QS[Quick Sight<br/>Conversational BI<br/>& Dashboards]
        QA[Quick Automate & Flows<br/>Workflow Engine<br/>Event Triggers<br/>Multi-Agent Orchestration]
        CA[Chat Agents<br/>FitMap Assistant<br/>Sales Assistant<br/>Merch Intelligence]
    end
    
    subgraph STRUCT["STRUCTURED DATA LAYER"]
        RS[(Redshift<br/>Sales Data<br/>FitMap Metrics)]
        ATH[(Athena<br/>Query Lake<br/>Analytics)]
        RDS[(RDS/Aurora<br/>Transactional<br/>Data)]
        DDB[(DynamoDB<br/>Real-time<br/>Events)]
    end
    
    subgraph UNSTRUCT["UNSTRUCTURED DATA LAYER"]
        S3[Amazon S3<br/>Documents<br/>Reports<br/>Images]
        SP[SharePoint<br/>Policies<br/>Procedures<br/>Knowledge]
        OL[Outlook/Exchange<br/>Emails<br/>Calendars]
        GD[Google Drive<br/>Shared Files<br/>Collaboration]
    end
    
    subgraph APPS["ENTERPRISE APPLICATIONS"]
        CRM[CRM Salesforce<br/>Customers<br/>Opportunities]
        ERP[ERP<br/>Inventory<br/>Orders<br/>Supply Chain]
        POS[Omniful POS<br/>Real-time Sales<br/>Store Data]
        JIRA[Jira<br/>Task Management<br/>Workflows<br/>Tickets]
        PE[Pricing Engine<br/>Dynamic Pricing]
        IMS[Inventory Mgmt<br/>Stock Levels]
        FM[FitMap API<br/>Body Measurements<br/>Size Recommendations]
        SL[Slack<br/>Alerts<br/>Notifications]
    end
    
    subgraph EXT["EXTERNAL DATA SOURCES"]
        WEB[Web Data<br/>Trends<br/>Research<br/>News]
        MKT[Market Data<br/>Industry<br/>Forecasts]
        COMP[Competitor Intel<br/>Pricing<br/>Products]
        REG[Regulatory Data<br/>Compliance<br/>Updates]
    end
    
    subgraph AWS["AWS FOUNDATION SERVICES"]
        BR[Bedrock<br/>LLM Models<br/>Gen AI]
        SM[SageMaker<br/>Custom ML<br/>Training]
        LM[Lambda<br/>Functions<br/>Execution]
        EB[EventBridge<br/>Event Triggers<br/>Automation]
    end
    
    subgraph UI["USER INTERFACES"]
        EMB[Embedded Chat<br/>In POS/CRM/Apps]
        WEB_UI[Quick Suite Web<br/>Dashboards<br/>Reports<br/>Admin Console]
        MOB[Mobile Access<br/>Field Teams<br/>Store Managers<br/>Sales Reps]
    end
    
    %% Connections from Data Sources to Quick Suite
    RS --> QI
    ATH --> QI
    RDS --> QI
    DDB --> QI
    S3 --> QI
    SP --> QI
    OL --> QI
    GD --> QI
    CRM --> QI
    ERP --> QI
    POS --> QI
    JIRA --> QI
    PE --> QI
    IMS --> QI
    FM --> QI
    SL --> QI
    WEB --> QR
    MKT --> QR
    COMP --> QR
    REG --> QR
    
    %% Quick Suite Internal Connections
    QI --> QR
    QI --> QS
    QI --> QA
    QR --> QA
    QS --> QA
    QI --> CA
    QR --> CA
    QS --> CA
    
    %% AWS Foundation to Quick Suite
    BR --> QR
    BR --> CA
    SM --> QA
    LM --> QA
    EB --> QA
    
    %% Quick Suite to Actions
    QA --> PE
    QA --> IMS
    QA --> ERP
    QA --> SL
    QA --> JIRA
    CA --> EMB
    CA --> WEB_UI
    CA --> MOB
    
    %% Styling
    classDef quicksuite fill:#FF9900,stroke:#232F3E,stroke-width:3px,color:#fff
    classDef data fill:#3B48CC,stroke:#232F3E,stroke-width:2px,color:#fff
    classDef apps fill:#147EBA,stroke:#232F3E,stroke-width:2px,color:#fff
    classDef aws fill:#232F3E,stroke:#FF9900,stroke-width:2px,color:#fff
    classDef ui fill:#7AA116,stroke:#232F3E,stroke-width:2px,color:#fff
    
    class QI,QR,QS,QA,CA quicksuite
    class RS,ATH,RDS,DDB,S3,SP,OL,GD data
    class CRM,ERP,POS,JIRA,PE,IMS,FM,SL,WEB,MKT,COMP,REG apps
    class BR,SM,LM,EB aws
    class EMB,WEB_UI,MOB ui
```

## Flow 1: Autonomous Restock-to-Price Adjustment (A-RPA)

```mermaid
flowchart LR
    IMS[Inventory Management<br/>System]
    QI[Quick Index]
    QAA[Quick Automate<br/>Agent]
    DETECT{Detects:<br/>Low Stock Alert}
    PE[Pricing Engine<br/>Dynamic Price ↑]
    CMS[Merchandising CMS<br/>Update Product Page]
    LOG[Logistics System<br/>Priority Restock]
    SLACK[Slack Alert]
    
    IMS --> QI
    QI --> QAA
    QAA --> DETECT
    DETECT --> PE
    DETECT --> CMS
    PE --> SLACK
    CMS --> SLACK
    SLACK --> LOG
    
    classDef source fill:#3B48CC,stroke:#232F3E,stroke-width:2px,color:#fff
    classDef agent fill:#FF9900,stroke:#232F3E,stroke-width:3px,color:#fff
    classDef action fill:#147EBA,stroke:#232F3E,stroke-width:2px,color:#fff
    classDef alert fill:#7AA116,stroke:#232F3E,stroke-width:2px,color:#fff
    
    class IMS source
    class QI,QAA,DETECT agent
    class PE,CMS,LOG action
    class SLACK alert
```

## Flow 2: FitMap Intelligence Query

```mermaid
flowchart TD
    USER[User Query:<br/>'What are Q4 sizing trends<br/>for customers 35-50?']
    QRA[Quick Research<br/>Agent]
    FM[FitMap API]
    RS[Redshift Data]
    S3[S3 Reports]
    SYN[Synthesized Report<br/>Generated in 2 minutes]
    CHAT[Delivered via<br/>Chat Interface]
    
    USER --> QRA
    QRA --> FM
    QRA --> RS
    QRA --> S3
    FM --> SYN
    RS --> SYN
    S3 --> SYN
    SYN --> CHAT
    
    classDef user fill:#7AA116,stroke:#232F3E,stroke-width:2px,color:#fff
    classDef agent fill:#FF9900,stroke:#232F3E,stroke-width:3px,color:#fff
    classDef data fill:#3B48CC,stroke:#232F3E,stroke-width:2px,color:#fff
    classDef output fill:#147EBA,stroke:#232F3E,stroke-width:2px,color:#fff
    
    class USER user
    class QRA agent
    class FM,RS,S3 data
    class SYN,CHAT output
```

## Flow 3: Sales Assistant (Embedded in POS)

```mermaid
flowchart TD
    SR[Sales Rep in POS]
    EC[Embedded Chat Agent]
    QUERY['Show customer purchase<br/>history + FitMap profile']
    QI[Quick Index Queries]
    CRM[CRM<br/>Customer Data]
    FM[FitMap API<br/>Body Measurements]
    OH[Order History<br/>Redshift]
    PC[Product Catalog<br/>S3]
    RESP[Instant Response<br/>in POS Interface]
    REC[Personalized Size<br/>Recommendations]
    
    SR --> EC
    EC --> QUERY
    QUERY --> QI
    QI --> CRM
    QI --> FM
    QI --> OH
    QI --> PC
    CRM --> RESP
    FM --> RESP
    OH --> RESP
    PC --> RESP
    RESP --> REC
    
    classDef user fill:#7AA116,stroke:#232F3E,stroke-width:2px,color:#fff
    classDef agent fill:#FF9900,stroke:#232F3E,stroke-width:3px,color:#fff
    classDef data fill:#3B48CC,stroke:#232F3E,stroke-width:2px,color:#fff
    classDef output fill:#147EBA,stroke:#232F3E,stroke-width:2px,color:#fff
    
    class SR user
    class EC,QI agent
    class CRM,FM,OH,PC data
    class QUERY,RESP,REC output
```

## Flow 4: Automated Financial Reporting

```mermaid
flowchart TD
    EB[EventBridge Trigger<br/>Monthly Schedule]
    QAF[Quick Automate<br/>Flow]
    RQ[Redshift Query<br/>Sales Metrics]
    S3D[S3 Documents<br/>Policy Manual]
    GEN[Generate Executive<br/>Report]
    OUT[Distribute via<br/>Outlook]
    SP[Post to<br/>SharePoint]
    SL[Slack<br/>Notification]
    
    EB --> QAF
    QAF --> RQ
    QAF --> S3D
    RQ --> GEN
    S3D --> GEN
    GEN --> OUT
    GEN --> SP
    GEN --> SL
    
    classDef trigger fill:#232F3E,stroke:#FF9900,stroke-width:2px,color:#fff
    classDef agent fill:#FF9900,stroke:#232F3E,stroke-width:3px,color:#fff
    classDef data fill:#3B48CC,stroke:#232F3E,stroke-width:2px,color:#fff
    classDef output fill:#147EBA,stroke:#232F3E,stroke-width:2px,color:#fff
    
    class EB trigger
    class QAF agent
    class RQ,S3D data
    class GEN,OUT,SP,SL output
```

## Security & Governance Layer

```mermaid
flowchart TD
    IAM[IAM & ACCESS CONTROL<br/>• Role-Based Access RBAC<br/>• Data Source Permissions<br/>• Agent Action Boundaries]
    AUDIT[AUDIT & COMPLIANCE<br/>• CloudTrail Logging<br/>• Action Transparency<br/>• Data Lineage Tracking]
    GOV[DATA GOVERNANCE<br/>• Runs in DXL AWS Tenancy<br/>• No Data Leaves Environment<br/>• Full Control & Sovereignty]
    
    IAM --> AUDIT
    AUDIT --> GOV
    
    classDef security fill:#DD344C,stroke:#232F3E,stroke-width:3px,color:#fff
    
    class IAM,AUDIT,GOV security
```

## Simplified High-Level Architecture

```mermaid
graph TB
    subgraph Users["👥 USERS"]
        U1[Store Managers]
        U2[Sales Reps]
        U3[Analysts]
        U4[Executives]
    end
    
    subgraph QuickSuite["🤖 AWS QUICK SUITE"]
        direction LR
        Index[Quick Index]
        Research[Quick Research]
        Sight[Quick Sight]
        Automate[Quick Automate]
        Agents[Chat Agents]
    end
    
    subgraph Data["💾 DATA SOURCES"]
        D1[(Redshift)]
        D2[(S3)]
        D3[FitMap API]
        D4[CRM/ERP]
    end
    
    subgraph Actions["⚡ ACTIONS"]
        A1[Pricing Engine]
        A2[Inventory System]
        A3[Notifications]
        A4[Reports]
    end
    
    Users --> QuickSuite
    Data --> QuickSuite
    QuickSuite --> Actions
    
    classDef userStyle fill:#7AA116,stroke:#232F3E,stroke-width:2px,color:#fff
    classDef suiteStyle fill:#FF9900,stroke:#232F3E,stroke-width:3px,color:#fff
    classDef dataStyle fill:#3B48CC,stroke:#232F3E,stroke-width:2px,color:#fff
    classDef actionStyle fill:#147EBA,stroke:#232F3E,stroke-width:2px,color:#fff
    
    class U1,U2,U3,U4 userStyle
    class Index,Research,Sight,Automate,Agents suiteStyle
    class D1,D2,D3,D4 dataStyle
    class A1,A2,A3,A4 actionStyle
```

---

## How to Use These Diagrams

### Option 1: Mermaid Live Editor
1. Go to https://mermaid.live/
2. Copy any diagram code above
3. Paste into the editor
4. Export as PNG, SVG, or PDF

### Option 2: Draw.io with Mermaid Plugin
1. Go to https://app.diagrams.net/
2. Click "Arrange" → "Insert" → "Advanced" → "Mermaid"
3. Paste the Mermaid code
4. Click "Insert"

### Option 3: VS Code with Mermaid Extension
1. Install "Markdown Preview Mermaid Support" extension
2. Create a .md file with the Mermaid code
3. Preview the markdown file
4. Right-click diagram to export

### Option 4: GitHub/GitLab
- Both platforms natively render Mermaid diagrams in markdown files
- Just commit the .md file with Mermaid code blocks

---

## Color Legend

- 🟠 **Orange (#FF9900)**: AWS Quick Suite Components
- 🔵 **Blue (#3B48CC)**: Data Sources
- 🔷 **Light Blue (#147EBA)**: Enterprise Applications & Actions
- ⬛ **Dark (#232F3E)**: AWS Foundation Services
- 🟢 **Green (#7AA116)**: User Interfaces
- 🔴 **Red (#DD344C)**: Security & Governance
