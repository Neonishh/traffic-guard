# Home.py
import streamlit as st
from database import Database
import pandas as pd

st.set_page_config(
    page_title="Traffic Violation Management",
    page_icon="🚦",
    layout="wide"
)

db = Database()

st.title("🚦 Traffic Violation Management System")
st.markdown("---")

# Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    drivers = db.fetch_data("SELECT COUNT(*) as count FROM Driver")
    st.metric("👤 Drivers", drivers[0]['count'] if drivers else 0)

with col2:
    violations = db.fetch_data("SELECT COUNT(*) as count FROM Violation")
    st.metric("⚠️ Violations", violations[0]['count'] if violations else 0)

with col3:
    unpaid = db.fetch_data("SELECT COUNT(*) as count FROM Penalty WHERE Status = 'Unpaid'")
    st.metric("💰 Unpaid", unpaid[0]['count'] if unpaid else 0)

with col4:
    total = db.fetch_data("SELECT COALESCE(SUM(Amount), 0) as total FROM Penalty WHERE Status = 'Unpaid'")
    st.metric("💵 Amount", f"₹{total[0]['total']:,.0f}" if total else "₹0")

st.markdown("---")


st.info("👈 Use sidebar to manage data")
