# 📊 FedEx DCA Intelligence Hub

> AI-Powered Debt Collection Agency Management & Recovery Intelligence Platform

An enterprise-grade, AI-driven decision intelligence platform for managing thousands of overdue B2B accounts through Debt Collection Agencies (DCAs). Built with **explainability, governance, and human-in-the-loop decision support** at its core.

---

## 🎯 Problem Statement

FedEx manages thousands of overdue B2B customer accounts through external Debt Collection Agencies. Traditional manual processes suffer from:

- ❌ **No visibility** into recovery progress and case status  
- ❌ **Manual prioritization** based on gut feeling, not data  
- ❌ **Weak accountability** - DCA performance largely untracked  
- ❌ **Delayed escalations** - missed SLA breaches  
- ❌ **Zero auditability** - compliance and governance gaps  
- ❌ **Inefficient allocation** - wrong cases sent to wrong DCAs  

---

## ✨ Solution: AI-Assisted Decision Engine

A **real-time intelligence platform** that orchestrates case management between FedEx and its DCAs through:

### Core Capabilities

#### 🎯 Smart Case Prioritization
- **Multi-factor recovery scoring** combining:
  - Invoice aging decay
  - Business segment analysis
  - Dispute status impact
  - DCA responsiveness metrics
  - Payment history assessment
  - SLA breach penalties
  
- **Risk classification** (Critical → Low)
- **Next-best-action recommendations**

#### 📈 Predictive Recovery Analytics
- **Recovery probability prediction** (0-100%)
- **Churn risk assessment** - identify at-risk cases before they slip
- **Optimal follow-up timing** - data-driven contact strategies
- **DCA efficiency scoring** - performance accountability
- **Confidence intervals** - explainability for every decision

#### 👥 DCA Performance Management
- Real-time performance dashboards
- Accountability metrics & KPI tracking
- Case allocation recommendations
- Performance vs. SLA compliance analysis

#### 🔍 Real-Time Dashboard & Monitoring
- **Command Center**: Live case overview with filters
- **Case Management**: Add, update, and track cases
- **Workflow & SLA Management**: SLA tracking and breach prevention
- **Advanced Analytics**: Visual insights with Plotly charts
- **Predictive AI Insights**: ML-powered recommendations
- **Live Activity Feed**: Real-time DCA updates
- **Audit Trail**: Complete compliance & governance logs

#### 🔐 Role-Based Access Control
- **Admin**: Full system access
- **Manager**: Case management and analytics
- **DCA Agent**: Case view and update
- **Finance**: Reporting and audit

---

## 🏗️ Architecture

```
fedex-dca-decision-engine/
├── app.py                          # Main Streamlit application (1600+ lines)
├── models/
│   └── scoring.py                  # ML scoring & intelligence engine
├── auth.py                         # Role-based authentication
├── audit.py                        # Audit logging & compliance
├── data/
│   ├── nexus_accounts.csv          # Synthetic case dataset
│   ├── audit_log.csv               # Audit trail
│   └── data_gen.py                 # Data generation utilities
├── requirements.txt                # Dependencies
└── docs/                           # Architecture & guides
```

---

## 🧠 ML Intelligence Features

### Recovery Score Calculation
Weighted multi-factor model:
- **Ageing Factor (35%)**: Exponential decay - older cases lose recovery potential faster
- **Business Type (15%)**: Enterprise clients score higher than SMBs
- **Dispute Status (40%)**: Open disputes significantly reduce probability
- **DCA Responsiveness (20%)**: Recent DCA updates boost confidence
- **Payment History (15%)**: Good payment history increases score
- **SLA Status (25%)**: Breached SLAs reduce priority
- **Invoice Amount (10%)**: Larger amounts increase urgency

### Predictive Models
- `compute_recovery_probability()` - Recovery likelihood (0-100%)
- `compute_churn_risk()` - Risk of case abandonment
- `compute_optimal_followup_timing()` - Best contact window
- `risk_assessment()` - Overall risk classification
- `get_predictive_insights()` - AI-powered recommendations

---

## 🚀 Key Features

