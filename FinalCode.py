#Libraries
import tkinter
from tkinter import *
from tkinter.ttk import Combobox
import random
import sys
from tkinter import messagebox
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PIL import Image, ImageTk
import time
import pymysql
from datetime import datetime
import os
import board
import busio
from digitalio import DigitalInOut, Direction
import adafruit_fingerprint
import pyrebase
from datetime import datetime
import serial

led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

uart = serial.Serial("/dev/ttyS0", baudrate=57600, timeout=1)

finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

config = {
  "apiKey": "AIzaSyBdEHEkGSN8GY28D09WkLsO13BsbGKZmGM",
  "authDomain": "health-monitoring-system-f0abd.firebaseapp.com",
  "databaseURL": "https://health-monitoring-system-f0abd-default-rtdb.firebaseio.com",
  "projectId": "health-monitoring-system-f0abd",
  "storageBucket": "health-monitoring-system-f0abd.appspot.com",
  "messagingSenderId": "145240768776",
  "appId": "1:145240768776:web:c31e640b2319fdbb986cbd",
  "measurementId": "G-8CK2DJ436J"
}

firebase = pyrebase.initialize_app(config)
database = firebase.database()

#conencting to database
conn = pymysql.connect(host='localhost', user='localuser1', password='rootuser', database='sensordb')
cursor = conn.cursor()

Mainscreen = Tk()
Mainscreen.title("Health Monitoring System")
Mainscreen.geometry('600x600')
Mainscreen.configure(background="bisque")

# ==================================== Existing Student ===============================================================

