from database.connection import get_db

# ---------------- User Table Functions ----------------

def addUser(username: str, email: str, password: str):
    db = None
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO USERS (USERNAME, EMAIL, PASSWORD) VALUES (?, ?, ?)",
            (username, email.lower(), password)
        )
        db.commit()
        return True
    except Exception as e:
        print("Error in addUser:", e)
        return False
    finally:
        if db:
            db.close()


def checkUserStatus(email: str):
    db = None
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "SELECT USERID FROM USERS WHERE EMAIL = ?",
            (email.lower(),)
        )
        return cursor.fetchone() is not None
    except Exception as e:
        print("Error in checkUserStatus:", e)
        return False
    finally:
        if db:
            db.close()


def getPasswordFromDB(email: str):
    db = None
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "SELECT PASSWORD FROM USERS WHERE EMAIL = ?",
            (email.lower(),)
        )
        row = cursor.fetchone()
        return row["PASSWORD"] if row else None
    except Exception as e:
        print("Error in getPasswordFromDB:", e)
        return None
    finally:
        if db:
            db.close()


def updatePassword(email: str, new_password: str):
    db = None
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "UPDATE USERS SET PASSWORD = ? WHERE EMAIL = ?",
            (new_password, email.lower())
        )
        db.commit()
        return cursor.rowcount == 1
    except Exception as e:
        print("Error in updatePassword:", e)
        return False
    finally:
        if db:
            db.close()


# ---------------- Notes Table Functions ----------------

def addNotesInDB(email: str, title: str, content: str):
    db = None
    try:
        db = get_db()
        cursor = db.cursor()

        cursor.execute(
            "SELECT USERID FROM USERS WHERE EMAIL = ?",
            (email.lower(),)
        )
        row = cursor.fetchone()
        if not row:
            return False

        cursor.execute(
            "INSERT INTO NOTES (USERID, EMAIL, TITLE, CONTENT) VALUES (?, ?, ?, ?)",
            (row["USERID"], email.lower(), title, content)
        )
        db.commit()
        return True
    except Exception as e:
        print("Error in addNotesInDB:", e)
        return False
    finally:
        if db:
            db.close()


def getNotesFromDB(email: str):
    db = None
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "SELECT NOTEID, TITLE, CONTENT FROM NOTES WHERE EMAIL = ?",
            (email.lower(),)
        )
        return cursor.fetchall()
    except Exception as e:
        print("Error in getNotesFromDB:", e)
        return []
    finally:
        if db:
            db.close()


def getNoteById(note_id: int, email: str):
    db = None
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "SELECT NOTEID, TITLE, CONTENT FROM NOTES WHERE NOTEID = ? AND EMAIL = ?",
            (note_id, email.lower())
        )
        return cursor.fetchone()
    except Exception as e:
        print("Error in getNoteById:", e)
        return None
    finally:
        if db:
            db.close()


def updateNoteInDB(note_id: int, email: str, title: str, content: str):
    db = None
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "UPDATE NOTES SET TITLE = ?, CONTENT = ? WHERE NOTEID = ? AND EMAIL = ?",
            (title, content, note_id, email.lower())
        )
        db.commit()
        return cursor.rowcount == 1
    except Exception as e:
        print("Error in updateNoteInDB:", e)
        return False
    finally:
        if db:
            db.close()


def deleteNoteFromDB(note_id: int, email: str):
    db = None
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "DELETE FROM NOTES WHERE NOTEID = ? AND EMAIL = ?",
            (note_id, email.lower())
        )
        db.commit()
        return cursor.rowcount == 1
    except Exception as e:
        print("Error in deleteNoteFromDB:", e)
        return False
    finally:
        if db:
            db.close()
