import streamlit as st
import pandas as pd
from src.gemini_api import generate_sql_from_text
from src.database import get_db_connection

# Configurările de bază ale paginii
st.set_page_config(page_title="Dashboard Hackathon", page_icon="🏥", layout="wide")

st.title("Dashboard 🏥")

# Verificăm starea conexiunii la pornirea aplicației
if get_db_connection():
    st.success("Conexiunea la baza de date a fost realizată cu succes!")
else:
    st.error("Eroare de conexiune la baza de date Azure!")

st.divider()

# --- FUNCȚIE INTERNĂ PENTRU EXECUTAREA SQL ---
def ruleaza_si_afiseaza_query(query_sql):
    """Se conectează, rulează query-ul cu pandas și randează tabelul pe loc."""
    conn = get_db_connection()
    if not conn:
        st.error("Nu s-a putut stabili conexiunea cu Azure SQL pentru această interogare.")
        return

    try:
        # Citim datele
        df = pd.read_sql(query_sql, conn)
        
        # Afișăm rezultatul
        if not df.empty:
            st.success(f"Am extras {len(df)} înregistrări cu succes!")
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Interogarea a rulat cu succes, dar nu s-au găsit date (0 rânduri returnate).")
            
    except Exception as e:
        st.error("❌ Eroare la execuția SQL în Azure:")
        st.code(str(e))
    finally:
        conn.close()

# --- ZONA BUTOANELOR SQL ---
st.header("📊 Interogări Rapide UPU & ATI (Top 10)")

# Am aranjat butoanele pe două coloane
col1, col2 = st.columns(2)

with col1:
    btn1 = st.button("1. Echipamente Critice Disponibile ACUM")
    btn2 = st.button("2. Personal Medical - Tura Noapte")
    btn3 = st.button("3. Pacienți Critici în Așteptare (>15 min)")

with col2:
    btn4 = st.button("4. Aparatură Suprasolicitată (>500 utilizări)")
    btn5 = st.button("5. Triage - Timp Mediu Așteptare (>45 min)")

st.write("### Rezultatul interogării:")

# --- LOGICA FIECĂRUI BUTON ---
if btn1:
    with st.spinner("Extragem echipamentele..."):
        query = """
            SELECT ResourceType, Location 
            FROM Resources_destination 
            WHERE IsAvailable = 1 AND ResourceType IN ('Ventilator', 'Pat ATI', 'Ecograf Mobil');
        """
        ruleaza_si_afiseaza_query(query)

elif btn2:
    with st.spinner("Căutăm personalul..."):
        query = """
            SELECT Name, Role 
            FROM Staff_table_dest 
            WHERE CurrentShift = 'Noapte' AND IsBusy = 0;
        """
        ruleaza_si_afiseaza_query(query)

elif btn3:
    with st.spinner("Căutăm pacienții..."):
        query = """
            SELECT PatientID, ArrivalTime, TriageLevel, WaitTimeMinutes 
            FROM Table_Patiens_flow_dest 
            WHERE TriageLevel IN ('Rosu', 'Galben') 
              AND WaitTimeMinutes > 15 
              AND Status = 'In Asteptare';
        """
        ruleaza_si_afiseaza_query(query)

elif btn4:
    with st.spinner("Analizăm aparatura..."):
        query = """
            SELECT R.ResourceType, COUNT(U.LogID) AS TotalUtilizari
            FROM Resources_destination R
            JOIN ResourceUsage_dest U ON R.ResourceID = U.ResourceID
            GROUP BY R.ResourceType
            HAVING COUNT(U.LogID) > 500;
        """
        ruleaza_si_afiseaza_query(query)

elif btn5:
    with st.spinner("Calculăm timpii medii..."):
        query = """
            SELECT TriageLevel, AVG(CAST(WaitTimeMinutes AS FLOAT)) AS TimpMediuAsteptare
            FROM Table_Patiens_flow_dest
            GROUP BY TriageLevel
            HAVING AVG(CAST(WaitTimeMinutes AS FLOAT)) > 45;
        """
        ruleaza_si_afiseaza_query(query)

st.divider()


# --- ZONA ASISTENȚĂ AI TEXT-TO-SQL (GEMINI) ---
st.header("🧠 Căutare Inteligentă (Gemini Text-to-SQL)")
st.write("Spune-mi ce date vrei să afli, iar Gemini va scrie și va rula codul SQL pentru tine!")

user_input_ai = st.text_input("Caută în limbaj natural:", placeholder="Ex: Arată-mi toți doctorii care sunt pe tura de zi.")

if st.button("Transformă în SQL și Caută"):
    if user_input_ai:
        with st.spinner("Gemini gândește și generează interogarea SQL..."):
            
            # 1. AI-ul generează textul SQL
            generated_sql = generate_sql_from_text(user_input_ai)
            
            if "Eroare AI" in generated_sql:
                st.error("A apărut o eroare la generarea codului cu Gemini.")
                st.write(generated_sql)
            else:
                # 2. Afișăm codul generat ca să impresionăm juriul
                st.info("💡 Codul SQL generat automat de Gemini:")
                st.code(generated_sql, language="sql")
                
                # 3. RULĂM CODUL în Azure folosind funcția noastră deja existentă!
                st.write("### 📊 Rezultatele extrase din baza de date:")
                ruleaza_si_afiseaza_query(generated_sql)
                
    else:
        st.warning("Te rog să introduci o dorință înainte de a apăsa butonul.")