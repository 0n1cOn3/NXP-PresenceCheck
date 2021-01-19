#!/bin/env python
#
# Made in 2021 in Switzerland
# by 0n1cOn3
# Version 0.1
#
import nxppy
import datetime
import pymongo
import time

# import os

date = datetime.datetime.now()
mifare = nxppy.Mifare()

myclient = pymongo.MongoClient("ServerIP")


dblist = myclient.list_database_names()
if "dbname" in dblist:
    print("The database exists.")
    print("Waiting for Tag...")

mydb = myclient["dbname"]
mycol = mydb["tag_user"]

# Print card UIDs as they are detected
# tag_dict = {}

while True:
    date = datetime.datetime.now()
    try:
        uid = mifare.select()
        if uid is not None:
            print("Tag scanned...\n")
            if mycol.find_one({"_id": uid}) is not None:
                entry = mycol.find_one({"_id": uid})
                data = entry["Date"]
                time_entry = data["Time"]
                dates = date.strftime("%d-%m-%Y")
                times = date.strftime("%H:%M:%S")
                if mycol.find_one({"_id":uid,"Date._id":dates}):
                   mycol.update_one({"_id":uid},{"$set":{"Date.Time":{"_id":times}}})
                else:
                    print("Nope...")
                
            else:
                name = str(input("Please insert username:\n"))
                dates = date.strftime("%d-%m-%Y")
                times = date.strftime("%H:%M:%S")
                mycol.insert_one({
                    "_id": uid,
                    "Name": name,
                    "Date": [{
                        "Time": [{
                            "in/out": "in"}.times]}.dates]})
                print("Username has been entered...")
            uid = None
            time.sleep(3)



    except nxppy.SelectError:
        # SelectError is raised if no card is in the field.
        pass
