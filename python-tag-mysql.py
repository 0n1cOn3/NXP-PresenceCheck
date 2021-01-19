#!/bin/env python
#
# Made in 2021 in Switzerland
# by 0n1cOn3
# Version 0.1
import nxppy
import datetime
import time
import mysql.connector
import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
print('Please Wait ...')

# sleep for 2 seconds after printing output
time.sleep(2)

# now call function we defined above
clear()

date = datetime.datetime.now()
mifare = nxppy.Mifare()
mydb = mysql.connector.connect(
    host="dbserver",
    user="user",
    passwd="",
    database="dbname"
)

mycursor = mydb.cursor()

while True:
    date = datetime.datetime.now()
    try:
        uid = mifare.select()
        if uid is not None:
            mydb = mysql.connector.connect(
                host="dbserver",
                user="user",
                passwd="",
                database="dbname"
            )

            sql = "select Name, Online, RFID from worker where RFID = '"+uid+"'"

            mycursor = mydb.cursor()

            mycursor.execute(sql)
            record = mycursor.fetchone()
            if record is None:
                print('No data with this TAG Found!\nPlease inform your HR Department about it!')
                print(uid)
                time.sleep(3)
            elif record[1] is 1:
                sql = "UPDATE worker SET Online = 0 WHERE RFID = '"+uid+"'"
                sql2 = "INSERT INTO trm (Date, Worker, Text) VALUES (%s, %s, %s)"
                val = (date, uid, "OUT")
                mycursor.execute(sql)
                mycursor.execute(sql2, val)

                mydb.commit()
                print('Hallo')

                time.sleep(2)
            elif record[1] is 0:
                sql = "UPDATE worker SET Online = 1 WHERE RFID = '"+uid+"'"
                sql2 = "INSERT INTO trm (Date, Worker, Text) VALUES (%s, %s, %s)"
                val = (date, uid, "IN")
                mycursor.execute(sql)
                mycursor.execute(sql2,val)

                mydb.commit()
                print('See you soon :)')
                time.sleep(2)


    except nxppy.SelectError:
        # SelectError is raised if no card is in the field.
        pass

    finally:
        if (mydb.is_connected()):
            mycursor.close()
            mydb.close()
            clear()
            print("Ready to Welcome/Bye Worker")
