import mysql.connector

mydb = mysql.connector.connect(host="localhost", user="root", passwd="ghuanying1115",
                               auth_plugin="mysql_native_password", database="rfid")

mycursor = mydb.cursor()

def connect():
    if (mydb):
        print("Connection Successful - Connected to: Rfid Attendance Database")
        mainmenu()

    else:
        print("Connection Unsuccessful")
        exit()

def mainmenu():
    print("[ Rfid Attendance Register ]")
    print("Registering New Profile, Please input the details below:")
    input_id = input("ID: ")
    mycursor.execute("Select * FROM profiles WHERE id = '" + input_id + "'")
    myresult = mycursor.fetchall()
    while myresult == input_id:
        print("This ID has already exist!")
        input_id = input("ID: ")
        mycursor.execute("Select * FROM profiles WHERE id = '" + input_id + "'")
    input_name = input("Name: ")
    input_age = int(input("Age: "))
    input_gender = input("Gender: M/F ?")
    while input_gender not in ('M', 'F'):
        print("Please Enter M or F")
        input_gender = input("Gender: M/F ?")
    sqlform = "Insert into profiles(id, name, age, gender) values(%s, %s, %s, %s)"
    registers = [input_id, input_name, input_age, input_gender]
    mycursor.execute(sqlform, registers)
    mydb.commit()
    print("Successfully Registered New Profile")
    print("\n\n")
    return mainmenu()

connect()


