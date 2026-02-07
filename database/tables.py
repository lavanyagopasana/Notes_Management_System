from database.connection import get_db

def create_tables():
    db = get_db()
    cursor = db.cursor()

    users_table_query = """
    CREATE TABLE IF NOT EXISTS USERS (
        USERID INTEGER PRIMARY KEY AUTOINCREMENT,
        USERNAME TEXT NOT NULL,
        EMAIL TEXT NOT NULL UNIQUE,
        PASSWORD TEXT NOT NULL
    );
    """

    notes_table_query = """
    CREATE TABLE IF NOT EXISTS NOTES (
        NOTEID INTEGER PRIMARY KEY AUTOINCREMENT,
        USERID INTEGER NOT NULL,
        EMAIL TEXT NOT NULL,
        TITLE TEXT NOT NULL,
        CONTENT TEXT,
        LAST_UPDATED DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (USERID) REFERENCES USERS(USERID)
            ON DELETE CASCADE
            ON UPDATE CASCADE
    );
    """

    cursor.execute(users_table_query)
    cursor.execute(notes_table_query)
    db.commit()
    print("tables created successfully")
