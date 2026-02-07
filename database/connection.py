import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "notes.db")

database_config = sqlite3.connect(DB_PATH, check_same_thread=False)
database_config.row_factory = sqlite3.Row

cursor = database_config.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")

print("Connected to SQLite database at:", DB_PATH)

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


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

