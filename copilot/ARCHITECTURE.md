# FedEx DCA Intelligence Hub - Architecture & Design

## 🏗️ Solution Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    FEDEX DCA INTELLIGENCE HUB                    │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      PRESENTATION LAYER                          │
│  (Streamlit Dashboard - 7 Pages)                                │
├─────────────────────────────────────────────────────────────────┤
│  • Dashboard (KPI, Analytics, Case Queue)                        │
│  • Case Management (Create, Search, Update)                      │
│  • Workflow Management (Status, SLA Tracking)                    │
│  • DCA Performance (Agent Metrics, Deep Dive)                    │
│  • Advanced Analytics (Trends, Insights)                         │
│  • Audit Trail (Compliance, Governance)                          │
│  • Database View (Full Dataset)                                  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    BUSINESS LOGIC LAYER                          │
├─────────────────────────────────────────────────────────────────┤
│  models/scoring.py - ML & Intelligence Engine                    │
│  • Recovery Score Calculator (Multi-factor)                      │
│  • Recovery Probability Predictor                                │
│  • Priority Score Engine                                         │
│  • Risk Assessment                                               │
│  • SLA Management                                                │
│  • Expected Recovery Calculator                                  │
│  • Smart Action Recommendations                                  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      DATA LAYER                                  │
├─────────────────────────────────────────────────────────────────┤
│  CSV Files (Extensible to SQL)                                   │
│  • data/nexus_accounts.csv (Cases)                               │
│  • data/audit_log.csv (Transactions)                             │
│                                                                  │
│  Columns in Case Data:                                           │
│  - case_id, customer_name, invoice_amount                        │
│  - ageing_days, business_type, dispute_status                    │
│  - assigned_dca, sla_status, status                              │
│  - recovery_score, recovery_probability                          │
│  - priority_score, expected_recovery                             │
│  - ai_next_action, risk_level                                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📊 Data Flow

```
USER ACTION
    ↓
├─→ Add Case → Scoring Engine → ML Calculations → Data Saved
│
├─→ Update Status → Audit Logged → History Tracked → Display Updated
│
├─→ View Dashboard → Query Data → Apply Filters → Visualize → Show KPIs
│
└─→ Check Performance → Aggregate by DCA → Calculate Metrics → Show Table
```

---

## 🤖 AI/ML Scoring Pipeline

```
INPUT CASE DATA
    ↓
┌─────────────────────────────────┐
│ RECOVERY SCORE CALCULATOR       │
│ • Ageing Decay (Exponential)    │
│ • Business Multiplier           │
│ • Dispute Impact                │
│ • DCA Responsiveness            │
│ • Payment History               │
│ • SLA Penalty                   │
│ • Invoice Amount Normalization  │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│ RECOVERY PROBABILITY ADJUSTER   │
│ • Apply ageing haircut          │
│ • Risk adjustment               │
│ • Predict % likelihood          │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│ PRIORITY SCORE ENGINE           │
│ • Probability × Amount × Urgency│
│ • Higher = More Urgent          │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│ EXPECTED RECOVERY CALCULATOR    │
│ • Invoice × Recovery Probability│
│ • Currency prediction           │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│ ACTION RECOMMENDATION ENGINE    │
│ • Check blockers (disputes)     │
│ • Check escalation criteria     │
│ • Recommend next action         │
└─────────────────────────────────┘
    ↓
ENRICHED CASE OBJECT
(Ready for dashboard & reporting)
```

---

## 🎯 Key Algorithms

### 1. Recovery Score (Multi-Factor ML)

```
score = 0.5 (base)

// Ageing: Exponential decay (realistic aging penalty)
ageing_factor = e^(-0.015 × ageing_days) × 0.35

// Business segment multiplier
if business_type == "Enterprise":
    segment_boost = 0.25
elif business_type == "Large":
    segment_boost = 0.10
else:
    segment_boost = -0.05 to -0.30

// Dispute blocker
if dispute_status == "Open":
    score -= 0.40
elif dispute_status == "Pending":
    score -= 0.20

// DCA responsiveness
responsiveness = max(0, 1 - (last_update_days / 30)) × 0.20

// SLA enforcement
if sla_status == "BREACHED":
    score -= 0.25
elif sla_status == "AT_RISK":
    score -= 0.10

// Invoice normalization
invoice_factor = min(amount / 500000, 1.0) × 0.10

Final: normalize(0, 1.0)
```

