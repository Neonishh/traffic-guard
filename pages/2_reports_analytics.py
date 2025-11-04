# 2_reports_analytics.py
import streamlit as st
import pandas as pd
from database import Database

st.set_page_config(page_title="Traffic Reports", page_icon="📊", layout="wide")

if "db_user" not in st.session_state or not st.session_state.db_user:
    st.warning("Please login from Home page first.")
    st.stop()

db = Database(st.session_state.db_user, st.session_state.db_pass)

st.title("📊 Reports & Analytics Dashboard")
st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs([
    "🧾 Driver Reports",
    "📍 Violation Summary",
    "🧮 Stored Procedures",
    "🧠 Functions & Custom Queries"
])

# Tab 1: Driver Reports
with tab1:
    st.subheader("Driver Violation History")
    driver_id = st.number_input("Enter Driver ID", min_value=1, step=1)
    if st.button("Get Violation History"):
        success, result, data = db.call_procedure("GetDriverViolationHistory", [driver_id])
        if data:
            st.dataframe(pd.DataFrame(data, columns=["Driver_ID", "Name", "Vehicle_ID", "Violation_ID", "Violation_Type", "Date_Time", "Location", "Penalty_Amount", "Penalty_Status"]))
        else:
            st.info("No data found or error executing procedure.")

# Tab 2: Violation Summary
with tab2:
    st.subheader("City-wise Violation Summary (JOIN + Aggregate)")
    query = "CALL GetViolationSummary()"
    data = db.fetch_data("SELECT * FROM (" + query.replace("CALL", "SELECT * FROM") + ") AS t")
    if data:
        st.dataframe(pd.DataFrame(data))
    else:
        st.info("No summary data found.")

# Tab 3: Stored Procedures
with tab3:
    st.subheader("Total Unpaid Fines per Driver")
    driver_id = st.number_input("Enter Driver ID for Total Fines", min_value=1, step=1, key="fine")
    if st.button("Calculate Fines"):
        success, result, data = db.call_procedure("CalculateTotalUnpaidFines", [driver_id])
        if data:
            st.dataframe(pd.DataFrame(data, columns=["Driver_ID", "Name", "Total_Unpaid_Fines"]))
        else:
            st.info("No unpaid fines for this driver.")

# Tab 4: Functions and Custom Queries
with tab4:
    st.subheader("Most Frequent Violation Type (Function)")
    data = db.fetch_data("SELECT GetMostFrequentViolationType() AS Most_Common_Violation;")
    if data:
        st.success(f"🚨 Most Common Violation: **{data[0]['Most_Common_Violation']}**")

    st.markdown("---")
    st.subheader("Nested Query — Drivers with Multiple Violations")
    data = db.fetch_data("SELECT * FROM DriversWithMultipleViolations;")
    if data:
        st.dataframe(pd.DataFrame(data))
    else:
        st.info("No drivers with multiple violations found.")
