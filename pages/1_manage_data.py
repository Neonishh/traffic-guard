# pages/1_Manage_Data.py
import streamlit as st
from database import Database
import pandas as pd
from datetime import datetime, date

db = Database(st.session_state.get('db_user'), st.session_state.get('db_pass'))

st.set_page_config(page_title="Manage Data", page_icon="📝", layout="wide")
st.title("📝 Data Management")
st.markdown("---")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "👤 Drivers", "🚗 Vehicles", "👮 Officers", 
    "⚠️ Violations", "💳 Payments", "📋 Appeals"
])

# ==================== DRIVERS ====================
with tab1:
    st.header("Drivers")
    
    drivers = db.fetch_data("SELECT * FROM Driver ORDER BY Driver_ID")
    if drivers:
        st.dataframe(pd.DataFrame(drivers), use_container_width=True)
    else:
        st.info("No drivers")
    
    st.markdown("---")
    
    # Add driver
    with st.expander("➕ Add Driver"):
        with st.form("add_driver"):
            name = st.text_input("Name*")
            address = st.text_area("Address")
            contact = st.text_input("Contact Number*")
            license = st.text_input("License Number*")
            
            if st.form_submit_button("Add Driver"):
                if not name or not contact or not license:
                    st.error("Fill required fields")
                else:
                    query = "INSERT INTO Driver (Name, Address, Contact_no, License_no) VALUES (%s, %s, %s, %s)"
                    success, msg = db.execute_query(query, (name, address, contact, license))
                    if success:
                        st.success("✅ Driver added!")
                        st.rerun()
                    else:
                        st.error(f"{msg}")
    
    # Update driver
    with st.expander("✏️ Update Driver"):
        if drivers:
            opts = {f"ID {d['Driver_ID']}: {d['Name']}": d['Driver_ID'] for d in drivers}
            sel = st.selectbox("Select Driver", opts.keys())
            
            if sel:
                did = opts[sel]
                d = next(x for x in drivers if x['Driver_ID'] == did)
                
                with st.form("update_driver"):
                    new_name = st.text_input("Name", value=d['Name'])
                    new_addr = st.text_area("Address", value=d['Address'] or "")
                    new_contact = st.text_input("Contact", value=d['Contact_no'])
                    new_lic = st.text_input("License", value=d['License_no'])
                    
                    if st.form_submit_button("Update"):
                        query = "UPDATE Driver SET Name=%s, Address=%s, Contact_no=%s, License_no=%s WHERE Driver_ID=%s"
                        success, msg = db.execute_query(query, (new_name, new_addr, new_contact, new_lic, did))
                        if success:
                            st.success("✅ Updated!")
                            st.rerun()
                        else:
                            st.error(f"{msg}")
    
    # Delete driver - WITH DEPENDENCY CHECK
    with st.expander("🗑️ Delete Driver"):
        if drivers:
            opts = {f"ID {d['Driver_ID']}: {d['Name']}": d['Driver_ID'] for d in drivers}
            to_del = st.selectbox("Select Driver", opts.keys(), key="del_d")
            
            if st.button("Check if Safe to Delete", key="check_driver"):
                did = opts[to_del]
                
                # Show vehicle count (will be CASCADE deleted)
                vehicles = db.fetch_data("SELECT COUNT(*) as count FROM Vehicle WHERE Driver_ID = %s", (did,))
                vehicle_count = vehicles[0]['count'] if vehicles else 0
                
                if vehicle_count > 0:
                    st.info(f"ℹ️ This driver has {vehicle_count} vehicle(s). They will be deleted automatically (CASCADE).")
                
                # Check for violations (blocks deletion)
                deps = db.check_dependencies('Driver', 'Driver_ID', did)
                
                if deps:
                    st.error(f"❌ Cannot delete! {', '.join(deps)}")
                    st.info("💡 Delete or resolve violations first")
                else:
                    st.success("✅ Safe to delete!")
            
            if st.button("Delete Driver", key="del_drv_btn") and st.checkbox("Confirm deletion", key="conf_del_drv"):
                did = opts[to_del]
                
                # Final check before deleting
                deps = db.check_dependencies('Driver', 'Driver_ID', did)
                
                if deps:
                    st.error(f"❌ Cannot delete! {', '.join(deps)}")
                else:
                    query = "DELETE FROM Driver WHERE Driver_ID=%s"
                    success, msg = db.execute_query(query, (did,))
                    if success:
                        st.success("✅ Driver deleted successfully!")
                        st.info("ℹ️ All vehicles owned by this driver were also deleted")
                        st.rerun()
                    else:
                        st.error(f"{msg}")

