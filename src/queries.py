import pandas as pd
from src.database import get_db_connection

def run_query(query_str: str):
    """Execută interogarea folosind metoda directă cu Pandas."""
    conn = get_db_connection()
    if not conn:
        return "Eroare: Nu m-am putut conecta la baza de date Azure."
    
    try:
        # Aici e secretul care a funcționat adineauri!
        df = pd.read_sql(query_str, conn)
        return df
    except Exception as e:
        return f"Eroare SQL: {e}"
    finally:
        conn.close()

# --- Funcțiile specifice pentru fiecare buton ---

def get_echipamente_critice():
    query = """
        SELECT ResourceType, Location 
        FROM Resources_destination 
        WHERE IsAvailable = 1 AND ResourceType IN ('Ventilator', 'Pat ATI', 'Ecograf Mobil');
    """
    return run_query(query)

def get_personal_medical_noapte():
    query = """
        SELECT Name, Role 
        FROM Staff_table_dest 
        WHERE CurrentShift = 'Noapte' AND IsBusy = 0;
    """
    return run_query(query)

def get_pacienti_critici_asteptare():
    query = """
        SELECT PatientID, ArrivalTime, TriageLevel, WaitTimeMinutes 
        FROM Table_Patiens_flow_dest 
        WHERE TriageLevel IN ('Rosu', 'Galben') 
          AND WaitTimeMinutes > 15 
          AND Status = 'In Asteptare';
    """
    return run_query(query)

def get_aparatura_suprasolicitata():
    query = """
        SELECT R.ResourceType, COUNT(U.LogID) AS TotalUtilizari
        FROM Resources_destination R
        JOIN ResourceUsage_dest U ON R.ResourceID = U.ResourceID
        GROUP BY R.ResourceType
        HAVING COUNT(U.LogID) > 500;
    """
    return run_query(query)

def get_timp_mediu_triage():
    query = """
        SELECT TriageLevel, AVG(CAST(WaitTimeMinutes AS FLOAT)) AS TimpMediuAsteptare
        FROM Table_Patiens_flow_dest
        GROUP BY TriageLevel
        HAVING AVG(CAST(WaitTimeMinutes AS FLOAT)) > 45;
    """
    return run_query(query)