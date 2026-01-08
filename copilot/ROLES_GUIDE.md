# Role-Based Access Control - Complete Guide

## 🎭 Three User Roles

Your system now has **3 different roles** with **different permissions**. Changing the role in the sidebar will automatically limit what pages and features you can access.

---

## 📊 Role Comparison Table

| Feature | FedEx Admin | DCA Agent | Compliance Officer |
|---------|-------------|-----------|-------------------|
| **Dashboard** | ✅ Full | ✅ View | ✅ View |
| **Add New Case** | ✅ Create | ❌ No | ❌ No |
| **Case Workflow** | ✅ All Cases | ✅ Assigned Only | ❌ No |
| **DCA Performance** | ✅ Full | ❌ No | ✅ View |
| **Analytics & Reports** | ✅ Full | ❌ No | ✅ View |
| **Audit Trail** | ✅ Full | ❌ No | ✅ Full |
| **Database View** | ✅ Full | ❌ No | ❌ No |

---

## 👨‍💼 **FedEx Admin** - Full Access

**Purpose:** Manage the entire DCA system

**What they can do:**
- ✅ View Dashboard (all metrics, all cases)
- ✅ **Create new cases** (Add New Case page)
- ✅ **Manage workflows** (update case status, SLA tracking)
- ✅ **View DCA performance** (scorecards, accountability)
- ✅ **View analytics** (insights, trends, recovery analysis)
- ✅ **View audit trail** (compliance, governance)
- ✅ **View full database** (raw data export)

**Responsibilities:**
- Create & manage cases
- Assign cases to DCAs
- Monitor SLA compliance
- Track DCA performance
- Make strategic decisions
- Ensure compliance

**Who is this?** System Administrators, Managers, Operations Lead

---

## 👤 **DCA Agent** - Case Management Only

**Purpose:** Handle assigned cases and update their status

**What they can do:**
- ✅ View Dashboard (cases overview)
- ✅ **View & Update My Cases** (Case Workflow page)
  - Search assigned cases
  - View case details
  - Update case status (ACTIVE → PENDING → ESCALATED → CLOSED)
  - Add notes/updates

**What they CANNOT do:**
- ❌ Create new cases
- ❌ View other agents' cases
- ❌ See performance metrics
- ❌ Access analytics
- ❌ View audit trail
- ❌ View raw database

**Responsibilities:**
- Work on assigned cases
- Update case status regularly
- Document actions taken
- Meet SLA deadlines
- Follow workflows

**Who is this?** DCA Agents, Collection Officers, Field Staff

---

## ⚖️ **Compliance Officer** - Audit & Reporting Only

**Purpose:** Monitor compliance, governance, and performance reporting

**What they can do:**
- ✅ View Dashboard (monitoring)
- ✅ **View DCA Performance** (Track agent efficiency)
- ✅ **View Analytics & Reports** (Insights and trends)
- ✅ **View Audit Trail** (Full compliance history)
  - See all actions
  - Filter by user, action, date
  - Export audit logs
  - Verify SLA compliance

**What they CANNOT do:**
- ❌ Create or modify cases
- ❌ Update case status
- ❌ View raw database
- ❌ Manage operations
- ❌ Make changes to system

**Responsibilities:**
- Monitor compliance
- Generate reports
- Track performance
- Verify audit trails
- Ensure governance
- Document for audits

**Who is this?** Compliance Officers, Auditors, QA Team, Finance/CFO

---

## 🔐 How Role-Based Access Works

### Sidebar Navigation
When you select a role, the sidebar **automatically shows/hides pages**:

```
FedEx Admin:
├─ 🏠 Dashboard          ✅ Visible
├─ ➕ Add New Case       ✅ Visible
├─ 📋 Case Workflow      ✅ Visible
├─ 👥 DCA Performance    ✅ Visible
├─ 📊 Analytics          ✅ Visible
├─ 🔍 Audit Trail        ✅ Visible
└─ 🗂️ Database           ✅ Visible

DCA Agent:
├─ 🏠 Dashboard          ✅ Visible
├─ 📋 My Cases           ✅ Visible (Workflow)
└─ [Others hidden]       ❌ Hidden

Compliance Officer:
├─ 🏠 Dashboard          ✅ Visible
├─ 📊 Analytics          ✅ Visible
├─ 👥 DCA Performance    ✅ Visible
├─ 🔍 Audit Trail        ✅ Visible
└─ [Others hidden]       ❌ Hidden
```

### Access Denied
If you try to access a page you don't have permission for:

```
🔒 Access Denied

Your role (DCA Agent) does not have access to this page.

Only FedEx Admin can view this.
```