def ExistingStudent():
    myvar = c1.get()
    if myvar.isdigit() == True:    
        if len(str((myvar))) <= 10 and len(str((myvar))) > 9:
            entry = cursor.execute(f"SELECT * from STUDENT where STU_ID = {myvar}")
            conn.commit()
            if entry != 0:
                #fetching data from database
                cursor.execute(f"SELECT STU_NAME from STUDENT where STU_ID = {myvar}")
                fetchname = cursor.fetchone()
                
                cursor.execute(f"SELECT STU_ID from STUDENT where STU_ID = {myvar}")
                fetchid = cursor.fetchone()
                
                cursor.execute(f"SELECT STU_MAIL from STUDENT where STU_ID = {myvar}")
                fetchmail = cursor.fetchone()
                
                screen1 = Tk()
                screen1.title("Student Data")
                screen1.geometry('700x600')
                main_title = Label(screen1, text='Displaying Student Data', font=('Arial', 26), fg='red', background="bisque")
                main_title.place(x=120, y=0)

                # ==================================== IMAGE DETECTION ============================================================
                #             frame = Frame(screen1, width=600, height=400)
                #             frame.pack()
                #             frame.place(anchor='center', relx=0.5, rely=0.5)
                # 
                #             # Create an object of tkinter ImageTk
                #             img = ImageTk.PhotoImage(Image.open("images.jpg"))
                # 
                #             # Create a Label Widget to display the text or Image
                #             label = Label(image = img)
                #             label.pack()


                namelabel = Label(screen1, text='Student Name: ', font=('Arial', 20), fg='red')
                namelabel.place(x=50, y=300)
                disp_name = Label(screen1, text=fetchname, font=('Arial', 20), fg='red')
                disp_name.place(x=260, y=300)
                idlabel = Label(screen1, text='Student ID: ', font=('Arial', 20), fg='red')
                idlabel.place(x=50, y=340)
                disp_id = Label(screen1, text=fetchid , font=('Arial', 20), fg='red')
                disp_id.place(x=260, y=340)
                maillabel = Label(screen1, text='Guardian mail: ', font=('Arial', 20), fg='red')
                maillabel.place(x=50, y=380)
                disp_mail = Label(screen1, text=fetchmail, font=('Arial', 20), fg='red')
                disp_mail.place(x=260, y=380)
                
                StartCheck = Label(screen1, text='Start Checkup: ', font=('Arial', 20), fg='red')
                StartCheck.place(x=50, y=420)
                
                
                # ================================================== PREVIOUS RECORD =======================================
                
                def prevrecords():
                    screen1 = Tk()
                    screen1.title("Student Previous Data")
                    screen1.geometry('600x600')

                    s_name = Label(screen1, text='Student Name: ', font=('Arial', 20), fg='red')
                    s_name.place(x=50, y=300)
                    name_out = Label(screen1, text=fetchname, font=('Arial', 20), fg='red')
                    name_out.place(x=260, y=300)

                    s_id = Label(screen1, text='Student ID: ', font=('Arial', 20), fg='red')
                    s_id.place(x=50, y=340)
                    id_out = Label(screen1, text=fetchid, font=('Arial', 20), fg='red')
                    id_out.place(x=260, y=340)

                    sen1 = Label(screen1, text='SPO2: ', font=('Arial', 20), fg='red')
                    sen1.place(x=50, y=380)
                    cursor.execute(f"SELECT SPO2 from SENSORDATA where STU_ID = {myvar}")
                    fetchspo2 = cursor.fetchone()
                    sen1_out = Label(screen1, text=fetchspo2, font=('Arial', 20), fg='red')
                    sen1_out.place(x=260, y=380)

                    sen2 = Label(screen1, text='TEMPERATURE: ', font=('Arial', 20), fg='red')
                    sen2.place(x=50, y=420)
                    cursor.execute(f"SELECT TEMP from SENSORDATA where STU_ID = {myvar}")
                    fetchtemp = cursor.fetchone()
                    sen2_out = Label(screen1, text=fetchtemp, font=('Arial', 20), fg='red')
                    sen2_out.place(x=260, y=420)

                    sen3 = Label(screen1, text='PULSE: ', font=('Arial', 20), fg='red')
                    sen3.place(x=50, y=460)
                    cursor.execute(f"SELECT PULSE from SENSORDATA where STU_ID = {myvar}")
                    fetchpulse = cursor.fetchone()
                    sen3_out = Label(screen1, text=fetchpulse, font=('Arial', 20), fg='red')
                    sen3_out.place(x=260, y=460)

                # ==================================== SENSOR's START READING ==============================================
                def StartReading():
                    Sensorscreen = Tk()
                    Sensorscreen.title("Student Checkup")
                    Sensorscreen.geometry('600x600')
                    StoreData()
                    tq = Label(Sensorscreen, text='Sensor 1:', font=('Arial', 20), fg='red', background="bisque")
                    tq.place(x=50, y=150)
                    # iq = Button(Sensorscreen, text='start',font=('Arial', 16), fg='red', background="white", command = StoreData)
                    # iq.place(x=200, y=150)
                    tq = Label(Sensorscreen, text=RetrieveTemp(), font=('Arial', 20), fg='red', background="bisque")
                    tq.place(x=400, y=150) 
                    tw = Label(Sensorscreen, text='Sensor 2: ', font=('Arial', 20), fg='red', background="bisque")
                    tw.place(x=50, y=200)
                    # iw = Button(Sensorscreen, text='Start',font=('Arial', 16), fg='red', background="white", command = Communicate1)
                    # iw.place(x=200, y=200)
                    tq = Label(Sensorscreen, text=RetrieveSPO2, font=('Arial', 20), fg='red', background="bisque")
                    tq.place(x=400, y=200)
                    te = Label(Sensorscreen, text='Sensor 3:', font=('Arial', 20), fg='red', background="bisque")
                    te.place(x=50, y=250)
                    # ie = Button(Sensorscreen, text='Start',font=('Arial', 16), fg='red', background="white", command = Communicate2)
                    # ie.place(x=200, y=250)
                    tq = Label(Sensorscreen, text=RetrievePulse, font=('Arial', 20), fg='red', background="bisque")
                    tq.place(x=400, y=250)
                StartButton1 = Button(screen1, text='Start',font=('Arial', 16), fg='red', background="white", command=StartReading)
                StartButton1.place(x=260, y=420)
                PreviousData1 = Label(screen1, text='Previous Data: ', font=('Arial', 20), fg='red')
                PreviousData1.place(x=50, y=460)
                PreviousButton1 = Button(screen1, text='Previous record',font=('Arial', 16), fg='red', background="white", command = prevrecords)
                PreviousButton1.place(x=260, y=460)

                def StoreData():
                    now = datetime.now()
                    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
                    Pulse = int(database.child("Pulse").child("FinalPulse").child("P").get())
                    SpO2 = int(database.child("SpO2").child("FinalPulse").child("S").get())
                    Temp = float(database.child("Temperature").child("FinalTemp").child("T").get())
                    cursor.execute("INSERT INTO SENSORDATA VALUES (%s, %s, %s, %s, %s)", (myvar, SpO2, Pulse, Temp, formatted_date))
                    conn.commit()
                
                def RetrieveTemp():
                    cursor.execute(f"SELECT TEMP FROM SENSORDATA WHERE STU_ID = {myvar}")
                    fetchTemp = int(cursor.fetchone())
                    return fetchTemp

                def RetrievePulse():
                    cursor.execute(f"SELECT PULSE FROM SENSORDATA WHERE STU_ID = {myvar}")
                    fetchPulse = int(cursor.fetchone())
                    return fetchPulse

                def RetrieveSPO2():
                    cursor.execute(f"SELECT SPO2 FROM SENSORDATA WHERE STU_ID = {myvar}")
                    fetchSPO2 = float(cursor.fetchone())
                    return fetchSPO2

            else:
                messagebox.showerror("Error 404", "Entered ID does not exist")
        elif len(str((myvar))) > 10 or len(str((myvar))) < 10:
            messagebox.showerror("Error","Entered ID of " + str(len(str(myvar))) + " digit is Invalid")
    elif myvar.isdigit() == False:
        messagebox.showerror("Error", "Entered ID is Invalid")

