#!/bin/python3 -u
import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv('db_password'),
    database="burnt_bot"
)

mycursor = mydb.cursor()

#mycursor.execute("CREATE DATABASE burnt_bot")
#mycursor.execute("CREATE TABLE buyers (name VARCHAR(255), id VARCHAR(255), inviter VARCHAR(255), inviter_id VARCHAR(255))")
#mycursor.execute("CREATE TABLE commissions (name VARCHAR(255), id VARCHAR(255), buyer VARCHAR(255), amount VARCHAR(255))")

mycursor.execute("SHOW TABLES")

for x in mycursor:
  print(x)