| Feature | Description |
|---------|-------------|
| **Real-Time Dashboard** | Live case metrics, KPIs, and status overview |
| **Smart Filtering** | Filter by risk level, status, DCA, business type |
| **Case Management** | Create, update, track cases with auto-computed scores |
| **SLA Monitoring** | Automatic SLA tracking (OK → AT_RISK → BREACHED) |
| **DCA Accountability** | Performance tracking, efficiency scores, responsiveness metrics |
| **Predictive Analytics** | Recovery probability, churn risk, optimal timing |
| **Explainability** | Every recommendation includes confidence and reasoning |
| **Audit Trail** | Full compliance logs for regulatory requirements |
| **Indian Currency Format** | Automatic ₹ formatting for amounts |
| **Mobile Responsive** | Works on desktop and mobile devices |

---

## 💻 Technology Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Streamlit (Web UI) |
| **ML/Analytics** | Pandas, NumPy, Scikit-learn |
| **Visualization** | Plotly Express & Graph Objects |
| **Backend** | Python 3.11+ |
| **Data** | CSV-based (easily integrable with databases) |
| **Authentication** | Session-state role-based access |

---

## 📋 Dashboard Pages

1. **📊 Real-Time Command Center**
   - Live case overview with key metrics
   - Status distribution & risk breakdown
   - Quick filters for case discovery

2. **✏️ Add New Case**
   - Streamlined case entry form
   - Auto-computed recovery scores
   - Instant SLA assignment

3. **📋 Case Workflow & SLA Management**
   - Case-by-case detail view
   - Status updates & progress tracking
   - SLA status monitoring
   - Next-best-action recommendations

4. **👥 DCA Performance & Accountability**
   - DCA-wise performance metrics
   - Case allocation analysis
   - Responsiveness & efficiency scoring
   - Comparative performance charts

5. **📊 Advanced Analytics & Insights**
   - Recovery trend analysis
   - Business segment breakdown
   - Risk distribution heatmaps
   - Age-wise case distribution
   - DCA allocation optimization

6. **🧠 Predictive Analytics & AI Insights**
   - Recovery probability forecasts
   - High-risk cases identification
   - Churn risk alerts
   - Optimal timing recommendations
   - AI-powered next steps

7. **⚡ Live DCA Activity & Updates**
   - Real-time activity feed
   - DCA response tracking
   - Update timeline
   - Performance trending

8. **🔍 Compliance & Audit Trail**
   - Complete action logs
   - User activity tracking
   - Change history
   - Governance compliance reports

---

## 🔧 Installation & Setup

### Prerequisites
- Python 3.11 or higher
- pip or conda

### Local Setup

```bash
# Clone repository
git clone https://github.com/yuvadepcodes/fedex-dca-decision-engine.git
cd fedex-dca-decision-engine

# Install dependencies
pip install -r requirements.txt

# Run Streamlit app
streamlit run app.py
```

The app will be available at `http://localhost:8501`

### Docker Setup

```bash
docker build -t fedex-dca .
docker run -p 8501:8501 fedex-dca
```

---

## 🌐 Streamlit Cloud Deployment

### Quick Deploy

1. Push code to GitHub: `git push`
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Create new app:
   - Repository: `yuvadepcodes/fedex-dca-decision-engine`
   - Branch: `main`
   - Main file: `app.py`
4. Click **Deploy** → Live in 2-3 minutes!

