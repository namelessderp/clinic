from flask import *
import sqlite3
app = Flask(__name__)
def UpdateCursor(nric,clinic,type_info):
    conn = sqlite3.connect("New Clinic.db")
    if type_info!= "patient":
        lst = ["type_info","nric","first_name","last_name","dob","address","contact","gender","clinic","clinic_address","clinic_contact","status"]
        cursor = conn.execute("SELECT Person.type,Person.NRIC,Person.First_name,Person.Last_name,Person.Date_of_birth,Person.Home_address, Person.Contact_number,Person.Gender,ClinicInfo.Clinic,ClinicInfo.Clinic_address,ClinicInfo.Clinic_contact,Staff.Status FROM Person,ClinicInfo,Staff WHERE Person.NRIC = Staff.NRIC and ClinicInfo.Clinic = Staff.Clinic AND Person.NRIC = ? AND Staff.Clinic = ?",(nric,clinic)).fetchall()
##        if cursor.fetchone() == None:
##            return 
    else:
        lst = ["type_info","nric","first_name","last_name","dob","address","contact","gender","clinic","clinic_address","clinic_contact","allergy"]
        cursor = conn.execute("SELECT Person.type,Person.NRIC,Person.First_name,Person.Last_name,Person.Date_of_birth,Person.Home_address, Person.Contact_number,Person.Gender,ClinicInfo.Clinic,ClinicInfo.Clinic_address,ClinicInfo.Clinic_contact,Person.Allergy FROM Person,ClinicInfo,Patient WHERE Person.NRIC = Patient.NRIC AND Patient.Clinic = ClinicInfo.Clinic AND Person.NRIC = ? AND Patient.Clinic = ?",(nric,clinic)).fetchall()
    return cursor,lst
    

@app.route("/")

def home():
    return render_template("Selection.html") # decorator

@app.route("/search_template")
def search_template():
    return render_template("Search.html")
    
@app.route("/Search",methods = ["POST"])

def Search():
    lst = []
    lst2 = []
    count = 0
    nric_lst = ["S","T"]
    length_check = True
    format_check = True
    clinic_check = True
    clinic_lst = ["Bedok","Jurong","Bishan","Clementi","Yishun"]
    conn = sqlite3.connect("New Clinic.db")
    #conn = sqlite3.connect("New Clinic - Copy (2).db")
    data = request.form
    type_info = data["type_info"]
    nric = data["nric"]
    clinic = data["clinic"]
                  
    if len(nric) != 9:#length
        return render_template("Search.html", length_check = length_check)
    
    if nric[0] not in nric_lst or nric[-1].isalpha() == False or nric[1:8].isdigit() == False:#format
        return render_template("Search.html", format_check = format_check)
    
    if clinic not in clinic_lst:#clinic exist
        return render_template("Search.html", clinic_check = clinic_check)
    
    if type_info!= "Patient":
        cursor = conn.execute("SELECT Person.type,Person.NRIC,Person.First_name,Person.Last_name,Person.Date_of_birth,Person.Home_address, Person.Contact_number,Person.Gender,ClinicInfo.Clinic,ClinicInfo.Clinic_address,ClinicInfo.Clinic_contact,Staff.Status FROM Person,ClinicInfo,Staff WHERE Person.NRIC = Staff.NRIC and ClinicInfo.Clinic = Staff.Clinic AND Person.NRIC = ? AND Staff.Clinic = ?",(nric,clinic))
    else:
        cursor = conn.execute("SELECT Person.type,Person.NRIC,Person.First_name,Person.Last_name,Person.Date_of_birth,Person.Home_address, Person.Contact_number,Person.Gender,ClinicInfo.Clinic,ClinicInfo.Clinic_address,ClinicInfo.Clinic_contact,Person.Allergy FROM Person,ClinicInfo,Patient WHERE Person.NRIC = Patient.NRIC AND Patient.Clinic = ClinicInfo.Clinic AND Person.NRIC = ? AND Patient.Clinic = ?",(nric,clinic))
    return render_template("Display.html",cursor = cursor,type_info = type_info)

@app.route("/add_template")
def add_template():
    return render_template("Add.html")

@app.route("/Add",methods = ["POST"])