# ================================== NEW STUDENT ENTRY ====================================================================================================

def Addnew():
    NewStudentscreen = Tk()
    NewStudentscreen.title("New Student Entry")
    NewStudentscreen.geometry('600x600')

    def submit():
        if len(str(entry2.get())) == 10:
            entry = cursor.execute(f"SELECT * from STUDENT where STU_ID = {entry2.get()}")
            conn.commit()
            if entry == 0:
                path = f"/home/pi/testing/datasets/{str(entry2.get())}"
                os.mkdir(path)
                cursor.execute("INSERT INTO STUDENT(STU_IMAGE, STU_ID, STU_NAME, STU_MAIL, STU_FINGER) VALUES (%s, %s, %s, %s, %s)", (path, entry2.get(), entry1.get(), entry3.get(), str(secretid)))
                conn.commit()
                messagebox.showinfo("Notification", "Student registered successfuly")
                NewStudentscreen.destroy()
            else:
                messagebox.showerror("Error", "Entered ID already exists")
        else:
            messagebox.showerror("Error", "Entered ID is Invalid")
        
    inputname = Label(NewStudentscreen, text='Enter Student Name: ', font=('Arial', 20), fg='red', background="bisque")
    inputname.place(x=30, y=100)
    inputid = Label(NewStudentscreen, text='Enter Student ID: ', font=('Arial', 20), fg='red', background="bisque")
    inputid.place(x=30, y=150)
    inputmail = Label(NewStudentscreen, text='Enter Student Email-ID: ', font=('Arial', 20), fg='red', background="bisque")
    inputmail.place(x=30, y=200)
    inputfinger = Label(NewStudentscreen, text='Fingerprint Registeration: ', font=('Arial', 20), fg='red', background="bisque")
    inputfinger.place(x=30, y=250)

    entry1 = Entry(NewStudentscreen, font=('Arial', 20), width=10)#, textvariable = e_name)
    entry1.place(x=350, y=100)
    entry1.get()
    entry2 = Entry(NewStudentscreen, font=('Arial', 20), width=10)#textvariable = e_id, )
    entry2.place(x=350, y=150)
    entry2.get()
    entry3 = Entry(NewStudentscreen, font=('Arial', 20), width=10)#, textvariable = e_mail)
    entry3.place(x=350, y=200)
    submitbutton = Button(NewStudentscreen, text='SUBMIT', font=('Arial', 20), fg='red', background="white", command = submit)
    submitbutton.place(x=430, y=300)

    # ================ CHANGES FOR FINGERPRINT =====================================================================================================
    secretid = get_num
    startbutton = Button(NewStudentscreen, text='START', font=('Arial', 20), fg='red', background="white", command = lambda:enroll_finger(secretid))
    startbutton.place(x=430, y=250)


def get_fingerprint():
    """Get a finger print image, template it, and see if it matches!"""
    print("Waiting for image...")
    while finger.get_image() != adafruit_fingerprint.OK:
        pass
    print("Templating...")
    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        return False
    print("Searching...")
    if finger.finger_search() != adafruit_fingerprint.OK:
        return False
    return True


# pylint: disable=too-many-branches
def get_fingerprint_detail():
    """Get a finger print image, template it, and see if it matches!
    This time, print out each error instead of just returning on failure"""
    print("Getting image...", end="")
    i = finger.get_image()
    if i == adafruit_fingerprint.OK:
        print("Image taken")
    else:
        if i == adafruit_fingerprint.NOFINGER:
            print("No finger detected")
        elif i == adafruit_fingerprint.IMAGEFAIL:
            print("Imaging error")
        else:
            print("Other error")
        return -1

    print("Templating...", end="")
    i = finger.image_2_tz(1)
    if i == adafruit_fingerprint.OK:
        print("Templated")
    else:
        if i == adafruit_fingerprint.IMAGEMESS:
            print("Image too messy")
        elif i == adafruit_fingerprint.FEATUREFAIL:
            print("Could not identify features")
        elif i == adafruit_fingerprint.INVALIDIMAGE:
            print("Image invalid")
        else:
            print("Other error")
        return -1

    print("Searching...", end="")
    i = finger.finger_fast_search()
    # pylint: disable=no-else-return
    # This block needs to be refactored when it can be tested.
    if i == adafruit_fingerprint.OK:
        print("Found fingerprint!")
        return i
    else:
        if i == adafruit_fingerprint.NOTFOUND:
            print("No match found")
        else:
            print("Other error")
        return -1