---

## 📋 Use Case Examples

### Scenario 1: DCA Agent Starting Shift
1. Login as DCA Agent
2. See Dashboard with overview
3. Click "My Cases" (Case Workflow)
4. Search for assigned cases
5. Update case status
6. Add notes
7. That's it! Other pages are hidden

**Result:** DCA focuses on their work, no distractions

---

### Scenario 2: Manager Monitoring Performance
1. Login as FedEx Admin
2. View Dashboard → See all KPIs
3. Click "DCA Performance" → Check team metrics
4. Identify top performers & underperformers
5. Click "Analytics" → See trends
6. Make decisions on assignments

**Result:** Manager has full visibility & control

---

### Scenario 3: Compliance Audit
1. Login as Compliance Officer
2. View Dashboard → High-level overview
3. Click "Audit Trail" → See all actions
4. Filter by date range, user, action type
5. Click "Analytics" → See recovery trends
6. Export data for compliance report

**Result:** Complete audit trail with no operational access

---

## 🛡️ Why Role-Based Access?

### Security
- Users only see what they need
- Prevents accidental data changes
- Reduces human errors

### Compliance
- Audit trail shows who did what
- Segregation of duties enforced
- Compliance requirements met

### Efficiency
- Focused interface per role
- Reduces confusion
- Faster workflow

### Governance
- Clear responsibility per role
- Easy to track accountabilities
- Audit-ready system

---

## 🔄 Changing Roles

You can change roles anytime from the sidebar:

1. Look at "View As" section in sidebar
2. Select different role
3. Available pages automatically change
4. No page reload needed

**Try it:**
1. Select "DCA Agent" → See limited sidebar
2. Select "Compliance Officer" → See different pages
3. Select "FedEx Admin" → See full system

---

## 📊 What Compliance Officer Can Report

With Audit Trail + Analytics + Performance pages, Compliance Officer can generate:

✅ **Compliance Reports:**
- Case status transitions
- User activity timeline
- SLA breach events
- Change logs

✅ **Performance Reports:**
- DCA efficiency by month
- Recovery rate by agent
- Case aging analysis
- Portfolio risk assessment

✅ **Governance Reports:**
- Audit event count
- User activity tracking
- Data integrity verification
- Process compliance

---

## 🔐 Access Control Implementation

Every page now checks:
```
if check_access(["FedEx Admin", "DCA Agent"]):
    # Show page content
else:
    # Show access denied message
```

Pages Protected:
- ✅ Add New Case → FedEx Admin only
- ✅ Case Workflow → Admin + DCA Agent
- ✅ DCA Performance → Admin + Compliance
- ✅ Analytics → Admin + Compliance
- ✅ Audit Trail → Admin + Compliance
- ✅ Database → Admin only

---

## 📌 Key Points

1. **Role Selection:** Choose "View As" in sidebar
2. **Sidebar Updates:** Pages show/hide based on role
3. **Access Enforcement:** Each page verifies your role
4. **Audit Trail:** All actions logged with user role
5. **No Admin Bypass:** Role checks apply to everyone

---

## 🎯 Recommended Setup

### For Production Deployment:

**FedEx Admin Users:**
- System Administrator
- Operations Manager
- Portfolio Lead

**DCA Agent Users:**
- 10-20 collection officers
- 5-10 recovery specialists
- Field staff

**Compliance Officer Users:**
- 1-2 compliance professionals
- Internal audit team
- CFO/Finance team

---

## ❓ FAQ

**Q: Can a DCA Agent see other agents' cases?**
A: No, they can only search & update their own assigned cases.

**Q: Can a Compliance Officer make changes?**
A: No, they can only view reports and audit trail. No modifications allowed.

**Q: Can I switch roles?**
A: Yes, anytime. Just change "View As" in sidebar.

**Q: Are role changes logged?**
A: Yes, in the audit trail.

**Q: What if I try to access a restricted page?**
A: You'll see "Access Denied" message.

---

## 🚀 Test the Roles

### Try this now:

1. **As FedEx Admin:**
   - Create a case
   - Update its status
   - View audit trail
   - See all analytics

2. **Switch to DCA Agent:**
   - Try to create case → ❌ Access Denied
   - View "My Cases" → ✅ Works
   - Try analytics → ❌ Hidden

3. **Switch to Compliance Officer:**
   - View audit trail → ✅ Works
   - Try to create case → ❌ Access Denied
   - View analytics → ✅ Works

---

**Status: ✅ Role-Based Access Control Active**

All pages now enforce proper access control based on user role!
