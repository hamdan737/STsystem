#!/usr/bin/env python
import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import mariadb
import sys

db = mariadb.connect(
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
    cursor.execute("Select id,Department_Name,Sublocation,Location FROM dep WHERE RFID="+str(id))
    result = cursor.fetchone()

    if cursor.rowcount >= 1:
      cursor.execute("INSERT INTO docs (RFID,Department_ID,Department_Name,Employee,Sublocation,Location) VALUES (%s,%s,%s,%s,%s,%s)", (id,id,result[1],text,result[2],result[3]) )
      db.commit()
      time.sleep(2)
finally:
  GPIO.cleanup()