def Add():
    conn = sqlite3.connect("New Clinic.db")
    nric_lst = ["S","T"]
    gender_lst = ["Male","Female"]
    clinic_lst = ["Bedok","Jurong","Bishan","Clementi","Yishun"]
    status_lst = ["Active","Inactive"]
    length_check = True
    format_check = True
    clinic_check = True
    name_check = True
    dob_check = True
    contact_check = True
    gender_check = True
    status_check = True
    allergy_check = True
    #conn = sqlite3.connect("New Clinic.db")
    data = request.form
    type_info = data["type_info"]
    staff_type = data["staff_type"]
    nric = data["nric"]
    first_name = data["first_name"]
    last_name = data["last_name"]
    dob = data["dob"]
    home_addr = data["address"]
    contact = data["contact"]
    gender = data["gender"]
    clinic = data["clinic"]
    allergy = data["allergy"]
    status = data["status"]
    if len(nric) != 9:#length
        return render_template("Add.html", length_check = length_check,type_info = type_info)
    
    if nric[0] not in nric_lst or nric[-1].isalpha() == False or nric[1:8].isdigit() == False:#format
        return render_template("Add.html", format_check = format_check,type_info = type_info)
    
    if clinic not in clinic_lst:#clinic exist
        return render_template("Add.html", clinic_check = clinic_check,type_info = type_info)

    if last_name.isalpha() == False:
        return render_template("Add.html", name_check = name_check,type_info = type_info)
    if first_name.isalpha() == False:
        try:
            name_lst = first_name.split(" ")
            for name in name_lst:
                if name.isalpha() == False:
                    return render_template("Add.html", name_check = name_check,type_info = type_info)
        except:
            return render_template("Add.html", name_check = name_check,type_info = type_info)

    if contact.isdigit() == False or len(contact) != 8:
        return render_template("Add.html", contact_check = contact_check,type_info = type_info)

    if gender not in gender_lst:
        return render_template("Add.html", gender_check = gender_check,type_info = type_info)

    dob_lst = dob.split("/")
    for num in dob_lst:
        if num.isdigit() == False:
            return render_template("Add.html", dob_check = dob_check,type_info = type_info)
    
    if type_info != "patient":
      if status not in status_lst:
          return render_template("Add.html", status_check = status_check,type_info = type_info)
        
      person_info = (staff_type,nric,first_name,last_name,dob,home_addr,contact,gender,allergy)
      conn.execute("INSERT INTO Person(type,NRIC,First_name,Last_name,Date_of_birth,Home_address,Contact_number,Gender,Allergy) VALUES (?,?,?,?,?,?,?,?,?)",person_info)
      staff_info  = (nric,clinic,status)
      conn.execute("INSERT INTO Staff(NRIC,Clinic,Status) VALUES(?,?,?)",staff_info)
    else:
        if allergy.isalpha() == False:
          return render_template("Add.html", allergy_check = allergy_check,type_info = type_info)
        person_info = (type_info,nric,first_name,last_name,dob,home_addr,contact,gender,allergy)
        conn.execute("INSERT INTO Person(type,NRIC,First_name,Last_name,Date_of_birth,Home_address,Contact_number,Gender,Allergy) VALUES (?,?,?,?,?,?,?,?,?)",person_info)
        patient_info = (nric,clinic)
        conn.execute("INSERT INTO Patient(NRIC,Clinic) VALUES(?,?)",patient_info)
    conn.commit()
    conn.close()
    return render_template("Add Successful Page.html")

@app.route("/update_template")
def update_template():
    return render_template("Update.html")

@app.route("/Update",methods = ["POST"])

def Update():
    
    nric_lst = ["S","T"]
    clinic_lst = ["Bedok","Jurong","Bishan","Clementi","Yishun"]
    length_check = True
    format_check = True
    clinic_check = True
    names = ""
    conn = sqlite3.connect("New Clinic.db")
    data = request.form
    type_info = data["type_info"]
    nric = data["nric"]
    clinic = data["clinic"]
    
    if len(nric) != 9:#length
        return render_template("Update.html", length_check = length_check)
    
    if nric[0] not in nric_lst or nric[-1].isalpha() == False or nric[1:8].isdigit() == False:#format
        return render_template("Update.html", format_check = format_check)
    
    if clinic not in clinic_lst:#clinic exist
        return render_template("Update.html", clinic_check = clinic_check)
    
    if type_info!= "Patient":
        lst = ["type_info","nric","first_name","last_name","dob","address","contact","gender","clinic","clinic_address","clinic_contact","status"]
        cursor = conn.execute("SELECT Person.type,Person.NRIC,Person.First_name,Person.Last_name,Person.Date_of_birth,Person.Home_address, Person.Contact_number,Person.Gender,ClinicInfo.Clinic,ClinicInfo.Clinic_address,ClinicInfo.Clinic_contact,Staff.Status FROM Person,ClinicInfo,Staff WHERE Person.NRIC = Staff.NRIC and ClinicInfo.Clinic = Staff.Clinic AND Person.NRIC = ? AND Staff.Clinic = ?",(nric,clinic)).fetchall()
##        if cursor.fetchone() == None:
##            return 
    else:
        lst = ["type_info","nric","first_name","last_name","dob","address","contact","gender","clinic","clinic_address","clinic_contact","allergy"]
        cursor = conn.execute("SELECT Person.type,Person.NRIC,Person.First_name,Person.Last_name,Person.Date_of_birth,Person.Home_address, Person.Contact_number,Person.Gender,ClinicInfo.Clinic,ClinicInfo.Clinic_address,ClinicInfo.Clinic_contact,Person.Allergy FROM Person,ClinicInfo,Patient WHERE Person.NRIC = Patient.NRIC AND Patient.Clinic = ClinicInfo.Clinic AND Person.NRIC = ? AND Patient.Clinic = ?",(nric,clinic)).fetchall()
    return render_template("Update Page.html",cursor = cursor,type_info = type_info,lst = lst,names = names)

