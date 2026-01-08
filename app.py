import streamlit as st
import pandas as pd
import os
from models.scoring import apply_scoring

# --------------------------
# Page Config (RECTANGULAR)
# --------------------------
st.set_page_config(layout="wide")

# --------------------------
# Page + Role State
# --------------------------
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

if "role" not in st.session_state:
    st.session_state.role = "FedEx Admin"

# --------------------------
# Sidebar
# --------------------------
st.sidebar.title("FedEx DCA System")
role = st.sidebar.radio("Select Role", ["FedEx Admin", "DCA Agent"])
st.session_state.role = role

# --------------------------
# Load Data
# --------------------------
CSV_PATH = "data/nexus_accounts.csv"

if not os.path.exists(CSV_PATH):
    st.error("CSV not found. Generate nexus_accounts.csv first.")
    st.stop()

df = pd.read_csv(CSV_PATH)

# Type safety
df["ageing_days"] = df["ageing_days"].astype(int)
df["invoice_amount"] = df["invoice_amount"].astype(float)
df["last_dca_update_days"] = df["last_dca_update_days"].astype(int)

# Apply AI scoring
df = apply_scoring(df)

# Top-priority queue
df_view = df[df["recovery_score"] > 0.6]

# --------------------------
# Utilities
# --------------------------
def get_new_case_id(df):
    nums = []
    for cid in df["case_id"]:
        try:
            nums.append(int(cid.split("_")[1]))
        except:
            pass
    return f"CASE_{max(nums, default=0) + 1}"

# --------------------------
# Top Right Navigation
# --------------------------
col1, col2, col3 = st.columns([8, 1, 1])
with col3:
    if st.button("📊 View Database"):
        st.session_state.page = "Database"

# --------------------------
# Dashboard
# --------------------------
def show_dashboard(df_view):
    st.markdown("## Daily Action Queue")

    tab1, tab2 = st.tabs(["Assigned", "In Progress"])

    with tab1:
        assigned = df_view[df_view["last_dca_update_days"] <= 2]
        st.dataframe(assigned, use_container_width=True, height=420)

    with tab2:
        in_progress = df_view[df_view["last_dca_update_days"] > 2]
        st.dataframe(in_progress, use_container_width=True, height=420)

    # --------------------------
    # Admin Controls
    # --------------------------
    if st.session_state.role == "FedEx Admin":

        st.markdown("---")
        st.markdown("## Add New Enterprise")

        with st.form("add_enterprise"):
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                customer_name = st.text_input("Customer Name")
            with c2:
                invoice_amount = st.number_input("Invoice Amount (INR)", min_value=1000)
            with c3:
                ageing_days = st.number_input("Ageing Days", min_value=0)
            with c4:
                dispute_status = st.selectbox("Dispute Status", ["None", "Open", "Resolved"])

            submit = st.form_submit_button("Add Enterprise")

            if submit:
                df_all = pd.read_csv(CSV_PATH)
                new_row = {
                    "case_id": get_new_case_id(df_all),
                    "customer_name": customer_name,
                    "ageing_days": ageing_days,
                    "invoice_amount": invoice_amount,
                    "business_type": "Enterprise",
                    "dispute_status": dispute_status,
                    "assigned_dca": "",
                    "last_dca_update_days": 0,
                    "sla_status": "OK",
                    "status": "ACTIVE"
                }
                df_all = pd.concat([df_all, pd.DataFrame([new_row])], ignore_index=True)
                df_all.to_csv(CSV_PATH, index=False)
                st.success("Enterprise added successfully")

        # --------------------------
        # Assign DCA
        # --------------------------
        st.markdown("---")
        st.markdown("## Assign DCA Agent")

        df_all = pd.read_csv(CSV_PATH)

        c1, c2 = st.columns([2, 1])
        with c1:
            case_id_input = st.text_input("Enter Case ID (e.g. CASE_12)")
        with c2:
            agent = st.selectbox("Assign to DCA", ["DCA_A", "DCA_B", "DCA_C"])

        if case_id_input:
            if case_id_input in df_all["case_id"].values:
                case = df_all[df_all["case_id"] == case_id_input].iloc[0]

                st.markdown(
                    f"""
                    **Customer:** {case.get('customer_name','')}  
                    **Amount:** INR {case['invoice_amount']}  
                    **Business:** {case['business_type']}  
                    **Current DCA:** {case['assigned_dca'] or 'Unassigned'}
                    """
                )

                if st.button("Assign"):
                    df_all.loc[df_all["case_id"] == case_id_input, "assigned_dca"] = agent
                    df_all.to_csv(CSV_PATH, index=False)
                    st.success(f"{case_id_input} assigned to {agent}")
            else:
                st.warning("Invalid Case ID")

# --------------------------
# DCA Dashboard
# --------------------------
def show_dca_dashboard(df_view):
    dca = st.selectbox("Select DCA", ["DCA_A", "DCA_B", "DCA_C"])
    df_dca = df_view[df_view["assigned_dca"] == dca]
    st.markdown(f"## {dca} – Assigned Cases")
    st.dataframe(df_dca, use_container_width=True, height=420)

# --------------------------
# Database Page
# --------------------------
def show_database_page():
    st.markdown("## 📁 Nexus Master Database")

    df_all = pd.read_csv(CSV_PATH)

    c1, c2 = st.columns(2)
    with c1:
        dca_filter = st.selectbox("Filter by DCA", ["All"] + sorted(df_all["assigned_dca"].unique()))
    with c2:
        status_filter = st.selectbox("Filter by Status", ["All"] + sorted(df_all["status"].unique()))

    if dca_filter != "All":
        df_all = df_all[df_all["assigned_dca"] == dca_filter]
    if status_filter != "All":
        df_all = df_all[df_all["status"] == status_filter]

    st.dataframe(df_all, use_container_width=True, height=500)

    st.markdown("---")
    if st.button("⬅ Back to Dashboard"):
        st.session_state.page = "Dashboard"

# --------------------------
# Router
# --------------------------
if st.session_state.page == "Database":
    show_database_page()
else:
    if st.session_state.role == "FedEx Admin":
        show_dashboard(df_view)
    else:
        show_dca_dashboard(df_view)
