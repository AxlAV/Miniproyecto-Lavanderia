import pyodbc
from datetime import datetime

def connect_to_db():
    connection_string = (
        "Driver={SQL Server};"
        "Server=localhost;"
        "Database=LavanderiaDB;"
        "Trusted_Connection=yes;"
    )
    try:
        connection = pyodbc.connect(connection_string)
        return connection
    except pyodbc.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def format_date(date_obj):
    if isinstance(date_obj, datetime):
        return date_obj.strftime("%d-%m-%Y %H:%M:%S")
    return date_obj
