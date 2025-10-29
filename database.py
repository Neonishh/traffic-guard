# database.py
import mysql.connector
from mysql.connector import Error
import streamlit as st

class Database:
    def __init__(self):
        self.host = 'localhost'
        self.database = 'TrafficViolationDB'
        self.user = 'root'
        self.password = 'captain'  # CHANGE THIS
    
    def get_connection(self):
        """Get database connection"""
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
        """Execute INSERT, UPDATE, DELETE queries"""
        connection = self.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(query, params or ())
                connection.commit()
                return True, "Operation successful"
            except Error as e:
                return False, str(e)
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()
        return False, "Connection failed"
    
    def fetch_data(self, query, params=None):
        """Execute SELECT queries"""
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
                if connection.is_connected():
                    cursor.close()
                    connection.close()
        return []
    
    def call_procedure(self, proc_name, args):
        """Call stored procedure"""
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
                if connection.is_connected():
                    cursor.close()
                    connection.close()
        return False, "Connection failed", []
