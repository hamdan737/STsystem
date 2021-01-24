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
    cursor.execute("SELECT * FROM st_users WHERE user_onlinest ="+str(1))
    result = cursor.fetchone()

    if cursor.rowcount >= 1:
      cursor.execute("INSERT INTO st_documents (doc_name,doc_rfid,employee_id,employee_name,sub_location,location) VALUES (%s,%s,%s,%s,%s,%s)", (text,id,result[0],result[2],result[9],result[8]))
      db.commit()
      print("Scanned")
    else:
      print("You are not loged in please login to the web system and scan document again to save changes")
  
  time.sleep(2)
finally:
  GPIO.cleanup()
