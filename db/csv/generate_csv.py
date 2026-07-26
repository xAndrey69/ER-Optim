import csv
import random
from datetime import datetime, timedelta

# Setări
NUM_PATIENTS = 10000
NUM_RESOURCES = 100
NUM_STAFF = 50
NUM_LOGS = 15000

start_date = datetime(2026, 7, 1)

def random_date(start, days):
    return start + timedelta(minutes=random.randint(0, days * 24 * 60))

# 1. Generare PatientsFlow
print("Generare PatientsFlow.csv...")
with open('PatientsFlow.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    # AM MODIFICAT AICI: Adăugare coloană StaffID
    writer.writerow(['PatientID', 'ArrivalTime', 'TriageLevel', 'WaitTimeMinutes', 'Status', 'StaffID'])
    
    triage_levels = ['Albastru', 'Verde', 'Galben', 'Rosu']
    statuses = ['In Asteptare', 'Preluat', 'Externat']
    
    for i in range(1, NUM_PATIENTS + 1):
        arrival = random_date(start_date, 30)
        # Ponderi: majoritatea sunt cazuri non-critice (Verde/Galben)
        triage = random.choices(triage_levels, weights=[10, 45, 35, 10])[0]
        wait_time = random.randint(5, 240) if triage != 'Rosu' else random.randint(0, 30)
        status = random.choices(statuses, weights=[20, 30, 50])[0]
        
        # AM MODIFICAT AICI: Setăm StaffID doar dacă pacientul a fost preluat
        staff_id = random.randint(1, NUM_STAFF) if status == 'Preluat' else 'NULL'
        
        writer.writerow([i, arrival.strftime('%Y-%m-%d %H:%M'), triage, wait_time, status, staff_id])

# 2. Generare Resources
print("Generare Resources.csv...")
with open('Resources.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['ResourceID', 'ResourceType', 'Location', 'IsAvailable'])
    
    resource_types = ['Pat ATI', 'Ventilator', 'Ecograf Mobil', 'Defibrilator', 'Targa', 'Aparat EKG']
    locations = ['Reanimare', 'Hol UPU', 'Camera Trauma', 'Camera Consult', 'Depozit']
    
    for i in range(1, NUM_RESOURCES + 1):
        rtype = random.choice(resource_types)
        loc = f"{random.choice(locations)} {random.randint(1, 5)}"
        is_avail = random.choice([0, 1])
        writer.writerow([i, rtype, loc, is_avail])

# 3. Generare Staff
print("Generare Staff.csv...")
with open('Staff.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['StaffID', 'Name', 'Role', 'CurrentShift', 'IsBusy'])
    
    roles = ['Medic Urgentist', 'Asistent', 'Brancardier', 'Chirurg', 'Cardiolog', 'Neurolog']
    shifts = ['Zi', 'Noapte']
    
    for i in range(1, NUM_STAFF + 1):
        name = f"Personal_{i}"
        role = random.choices(roles, weights=[30, 40, 15, 5, 5, 5])[0]
        shift = random.choice(shifts)
        is_busy = random.choice([0, 1])
        writer.writerow([i, name, role, shift, is_busy])

# 4. Generare ResourceUsage (15.000 de loguri)
print("Generare ResourceUsage.csv...")
with open('ResourceUsage.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['LogID', 'ResourceID', 'PatientID', 'StartTime', 'EndTime'])
    
    for i in range(1, NUM_LOGS + 1):
        res_id = random.randint(1, NUM_RESOURCES)
        pat_id = random.randint(1, NUM_PATIENTS)
        start_time = random_date(start_date, 30)
        # Durata utilizării între 10 și 120 de minute
        end_time = start_time + timedelta(minutes=random.randint(10, 120))
        
        # Lăsăm ~10% din log-uri fără EndTime (aparatură încă în uz)
        end_time_str = end_time.strftime('%Y-%m-%d %H:%M') if random.random() > 0.1 else 'NULL'
        
        writer.writerow([i, res_id, pat_id, start_time.strftime('%Y-%m-%d %H:%M'), end_time_str])

print("Gata! Au fost generate cele 4 fișiere CSV.")