**Result Range:** 0.0 (no recovery) to 1.0 (certain recovery)

### 2. Recovery Probability (%)

```
base_probability = recovery_score × 100

// Apply ageing adjustment
if ageing_days > 180:
    base_probability *= 0.6  // 40% haircut
elif ageing_days > 120:
    base_probability *= 0.75 // 25% haircut
elif ageing_days > 60:
    base_probability *= 0.9  // 10% haircut

Result: % likelihood of recovery (0-100%)
```

### 3. Priority Score (Urgency Ranking)

```
urgency_factor = 1 + (ageing_days / 180)
// Ranges from 1.0 (new) to 2.0+ (very old)

priority = recovery_probability 
         × invoice_amount 
         × urgency_factor

Higher = More Urgent
```

### 4. Risk Assessment

```
if ageing_days > 120 AND dispute_status == "Open":
    risk = CRITICAL
elif ageing_days > 120:
    risk = HIGH
elif ageing_days > 60:
    risk = MEDIUM
else:
    risk = LOW
```

---

## 📈 KPI Dashboard Calculations

```
EXECUTIVE KPIs:
├─ Portfolio Value = SUM(invoice_amount)
├─ Expected Recovery = SUM(expected_recovery)
├─ At-Risk Portfolio = SUM(where risk_level in [HIGH, CRITICAL])
├─ Avg Ageing Days = MEAN(ageing_days)
├─ SLA Breaches = COUNT(sla_status == BREACHED)
├─ Critical Cases = COUNT(risk_level == CRITICAL)
└─ Recovery Rate % = Expected Recovery / Portfolio Value

DCA PERFORMANCE METRICS:
├─ Cases Assigned = COUNT(per DCA)
├─ Portfolio Value = SUM(invoice_amount per DCA)
├─ Expected Recovery = SUM(expected_recovery per DCA)
├─ Avg Ageing = MEAN(ageing_days per DCA)
├─ Recovery Efficiency % = Expected Recovery / Portfolio Value
└─ SLA Compliant = COUNT(sla_status == OK per DCA)
```

---

## 🔄 Workflow States & Transitions

```
┌──────────┐
│ CREATED  │
└────┬─────┘
     │
     ↓
┌──────────────┐
│   ACTIVE     │ ← Initial state after creation
└────┬─────────┘
     │
     ├─→ ┌──────────────────┐
     │   │ PENDING_REVIEW   │ ← Awaiting decision
     │   └──────────────────┘
     │
     ├─→ ┌──────────────────┐
     │   │  ESCALATED       │ ← Legal/Manager review
     │   └──────────────────┘
     │
     └─→ ┌──────────────────┐
         │    CLOSED        │ ← Final (recovered/written off)
         └──────────────────┘

All transitions logged with:
- Timestamp
- User who made change
- Update notes
- Audit trail
```

---

## 🔐 Role-Based Access Control

```
┌─────────────────────────────────────────────────────────────┐
│                     ACCESS MATRIX                            │
├─────────────────────────────────────────────────────────────┤
│ Feature           │ Admin  │ DCA Agent │ Compliance Officer  │
├─────────────────────────────────────────────────────────────┤
│ Dashboard         │  ✅    │    ✅     │       ✅            │
│ Create Case       │  ✅    │    ❌     │       ❌            │
│ Update Status     │  ✅    │    ✅     │       ❌            │
│ View Analytics    │  ✅    │    ❌     │       ✅            │
│ View Audit Trail  │  ✅    │    ❌     │       ✅            │
│ View DCA Perf     │  ✅    │    ❌     │       ✅            │
│ Assign Cases      │  ✅    │    ❌     │       ❌            │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 Data Model

### Cases Table (nexus_accounts.csv)

```
case_id                 (String)    - Unique identifier
customer_name          (String)    - Enterprise/Customer
invoice_amount         (Float)     - Amount in ₹
ageing_days            (Int)       - Days in system
business_type          (String)    - Enterprise/Large/Medium/Small
dispute_status         (String)    - None/Open/Pending/Resolved
assigned_dca           (String)    - DCA_A, DCA_B, etc
last_dca_update_days   (Int)       - Days since last update
sla_status             (String)    - OK/AT_RISK/BREACHED
status                 (String)    - ACTIVE/PENDING_REVIEW/ESCALATED/CLOSED
created_date           (Timestamp) - Case creation date