# ==================== VEHICLES ====================
with tab2:
    st.header("Vehicles")
    
    vehicles = db.fetch_data("""
        SELECT v.*, d.Name as Owner 
        FROM Vehicle v 
        LEFT JOIN Driver d ON v.Driver_ID = d.Driver_ID
        ORDER BY v.Vehicle_ID
    """)
    if vehicles:
        st.dataframe(pd.DataFrame(vehicles), use_container_width=True)
    else:
        st.info("No vehicles")
    
    st.markdown("---")
    
    # Add vehicle
    with st.expander("➕ Add Vehicle"):
        dlist = db.fetch_data("SELECT Driver_ID, Name FROM Driver")
        
        if not dlist:
            st.warning("Add drivers first")
        else:
            with st.form("add_vehicle"):
                year = st.number_input("Year*", min_value=1990, max_value=2025, value=2020)
                model = st.text_input("Model*")
                color = st.text_input("Color")
                plate = st.text_input("License Plate*")
                
                dopts = {f"ID {d['Driver_ID']}: {d['Name']}": d['Driver_ID'] for d in dlist}
                owner = st.selectbox("Owner*", dopts.keys())
                
                if st.form_submit_button("Add Vehicle"):
                    if not model or not plate:
                        st.error("Fill required fields")
                    else:
                        query = "INSERT INTO Vehicle (Registration_year, Model, Color, License_plate, Driver_ID) VALUES (%s, %s, %s, %s, %s)"
                        success, msg = db.execute_query(query, (year, model, color, plate, dopts[owner]))
                        if success:
                            st.success("✅ Vehicle added!")
                            st.rerun()
                        else:
                            st.error(f"{msg}")
    
    # Update vehicle
    with st.expander("✏️ Update Vehicle"):
        if vehicles:
            dlist = db.fetch_data("SELECT Driver_ID, Name FROM Driver")
            vopts = {f"ID {v['Vehicle_ID']}: {v['License_plate']}": v['Vehicle_ID'] for v in vehicles}
            sel = st.selectbox("Select Vehicle", vopts.keys())
            
            if sel:
                vid = vopts[sel]
                v = next(x for x in vehicles if x['Vehicle_ID'] == vid)
                
                with st.form("update_vehicle"):
                    new_year = st.number_input("Year", value=v['Registration_year'])
                    new_model = st.text_input("Model", value=v['Model'])
                    new_color = st.text_input("Color", value=v['Color'] or "")
                    new_plate = st.text_input("Plate", value=v['License_plate'])
                    
                    dopts = {f"ID {d['Driver_ID']}: {d['Name']}": d['Driver_ID'] for d in dlist}
                    curr_owner = f"ID {v['Driver_ID']}: {v['Owner']}"
                    idx = list(dopts.keys()).index(curr_owner) if curr_owner in dopts else 0
                    new_owner = st.selectbox("Owner", dopts.keys(), index=idx)
                    
                    if st.form_submit_button("Update"):
                        query = "UPDATE Vehicle SET Registration_year=%s, Model=%s, Color=%s, License_plate=%s, Driver_ID=%s WHERE Vehicle_ID=%s"
                        success, msg = db.execute_query(query, (new_year, new_model, new_color, new_plate, dopts[new_owner], vid))
                        if success:
                            st.success("✅ Updated!")
                            st.rerun()
                        else:
                            st.error(f"{msg}")
    
    # Delete vehicle - WITH DEPENDENCY CHECK
    with st.expander("🗑️ Delete Vehicle"):
        if vehicles:
            vopts = {f"ID {v['Vehicle_ID']}: {v['License_plate']}": v['Vehicle_ID'] for v in vehicles}
            to_del = st.selectbox("Select Vehicle", vopts.keys(), key="del_v")
            
            if st.button("Check if Safe to Delete", key="check_veh"):
                vid = vopts[to_del]
                deps = db.check_dependencies('Vehicle', 'Vehicle_ID', vid)
                
                if deps:
                    st.error(f"❌ Cannot delete! {', '.join(deps)}")
                    st.info("💡 Delete violations first")
                else:
                    st.success("✅ Safe to delete!")
            
            if st.button("Delete Vehicle", key="del_veh_btn") and st.checkbox("Confirm", key="conf_v"):
                vid = vopts[to_del]
                deps = db.check_dependencies('Vehicle', 'Vehicle_ID', vid)
                
                if deps:
                    st.error(f"❌ Cannot delete! {', '.join(deps)}")
                else:
                    query = "DELETE FROM Vehicle WHERE Vehicle_ID=%s"
                    success, msg = db.execute_query(query, (vid,))
                    if success:
                        st.success("✅ Vehicle deleted!")
                        st.rerun()
                    else:
                        st.error(f"{msg}")

