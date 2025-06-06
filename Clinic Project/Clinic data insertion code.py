import sqlite3
conn = sqlite3.connect("New Clinic.db")
file = open("CLINICS_DATA.csv","r")
header = file.readline()
clinic_lst = []
nric_lst = []
for line in file:
    line = line.strip()
    person_type,nric,first_name,last_name,date_of_birth,home_address,contact_number,gender,clinic,clinic_address,clinic_contact,allergy,status = line.split(",")
    if clinic not in clinic_lst:
        print(clinic)
        clinic_lst.append(clinic)
        conn.execute("INSERT INTO ClinicInfo(Clinic,Clinic_address,Clinic_contact) VALUES(?,?,?)",(clinic,clinic_address,clinic_contact))
    if nric not in nric_lst:
        conn.execute("INSERT INTO Person(type,NRIC,First_name,Last_name,Date_of_birth,Home_address,Contact_number,Gender,Allergy) VALUES(?,?,?,?,?,?,?,?,?)",(person_type,nric,first_name,last_name,date_of_birth,home_address,contact_number,gender,allergy))
        nric_lst.append(nric)
    if person_type != "patient":
        conn.execute("INSERT INTO Staff(NRIC,Clinic,Status) VALUES(?,?,?)",(nric,clinic,status))
    else:
        conn.execute("INSERT INTO Patient(NRIC,Clinic) VALUES(?,?)",(nric,clinic))
conn.commit()
file.close()
conn.close()
