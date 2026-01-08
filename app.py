import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from models.scoring import (apply_scoring, compute_recovery_probability, risk_assessment, 
                           compute_churn_risk, compute_optimal_followup_timing, 
                           get_predictive_insights, compute_dca_efficiency_score)

# ================= CONFIG =================
st.set_page_config(
    page_title="FedEx DCA Intelligence Hub", 
    layout="wide", 
    initial_sidebar_state="expanded",
    menu_items={
        "About": "FedEx DCA Management  - AI-Powered Recovery Intelligence"
    }
)

DATA_PATH = "data/nexus_accounts.csv"
AUDIT_PATH = "data/audit_log.csv"

# ================= SESSION STATE =================
if "page" not in st.session_state:
    st.session_state.page = "dashboard"
if "user_role" not in st.session_state:
    st.session_state.user_role = "Admin"
if "case_filters" not in st.session_state:
    st.session_state.case_filters = {"risk_level": "ALL", "status": "ACTIVE"}

def go_dashboard():
    st.session_state.page = "dashboard"

def format_currency(value):
    """Format value as Indian currency"""
    return f"₹{int(value):,}"

# ================= LOAD / SAVE =================
def load_data():
    df = pd.read_csv(DATA_PATH)
    if "customer_name" not in df.columns:
        df["customer_name"] = "UNKNOWN"
    return df

def save_data(df):
    df.to_csv(DATA_PATH, index=False)

def log_audit(case_id, action, user, details=""):
    entry = {
        "timestamp": datetime.now(),
        "case_id": case_id,
        "action": action,
        "user": user,
        "details": details
    }
    try:
        audit = pd.read_csv(AUDIT_PATH)
        audit = pd.concat([audit, pd.DataFrame([entry])], ignore_index=True)
    except:
        audit = pd.DataFrame([entry])
    audit.to_csv(AUDIT_PATH, index=False)

def calculate_sla_status(case_date, days_in_system):
    """Calculate SLA status based on days in system"""
    if days_in_system > 30:
        return "BREACHED"
    elif days_in_system > 20:
        return "AT_RISK"
    else:
        return "OK"
    st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: 'Segoe UI', Inter, sans-serif;
    background: linear-gradient(135deg, #0F1419 0%, #1a1f2e 100%);
    color: #E5E7EB;
}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111827 0%, #0a0e17 100%);
    border-right: 3px solid #FF6600;
}

section[data-testid="stSidebar"] button {
    border-radius: 8px;
    transition: all 0.2s ease;
}

section[data-testid="stSidebar"] button:hover {
    background-color: rgba(255, 102, 0, 0.15) !important;
    border-left: 4px solid #FF6600;
}

/* ===== HEADERS & TYPOGRAPHY ===== */
h1, h2, h3, h4 {
    color: #F9FAFB;
    font-weight: 800;
    letter-spacing: -0.5px;
    margin-top: 20px;
    margin-bottom: 15px;
}

h1 {
    font-size: 36px;
    border-bottom: 3px solid #FF6600;
    padding-bottom: 12px;
}

h2 {
    font-size: 24px;
    color: #E5E7EB;
}

h3 {
    font-size: 18px;
    color: #D1D5DB;
}