# ==================== OFFICERS ====================
with tab3:
    st.header("Officers")
    
    officers = db.fetch_data("SELECT * FROM Officer ORDER BY Officer_ID")
    if officers:
        st.dataframe(pd.DataFrame(officers), use_container_width=True)
    else:
        st.info("No officers")
    
    st.markdown("---")
    
    with st.expander("➕ Add Officer"):
        with st.form("add_officer"):
            name = st.text_input("Name*")
            rank = st.selectbox("Rank", ["Inspector", "Sub-Inspector", "Head Constable", "Constable"])
            badge = st.text_input("Badge Number*")
            contact = st.text_input("Contact")
            
            if st.form_submit_button("Add Officer"):
                if not name or not badge:
                    st.error("Fill required fields")
                else:
                    query = "INSERT INTO Officer (Name, Officer_Rank, Badge_no, Contact_no) VALUES (%s, %s, %s, %s)"
                    success, msg = db.execute_query(query, (name, rank, badge, contact))
                    if success:
                        st.success("✅ Officer added!")
                        st.rerun()
                    else:
                        st.error(f"{msg}")

# ==================== VIOLATIONS ====================
with tab4:
    st.header("Violations")
    
    violations = db.fetch_data("""
        SELECT v.*, ve.License_plate, d.Name as Driver, 
               o.Name as Officer, p.Amount, p.Status
        FROM Violation v
        JOIN Vehicle ve ON v.Vehicle_ID = ve.Vehicle_ID
        JOIN Driver d ON ve.Driver_ID = d.Driver_ID
        JOIN Officer o ON v.Officer_ID = o.Officer_ID
        LEFT JOIN Penalty p ON v.Violation_ID = p.Violation_ID
        ORDER BY v.Date_Time DESC
    """)
    if violations:
        st.dataframe(pd.DataFrame(violations), use_container_width=True)
    else:
        st.info("No violations")
    
    st.markdown("---")
    
    with st.expander("➕ Record Violation"):
        st.info("💡 Penalty & ViolationType_ID auto-created by triggers!")
        
        vlist = db.fetch_data("""
            SELECT v.Vehicle_ID, v.License_plate, d.Name as Driver_Name
            FROM Vehicle v 
            JOIN Driver d ON v.Driver_ID = d.Driver_ID
        """)
        olist = db.fetch_data("SELECT Officer_ID, Name FROM Officer")
        
        if not vlist or not olist:
            st.warning("Add vehicles and officers first")
        else:
            with st.form("add_violation"):
                col1, col2 = st.columns(2)
                
                with col1:
                    vopts = {f"{v['License_plate']} ({v['Driver_Name']})": v['Vehicle_ID'] for v in vlist}
                    vehicle = st.selectbox("Vehicle*", vopts.keys())
                    
                    vtype = st.selectbox("Type*", [
                        "Speeding", "Signal Jump", "Parking Violation", 
                        "Drunk Driving", "Underage Driving", "Seatbelt Violation", 
                        "Mobile Usage", "No Insurance"
                    ])
                    
                    location = st.text_input("Location*")
                
                with col2:
                    oopts = {f"ID {o['Officer_ID']}: {o['Name']}": o['Officer_ID'] for o in olist}
                    officer = st.selectbox("Officer*", oopts.keys())
                    
                    vdate = st.date_input("Date", value=date.today())
                    vtime = st.time_input("Time")
                
                if st.form_submit_button("Record Violation"):
                    if not location:
                        st.error("Fill all fields")
                    else:
                        dt = datetime.combine(vdate, vtime)
                        
                        # ViolationType_ID will be auto-set by trigger
                        query = "INSERT INTO Violation (Date_Time, Type, Location, Vehicle_ID, Officer_ID) VALUES (%s, %s, %s, %s, %s)"
                        success, msg = db.execute_query(query, (dt, vtype, location, vopts[vehicle], oopts[officer]))
                        
                        if success:
                            st.success("✅ Violation recorded!")
                            st.info("🔔 Penalty & ViolationType_ID auto-created by triggers!")
                            st.rerun()
                        else:
                            st.error(f"{msg}")

