# FedEx DCA Intelligence Hub - Quick Start Guide

## 🚀 Getting Started

### 1. **Start the Application**
```bash
streamlit run app.py
```
Open browser to: `http://localhost:8501`

### 2. **Navigate the Sidebar**
- Select your role: **Admin**, **DCA Agent**, or **Compliance Officer**
- Click any navigation button to access different sections

---

## 📱 Page Guide

### 🏠 Dashboard (Landing Page)
**What it does:** Real-time executive command center

**Key Features:**
- 4 Executive KPIs (Portfolio Value, Expected Recovery, At-Risk Portfolio, Avg Ageing)
- Risk distribution pie chart
- Recovery probability histogram
- SLA status breakdown
- Ageing trend line chart
- AI-prioritized case queue with filters
- CSV export button for reporting

**How to use:**
1. View top-level metrics instantly
2. Filter cases by Risk Level, SLA Status, Recovery Probability
3. Sort cases by AI priority score
4. Export for external reporting

---

### ➕ Add New Case
**What it does:** Create new cases in the system

**Input Fields:**
- Enterprise/Customer Name (text)
- Invoice Amount in ₹ (number)
- Ageing Days (number)
- Business Type (Enterprise/Large/Medium/Small)
- Dispute Status (None/Open/Pending_Resolution)

**How to use:**
1. Fill in all fields
2. Click "Save"
3. Case gets AI scoring automatically
4. Case appears in dashboard immediately

---

### 📋 Case Workflow
**What it does:** Manage case status & SLA tracking

**Features:**
- Case search by ID
- View current case details
- Update case status (ACTIVE → PENDING_REVIEW → ESCALATED → CLOSED)
- Add update notes for audit trail
- SLA compliance dashboard

**How to use:**
1. Enter Case ID to search
2. View current status & details
3. Select new status from dropdown
4. Add notes explaining the action
5. Click "Update Status"
6. Change logged to audit trail automatically

---

### 👥 DCA Performance
**What it does:** Track individual agent effectiveness

**Sections:**
1. **Performance Scorecard:**
   - Cases assigned per agent
   - Portfolio value per agent
   - Expected recovery per agent
   - Average ageing (lower = better)
   - Recovery efficiency % (higher = better)
   - SLA compliance rate

2. **Deep Dive:**
   - Select individual DCA agent
   - See their specific metrics
   - View their recent cases
   - Track their SLA compliance

**How to use:**
1. Review the scorecard table for all agents
2. Identify top performers (high recovery efficiency)
3. Select an agent from dropdown for detailed view
4. Review their case portfolio
5. Use for performance reviews & incentives

---

### 📊 Analytics & Reports
**What it does:** Advanced insights & trend analysis

**Insights Include:**
- 🚨 Number of critical cases (>120 days + disputes)
- ✅ High recovery probability cases (>75%)
- ⏳ Aging cases (>90 days)

**Charts:**
- Recovery trend by probability buckets
- Case count vs expected recovery
- Portfolio distribution

**How to use:**
1. Review key insight metrics
2. Analyze recovery trends
3. Identify which probability buckets have highest value
4. Use for strategic decision-making

---

### 🔍 Audit Trail
**What it does:** Compliance & governance tracking

**Features:**
- Full log of all actions
- Filter by action type
- Filter by user
- Filter by date range (last N days)
- View timestamp of every change
- See update notes

**Columns:**
- Timestamp: When action occurred
- Case ID: Which case was affected
- Action: What was done
- User: Who did it
- Details: Notes on the action

**How to use:**
1. Filter by action type (e.g., "Case Created", "Status Updated")
2. Filter by user (e.g., "FedEx Admin", "DCA_Agent")
3. Set date range
4. Export for compliance reporting
5. Use for dispute resolution & audit trails

**Audit Statistics:**
- Total events logged
- Number of unique users
- Types of actions tracked

---

### 🗂️ Database
**What it does:** View complete dataset

**Contents:**
- All cases with all fields
- Real-time data view
- Sortable/searchable columns

**How to use:**
1. Browse complete dataset
2. Sort by any column (click header)
3. Search for specific values
4. Use for manual reviews or audits

---

## 🎯 AI Scoring Explained

