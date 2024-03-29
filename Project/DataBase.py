import sqlite3

connection = sqlite3.connect("DataBase.db")
cursor = connection.cursor()

cursor.execute("create table if not exists DataBase (PESEL INTEGER PRIMARY KEY, FirstName TEXT, LastName TEXT, Street TEXT, City TEXT, ZipCode TEXT)")

connection.commit()
connection.close()