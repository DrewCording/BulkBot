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
mycursor.execute("CREATE TABLE buyers (date VARCHAR(255), name VARCHAR(255), id VARCHAR(255), inviter VARCHAR(255), inviter_id VARCHAR(255))")
mycursor.execute("CREATE TABLE commissions (date VARCHAR(255), name VARCHAR(255), id VARCHAR(255), buyer VARCHAR(255), amount VARCHAR(255))")

#mycursor.execute("SHOW TABLES")

#mycursor.execute("SELECT * FROM buyers WHERE id=852195369956671499")
#myresult=mycursor.fetchall()

print(myresult[0][2])
