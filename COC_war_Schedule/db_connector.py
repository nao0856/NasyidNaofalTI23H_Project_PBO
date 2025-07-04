# db_connector.py
import mysql.connector
from mysql.connector import Error

def connect_to_db():
    """Membuat dan mengembalikan objek koneksi database."""
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            # Pastikan nama database sudah sesuai dengan yang dibuat
            database='coc_tracker_db' 
        )
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Error saat menghubungkan ke MySQL: {e}")
        return None