# pylint: disable=too-many-statements
def enroll_finger(location):
    """Take a 2 finger images and template it, then store in 'location'"""
    for fingerimg in range(1, 3):
        if fingerimg == 1:
            print("Place finger on sensor...", end="")
        else:
            print("Place same finger again...", end="")

        while True:
            i = finger.get_image()
            if i == adafruit_fingerprint.OK:
                print("Image taken")
                break
            if i == adafruit_fingerprint.NOFINGER:
                print(".", end="")
            elif i == adafruit_fingerprint.IMAGEFAIL:
                print("Imaging error")
                return False
            else:
                print("Other error")
                return False

        print("Templating...", end="")
        i = finger.image_2_tz(fingerimg)
        if i == adafruit_fingerprint.OK:
            print("Templated")
        else:
            if i == adafruit_fingerprint.IMAGEMESS:
                print("Image too messy")
            elif i == adafruit_fingerprint.FEATUREFAIL:
                print("Could not identify features")
            elif i == adafruit_fingerprint.INVALIDIMAGE:
                print("Image invalid")
            else:
                print("Other error")
            return False

        if fingerimg == 1:
            print("Remove finger")
            time.sleep(1)
            while i != adafruit_fingerprint.NOFINGER:
                i = finger.get_image()

    print("Creating model...", end="")
    i = finger.create_model()
    if i == adafruit_fingerprint.OK:
        print("Created")
    else:
        if i == adafruit_fingerprint.ENROLLMISMATCH:
            print("Prints did not match")
        else:
            print("Other error")
        return False

    print("Storing model #%d..." % location, end="")
    i = finger.store_model(location)
    if i == adafruit_fingerprint.OK:
        print("Stored")
    else:
        if i == adafruit_fingerprint.BADLOCATION:
            print("Bad storage location")
        elif i == adafruit_fingerprint.FLASHERR:
            print("Flash storage error")
        else:
            print("Other error")
        return False

    return True


def get_num():
    """Use input() to get a valid number from 1 to 127. Retry till success!"""
    cursor.execute("SELECT STU_FINGER FROM STUDENT")
    fetchfinger = cursor.fetchone()
    while fetchfinger < 127 and fetchfinger > 0:
        try:
            fetchfinger += 1
        except ValueError:
            pass
    return fetchfinger

def find_student():
    if get_fingerprint_detail() == -1:
        messagebox.showerror("Error 404", "No student found matching with the current fingerprint")
        return 0
    else:
        cursor.execute(f"SELECT STU_ID FROM STUDENT WHERE STU_FINGER = {get_fingerprint_detail()}")
        findfinger = int(cursor.fetchone())
        return findfinger


###############################################################################################################

# ===============================****** MAIN SCREEN *******================================================
sc1 = StringVar('')
t1 = Label(Mainscreen, text='Health Monitoring System', font=('Arial', 26), fg='red', background="bisque")
t1.place(x=110, y=0)
t2 = Label(Mainscreen, text='Face Recognization:', font=('Arial', 14), background="bisque")
t2.place(x=70, y=90)
il = Button(Mainscreen, text='Start',font=('Arial', 14), fg='red', background="white")
il.place(x=310, y=85)

fingersense = Label(Mainscreen, text='Fingerprint Recognization:', font=('Arial', 14), background='bisque')
fingersense.place(x = 70, y = 110)
startsense = Button(Mainscreen, text='Start',font=('Arial', 14), fg='red', background="white")
startsense.place(x=310, y=105)

t3 = Label(Mainscreen, text='OR', font=('Arial', 14),  fg='red', background="bisque")
t3.place(x=260, y=155)
t4 = Label(Mainscreen, text='Enter Student ID: ', font=('Arial', 14),  fg='black', background="bisque")
t4.place(x=135, y=215)
c1 = Entry(Mainscreen, font=('Arial', 14), width=10)
c1.place(x=310, y=213)
b = Button(Mainscreen, text='OK', font=('Arial', 14), fg='red', background="white", command = ExistingStudent)
b.place(x=430, y=210)
t5 = Label(Mainscreen, text='Add New Student ', font=('Arial', 14),  fg='black', background="bisque")
t5.place(x=235, y=315)
b = Button(Mainscreen, text='OK', font=('Arial', 14), fg='red', background="white", command = Addnew)
b.place(x=430, y=310)

Mainscreen.mainloop()
