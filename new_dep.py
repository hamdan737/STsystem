#!/usr/bin/env python

import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import mysql.connector

db = mysql.connector.connect(
  host="localhost",
  user="docadmin",
  passwd="12345",
  database="STsystem"
)

cursor = db.cursor()
reader = SimpleMFRC522()

try:
  while True:
    id, text = reader.read()
    cursor.execute("SELECT id FROM dep WHERE RFID="+str(id))
    cursor.fetchone()

    if cursor.rowcount >= 1:
      overwrite = input("Overwite (Y/N)? ")
      if overwrite[0] == 'Y' or overwrite[0] == 'y':
        time.sleep(1)
        sql_insert = "UPDATE dep SET  Department_Name = %s,Sublocation = %s,Location = %s WHERE RFID=%s"
      else:
        continue;
    else:
      sql_insert = "INSERT INTO dep (Department_Name,RFID,Sublocation,Location) VALUES (%s, %s,%s,%s)"
    new_name = input("Department Name: ")
    new_Sublocation = input("Sublocation:")
    new_location = input("location: ")
    cursor.execute(sql_insert, (new_name, id,new_Sublocation,new_location))

    db.commit()

    time.sleep(2)
finally:
    GPIO.cleanup()