@app.route("/Updated",methods = ["POST"])

def Updated():
    nric_lst = ["S","T"]
    gender_lst = ["Male","Female"]
    clinic_lst = ["Bedok","Jurong","Bishan","Clementi","Yishun"]
    status_lst = ["Active","Inactive"]
    length_check = True
    format_check = True
    clinic_check = True
    name_check = True
    dob_check = True
    contact_check = True
    gender_check = True
    status_check = True
    allergy_check = True
    conn = sqlite3.connect("New Clinic.db")
    data = request.form
    type_info = data["type_info"]
    nric = data["nric"]
    first_name = data["first_name"]
    last_name = data["last_name"]
    dob = data["dob"]
    home_addr = data["address"]
    contact = data["contact"]
    gender = data["gender"]
    clinic = data["clinic"]
    clinic_address = data["clinic_address"]
    clinic_contact = data["clinic_contact"]
    cursor,lst = UpdateCursor(nric,clinic,type_info)
    
    if clinic not in clinic_lst:#clinic exist
        return render_template("Update Page.html", clinic_check = clinic_check,type_info = type_info,cursor = cursor, lst = lst)

    if last_name.isalpha() == False:
        return render_template("Update Page.html", name_check = name_check,type_info = type_info,cursor = cursor, lst = lst)
    if first_name.isalpha() == False:
        try:
            name_lst = first_name.split(" ")
            for name in name_lst:
                if name.isalpha() == False:
                    return render_template("Update Page.html", name_check = name_check,type_info = type_info,cursor = cursor, lst = lst)
        except:
            return render_template("Update Page.html", name_check = name_check,type_info = type_info,cursor = cursor, lst = lst)

    if contact.isdigit() == False or len(contact) != 8:
        return render_template("Update Page.html", contact_check = contact_check,type_info = type_info,cursor = cursor, lst = lst)

    if gender not in gender_lst:
        return render_template("Update Page.html", gender_check = gender_check,type_info = type_info,cursor = cursor, lst = lst)

    dob_lst = dob.split("/")
    for num in dob_lst:
        if num.isdigit() == False:
            return render_template("Update Page.html", dob_check = dob_check,type_info = type_info,cursor = cursor, lst = lst)
    
    if type_info != "patient":
        status = data["status"]
        if status not in status_lst:
          return render_template("Update Page.html", status_check = status_check,type_info = type_info,cursor = cursor, lst = lst)
        allergy = "" #Allergy inserted is empty 
        person_info = (type_info,first_name,last_name,dob,home_addr,contact,gender,allergy,nric)
        conn.execute("UPDATE Person SET type = ?, First_name = ?, Last_name = ?,Date_of_birth = ?,Home_address = ?,Contact_number = ?,Gender = ?,Allergy = ? WHERE Person.NRIC = ?",person_info)#check
        status = data["status"]
        conn.execute("UPDATE Staff SET Status = ? WHERE NRIC = ?",(status,nric))#check
    else:
        allergy = data["allergy"]
        if allergy.isalpha() == False:
          return render_template("Update Page.html", allergy_check = allergy_check,type_info = type_info,cursor = cursor, lst = lst)
        person_info = (type_info,first_name,last_name,dob,home_addr,contact,gender,allergy,nric)
        conn.execute("UPDATE Person SET type = ?, First_name = ?, Last_name = ?,Date_of_birth = ?,Home_address = ?,Contact_number = ?,Gender = ?,Allergy = ? WHERE Person.NRIC = ?",person_info)#check
    conn.commit()
    return render_template("Update Successful Page.html",type_info = type_info)

@app.route("/count_template")
def count_template():
    return render_template("Count.html")

@app.route("/Count",methods = ["POST"])

def Count():
    clinic_lst = ["Bedok","Jurong","Bishan","Clementi","Yishun"]
    clinic_check = True
    conn = sqlite3.connect("New Clinic.db")
    data = request.form
    clinic = data["clinic"]
    if clinic not in clinic_lst:#clinic exist
        return render_template("Search.html", clinic_check = clinic_check)
    count = conn.execute("SELECT COUNT(Patient.NRIC) FROM Person,Patient WHERE Patient.NRIC = Person.NRIC AND Patient.Clinic = ?",(clinic,)).fetchone()#rmb ,
    return render_template("Clinic Display.html",clinic = clinic, count = count)
    
@app.route("/Back")

def Back():
    return render_template("Selection.html")



if __name__ == "__main__":
    app.run(port = 5012,debug = True)
           
