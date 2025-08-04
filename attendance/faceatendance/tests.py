import pyodbc

# Connection parameters
server = 'DESKTOP-UG2UICL\SQLEXPRESS'
database = 'FaceAttendanceDB'

# Connection string for Windows Authentication
conn_str = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"Trusted_Connection=yes;"
)

# Test connection
try:
    conn = pyodbc.connect(conn_str)
    print("Connection successful!")
    conn.close()
except pyodbc.Error as e:
    print("Connection failed:", e)