**Live Demo**: [fedex-dca-decision-engine.streamlit.app](https://fedex-dca-decision-engine.streamlit.app)

---

## 📊 Sample Data

The app comes with **synthetic but realistic case data** (`data/nexus_accounts.csv`):

| Field | Example | Purpose |
|-------|---------|---------|
| case_id | NEXUS-001 | Unique case identifier |
| customer_name | Acme Corp | Customer reference |
| invoice_amount | ₹500,000 | Outstanding amount |
| ageing_days | 45 | Days overdue |
| business_type | Enterprise | Segment classification |
| status | ACTIVE | Current case status |
| dca_assigned | DCA-Alpha | Responsible agency |
| dispute_status | Open | Payment dispute status |
| last_dca_update_days | 7 | DCA contact recency |
| recovery_score | 0.745 | AI-computed recovery likelihood |

---

## 🎓 How It Works

### Case Scoring Pipeline

```
Raw Case Data
     ↓
Multi-Factor Scoring Engine
├─ Ageing Analysis
├─ Segment Classification
├─ Dispute Impact Assessment
├─ DCA Performance Evaluation
├─ Payment History Review
├─ SLA Status Check
└─ Amount Normalization
     ↓
Recovery Score (0-1)
     ↓
Recovery Probability (0-100%)
     ↓
Risk Classification (CRITICAL → LOW)
     ↓
Next-Best-Action Recommendation
     ↓
Dashboard & Alerts
```

### Decision Support Flow

```
1. Ingest Case Data
   ↓
2. Compute Intelligence Scores
   ↓
3. Generate Recommendations
   ↓
4. Present to Decision-Maker
   ↓
5. Log Action & Audit Trail
   ↓
6. Track Outcomes & Feedback
   ↓
7. Continuous Model Improvement
```

---

## 📈 Key Metrics

- **Total Cases**: Cases under management
- **Active Cases**: Currently open
- **Avg Recovery Score**: Mean recovery likelihood
- **High-Risk Cases**: Requires immediate attention
- **SLA Breach Rate**: % cases with breached SLAs
- **DCA Responsiveness**: Avg days since last DCA update
- **Avg Aging**: Mean days overdue
- **Recovery Probability**: Weighted average likelihood

---

## 🔐 Security & Compliance

- ✅ **Role-Based Access Control** (Admin, Manager, DCA Agent, Finance)
- ✅ **Audit Logging** (Every action logged with timestamp & user)
- ✅ **Data Governance** (Synthetic data, demo-safe)
- ✅ **SLA Compliance** (Automated SLA tracking & breach alerts)
- ✅ **Explainability** (Every decision includes reasoning)

---

## 🚀 Roadmap

### Phase 1 (Current) ✅
- Core intelligence layer
- Multi-factor scoring engine
- Real-time dashboard
- Role-based access control
- Audit trail & compliance

### Phase 2 (Q2 2026)
- Advanced ML models (XGBoost, Neural Networks)
- Feedback learning loops
- API integration with DCAs
- Historical trend analysis
- Automated escalation workflows

### Phase 3 (Q3-Q4 2026)
- Enterprise database integration (SQL Server, PostgreSQL)
- ERP/SAP connectors
- White-label customization
- Mobile app
- Real-time alerts & notifications

---

## 📝 Data Dictionary

### nexus_accounts.csv
| Column | Type | Description |
|--------|------|-------------|
| case_id | string | Unique case identifier |
| customer_name | string | Customer business name |
| invoice_amount | float | Outstanding invoice amount |
| ageing_days | int | Days since invoice due date |
| business_type | string | Segment (Enterprise/Large/Medium/Small) |
| status | string | ACTIVE / RESOLVED / ESCALATED |
| dca_assigned | string | DCA agency responsible |
| dispute_status | string | Open / Resolved / Pending_Resolution |
| last_dca_update_days | int | Days since last DCA contact |
| recovery_score | float | AI-computed score (0-1) |
| sla_status | string | OK / AT_RISK / BREACHED |
| payment_history | string | Good / Bad / Neutral |

---

## 🤝 Contributing

This project is open for extensions and improvements:

1. **Add new scoring factors** → Modify `models/scoring.py`
2. **Create custom visualizations** → Extend dashboard pages
3. **Integrate external data** → Enhance `data/data_gen.py`
4. **Build API layer** → Add FastAPI endpoints
5. **Deploy to cloud** → AWS/Azure/GCP templates

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details

---

## ⚡ Quick Reference

| Task | Command |
|------|---------|
| Run locally | `streamlit run app.py` |
| Install deps | `pip install -r requirements.txt` |
| Generate data | `python data/data_gen.py` |
| Deploy to Cloud | Push to GitHub, use Streamlit Cloud |
| View logs | Check `data/audit_log.csv` |

---

## 📞 Support

- **Issues**: Create GitHub issue for bugs/features
- **Questions**: Open a discussion
- **Demo**: Visit live app at (https://fedex-dca-decision-engine.streamlit.app)

---

## ⚠️ Disclaimer

All data used in this project is **synthetic** and created solely for demonstration purposes. This is a **prototype/MVP** designed to showcase decision intelligence capabilities for enterprise debt collection management.

**Not production-ready without**: Security hardening, database integration, compliance audit, load testing, and data validation against real DCA integrations.

---

**Last Updated**: January 8, 2026  
**Status**: ✅ Deployed & Live  
**Version**: 1.0.0
