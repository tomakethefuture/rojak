import mysql.connector
import datetime
from datetime import datetime

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="ghuanying1115",
    auth_plugin="mysql_native_password",
    database="rfid"
    )

mycursor = mydb.cursor()

def connect():
    if (mydb):
        print("Connection Successful - Connected to: Rfid Attendance Database")
        mainmenu()
    else:
        print("Connection Unsuccessful")
        exit()

def mainmenu():
    print("[ Rfid Attendance Recorder ]")
    print("1. Check In")
    print("2. Check Out")
    input_option  = input("Enter your Options: ")
    while input_option not in ('1', '2'):
        input_option = input("Enter your Options:")
    input_id = input("Please Enter your ID: ")
    take_attendance(input_id, input_option)

def take_attendance(id, status):
    if status == '1':
        attendance_status = 'IN'
    if status == '2':
        attendance_status = 'OUT'
    mycursor.execute("Select * FROM profiles WHERE id = '" + id + "'")
    myresult = mycursor.fetchall()
    if not myresult:
        print("Profile NOT found with current ID!")
        print("\n\n")
    else:
        for row in myresult:
            print(row)
            print("\n\n")
            print("ID: " + str(row[0]))
            attendance_id = row[0]
            print("Name: " + row[1])
            attendance_name = row[1]
            print("Age: " + str(row[2]))
            print("Gender: " + row[3])
            now = datetime.now()
            attendance_date = now.strftime("%d-%m-%Y")
            print("Time:" + attendance_date)
            attendance_time = now.strftime("%H:%M:%S")
            print("Date:" + now.strftime("%H:%M:%S") + " (" + now.strftime("%A") + ")")
            print("Status:" + attendance_status)
            insertsql(int(attendance_id), attendance_name, attendance_date, attendance_time, attendance_status)
    return mainmenu()

def insertsql(id, name, date, time, status):
    sqlform = "Insert into attendance(id, name, date, time, status) values (%s, %s, %s, %s, %s)"
    attendances = [id, name, date, time, status]
    mycursor.execute(sqlform, attendances)
    mydb.commit()
    print("Attendance Taken!\n\n")
    return mainmenu()


mainmenu()