### Recovery Score (0.0 to 1.0)
- **0.0-0.3:** Low recovery chance
- **0.3-0.6:** Medium recovery chance
- **0.6-0.8:** High recovery chance
- **0.8-1.0:** Very high recovery chance

### Recovery Probability (%)
- Same as above but as percentage
- Accounts for realistic aging decay
- Used for expected recovery calculation

### Priority Score
- **Higher = More Urgent**
- Calculated as: Recovery Probability × Invoice Amount × Urgency Factor
- Older cases get higher multiplier (more urgent)

### Risk Level
- **🔴 CRITICAL:** >120 days AND open disputes
- **🟠 HIGH:** >120 days
- **🟡 MEDIUM:** 60-120 days
- **🟢 LOW:** <60 days

### SLA Status
- **OK:** <20 days in system
- **AT_RISK:** 20-30 days in system
- **BREACHED:** >30 days in system

---

## 💡 Pro Tips

1. **Use the Dashboard Filter** to focus on specific cases
   - Filter by CRITICAL + HIGH risk = urgent cases
   - Filter by BREACHED SLA = immediate action needed
   - Filter by >75% recovery = high confidence cases

2. **Check DCA Performance** regularly for accountability
   - Look for agents with high recovery efficiency
   - Identify underperformers for support
   - Use for performance bonuses/incentives

3. **Review Audit Trail** for compliance
   - Weekly compliance checks
   - Month-end reporting
   - Dispute resolution
   - User activity tracking

4. **Use Case Workflow** to enforce processes
   - Status updates track case lifecycle
   - SLA dashboard shows compliance
   - Notes create decision audit trail

5. **Export Data** for external reporting
   - CSV download available on dashboard
   - Use for executive presentations
   - Share with stakeholders

---

## 📊 Recommended Workflows

### **Daily (Admin):**
1. Open Dashboard
2. Check CRITICAL + HIGH risk cases
3. Check SLA status (BREACHED items)
4. Assign cases to available DCAs
5. Monitor high-value cases

### **Weekly (Admin):**
1. Run DCA Performance report
2. Review audit trail for compliance
3. Check recovery predictions
4. Forecast expected recovery amount
5. Identify training needs

### **Monthly (Compliance Officer):**
1. Export audit trail for month
2. Verify all cases have proper documentation
3. Generate compliance report
4. Check SLA compliance rates
5. Identify process improvements

### **Per Case (DCA Agent):**
1. View assigned cases in workflow
2. Update status with notes
3. Review recommended actions
4. Document all interactions
5. Check SLA deadline

---

## 🔐 User Roles

### **FedEx Admin**
- ✅ View everything
- ✅ Create new cases
- ✅ Update case status
- ✅ View all analytics
- ✅ View audit trails

### **DCA Agent**
- ✅ View assigned cases
- ✅ Update case status
- ✅ Add update notes
- ✅ See recommended actions

### **Compliance Officer**
- ✅ View audit trails
- ✅ Generate compliance reports
- ✅ View all analytics
- ✅ Export audit data

---

## ❓ FAQ

**Q: How are cases prioritized?**
A: By AI priority score = Recovery Probability × Invoice Amount × Age Urgency. Higher score = higher priority.

**Q: What does "At-Risk Portfolio" mean?**
A: Cases with CRITICAL or HIGH risk level (120+ days aging or disputes).

**Q: How is recovery probability calculated?**
A: Multi-factor ML model considering ageing, business type, disputes, SLA status, payment history.

**Q: What happens if SLA is breached?**
A: Case shows BREACHED status and appears in urgent filters. Automatic escalation recommended.

**Q: Can I export data?**
A: Yes! CSV download button available on Dashboard for reports.

**Q: How do I check if a DCA is performing well?**
A: Check DCA Performance page - look for high "Recovery Efficiency %" and high "Avg Recovery Prob".

**Q: Is there a way to track who changed what?**
A: Yes! Full audit trail on Audit page - shows timestamp, user, action, and notes.

---

## 📞 Support

For issues or questions:
1. Check this guide
2. Review Dashboard tooltips
3. Check Audit Trail for recent changes
4. Contact FedEx Admin team

---

**Last Updated:** January 8, 2026
**Version:** 2.0 - Enterprise Edition
