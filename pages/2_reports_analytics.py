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

# ADDED tab5 for Custom Reports
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🧾 Driver Reports",
    "📍 Violation Summary",
    "🧮 Stored Procedures",
    "🧠 Functions & Custom Queries",
    "⭐ Custom Reports"
])

# Tab 1: Driver Reports (Using call_procedure)
with tab1:
    st.subheader("Driver Violation History")
    driver_id = st.number_input("Enter Driver ID", min_value=1, step=1)
    if st.button("Get Violation History"):
        success, result, data = db.call_procedure("GetDriverViolationHistory", [driver_id])
        if data:
            st.dataframe(pd.DataFrame(data, columns=["Driver_ID", "Name", "Vehicle_ID", "Violation_ID", "Violation_Type", "Date_Time", "Location", "Penalty_Amount", "Penalty_Status"]))
        else:
            st.info("No data found or error executing procedure.")

# Tab 2: Violation Summary (CORRECTED CODE BLOCK)
with tab2:
    st.subheader("City-wise Violation Summary (JOIN + Aggregate)")
    
    # Use the call_procedure method for stored procedures that return results
    success, result, data = db.call_procedure("GetViolationSummary", [])
    
    if data:
        # NOTE: The columns need to be explicitly named here as call_procedure returns tuples by default
        # Assuming the procedure columns are: City, Total_Violations, Total_Penalties, Unpaid_Count
        column_names = ["City", "Total_Violations", "Total_Penalties", "Unpaid_Count"]
        st.dataframe(pd.DataFrame(data, columns=column_names), use_container_width=True)
    else:
        st.info("No summary data found.")
        if not success:
            st.error(f"Error calling procedure: {result}")


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
    # This works because it's a FUNCTION, not a procedure
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
        
# ----------------------------------------------------
# Tab 5: CUSTOM REPORTS (NEW SECTION)
# ----------------------------------------------------
with tab5:
    st.header("Custom SQL Reports")
    
    # --- JOIN Query: Get Violation Details ---
    st.subheader("Detailed Violation Report (JOIN Query)")
    
    JOIN_QUERY = """
        SELECT 
            v.Violation_ID,
            v.Date_Time,
            v.Type AS Violation_Type,
            v.Location,
            d.Name AS Driver_Name,
            d.License_no,
            ve.License_plate,
            ve.Model,
            o.Name AS Officer_Name,
            p.Amount AS Fine_Amount,
            p.Status AS Payment_Status
        FROM Violation v
        JOIN Vehicle ve ON v.Vehicle_ID = ve.Vehicle_ID
        JOIN Driver d ON ve.Driver_ID = d.Driver_ID
        JOIN Officer o ON v.Officer_ID = o.Officer_ID
        LEFT JOIN Penalty p ON v.Violation_ID = p.Violation_ID
        ORDER BY v.Date_Time DESC;
    """
    
    data_join = db.fetch_data(JOIN_QUERY)
    
    if data_join:
        st.dataframe(pd.DataFrame(data_join), use_container_width=True)
    else:
        st.info("No detailed violation data found.")
        
    st.markdown("---")
    
    # --- AGGREGATE Query: Revenue and Violation Statistics ---
    st.subheader("Revenue and Violation Statistics (AGGREGATE Query)")
    
    AGGREGATE_QUERY = """
        SELECT 
            COUNT(DISTINCT d.Driver_ID) AS Total_Drivers,
            COUNT(v.Violation_ID) AS Total_Violations,
            SUM(p.Amount) AS Total_Revenue,
            AVG(p.Amount) AS Average_Fine,
            MAX(p.Amount) AS Highest_Fine,
            MIN(p.Amount) AS Lowest_Fine,
            SUM(CASE WHEN p.Status = 'Paid' THEN p.Amount ELSE 0 END) AS Revenue_Collected,
            SUM(CASE WHEN p.Status = 'Unpaid' THEN p.Amount ELSE 0 END) AS Revenue_Pending
        FROM Driver d
        JOIN Vehicle ve ON d.Driver_ID = ve.Driver_ID
        JOIN Violation v ON ve.Vehicle_ID = v.Vehicle_ID
        JOIN Penalty p ON v.Violation_ID = p.Violation_ID;
    """
    
    data_agg = db.fetch_data(AGGREGATE_QUERY)
    
    if data_agg:
        # Display the single row of aggregate data
        st.dataframe(pd.DataFrame(data_agg), use_container_width=True)
    else:
        st.error("Could not fetch revenue and statistics data.")