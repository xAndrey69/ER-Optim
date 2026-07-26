import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

def ask_gemini(prompt):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    try:
        response = client.models.generate_content(
            model='gemini-flash-latest',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"Eroare AI: {e}"

def generate_sql_from_text(user_prompt):
    """
    Traduce cererea în limbaj natural în SQL valid pentru Azure,
    folosind schema exactă, relațiile și datele reale din baza ta.
    """
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    
    schema_info = """
    Ești un expert senior în baze de date Microsoft SQL Server (T-SQL). 
    Rolul tău este să transformi cererea utilizatorului într-o interogare SQL validă, curată și corectă.
    
    SCHEMA EXACTă ȘI VALORILE REALE DIN BAZA DE DATE:
    
    1. Tabela [dbo].[Table_Patiens_flow_dest]
       - PatientID (int)
       - ArrivalTime (datetime)
       - TriageLevel (varchar: 'Rosu', 'Galben', 'Verde')
       - WaitTimeMinutes (int)
       - Status (varchar: 'In Asteptare', 'Preluat', 'Externat')
       - StaffID (int, legătură opțională spre personal)
       
    2. Tabela [dbo].[Staff_table_dest]
       - StaffID (int)
       - Name (varchar: ex. 'Personal_1')
       - Role (varchar: 'Asistent', 'Brancardier', 'Chirurg', 'Medic Urgentist', 'Neurolog')
       - CurrentShift (varchar: 'Noapte', 'Zi')
       - IsBusy (int: 0 = disponibil, 1 = ocupat)
       
    3. Tabela [dbo].[ResourceUsage_dest]
       - LogID (int)
       - ResourceID (int)
       - PatientID (int)
       - StartTime (datetime)
       - EndTime (datetime)
       
    4. Tabela [dbo].[Resources_destination]
       - ResourceID (int)
       - ResourceType (varchar: 'Targa', 'Ecograf Mobil', 'Defibrilator', 'Pat ATI', 'Ventilator', 'Aparat EKG')
       - Location (varchar: ex. 'Camera Trauma 2', 'Depozit 1', 'Reanimare 2')
       - IsAvailable (int: 1 = disponibil, 0 = ocupat/indisponibil)

    REGULI STRICTE DE GENERARE:
    - Returnează DOAR codul SQL brut. Fără formatare markdown (fără ```sql și fără ```), fără explicații, fără salutări.
    - Folosește denumirile exacte ale tabelelor și coloanelor.
    - Respectă tipul de date din exemple (de ex: IsAvailable = 1 sau IsBusy = 0 sunt numerice, TriageLevel='Rosu' este text).
    - Folosește JOIN-uri corecte când e nevoie (ex: ResourceUsage_dest JOIN Resources_destination ON ResourceID).
    - Pune întotdeauna "SELECT TOP (50)" la începutul oricărui query de selecție pentru a garanta afișarea rapidă a datelor.
    """
    
    full_prompt = f"{schema_info}\n\nCererea utilizatorului: {user_prompt}"
    
    try:
        response = client.models.generate_content(
            model='gemini-flash-latest',
            contents=full_prompt,
        )
        
        sql_query = response.text.strip()
        
        # Curățare completă de blocuri markdown
        if sql_query.startswith("```sql"):
            sql_query = sql_query[6:]
        if sql_query.startswith("```"):
            sql_query = sql_query[3:]
        if sql_query.endswith("```"):
            sql_query = sql_query[:-3]
            
        return sql_query.strip()
        
    except Exception as e:
        return f"Eroare AI: {e}"