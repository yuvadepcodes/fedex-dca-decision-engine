import streamlit as st

def role_toggle():
    if "role" not in st.session_state:
        st.session_state.role = "FedEx Admin"
    role = st.radio("Select Role", ["FedEx Admin", "DCA Agent"])
    st.session_state.role = role
    return role