AI CALCULATED FIELDS:
recovery_score         (Float)     - 0.0-1.0
recovery_probability   (Float)     - 0-100 %
priority_score         (Float)     - Urgency rank
expected_recovery      (Float)     - ₹ amount
ai_next_action         (String)    - Recommended action
risk_level             (String)    - CRITICAL/HIGH/MEDIUM/LOW
```

### Audit Log Table (audit_log.csv)

```
timestamp       (Datetime)  - When action occurred
case_id         (String)    - Which case
action          (String)    - What was done
user            (String)    - Who did it
details         (String)    - Additional notes
```

---

## 🚀 Deployment Architecture

```
LOCAL DEVELOPMENT
    ↓
├─ Python 3.10+
├─ Streamlit (UI Framework)
├─ Plotly (Visualizations)
├─ Pandas (Data Processing)
├─ NumPy (Math Operations)
└─ CSV Files (Data Storage)

PRODUCTION READY FOR:
├─ Docker Containerization
├─ Cloud Deployment (AWS/GCP/Azure)
├─ Database Migration (PostgreSQL/MongoDB)
├─ API Layer (FastAPI)
├─ CI/CD Pipeline
└─ Load Balancing & Scaling
```

---

## 🔄 Future Enhancement Roadmap

### Phase 2 (Database)
- Replace CSV with PostgreSQL
- Add data validation layer
- Implement connection pooling

### Phase 3 (Integration)
- REST API for third-party access
- Webhook notifications
- Email alerts for SLA breaches

### Phase 4 (Advanced ML)
- Linear Regression for recovery prediction
- Random Forest for risk classification
- Time series forecasting
- Anomaly detection

### Phase 5 (Automation)
- RPA for legacy system sync
- Automated escalations
- Auto-assignment to optimal DCA

### Phase 6 (Mobile)
- Mobile app for DCA agents
- Push notifications
- Offline case access

### Phase 7 (Enterprise)
- Multi-tenant support
- Custom workflows
- Advanced reporting
- BI integration (Tableau/PowerBI)

---

## 🎯 Success Metrics

### Immediate (0-3 months)
- ✅ 100% case visibility (vs manual Excel)
- ✅ Real-time dashboard (vs delayed reports)
- ✅ Automated SLA alerts (vs manual tracking)
- ✅ Complete audit trail (vs scattered emails)

### Short-term (3-6 months)
- 📈 20-30% improvement in recovery rate
- ⏰ 40% reduction in case ageing
- 📊 95%+ SLA compliance
- 🎯 Optimal DCA allocation

### Long-term (6-12 months)
- 💰 3-5x improvement in portfolio value realized
- 🔍 98%+ audit trail completeness
- 🤖 ML predictions accurate within 15%
- 🚀 Scalable to 10,000+ cases

---

## 📞 Technical Support

### Key Files:
- `app.py` - Main Streamlit application
- `models/scoring.py` - ML scoring engine
- `data/nexus_accounts.csv` - Cases data
- `data/audit_log.csv` - Audit trail

### To Run:
```bash
streamlit run app.py
```

### To Extend:
1. Add new columns to data CSV
2. Update scoring functions in models/scoring.py
3. Add new pages to app.py
4. Update audit logging

---

**Architecture Version:** 2.0
**Last Updated:** January 8, 2026
**Status:** Production Ready
