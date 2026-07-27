# ER-Optim 
**Sistem Inteligent de Triaj și Management al Resurselor pentru UPU**

Proiect dezvoltat în cadrul **Hackathon Data Journey 2026** .

## Echipa: Prăjituri
* **Costin Andrei-Filip**
* **Guțu Raluca-Andreea**
* **Gaiță-Lukacs Alexandu-George**

---

## Descrierea Proiectului
**ER-Optim** este o platformă end-to-end (E2E) concepută pentru a rezolva problema supraaglomerării din Unitățile de Primiri Urgențe (UPU). Printr-o abordare fundamentată pe date (*data-driven*), sistemul digitalizează fluxul pacienților, monitorizează disponibilitatea echipamentelor critice și a personalului de gardă, și oferă asistență decizională în timp real.

Aplicația inovează prin integrarea unui modul **Text-to-SQL bazat pe inteligență artificială (Google Gemini)**, care permite cadrelor medicale să interogheze baza de date în limbaj natural, fără a necesita cunoștințe tehnice.

---

## Arhitectura și Tehnologii Utilizate

Fluxul de date este construit pe următoarea arhitectură tehnologică:

1. **Generare Date (Python):** Crearea unui volum masiv de date sintetice (10K+ pacienți, log-uri, resurse, personal) exportate în format CSV.
2. **Proces ETL (SSIS):** Extragerea, transformarea (maparea tipurilor de date) și încărcarea datelor folosind pachete SQL Server Integration Services.
3. **Stocare Cloud (Azure SQL Database):** Bază de date relațională, scalabilă și securizată în cloud.
4. **Backend & Frontend (Streamlit + pyodbc):** Interfață web interactivă conectată la instanța Azure.
5. **Modul AI (Google Gemini API):** Procesare NLP (Text-to-SQL) prin inginerie avansată de prompt-uri.
6. **Business Intelligence (Power BI):** Dashboard-uri decizionale pentru managementul spitalului.

---

## Structura Bazei de Date (Schema)
Sistemul utilizează 4 tabele relaționale principale:
* `Table_Patiens_flow_dest` - Date despre pacienți (ID, nivel triaj, timp așteptare, status).
* `Staff_table_dest` - Detalii despre personalul medical (rol, tură, disponibilitate).
* `Resources_destination` - Echipamentele din spital (tip, locație, status).
* `ResourceUsage_dest` - Jurnalul de utilizare al echipamentelor per pacient.

---
