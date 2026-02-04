# import mysql.connector as SQLC

# # 1. login to database
# database_config = SQLC.connect(
#                         host = 'localhost',
#                         user = 'root',
#                         password = 'root', # your myswl workbench password
#                         database = 'notes_management3234'
#                     )

# # 2. creating cursor object
# cursor = database_config.cursor()

import sqlite3
# SQLite connection
database_config = sqlite3.connect("notes.db", check_same_thread=False)
cursor = database_config.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")
print('Connected to SQLite database successfully')

# print(database_config)
# print(cursor)

# # creating database
# create_database_query = "CREATE DATABASE IF NOT EXISTS ANIMALS;"
# # 3. execute() function is used to execute the sql queries
# cursor.execute(create_database_query)
# print("Database created successfully")

# # selecting database
# cursor.execute("USE ANIMALS;")

# # CREATING TABLE
# animal_table_query = """
#                     CREATE TABLE ANIMAL(
#                     NAME VARCHAR(30),
#                     AGE INT
#                     );"""
# cursor.execute(animal_table_query)
# print(cursor)
# print("Table created successfully")