import pyodbc

def connect_to_db():
    server = 'localhost'
    database = 'LavanderiaDB'
    # username = 'tu_usuario'
    # password = 'tu_contraseña'
    
    connection_string = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        # f"UID={username};"
        # f"PWD={password};"
        f"Trusted_Connection=yes;"
    )

    try:
        connection = pyodbc.connect(connection_string)
        return connection
    except pyodbc.Error as e:
        print("Error al conectar a la base de datos:", e)
        return None
