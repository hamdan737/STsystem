#!/usr/bin/env python

import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import mysql.connector

db = mysql.connector.connect(
  host="localhost",
  user="docadmin",
  passwd="12345",
  database="stsystem"
)

cursor = db.cursor()
reader = SimpleMFRC522()

try:
  while True:
    id, text = reader.read()
    cursor.execute("SELECT * FROM st_users  WHERE user_level="+str(1))
    results = cursor.fetchone()

    if results[5]==1:
      sql_insert = "INSERT INTO st_documents  (doc_name,doc_rfid,employee_id,employee_name,sub_location,location) VALUES (%s,%s,%s,%s,%s,%s)"
      cursor.execute(sql_insert, (text,id,results[0],results[2],results[9],results[8]))
      db.commit()
      print("Success")
    else:
      print("The admin is not login you can not add new documents")
    
    time.sleep(2)
finally:
    GPIO.cleanup()
