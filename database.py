# database.py
import mysql.connector
from mysql.connector import Error
import streamlit as st

class Database:
    def __init__(self, user=None, password=None):
        self.host = 'localhost'
        self.database = 'TrafficVioDB'
        self.user = user or st.session_state.get('db_user', 'root')
        self.password = password or st.session_state.get('db_pass', 'captain')
    
    def get_connection(self):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            return connection
        except Error as e:
            st.error(f"Database connection error: {e}")
            return None
    
    def execute_query(self, query, params=None):
        connection = self.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(query, params or ())
                connection.commit()
                return True, "✅ Operation successful"
            except Error as e:
                return False, f"❌ {str(e)}"
            finally:
                cursor.close()
                connection.close()
        return False, "Connection failed"
    
    def fetch_data(self, query, params=None):
        connection = self.get_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                cursor.execute(query, params or ())
                result = cursor.fetchall()
                return result
            except Error as e:
                st.error(f"Query error: {e}")
                return []
            finally:
                cursor.close()
                connection.close()
        return []
    
    def check_dependencies(self, table, id_column, id_value):
        """Check if record has violations (blocking deletion)"""
        connection = self.get_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                dependencies = []
                
                if table == 'Driver':
                    # Check if driver's vehicles have violations
                    cursor.execute("""
                        SELECT COUNT(*) as count 
                        FROM Violation v
                        JOIN Vehicle ve ON v.Vehicle_ID = ve.Vehicle_ID
                        WHERE ve.Driver_ID = %s
                    """, (id_value,))
                    violation_count = cursor.fetchone()['count']
                    if violation_count > 0:
                        dependencies.append(f"{violation_count} violation(s) on their vehicles")
                
                elif table == 'Vehicle':
                    # Check violations for this vehicle
                    cursor.execute("SELECT COUNT(*) as count FROM Violation WHERE Vehicle_ID = %s", (id_value,))
                    violation_count = cursor.fetchone()['count']
                    if violation_count > 0:
                        dependencies.append(f"{violation_count} violation(s)")
                
                elif table == 'Officer':
                    # Check violations recorded by officer
                    cursor.execute("SELECT COUNT(*) as count FROM Violation WHERE Officer_ID = %s", (id_value,))
                    violation_count = cursor.fetchone()['count']
                    if violation_count > 0:
                        dependencies.append(f"{violation_count} violation(s) recorded")
                
                return dependencies
                
            except Error as e:
                st.error(f"Error: {e}")
                return []
            finally:
                cursor.close()
                connection.close()
        return []
    
    def call_procedure(self, proc_name, args):
        connection = self.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                result = cursor.callproc(proc_name, args)
                connection.commit()
                
                results = []
                for result_cursor in cursor.stored_results():
                    results.extend(result_cursor.fetchall())
                
                return True, result, results
            except Error as e:
                return False, str(e), []
            finally:
                cursor.close()
                connection.close()
        return False, "Connection failed", []