/* ===== METRIC CARDS - ENHANCED ===== */
[data-testid="metric-container"] {
    background: linear-gradient(135deg, #1F2937 0%, #111827 100%);
    border: 2px solid rgba(255, 102, 0, 0.4);
    padding: 24px;
    border-radius: 16px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

[data-testid="metric-container"]:hover {
    border-color: #FF6600;
    box-shadow: 0 12px 48px rgba(255, 102, 0, 0.3);
    transform: translateY(-4px);
}

[data-testid="metric-container"] [data-testid="metric-label"] {
    color: #9CA3AF;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
}

[data-testid="metric-container"] [data-testid="metric-value"] {
    font-size: 36px !important;
    font-weight: 900 !important;
    color: #FF6600 !important;
}

[data-testid="metric-container"] [data-testid="metric-delta"] {
    font-weight: 700;
    font-size: 14px;
}

/* ===== CARDS & CONTAINERS ===== */
.card {
    background: linear-gradient(135deg, #1F2937 0%, #111827 100%);
    border: 2px solid rgba(255, 102, 0, 0.2);
    padding: 24px;
    border-radius: 16px;
    margin-bottom: 20px;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
    transition: all 0.3s ease;
}

.card:hover {
    border-color: #FF6600;
    box-shadow: 0 15px 60px rgba(255, 102, 0, 0.2);
    transform: translateY(-2px);
}

.card-title {
    font-size: 12px;
    color: #9CA3AF;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 8px;
}

.card-value {
    font-size: 32px;
    font-weight: 900;
    color: #FF6600;
    margin-top: 8px;
}

/* ===== STATUS BADGES ===== */
.badge-ok {
    display: inline-block;
    background: linear-gradient(135deg, #10B981 0%, #34D399 100%);
    color: #000;
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 700;
    box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.badge-at-risk {
    display: inline-block;
    background: linear-gradient(135deg, #F59E0B 0%, #FBBF24 100%);
    color: #000;
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 700;
    box-shadow: 0 4px 15px rgba(245, 158, 11, 0.3);
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.badge-breached {
    display: inline-block;
    background: linear-gradient(135deg, #EF4444 0%, #F87171 100%);
    color: #fff;
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 700;
    box-shadow: 0 4px 15px rgba(239, 68, 68, 0.3);
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.badge-critical {
    display: inline-block;
    background: linear-gradient(135deg, #7C2D12 0%, #DC2626 100%);
    color: #fff;
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 700;
    box-shadow: 0 4px 15px rgba(220, 38, 38, 0.4);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    animation: pulse-critical 2s infinite;
}

@keyframes pulse-critical {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.8; }
}

.badge-high {
    display: inline-block;
    background: linear-gradient(135deg, #FF6600 0%, #FF8C42 100%);
    color: #000;
    padding: 8px 16px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
    box-shadow: 0 4px 15px rgba(255, 102, 0, 0.3);
}

.badge-med {
    display: inline-block;
    background: linear-gradient(135deg, #4D148C 0%, #7C3AED 100%);
    color: white;
    padding: 8px 16px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
    box-shadow: 0 4px 15px rgba(77, 20, 140, 0.3);
}

.badge-low {
    display: inline-block;
    background: linear-gradient(135deg, #10B981 0%, #34D399 100%);
    color: black;
    padding: 8px 16px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
    box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
}

/* ===== TABLES & DATAFRAME ===== */
[data-testid="stDataFrame"] {
    background: #0E1117 !important;
    border: 2px solid rgba(255, 102, 0, 0.2) !important;
    border-radius: 12px !important;
}

[data-testid="stDataFrame"] thead {
    background: linear-gradient(180deg, #1F2937 0%, #111827 100%) !important;
    border-bottom: 2px solid #FF6600 !important;
}

[data-testid="stDataFrame"] tbody tr {
    transition: all 0.2s ease;
}

[data-testid="stDataFrame"] tbody tr:hover {
    background-color: rgba(255, 102, 0, 0.1) !important;
}

[data-testid="stDataFrame"] tbody tr:nth-child(odd) {
    background-color: rgba(15, 20, 25, 0.5) !important;
}

/* ===== BUTTONS ===== */
.stButton>button {
    background: linear-gradient(135deg, #FF6600 0%, #FF8C42 100%) !important;
    color: #000 !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    border: none !important;
    padding: 12px 24px !important;
    box-shadow: 0 4px 15px rgba(255, 102, 0, 0.3) !important;
    transition: all 0.3s ease !important;
    font-size: 14px !important;
}

.stButton>button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(255, 102, 0, 0.5) !important;
    background: linear-gradient(135deg, #FF8C42 0%, #FFB84D 100%) !important;
}

.stButton>button:active {
    transform: translateY(0) !important;
}

/* ===== FORM INPUTS ===== */
.stTextInput>div>div>input,
.stNumberInput>div>div>input,
.stSelectbox>div>div>select,
.stMultiSelect>div>div>div,
.stSlider>div>div>div {
    background-color: #1F2937 !important;
    color: #F9FAFB !important;
    border: 2px solid rgba(255, 102, 0, 0.2) !important;
    border-radius: 10px !important;
    padding: 12px !important;
    transition: all 0.2s ease !important;
}

.stTextInput>div>div>input:focus,
.stNumberInput>div>div>input:focus,
.stSelectbox>div>div>select:focus,
.stMultiSelect>div>div>div:focus {
    border-color: #FF6600 !important;
    box-shadow: 0 0 0 3px rgba(255, 102, 0, 0.15) !important;
    background-color: #111827 !important;
}

/* ===== TABS ===== */
.stTabs [data-baseweb="tab-list"] {
    border-bottom: 2px solid rgba(255, 102, 0, 0.2);
}

.stTabs [data-baseweb="tab"] {
    color: #9CA3AF;
    border-radius: 10px 10px 0 0;
    transition: all 0.2s ease;
}

.stTabs [aria-selected="true"] {
    background-color: rgba(255, 102, 0, 0.2);
    color: #FF6600;
    border-bottom: 3px solid #FF6600;
}

/* ===== ALERTS & MESSAGES ===== */
.stSuccess {
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(52, 211, 153, 0.05) 100%) !important;
    border-left: 4px solid #10B981 !important;
    border-radius: 8px !important;
}

.stWarning {
    background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(251, 191, 36, 0.05) 100%) !important;
    border-left: 4px solid #F59E0B !important;
    border-radius: 8px !important;
}

.stError {
    background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(248, 113, 113, 0.05) 100%) !important;
    border-left: 4px solid #EF4444 !important;
    border-radius: 8px !important;
}

.stInfo {
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(96, 165, 250, 0.05) 100%) !important;
    border-left: 4px solid #3B82F6 !important;
    border-radius: 8px !important;
}

/* ===== DIVIDER ===== */
hr {
    border-color: rgba(255, 102, 0, 0.2) !important;
    margin: 20px 0 !important;
}

/* ===== STATUS COLORS ===== */
.status-active {
    color: #10B981;
    font-weight: 700;
.badge-low {
    background: linear-gradient(135deg, #10B981 0%, #34D399 100%);
    color: black;
    padding: 8px 16px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
    box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
}

/* Tables */
[data-testid="stDataFrame"] {
    background: #0E1117 !important;
    border: 2px solid rgba(255, 102, 0, 0.2) !important;
    border-radius: 12px;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(135deg, #FF6600 0%, #FF8C42 100%) !important;
    color: #000 !important;
    border-radius: 10px;
    font-weight: 700;
    border: none !important;
    padding: 12px 24px !important;
    box-shadow: 0 4px 15px rgba(255, 102, 0, 0.3) !important;
    transition: all 0.3s ease !important;
}

.stButton>button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(255, 102, 0, 0.5) !important;
}

/* Form inputs */
.stTextInput>div>div>input,
.stNumberInput>div>div>input,
.stSelectbox>div>div>select {
    background-color: #1F2937 !important;
    color: #F9FAFB !important;
    border: 2px solid rgba(255, 102, 0, 0.2) !important;
    border-radius: 10px !important;
}

.stTextInput>div>div>input:focus,
.stNumberInput>div>div>input:focus,
.stSelectbox>div>div>select:focus {
    border-color: #FF6600 !important;
    box-shadow: 0 0 0 3px rgba(255, 102, 0, 0.1) !important;
}

/* Divider */
hr {
    border-color: rgba(255, 102, 0, 0.2) !important;
}

/* Status indicators */
.status-active {
    color: #10B981;
    font-weight: 700;
}

.status-breached {
    color: #FF6600;
    font-weight: 700;
}

/* Animations */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

[data-testid="metric-container"] {
    animation: fadeInUp 0.5s ease-out;
}
</style>
""", unsafe_allow_html=True)

# ================= UI HELPER FUNCTIONS =================
def render_status_badge(status):
    """Render colored status badge"""
    if status == "OK":
        return '<span class="badge-ok">✓ OK</span>'
    elif status == "AT_RISK":
        return '<span class="badge-at-risk">⚠ At Risk</span>'
    elif status == "BREACHED":
        return '<span class="badge-breached">✗ Breached</span>'
    else:
        return '<span class="badge-ok">Unknown</span>'

def render_risk_badge(risk_level):
    """Render risk level badge"""
    if risk_level == "CRITICAL":
        return '<span class="badge-critical">🚨 Critical</span>'
    elif risk_level == "HIGH":
        return '<span class="badge-high">⬆ High</span>'
    elif risk_level == "MEDIUM":
        return '<span class="badge-med">→ Medium</span>'
    else:
        return '<span class="badge-low">↓ Low</span>'

def render_metric_card(title, value, trend=None, trend_color="green"):
    """Render an enhanced metric card"""
    trend_html = ""
    if trend:
        arrow = "↑" if trend > 0 else "↓"
        color = "#10B981" if trend_color == "green" else "#EF4444"
        trend_html = f'<span style="color: {color}; font-size: 12px; margin-left: 8px;">{arrow} {trend}%</span>'
    
    return f"""
    <div style="background: linear-gradient(135deg, #1F2937 0%, #111827 100%); 
                border: 2px solid rgba(255, 102, 0, 0.3); padding: 20px; border-radius: 12px;
                text-align: center; transition: all 0.3s ease;">
        <p style="color: #9CA3AF; font-size: 12px; font-weight: 700; text-transform: uppercase; margin: 0 0 8px 0;">
            {title}
        </p>
        <p style="color: #FF6600; font-size: 28px; font-weight: 900; margin: 8px 0 0 0;">
            {value}{trend_html}
        </p>
    </div>
    """

def render_section_header(title, subtitle=""):
    """Render a professional section header"""
    subtitle_html = f'<p style="color: #9CA3AF; font-size: 13px; margin: 4px 0 0 0;">{subtitle}</p>' if subtitle else ""
    return f"""
    <div style="margin-bottom: 24px;">
        <h2 style="color: #F9FAFB; font-size: 24px; font-weight: 900; margin: 0 0 4px 0; 
                   border-bottom: 3px solid #FF6600; padding-bottom: 8px; display: inline-block;">
            {title}
        </h2>
        {subtitle_html}
    </div>
    """

# ================= INTELLIGENCE =================
def recovery_score(row):
    score = 0.4
    score += 0.3 if row["business_type"] == "Enterprise" else 0.1
    score -= min(row["ageing_days"] / 180, 1) * 0.2
    if row["dispute_status"] == "Open":
        score -= 0.2
    return round(max(min(score, 1), 0), 2)

def next_best_action(row):
    if row["dispute_status"] == "Open":
        return "Wait for Dispute Resolution"
    if row["ageing_days"] > 120:
        return "Escalate to Legal"
    if row["invoice_amount"] > 200000:
        return "Senior Negotiation"
    return "Standard Follow-up"

# ================= DATA =================
df = load_data()
df = apply_scoring(df)  # Apply new ML scoring
df["sla_status"] = df.apply(lambda r: calculate_sla_status(r.get("created_date"), r["ageing_days"]), axis=1)
df["priority_score"] = df["recovery_score"] * df["invoice_amount"]

# ================= SIDEBAR LOGO =================
with st.sidebar:
    # Professional logo section
    st.markdown("""
    <div style="text-align: center; padding: 12px 0 20px 0; border-bottom: 2px solid rgba(255, 102, 0, 0.3); margin-bottom: 20px;">
        <p style="margin: 0; font-size: 10px; letter-spacing: 2px; color: #9CA3AF; font-weight: 700; text-transform: uppercase;">
            Debt Collection Management
        </p>
        <h2 style="margin: 8px 0 0 0; font-size: 22px; font-weight: 900; letter-spacing: -0.5px;">
            <span style="color: #4D148C;">FedEx</span> <span style="color: #FF6600;">DCA</span>
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Home button - clean and professional
    if st.button("↖ Return to Dashboard", key="sidebar_home", use_container_width=True, help="Go to main dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()
    
    st.markdown("---")
    
    st.markdown("""
    <p style="font-size: 12px; font-weight: 700; color: #FF6600; text-transform: uppercase; letter-spacing: 1px; margin: 16px 0 12px 0;">
        System Navigation
    </p>
    """, unsafe_allow_html=True)
    
    role = st.radio("View As", ["FedEx Admin", "DCA Agent", "Compliance Officer"])

    st.divider()
    st.markdown("""
    <p style="font-size: 11px; font-weight: 700; color: #9CA3AF; text-transform: uppercase; letter-spacing: 0.8px; margin: 0;">
        📋 Available Pages
    </p>
    """, unsafe_allow_html=True)

    
    # Store role in session state for enforcement
    st.session_state.user_role = role
    
    # ADMIN - Full Access
    if role == "FedEx Admin":
        st.markdown("*All Features Available*")
        if st.button("🏠 Dashboard", use_container_width=True):
            st.session_state.page = "dashboard"
        if st.button("➕ Add New Case", use_container_width=True):
            st.session_state.page = "add"
        if st.button("📝 Assign Case", use_container_width=True):
            st.session_state.page = "assign"
        if st.button("📋 Case Workflow", use_container_width=True):
            st.session_state.page = "workflow"
        if st.button("👥 DCA Performance", use_container_width=True):
            st.session_state.page = "dca_performance"
        if st.button("📊 Analytics & Reports", use_container_width=True):
            st.session_state.page = "analytics"
        if st.button("🧠 Predictive Analytics", use_container_width=True):
            st.session_state.page = "predictive"
        if st.button("⚡ Live Updates", use_container_width=True):
            st.session_state.page = "live_updates"
        if st.button("🔍 Audit Trail", use_container_width=True):
            st.session_state.page = "audit"
        
        if st.button("🗂️ Database", use_container_width=True):
            st.session_state.page = "database"
    
    # DCA AGENT - Limited Access (View assigned cases only)
    elif role == "DCA Agent":
        st.markdown("*Case Management Only*")
        if st.button("🏠 Dashboard", use_container_width=True):
            st.session_state.page = "dashboard"
        if st.button("📋 My Cases", use_container_width=True):
            st.session_state.page = "workflow"
        st.info("📌 Access limited to assigned cases")
    
    # COMPLIANCE OFFICER - Audit & Analytics Only
    elif role == "Compliance Officer":
        st.markdown("*Audit & Reporting Only*")
        if st.button("🏠 Dashboard", use_container_width=True):
            st.session_state.page = "dashboard"
        if st.button("📊 Analytics & Reports", use_container_width=True):
            st.session_state.page = "analytics"
        if st.button("🧠 Predictive Analytics", use_container_width=True):
            st.session_state.page = "predictive"
        if st.button("⚡ Live Updates", use_container_width=True):
            st.session_state.page = "live_updates"
        if st.button("🔍 Audit Trail", use_container_width=True):
            st.session_state.page = "audit"
        st.info("📌 Access limited to audit & reporting")

    st.divider()
    st.markdown(f"**User Role:** {role}")
    st.markdown(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")

# ================= TOP-RIGHT HOME LINK =================
home_col1, home_col2 = st.columns([6, 1])
with home_col2:
    if st.button("↖ Home", key="top_home", use_container_width=True, help="Return to dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()

# ================= HANDLE QUERY PARAM =================
query_params = st.query_params
if "page" in query_params:
    st.session_state.page = query_params["page"]

# ================= ROLE-BASED ACCESS CONTROL =================
def check_access(required_roles):
    """Check if current user role has access to page"""
    current_role = st.session_state.get("user_role", "FedEx Admin")
    if current_role not in required_roles:
        st.error(f"🔒 Access Denied\n\nYour role ({current_role}) does not have access to this page.\n\nOnly {', '.join(required_roles)} can view this.")
        return False
    return True

# ================= DASHBOARD =================
if st.session_state.page == "dashboard":
    # Big logo on dashboard - Professional FedEx theme
    st.markdown(
        """
        <div style="margin-top:-20px; margin-bottom:32px; text-align:center;">
            <div style="padding: 24px 0; background: linear-gradient(180deg, rgba(71, 71, 71, 0.05) 0%, rgba(71, 71, 71, 0) 100%); border-radius: 12px;">
                <p style="margin: 0; font-size: 12px; letter-spacing: 2.5px; color: #9CA3AF; font-weight: 700; text-transform: uppercase;">Debt Collection Management</p>
                <h1 style="margin: 8px 0 0 0; font-size: 48px; font-weight: 900; letter-spacing: -1.5px;">
                    <span style="color: #4D148C;">Fed</span><span style="color: #FF6600;">Ex</span> <span style="color: #FF6600;">DCA</span>
                </h1>
                <p style="margin: 16px 0 0 0; font-size: 13px; letter-spacing: 0.8px; color: #D1D5DB; font-weight: 500;">AI-POWERED RECOVERY INTELLIGENCE PLATFORM</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.title("📊 Real-Time Command Center")
    # Recent Updates panel (visible to FedEx Admin & Compliance Officer)
    header_main_col, header_updates_col = st.columns([4, 1])
    
    # ========== KEY PERFORMANCE INDICATORS ==========
    st.subheader("🎯 Executive KPIs")
    
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4, gap="medium")
    
    # Calculate KPIs
    total_value = df["invoice_amount"].sum()
    expected_recovery = df["expected_recovery"].sum()
    recovery_rate = (expected_recovery / total_value * 100) if total_value > 0 else 0
    sla_breaches = (df["sla_status"] == "BREACHED").sum()
    active_cases = (df["status"] == "ACTIVE").sum()
    high_priority = (df["risk_level"] == "CRITICAL").sum()
    avg_ageing = df["ageing_days"].mean()
    portfolio_at_risk = df[df["risk_level"].isin(["HIGH", "CRITICAL"])]["invoice_amount"].sum()
    
    # Enhanced KPI Cards with better styling
    st.markdown("""
    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 24px;">
    """, unsafe_allow_html=True)
    
    kpi_cards = [
        {
            "icon": "💼",
            "title": "Portfolio Value",
            "value": format_currency(total_value),
            "delta": f"{active_cases} Active Cases",
            "color": "#FF6600"
        },
        {
            "icon": "📈",
            "title": "Expected Recovery",
            "value": format_currency(expected_recovery),
            "delta": f"{recovery_rate:.1f}% Recovery Rate",
            "color": "#10B981"
        },
        {
            "icon": "⚠️",
            "title": "At-Risk Portfolio",
            "value": format_currency(portfolio_at_risk),
            "delta": f"{high_priority} Critical",
            "color": "#EF4444"
        },
        {
            "icon": "📋",
            "title": "Avg. Ageing",
            "value": f"{int(avg_ageing)} days",
            "delta": f"{sla_breaches} SLA Breaches",
            "color": "#F59E0B"
        }
    ]
    
    col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
    kpi_cols = [col_kpi1, col_kpi2, col_kpi3, col_kpi4]
    
    for idx, (col, card) in enumerate(zip(kpi_cols, kpi_cards)):
        with col:
            st.metric(
                label=f"{card['icon']} {card['title']}",
                value=card['value'],
                delta=card['delta'],
                delta_color="normal"
            )

    st.divider()
    
    # ========== RISK DISTRIBUTION & RECOVERY INSIGHTS ==========
    st.subheader("📊 Portfolio Analytics")
    
    chart_col1, chart_col2, chart_col3 = st.columns(3, gap="medium")
    
    with chart_col1:
        # Risk Level Pie Chart
        risk_dist = df["risk_level"].value_counts()
        colors = {"CRITICAL": "#FF0000", "HIGH": "#FF6600", "MEDIUM": "#FFB84D", "LOW": "#10B981"}
        fig_risk = px.pie(
            values=risk_dist.values,
            names=risk_dist.index,
            title="Case Risk Distribution",
            color_discrete_map={k: colors[k] for k in risk_dist.index if k in colors}
        )
        fig_risk.update_layout(
            plot_bgcolor="#1F2937",
            paper_bgcolor="#0E1117",
            font=dict(color="#F9FAFB"),
            showlegend=True,
            height=400
        )
        st.plotly_chart(fig_risk, use_container_width=True)
    
    with chart_col2:
        # Recovery Probability Distribution
        fig_prob = px.histogram(
            df,
            x="recovery_probability",
            nbins=15,
            title="Recovery Probability Distribution",
            labels={"recovery_probability": "Recovery Probability (%)", "count": "Cases"},
            color_discrete_sequence=["#4D148C"]
        )
        fig_prob.update_layout(
            plot_bgcolor="#1F2937",
            paper_bgcolor="#0E1117",
            font=dict(color="#F9FAFB"),
            height=400,
            showlegend=False
        )
        st.plotly_chart(fig_prob, use_container_width=True)
    
    with chart_col3:
        # SLA Status Breakdown
        sla_dist = df["sla_status"].value_counts()
        sla_colors = {"OK": "#10B981", "AT_RISK": "#FFB84D", "BREACHED": "#FF0000"}
        fig_sla = px.bar(
            x=sla_dist.index,
            y=sla_dist.values,
            title="SLA Status Overview",
            labels={"x": "Status", "y": "Number of Cases"},
            color=sla_dist.index,
            color_discrete_map={k: sla_colors[k] for k in sla_dist.index if k in sla_colors}
        )
        fig_sla.update_layout(
            plot_bgcolor="#1F2937",
            paper_bgcolor="#0E1117",
            font=dict(color="#F9FAFB"),
            showlegend=False,
            height=400
        )
        st.plotly_chart(fig_sla, use_container_width=True)
    
    st.divider()
    
    # ========== AGEING TREND ==========
    st.subheader("📉 Portfolio Ageing Trend")
    
    ageing_trend = df.groupby("ageing_days").size().reset_index(name="count")
    fig_ageing = px.line(
        ageing_trend.sort_values("ageing_days"),
        x="ageing_days",
        y="count",
        title="Cases by Ageing Days",
        labels={"ageing_days": "Days in System", "count": "Number of Cases"},
        markers=True,
        line_shape="spline"
    )
    fig_ageing.update_traces(line=dict(color="#FF6600", width=3), marker=dict(size=8))
    fig_ageing.update_layout(
        plot_bgcolor="#1F2937",
        paper_bgcolor="#0E1117",
        font=dict(color="#F9FAFB"),
        hovermode="x unified",
        height=350
    )
    st.plotly_chart(fig_ageing, use_container_width=True)
    
    st.divider()
    
    # ========== INTELLIGENT CASE QUEUE ==========
    st.subheader("🎯 AI-Prioritized Case Queue (Top 30)")
    
    # Filter controls
    filter_col1, filter_col2, filter_col3 = st.columns(3)
    
    with filter_col1:
        risk_filter = st.multiselect(
            "Risk Level Filter",
            options=["CRITICAL", "HIGH", "MEDIUM", "LOW"],
            default=["CRITICAL", "HIGH"]
        )
    
    with filter_col2:
        sla_filter = st.multiselect(
            "SLA Status Filter",
            options=["BREACHED", "AT_RISK", "OK"],
            default=["BREACHED", "AT_RISK"]
        )
    
    with filter_col3:
        min_recovery = st.slider("Min Recovery Probability (%)", 0, 100, 0)
    
    # Apply filters
    filtered_df = df[
        (df["risk_level"].isin(risk_filter)) &
        (df["sla_status"].isin(sla_filter)) &
        (df["recovery_probability"] >= min_recovery)
    ].sort_values("priority_score", ascending=False)
    
    # Format display dataframe
    display_cols = [
        "case_id",
        "customer_name",
        "invoice_amount",
        "ageing_days",
        "recovery_probability",
        "risk_level",
        "sla_status",
        "assigned_dca",
        "ai_next_action"
    ]
    
    display_df = filtered_df[display_cols].head(30).copy()
    display_df["invoice_amount"] = display_df["invoice_amount"].apply(format_currency)
    display_df["recovery_probability"] = display_df["recovery_probability"].astype(str) + "%"
    
    st.dataframe(
        display_df,
        use_container_width=True,
        height=500,
        hide_index=True
    )
    
    # Export option
    csv = display_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Prioritized Queue (CSV)",
        data=csv,
        file_name=f"dca_queue_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

# ================= ADD ENTERPRISE =================
if st.session_state.page == "add":
    if check_access(["FedEx Admin"]):
        st.title("✏️ Add New Case")
        with st.form("add_enterprise"):
            customer_name = st.text_input("Enterprise / Customer Name")
            amount = st.number_input("Invoice Amount (₹)", min_value=1000)
            ageing = st.number_input("Ageing Days", min_value=1)
            business_type = st.selectbox("Business Type", ["Enterprise", "Large", "Medium", "Small"])
            dispute_status = st.selectbox("Dispute Status", ["None", "Open", "Pending_Resolution"])
            # Populate DCA options from existing data; fallback to UNASSIGNED
            try:
                dca_opts = [d for d in sorted(df['assigned_dca'].dropna().unique().tolist()) if d != ""]
            except Exception:
                dca_opts = []
            dca_options = ["UNASSIGNED"] + [d for d in dca_opts if d not in ["UNASSIGNED"]]
            assigned_dca = st.selectbox("Assign to DCA (optional)", options=dca_options, index=0)
            submit = st.form_submit_button("Save")

            if submit:
                new_case = {
                    "case_id": f"CASE_{len(df)+1}",
                    "customer_name": customer_name,
                    "ageing_days": ageing,
                    "invoice_amount": amount,
                    "business_type": business_type,
                    "dispute_status": dispute_status,
                    "assigned_dca": assigned_dca,
                    "last_dca_update_days": 0,
                    "sla_status": "OK",
                    "status": "ACTIVE",
                    "created_date": datetime.now()
                }
                df = pd.concat([df, pd.DataFrame([new_case])], ignore_index=True)
                # Persist and log only when the form is submitted
                save_data(df)
                log_audit(new_case["case_id"], "Case Created", role)
                if assigned_dca and assigned_dca != "UNASSIGNED":
                    log_audit(new_case["case_id"], f"Assigned to {assigned_dca}", role)
                st.success("✅ Case added successfully!")

# ================= ASSIGN CASE PAGE =================
elif st.session_state.page == "assign":
    if check_access(["FedEx Admin"]):
        st.title("📝 Assign Case to DCA")

        with st.form("assign_case_form"):
            case_id_input = st.text_input("Case ID to assign")
            try:
                dca_opts = [d for d in sorted(df['assigned_dca'].dropna().unique().tolist()) if d != ""]
            except Exception:
                dca_opts = []
            dca_options = ["UNASSIGNED"] + [d for d in dca_opts if d not in ["UNASSIGNED"]]
            assign_to = st.selectbox("Assign to DCA", options=dca_options, index=0)
            assign_submit = st.form_submit_button("Assign")

            if assign_submit:
                if case_id_input and case_id_input in df['case_id'].values:
                    df.loc[df['case_id'] == case_id_input, 'assigned_dca'] = assign_to
                    save_data(df)
                    log_audit(case_id_input, f"Assigned to {assign_to}", st.session_state.get('user_role', 'FedEx Admin'))
                    st.success(f"✅ {case_id_input} assigned to {assign_to}")
                else:
                    st.error("Case not found. Please verify the Case ID.")

# ================= WORKFLOW MANAGEMENT =================
elif st.session_state.page == "workflow":
    if check_access(["FedEx Admin", "DCA Agent"]):
        st.title("📋 Case Workflow & SLA Management")
    
    st.markdown("### Case Status Transitions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Search Case")
        case_search = st.text_input("Enter Case ID")
        
        if case_search and case_search in df["case_id"].values:
            case = df[df["case_id"] == case_search].iloc[0]
            
            st.markdown("#### Current Case Details")
            detail_cols = st.columns(2)
            with detail_cols[0]:
                st.write(f"**Customer:** {case['customer_name']}")
                st.write(f"**Amount:** {format_currency(case['invoice_amount'])}")
                st.write(f"**Status:** {case['status']}")
            with detail_cols[1]:
                st.write(f"**Ageing:** {case['ageing_days']} days")
                st.write(f"**Assigned DCA:** {case['assigned_dca']}")
                st.write(f"**SLA Status:** {case['sla_status']}")
            
            st.divider()
            
            st.markdown("#### Update Case Status")
            new_status = st.selectbox("New Status", ["ACTIVE", "PENDING_REVIEW", "ESCALATED", "CLOSED"])
            update_notes = st.text_area("Update Notes")
            
            if st.button("Update Status", use_container_width=True):
                df.loc[df["case_id"] == case_search, "status"] = new_status
                save_data(df)
                log_audit(case_search, f"Status Updated to {new_status}", role, update_notes)
                st.success(f"✅ Case {case_search} updated to {new_status}")
        elif case_search:
            st.warning("Case not found")
    
    with col2:
        st.subheader("SLA Dashboard")
        sla_summary = pd.DataFrame({
            "Status": df["sla_status"].value_counts().index,
            "Count": df["sla_status"].value_counts().values,
            "At Risk %": [f"{(df['sla_status'].value_counts()[s]/len(df)*100):.1f}%" for s in df["sla_status"].value_counts().index]
        })
        st.dataframe(sla_summary, use_container_width=True, hide_index=True)

# ================= DCA PERFORMANCE ANALYTICS =================
elif st.session_state.page == "dca_performance":
    if check_access(["FedEx Admin", "Compliance Officer"]):
        st.title("👥 DCA Performance & Accountability")
    
    st.subheader("📊 Agent Performance Scorecard")
    
    # Group by DCA
    dca_perf = df.groupby("assigned_dca").agg({
        "case_id": "count",
        "invoice_amount": "sum",
        "expected_recovery": "sum",
        "ageing_days": "mean",
        "recovery_probability": "mean",
        "sla_status": lambda x: (x == "OK").sum()
    }).rename(columns={
        "case_id": "Cases Assigned",
        "invoice_amount": "Total Portfolio",
        "expected_recovery": "Expected Recovery",
        "ageing_days": "Avg Ageing",
        "recovery_probability": "Avg Recovery Prob",
        "sla_status": "SLA Compliant"
    })
    
    dca_perf["Recovery Efficiency %"] = (dca_perf["Expected Recovery"] / dca_perf["Total Portfolio"] * 100).round(1)
    dca_perf = dca_perf.round(2)
    
    st.dataframe(dca_perf, use_container_width=True)
    
    st.divider()
    
    # Individual DCA drill-down
    st.subheader("📈 Individual DCA Deep Dive")
    selected_dca = st.selectbox("Select DCA Agent", df["assigned_dca"].unique())
    
    dca_cases = df[df["assigned_dca"] == selected_dca]
    
    perf_col1, perf_col2, perf_col3, perf_col4 = st.columns(4)
    
    with perf_col1:
        st.metric("Cases Assigned", len(dca_cases))
    with perf_col2:
        st.metric("Portfolio Value", format_currency(dca_cases["invoice_amount"].sum()))
    with perf_col3:
        st.metric("Expected Recovery", format_currency(dca_cases["expected_recovery"].sum()))
    with perf_col4:
        sla_ok = (dca_cases["sla_status"] == "OK").sum()
        st.metric("SLA Compliant", f"{sla_ok}/{len(dca_cases)}")
    
    st.markdown("**Recent Cases:**")
    st.dataframe(
        dca_cases[[
            "case_id", "customer_name", "invoice_amount", 
            "ageing_days", "recovery_probability", "sla_status"
        ]].head(10),
        use_container_width=True,
        hide_index=True
    )

# ================= ADVANCED ANALYTICS =================
elif st.session_state.page == "analytics":
    if check_access(["FedEx Admin", "Compliance Officer"]):
        st.title("📊 Advanced Analytics & Insights")
    
    st.subheader("💡 Key Insights")
    
    insight_col1, insight_col2, insight_col3 = st.columns(3)
    
    with insight_col1:
        critical_cases = len(df[df["risk_level"] == "CRITICAL"])
        st.metric(
            "🚨 Critical Cases",
            critical_cases,
            f"{critical_cases/len(df)*100:.1f}% of portfolio"
        )
    
    with insight_col2:
        high_recovery = len(df[df["recovery_probability"] > 75])
        st.metric(
            "✅ High Recovery Prob",
            high_recovery,
            f"Expected: {format_currency(df[df['recovery_probability'] > 75]['expected_recovery'].sum())}"
        )
    
    with insight_col3:
        aging_90plus = len(df[df["ageing_days"] > 90])
        st.metric(
            "⏳ Aging >90 Days",
            aging_90plus,
            f"{aging_90plus/len(df)*100:.1f}% at risk"
        )
    
    st.divider()
    
    st.subheader("📈 Recovery Trend Analysis")
    
    # Recovery by recovery probability buckets
    df["recovery_bucket"] = pd.cut(df["recovery_probability"], 
                                    bins=[0, 25, 50, 75, 100],
                                    labels=["Low (0-25%)", "Medium (25-50%)", "High (50-75%)", "Very High (75-100%)"])
    
    recovery_by_bucket = df.groupby("recovery_bucket").agg({
        "case_id": "count",
        "expected_recovery": "sum"
    }).reset_index()
    
    fig_recovery = px.bar(
        recovery_by_bucket,
        x="recovery_bucket",
        y=["case_id", "expected_recovery"],
        title="Cases & Expected Recovery by Probability Bucket",
        barmode="group",
        labels={"case_id": "Number of Cases", "expected_recovery": "Expected Recovery"}
    )
    fig_recovery.update_layout(
        plot_bgcolor="#1F2937",
        paper_bgcolor="#0E1117",
        font=dict(color="#F9FAFB")
    )
    st.plotly_chart(fig_recovery, use_container_width=True)

# ================= PREDICTIVE ANALYTICS =================
elif st.session_state.page == "predictive":
    if check_access(["FedEx Admin", "Compliance Officer"]):
        st.title("🧠 Predictive Analytics & AI Insights")
        
        st.markdown("**Advanced ML predictions for optimal case management and recovery strategy**")
        st.divider()
        
        # Compute predictive metrics for all cases
        df["churn_risk"] = df.apply(compute_churn_risk, axis=1)
        df["optimal_followup_days"] = df.apply(compute_optimal_followup_timing, axis=1)
        
        # Tabs for different analyses
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Recovery Probability Analysis",
            "⚠️ Churn Risk Assessment", 
            "📞 Follow-up Strategy",
            "👥 DCA Efficiency Scores"
        ])
        
        # ===== TAB 1: RECOVERY PROBABILITY =====
        with tab1:
            st.subheader("Recovery Probability Heatmap")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Average Recovery Probability", 
                         f"{df['recovery_probability'].mean():.1f}%")
                st.metric("High Confidence Cases (>70%)", 
                         len(df[df['recovery_probability'] > 70]))
                st.metric("Low Probability Cases (<30%)", 
                         len(df[df['recovery_probability'] < 30]))
            
            with col2:
                st.metric("Expected Total Recovery", 
                         format_currency(df['expected_recovery'].sum()))
                st.metric("At-Risk Cases (30-50%)", 
                         len(df[(df['recovery_probability'] >= 30) & (df['recovery_probability'] <= 50)]))
                st.metric("Medium Probability (50-70%)", 
                         len(df[(df['recovery_probability'] > 50) & (df['recovery_probability'] <= 70)]))
            
            st.divider()
            
            # Recovery probability distribution
            prob_dist = pd.cut(df['recovery_probability'], 
                              bins=[0, 20, 40, 60, 80, 100],
                              labels=['0-20%', '20-40%', '40-60%', '60-80%', '80-100%'])
            
            fig_prob_dist = px.bar(
                prob_dist.value_counts().sort_index(),
                title='Cases by Recovery Probability Range',
                labels={'index': 'Probability Range', 'value': 'Number of Cases'},
                color_discrete_sequence=['#EF4444', '#F97316', '#FBBF24', '#86EFAC', '#22C55E']
            )
            fig_prob_dist.update_layout(
                plot_bgcolor="#1F2937",
                paper_bgcolor="#0E1117",
                font=dict(color="#F9FAFB"),
                showlegend=False
            )
            st.plotly_chart(fig_prob_dist, use_container_width=True)
            
            # Top recovery cases
            st.subheader("🔝 Top 10 Highest Recovery Probability Cases")
            top_recovery = df.nlargest(10, 'recovery_probability')[
                ['case_id', 'customer_name', 'invoice_amount', 'recovery_probability', 
                 'ageing_days', 'dispute_status']
            ].copy()
            top_recovery['invoice_amount'] = top_recovery['invoice_amount'].apply(format_currency)
            top_recovery['recovery_probability'] = top_recovery['recovery_probability'].apply(lambda x: f"{x:.1f}%")
            st.dataframe(top_recovery, use_container_width=True, hide_index=True)
        
        # ===== TAB 2: CHURN RISK =====
        with tab2:
            st.subheader("Churn Risk Prediction")
            st.markdown("**Probability that customers WON'T pay - Higher % = Higher default risk**")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                avg_churn = df['churn_risk'].mean()
                st.metric("Average Churn Risk", f"{avg_churn:.1f}%")
            
            with col2:
                high_churn = len(df[df['churn_risk'] > 70])
                st.metric("🔴 CRITICAL Churn Risk (>70%)", high_churn)
            
            with col3:
                low_churn = len(df[df['churn_risk'] < 30])
                st.metric("🟢 Low Churn Risk (<30%)", low_churn)
            
            st.divider()
            
            # Churn vs Recovery scatter
            fig_churn_scatter = px.scatter(
                df,
                x='recovery_probability',
                y='churn_risk',
                size='invoice_amount',
                color='risk_level',
                hover_data=['case_id', 'customer_name', 'ageing_days'],
                title='Churn Risk vs Recovery Probability',
                labels={'recovery_probability': 'Recovery Probability (%)', 
                       'churn_risk': 'Churn Risk (%)'},
                color_discrete_map={'LOW': '#22C55E', 'MEDIUM': '#FBBF24', 
                                   'HIGH': '#F97316', 'CRITICAL': '#EF4444'}
            )
            fig_churn_scatter.update_layout(
                plot_bgcolor="#1F2937",
                paper_bgcolor="#0E1117",
                font=dict(color="#F9FAFB")
            )
            st.plotly_chart(fig_churn_scatter, use_container_width=True)
            
            # High churn risk cases
            st.subheader("🚨 High Churn Risk Cases (Immediate Action Required)")
            high_risk_churn = df[df['churn_risk'] > 70].nlargest(10, 'churn_risk')[
                ['case_id', 'customer_name', 'invoice_amount', 'churn_risk', 
                 'ageing_days', 'dispute_status']
            ].copy()
            high_risk_churn['invoice_amount'] = high_risk_churn['invoice_amount'].apply(format_currency)
            high_risk_churn['churn_risk'] = high_risk_churn['churn_risk'].apply(lambda x: f"{x:.1f}%")
            
            if len(high_risk_churn) > 0:
                st.dataframe(high_risk_churn, use_container_width=True, hide_index=True)
            else:
                st.success("✅ No high churn risk cases detected!")
        
        # ===== TAB 3: FOLLOW-UP STRATEGY =====
        with tab3:
            st.subheader("Optimal Follow-up Timing Recommendations")
            st.markdown("**AI-optimized contact frequency based on recovery probability and case aging**")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                urgent_3day = len(df[df['optimal_followup_days'] <= 3])
                st.metric("🔥 Urgent (≤3 days)", urgent_3day)
            
            with col2:
                medium_week = len(df[(df['optimal_followup_days'] > 3) & (df['optimal_followup_days'] <= 7)])
                st.metric("⚡ Weekly (4-7 days)", medium_week)
            
            with col3:
                biweekly = len(df[(df['optimal_followup_days'] > 7) & (df['optimal_followup_days'] <= 14)])
                st.metric("📅 Bi-weekly (8-14 days)", biweekly)
            
            with col4:
                monthly = len(df[df['optimal_followup_days'] > 14])
                st.metric("📆 Monthly+ (>14 days)", monthly)
            
            st.divider()
            
            # Follow-up frequency distribution
            followup_buckets = pd.cut(df['optimal_followup_days'],
                                     bins=[0, 3, 7, 14, 100],
                                     labels=['Urgent ≤3d', 'Weekly 4-7d', 'Bi-weekly 8-14d', 'Monthly >14d'])
            
            fig_followup = px.pie(
                followup_buckets.value_counts(),
                labels=followup_buckets.unique(),
                title='Case Distribution by Recommended Follow-up Frequency',
                color_discrete_sequence=['#EF4444', '#F97316', '#FBBF24', '#86EFAC']
            )
            fig_followup.update_layout(
                paper_bgcolor="#0E1117",
                font=dict(color="#F9FAFB")
            )
            st.plotly_chart(fig_followup, use_container_width=True)
            
            # Cases needing urgent follow-up
            st.subheader("🔥 Urgent Follow-up Required (Within 3 Days)")
            urgent_cases = df[df['optimal_followup_days'] <= 3].nlargest(10, 'priority_score')[
                ['case_id', 'customer_name', 'invoice_amount', 'optimal_followup_days',
                 'recovery_probability', 'churn_risk']
            ].copy()
            urgent_cases['invoice_amount'] = urgent_cases['invoice_amount'].apply(format_currency)
            urgent_cases['recovery_probability'] = urgent_cases['recovery_probability'].apply(lambda x: f"{x:.1f}%")
            urgent_cases['churn_risk'] = urgent_cases['churn_risk'].apply(lambda x: f"{x:.1f}%")
            urgent_cases['optimal_followup_days'] = urgent_cases['optimal_followup_days'].apply(lambda x: f"{int(x)} days")
            
            if len(urgent_cases) > 0:
                st.dataframe(urgent_cases, use_container_width=True, hide_index=True)
            else:
                st.success("✅ No urgent follow-ups needed!")
        
        # ===== TAB 4: DCA EFFICIENCY =====
        with tab4:
            st.subheader("Individual DCA Efficiency Scores")
            st.markdown("**Composite metric: Recovery Rate × Responsiveness × Resolution Rate**")
            
            # Calculate efficiency for each DCA
            dca_efficiency = []
            for dca in df['assigned_dca'].unique():
                dca_cases = df[df['assigned_dca'] == dca]
                efficiency = compute_dca_efficiency_score(dca_cases)
                avg_recovery = dca_cases['recovery_probability'].mean()
                cases_count = len(dca_cases)
                expected_recovery = dca_cases['expected_recovery'].sum()
                avg_responsiveness = 100 - dca_cases['last_dca_update_days'].mean()
                
                dca_efficiency.append({
                    'DCA': dca,
                    'Efficiency Score': efficiency,
                    'Cases': cases_count,
                    'Avg Recovery %': round(avg_recovery, 1),
                    'Responsiveness %': round(avg_responsiveness, 1),
                    'Expected Recovery': format_currency(expected_recovery)
                })
            
            efficiency_df = pd.DataFrame(dca_efficiency).sort_values('Efficiency Score', ascending=False)
            
            # Display efficiency scores
            fig_dca_eff = px.bar(
                efficiency_df,
                x='DCA',
                y='Efficiency Score',
                title='DCA Efficiency Comparison',
                color='Efficiency Score',
                color_continuous_scale='RdYlGn'
            )
            fig_dca_eff.update_layout(
                plot_bgcolor="#1F2937",
                paper_bgcolor="#0E1117",
                font=dict(color="#F9FAFB"),
                showlegend=False
            )
            st.plotly_chart(fig_dca_eff, use_container_width=True)
            
            # Detailed efficiency table
            st.subheader("📊 DCA Performance Details")
            st.dataframe(efficiency_df, use_container_width=True, hide_index=True)
            
            # Top performer highlights
            if len(efficiency_df) > 0:
                top_dca = efficiency_df.iloc[0]
                st.success(f"🏆 **Top Performer:** {top_dca['DCA']} with {top_dca['Efficiency Score']:.1f} efficiency score")
        
        # ===== CASE-LEVEL INSIGHTS =====
        st.divider()
        st.subheader("🔍 Case-Level Predictive Insights")
        st.markdown("Select a case to view comprehensive predictive analysis")
        
        selected_case = st.selectbox(
            "Select Case",
            options=df['case_id'].tolist(),
            format_func=lambda x: f"{x} - {df[df['case_id']==x]['customer_name'].values[0]}"
        )
        
        case_data = df[df['case_id'] == selected_case].iloc[0]
        insights = get_predictive_insights(case_data)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Recovery Probability", f"{insights['recovery_probability']:.1f}%")
        with col2:
            st.metric("Churn Risk", f"{insights['churn_risk']:.1f}%")
        with col3:
            st.metric("Optimal Follow-up", f"{insights['optimal_followup_days']} days")
        with col4:
            st.metric("Invoice Amount", format_currency(case_data['invoice_amount']))
        
        st.divider()
        
        col_insight1, col_insight2 = st.columns(2)
        
        with col_insight1:
            st.info(f"**Insight:** {insights['insight_type']}")
        
        with col_insight2:
            st.warning(f"**Recommendation:** {insights['recommendation']}")

# ================= LIVE UPDATES / DCA ACTIVITY =================
elif st.session_state.page == "live_updates":
    if check_access(["FedEx Admin", "Compliance Officer"]):
        st.title("⚡ Live DCA Activity & Updates")
        
        st.markdown("**Real-time tracking of all DCA actions and case updates**")

        st.divider()
        
        try:
            audit_df = pd.read_csv(AUDIT_PATH)
            
            if len(audit_df) == 0:
                st.info("No activity recorded yet")
            else:
                # Convert timestamp to datetime
                audit_df['timestamp'] = pd.to_datetime(audit_df['timestamp'])
                
                # Sort by most recent
                audit_df = audit_df.sort_values('timestamp', ascending=False)
                
                # Activity filters
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    time_filter = st.selectbox(
                        "Time Range",
                        ["Last Hour", "Last 24 Hours", "Last 7 Days", "All Time"]
                    )
                
                with col2:
                    dca_filter = st.multiselect(
                        "Filter by DCA",
                        options=["All"] + sorted(df['assigned_dca'].unique().tolist()),
                        default=["All"]
                    )
                
                with col3:
                    action_filter = st.multiselect(
                        "Filter by Action Type",
                        options=["All"] + sorted(audit_df['action'].unique().tolist()),
                        default=["All"]
                    )
                
                # Apply time filter
                now = datetime.now()
                if time_filter == "Last Hour":
                    filtered_audit = audit_df[audit_df['timestamp'] > (now - timedelta(hours=1))]
                elif time_filter == "Last 24 Hours":
                    filtered_audit = audit_df[audit_df['timestamp'] > (now - timedelta(days=1))]
                elif time_filter == "Last 7 Days":
                    filtered_audit = audit_df[audit_df['timestamp'] > (now - timedelta(days=7))]
                else:
                    filtered_audit = audit_df
                
                # Apply DCA filter
                if "All" not in dca_filter:
                    filtered_audit = filtered_audit[filtered_audit['user'].isin(dca_filter)]
                
                # Apply action filter
                if "All" not in action_filter:
                    filtered_audit = filtered_audit[filtered_audit['action'].isin(action_filter)]
                
                st.divider()
                
                # Stats
                metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
                
                with metric_col1:
                    st.metric("Total Updates", len(filtered_audit), delta=None)
                with metric_col2:
                    st.metric("Active DCAs", filtered_audit['user'].nunique(), delta=None)
                with metric_col3:
                    st.metric("Cases Updated", filtered_audit['case_id'].nunique(), delta=None)
                with metric_col4:
                    st.metric("Action Types", filtered_audit['action'].nunique(), delta=None)
                
                st.divider()
                
                # Live feed
                st.subheader("📡 Activity Feed")
                
                if len(filtered_audit) == 0:
                    st.info("No activities found for selected filters")
                else:
                    # Display as cards/timeline
                    for idx, row in filtered_audit.iterrows():
                        with st.container():
                            col_time, col_content = st.columns([1, 4])
                            
                            with col_time:
                                time_str = row['timestamp'].strftime('%H:%M:%S')
                                date_str = row['timestamp'].strftime('%m/%d')
                                st.markdown(f"**{time_str}**")
                                st.caption(date_str)
                            
                            with col_content:
                                # Action badge color coding
                                action = row['action']
                                if 'Status' in action or 'Update' in action:
                                    badge_color = "🟢"
                                elif 'Error' in action or 'Reject' in action:
                                    badge_color = "🔴"
                                elif 'Create' in action or 'Add' in action:
                                    badge_color = "🔵"
                                else:
                                    badge_color = "🟡"
                                
                                st.markdown(f"{badge_color} **{action}**")
                                
                                # Case and user details
                                details_str = f"**Case:** {row['case_id']} | **DCA:** {row['user']}"
                                if pd.notna(row['details']) and row['details'] != "":
                                    details_str += f" | **Details:** {row['details']}"
                                
                                st.caption(details_str)
                        
                        st.divider()
                
                # DCA Activity Summary
                st.subheader("👥 DCA Activity Summary")
                
                dca_activity = filtered_audit.groupby('user').agg({
                    'case_id': 'count',
                    'action': 'nunique',
                    'timestamp': lambda x: (now - x.max()).total_seconds() / 60  # minutes ago
                }).rename(columns={
                    'case_id': 'Actions Taken',
                    'action': 'Action Types',
                    'timestamp': 'Last Active (mins ago)'
                }).round(0)
                
                dca_activity = dca_activity.sort_values('Actions Taken', ascending=False)
                
                st.dataframe(dca_activity, use_container_width=True)
                
                # Action Type Distribution
                st.subheader("📊 Action Distribution")
                
                col_chart1, col_chart2 = st.columns(2)
                
                with col_chart1:
                    action_dist = filtered_audit['action'].value_counts().reset_index()
                    action_dist.columns = ['Action', 'Count']
                    
                    fig_action = px.bar(
                        action_dist,
                        x='Action',
                        y='Count',
                        title='Actions by Type',
                        labels={'Count': 'Number of Actions'}
                    )
                    fig_action.update_layout(
                        plot_bgcolor="#1F2937",
                        paper_bgcolor="#0E1117",
                        font=dict(color="#F9FAFB"),
                        xaxis_tickangle=-45
                    )
                    st.plotly_chart(fig_action, use_container_width=True)
                
                with col_chart2:
                    dca_dist = filtered_audit['user'].value_counts().reset_index()
                    dca_dist.columns = ['DCA', 'Count']
                    
                    fig_dca = px.pie(
                        dca_dist,
                        names='DCA',
                        values='Count',
                        title='Actions by DCA'
                    )
                    fig_dca.update_layout(
                        paper_bgcolor="#0E1117",
                        font=dict(color="#F9FAFB")
                    )
                    st.plotly_chart(fig_dca, use_container_width=True)
        
        except Exception as e:
            st.error(f"Error loading activity data: {str(e)}")

# ================= COMPLIANCE & AUDIT TRAIL =================
elif st.session_state.page == "audit":
    if check_access(["FedEx Admin", "Compliance Officer"]):
        st.title("🔍 Compliance & Audit Trail")
    
    st.subheader("📋 Full Audit Log")
    
    try:
        audit_df = pd.read_csv(AUDIT_PATH)
        
        # Filters
        filter_col1, filter_col2, filter_col3 = st.columns(3)
        
        with filter_col1:
            action_filter = st.multiselect(
                "Action Type",
                options=audit_df["action"].unique(),
                default=audit_df["action"].unique()[:3]
            )
        
        with filter_col2:
            user_filter = st.multiselect(
                "User",
                options=audit_df["user"].unique(),
                default=audit_df["user"].unique()
            )
        
        with filter_col3:
            days_back = st.slider("Last N Days", 1, 90, 30)
        
        # Filter audit
        filtered_audit = audit_df[
            (audit_df["action"].isin(action_filter)) &
            (audit_df["user"].isin(user_filter))
        ].sort_values("timestamp", ascending=False)
        
        st.dataframe(filtered_audit, use_container_width=True, hide_index=True)
        
        st.divider()
        st.subheader("📊 Audit Statistics")
        
        stat_col1, stat_col2, stat_col3 = st.columns(3)
        
        with stat_col1:
            st.metric("Total Audit Events", len(audit_df))
        with stat_col2:
            st.metric("Unique Users", audit_df["user"].nunique())
        with stat_col3:
            st.metric("Actions Logged", audit_df["action"].nunique())
        
    except:
        st.info("No audit log found yet")

# ================= DATABASE =================
if st.session_state.page == "database":
    if check_access(["FedEx Admin"]):
        st.title("Complete Dataset")
        st.dataframe(df, use_container_width=True, height=600)
