import streamlit as st
import pandas as pd
from model.prioritization import run_prioritization

st.set_page_config(
    page_title="FedEx DCA Decision Engine",
    layout="wide"
)

st.title("FedEx DCA Decision Engine")
st.caption("AI-assisted prioritization and allocation of overdue B2B cases")

st.markdown("---")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("data/cases.csv")

df = load_data()

st.subheader("Input Cases")
st.write("Sample of incoming overdue cases")
st.dataframe(df.head(10), use_container_width=True)

st.markdown("---")

st.subheader("AI-Powered Prioritization")

if st.button("Run Prioritization Engine"):
    result = run_prioritization(df)

    st.success("Prioritization completed successfully.")

    st.write("Top 10 High-Priority Cases")
    top_cases = result.sort_values(
        by="priority_score", ascending=False
    ).head(10)

    st.dataframe(
        top_cases[[
            "case_id",
            "overdue_amount",
            "days_overdue",
            "recovery_probability",
            "priority_score",
            "confidence_level",
            "recommended_dca"
        ]],
        use_container_width=True
    )

    st.markdown("---")
    st.subheader("Decision Summary")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "High Priority Cases",
            (result["priority_score"] >= 0.75).sum()
        )

    with col2:
        st.metric(
            "Medium Priority Cases",
            ((result["priority_score"] >= 0.5) &
             (result["priority_score"] < 0.75)).sum()
        )

    with col3:
        st.metric(
            "Low Priority Cases",
            (result["priority_score"] < 0.5).sum()
        )
