import os
import pyodbc
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():

    server = os.getenv("AZURE_SERVER")
    database = os.getenv("AZURE_DATABASE")
    username = os.getenv("AZURE_USER")
    password = os.getenv("AZURE_PASSWORD")
    
    driver = '{ODBC Driver 17 for SQL Server}' 
    
    connection_string = f"DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}"
    
    try:
        conn = pyodbc.connect(connection_string)
        return conn
    except Exception as e:
        print(f"Eroare critică la conectarea cu baza de date: {e}")
        return None

if __name__ == "__main__":
    print("Încercăm conectarea la Azure SQL...")
    conn = get_db_connection()
    
    if conn:
        print("Succes! Suntem conectați la baza de date din cloud!")
        
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM dbo.Table_Patiens_flow_dest;")
            
            print("\nDatele din tabela Operatori:")
            print("-" * 40)
            
            randuri = cursor.fetchall()
            for rand in randuri:
                print(f"ID: {rand[0]} | Nume: {rand[1]} | Rol: {rand[2]}")
                
            print("-" * 40)
            
        except Exception as e:
            print(f"Eroare la citirea datelor: {e}")
            
        finally:
            conn.close()
            print("Conexiunea a fost închisă în siguranță.")