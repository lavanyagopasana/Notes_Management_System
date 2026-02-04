# import sqlite3

# # SQLite connection
# database_config = sqlite3.connect("notes.db", check_same_thread=False)
# cursor = database_config.cursor()
# cursor.execute("PRAGMA foreign_keys = ON;")
# print('Connected to SQLite database successfully')

from database.connection import database_config, cursor

# ---------------- User Table Functions ----------------

def addUser(username: str, email: str, password: str):
    try:
        query = "INSERT INTO USERS (USERNAME, EMAIL, PASSWORD) VALUES (?, ?, ?)"
        cursor.execute(query, (username, email, password))
        database_config.commit()
        return True
    except Exception as e:
        return f"Error in addUser: {e}"


def checkUserStatus(email: str):
    try:
        query = "SELECT USERID FROM USERS WHERE EMAIL = ?"
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        return bool(result)
    except Exception as e:
        return f"Error in checkUserStatus: {e}"


def getPasswordFromDB(email: str):
    try:
        query = "SELECT PASSWORD FROM USERS WHERE EMAIL = ?"
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        if result:
            return result[0]
        return None
    except Exception as e:
        return f"Error in getPasswordFromDB: {e}"


def updatePassword(email: str, new_password: str):
    try:
        query = "UPDATE USERS SET PASSWORD = ? WHERE EMAIL = ?"
        cursor.execute(query, (new_password, email))
        database_config.commit()
        return cursor.rowcount == 1
    except Exception as e:
        return f"Error in updatePassword: {e}"


# ---------------- Notes Table Functions ----------------

def addNotesInDB(email: str, title: str, content: str):
    try:
        # get userid from users table
        cursor.execute("SELECT USERID FROM USERS WHERE EMAIL = ?", (email,))
        result = cursor.fetchone()
        if not result:
            return False
        userid = result[0]
        query = "INSERT INTO NOTES (USERID, EMAIL, TITLE, CONTENT) VALUES (?, ?, ?, ?)"
        cursor.execute(query, (userid, email, title, content))
        database_config.commit()
        return True
    except Exception as e:
        return f"Error in addNotesInDB: {e}"


def getNotesFromDB(email: str):
    try:
        query = "SELECT NOTEID, TITLE, CONTENT FROM NOTES WHERE EMAIL = ?"
        cursor.execute(query, (email,))
        return cursor.fetchall()
    except Exception as e:
        return f"Error in getNotesFromDB: {e}"


def getNoteById(note_id: int, email: str):
    try:
        query = "SELECT NOTEID, TITLE, CONTENT FROM NOTES WHERE NOTEID = ? AND EMAIL = ?"
        cursor.execute(query, (note_id, email))
        return cursor.fetchone()
    except Exception as e:
        return f"Error in getNoteById: {e}"


def updateNoteInDB(note_id: int, email: str, title: str, content: str):
    try:
        query = "UPDATE NOTES SET TITLE = ?, CONTENT = ? WHERE NOTEID = ? AND EMAIL = ?"
        cursor.execute(query, (title, content, note_id, email))
        database_config.commit()
        return cursor.rowcount == 1
    except Exception as e:
        return f"Error in updateNoteInDB: {e}"


def deleteNoteFromDB(note_id: int, email: str):
    try:
        query = "DELETE FROM NOTES WHERE NOTEID = ? AND EMAIL = ?"
        cursor.execute(query, (note_id, email))
        database_config.commit()
        return cursor.rowcount == 1
    except Exception as e:
        return f"Error in deleteNoteFromDB: {e}"
