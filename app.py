import streamlit as st
import pandas as pd
import os
from models.scoring import apply_scoring  # Make sure scoring.py exists

# --------------------------
# Sidebar Role Toggle
# --------------------------
if "role" not in st.session_state:
    st.session_state.role = "FedEx Admin"

role = st.sidebar.radio("Select Role", ["FedEx Admin", "DCA Agent"])
st.session_state.role = role

# --------------------------
# Load Data
# --------------------------
if not os.path.exists("data/nexus_accounts.csv"):
    st.error("CSV not found. Generate nexus_accounts.csv first!")
    st.stop()

df = pd.read_csv("data/nexus_accounts.csv")

# Ensure numeric columns
df["ageing_days"] = df["ageing_days"].astype(int)
df["invoice_amount"] = df["invoice_amount"].astype(float)
df["last_dca_update_days"] = df["last_dca_update_days"].astype(int)

# Apply scoring model
df = apply_scoring(df)
# Keep only top-priority cases (recovery_score > 0.6)
df_view = df[df["recovery_score"] > 0.6]

# --------------------------
# Helper: generate new CASE_ID
# --------------------------
def get_new_case_id(df):
    numeric_ids = []
    for cid in df["case_id"]:
        try:
            num = int(str(cid).split("_")[1])
            numeric_ids.append(num)
        except:
            continue
    return f"CASE_{max(numeric_ids, default=0) + 1}"

# --------------------------
# Dashboard Function
# --------------------------
def show_dashboard(df_view):
    st.subheader("Daily Action Queue")
    
    # Tabs for Assigned / In Progress
    tab1, tab2 = st.tabs(["Assigned", "In Progress"])
    
    with tab1:
        assigned = df_view[(df_view["status"]=="ACTIVE") & (df_view["last_dca_update_days"] <= 2)]
        st.dataframe(assigned, use_container_width=True)

    with tab2:
        in_progress = df_view[(df_view["status"]=="ACTIVE") & (df_view["last_dca_update_days"] > 2)]
        st.dataframe(in_progress, use_container_width=True)

    # --------------------------
    # Admin-only: Add Enterprise
    # --------------------------
    if role == "FedEx Admin":
        st.markdown("---")
        st.subheader("Add New Enterprise")
        with st.form("add_enterprise_form"):
            customer_name = st.text_input("Customer Name")
            invoice_amount = st.number_input("Invoice Amount (INR)", min_value=1000)
            ageing_days = st.number_input("Ageing Days", min_value=0)
            dispute_status = st.selectbox("Dispute Status", ["None","Open","Resolved"])
            submitted = st.form_submit_button("Add Enterprise")

            if submitted:
                df = pd.read_csv("data/nexus_accounts.csv")
                new_case_id = get_new_case_id(df)
                new_row = {
                    "case_id": new_case_id,
                    "customer_name": customer_name,
                    "invoice_amount": invoice_amount,
                    "business_type": "Enterprise",
                    "ageing_days": ageing_days,
                    "dispute_status": dispute_status,
                    "sla_status": "OK",
                    "last_dca_update_days": 0,
                    "assigned_dca": "",
                    "status": "ACTIVE"
                }
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                df.to_csv("data/nexus_accounts.csv", index=False)
                st.success(f"Enterprise '{customer_name}' added!")

        # --------------------------
        # Admin-only: Assign DCA manually
        # --------------------------
        st.markdown("---")
        st.subheader("Assign DCA Agent to Enterprise")
        df = pd.read_csv("data/nexus_accounts.csv")

        selected_case_id = st.text_input("Enter Case ID (e.g., CASE_5)")

        if selected_case_id:
            if selected_case_id in df["case_id"].values:
                selected_case = df[df["case_id"] == selected_case_id].iloc[0]
                st.markdown(f"**Customer:** {selected_case['customer_name']} | "
                            f"{selected_case['business_type']} | "
                            f"INR {selected_case['invoice_amount']} | "
                            f"Dispute: {selected_case['dispute_status']} | "
                            f"Assigned DCA: {selected_case['assigned_dca'] or 'None'}")

                agent = st.selectbox("Assign to DCA Agent", ["DCA_A", "DCA_B", "DCA_C"])

                if st.button("Assign DCA"):
                    df.loc[df["case_id"] == selected_case_id, "assigned_dca"] = agent
                    df.to_csv("data/nexus_accounts.csv", index=False)
                    st.success(f"{selected_case_id} assigned to {agent}")

            else:
                st.warning("Case ID not found in the system.")

# --------------------------
# DCA Dashboard
# --------------------------
def show_dca_dashboard(df_view):
    dca_name = st.selectbox("Select Your Name", ["DCA_A","DCA_B","DCA_C"])
    df_view = df_view[df_view["assigned_dca"] == dca_name]
    st.subheader(f"{dca_name} - Your Daily Action Queue")
    st.dataframe(df_view, use_container_width=True)

# --------------------------
# Page Routing
# --------------------------
if role == "FedEx Admin":
    show_dashboard(df_view)
else:
    show_dca_dashboard(df_view)
