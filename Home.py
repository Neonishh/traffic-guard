# Home.py
import streamlit as st
from database import Database
import pandas as pd

st.set_page_config(page_title="Traffic Violation Management", page_icon="🚦", layout="wide")

# Sidebar Login
if "db_user" not in st.session_state:
    st.session_state.db_user = None

st.sidebar.header("🔐 Database Login")

user_type = st.sidebar.selectbox("Login As", ["Admin", "Data Entry", "Viewer"])
if user_type == "Admin":
    username, password = "admin_user", "admin123"
elif user_type == "Data Entry":
    username, password = "data_entry", "entry123"
else:
    username, password = "viewer", "view123"

if st.sidebar.button("Connect"):
    st.session_state.db_user = username
    st.session_state.db_pass = password
    st.success(f"Connected as {username}")

if not st.session_state.db_user:
    st.warning("Please connect using sidebar before proceeding.")
    st.stop()

db = Database(st.session_state.db_user, st.session_state.db_pass)

st.title("🚦 Traffic Violation Management System")
st.markdown("---")

# Quick Stats
col1, col2, col3, col4 = st.columns(4)

drivers = db.fetch_data("SELECT COUNT(*) AS count FROM Driver")
violations = db.fetch_data("SELECT COUNT(*) AS count FROM Violation")
unpaid = db.fetch_data("SELECT COUNT(*) AS count FROM Penalty WHERE Status='Unpaid'")
amount = db.fetch_data("SELECT COALESCE(SUM(Amount),0) AS total FROM Penalty WHERE Status='Unpaid'")

with col1:
    st.metric("👤 Drivers", drivers[0]['count'] if drivers else 0)
with col2:
    st.metric("⚠️ Violations", violations[0]['count'] if violations else 0)
with col3:
    st.metric("💰 Unpaid Fines", unpaid[0]['count'] if unpaid else 0)
with col4:
    st.metric("💵 Total Due", f"₹{amount[0]['total']:,.0f}" if amount else "₹0")

st.markdown("---")
st.info("👈 Use the sidebar to navigate between management and reports.")