# ==================== PAYMENTS ====================
with tab5:
    st.header("Payments")
    
    penalties = db.fetch_data("""
        SELECT p.Penalty_ID, p.Amount, p.Status, p.Duedate,
               v.Type, v.Date_Time, d.Name as Driver, ve.License_plate
        FROM Penalty p
        JOIN Violation v ON p.Violation_ID = v.Violation_ID
        JOIN Vehicle ve ON v.Vehicle_ID = ve.Vehicle_ID
        JOIN Driver d ON ve.Driver_ID = d.Driver_ID
        ORDER BY p.Penalty_ID DESC
    """)
    
    if penalties:
        st.dataframe(pd.DataFrame(penalties), use_container_width=True)
    else:
        st.info("No penalties")
    
    st.markdown("---")
    
    with st.expander("💳 Pay Penalty"):
        unpaid = [p for p in penalties if p['Status'] == 'Unpaid'] if penalties else []
        
        if not unpaid:
            st.info("No unpaid penalties")
        else:
            popts = {f"ID {p['Penalty_ID']}: {p['Driver']} - {p['Type']} - ₹{p['Amount']}": 
                    p['Penalty_ID'] for p in unpaid}
            sel_pen = st.selectbox("Select Penalty*", popts.keys())
            
            payment_mode = st.selectbox("Payment Mode", ["Cash", "Card", "Online", "UPI"])
            
            if st.button("💳 Pay Now", type="primary"):
                pid = popts[sel_pen]
                amount = next(p['Amount'] for p in unpaid if p['Penalty_ID'] == pid)
                
                query = "INSERT INTO Payment (Date, Amount, ModeofPayment, Penalty_ID) VALUES (CURDATE(), %s, %s, %s)"
                success, msg = db.execute_query(query, (amount, payment_mode, pid))
                
                if success:
                    st.success("✅ Payment recorded!")
                    st.info("🔔 Penalty → 'Paid' (by trigger)")
                    st.rerun()
                else:
                    st.error(f"{msg}")

# ==================== APPEALS ====================
with tab6:
    st.header("Appeals")
    
    st.info("📋 File appeal → Penalty: Appealed (by trigger)")
    
    appeals = db.fetch_data("""
        SELECT a.Appeal_ID, a.Datefiled, a.Status, a.Reason,
               d.Name as Driver, v.Type, p.Status as Penalty_Status
        FROM Appeal a
        JOIN Violation v ON a.Violation_ID = v.Violation_ID
        JOIN Driver d ON a.Driver_ID = d.Driver_ID
        LEFT JOIN Penalty p ON v.Violation_ID = p.Violation_ID
        ORDER BY a.Datefiled DESC
    """)
    
    if appeals:
        st.dataframe(pd.DataFrame(appeals), use_container_width=True)
    else:
        st.info("No appeals")
    
    st.markdown("---")
    
    with st.expander("📝 File Appeal"):
        eligible = db.fetch_data("""
            SELECT v.Violation_ID, v.Type, v.Date_Time,
                   d.Driver_ID, d.Name, p.Amount
            FROM Violation v
            JOIN Vehicle ve ON v.Vehicle_ID = ve.Vehicle_ID
            JOIN Driver d ON ve.Driver_ID = d.Driver_ID
            LEFT JOIN Penalty p ON v.Violation_ID = p.Violation_ID
            WHERE v.Violation_ID NOT IN (SELECT Violation_ID FROM Appeal)
            AND (p.Status = 'Unpaid' OR p.Status IS NULL)
        """)
        
        if not eligible:
            st.warning("No violations for appeal")
        else:
            vopts = {f"ID {v['Violation_ID']}: {v['Name']} - {v['Type']} on {str(v['Date_Time'])[:10]} - ₹{v['Amount']}": 
                    (v['Violation_ID'], v['Driver_ID']) for v in eligible}
            
            selected = st.selectbox("Select Violation*", vopts.keys())
            reason = st.text_area("Reason* (min 10 chars)", height=100)
            
            if st.button("📤 Submit Appeal", type="primary"):
                if not reason or len(reason.strip()) < 10:
                    st.error("Provide detailed reason")
                else:
                    vid, did = vopts[selected]
                    
                    query = "INSERT INTO Appeal (Datefiled, Status, Reason, Violation_ID, Driver_ID) VALUES (CURDATE(), 'Pending', %s, %s, %s)"
                    success, msg = db.execute_query(query, (reason, vid, did))
                    
                    if success:
                        st.success("✅ Appeal filed!")
                        st.info("🔔 Penalty → 'Appealed' (by trigger)")
                        st.rerun()
                    else:
                        st.error(f"{msg}")