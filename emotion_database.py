import sqlite3
from datetime import datetime


def create_emotion_table():

    conn = sqlite3.connect("emotion_app.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS emotions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        emotion TEXT,
        date_time TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_emotion(emotion):

    conn = sqlite3.connect("emotion_app.db")
    cursor = conn.cursor()

    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        "INSERT INTO emotions(emotion,date_time) VALUES (?,?)",
        (emotion, time)
    )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_emotion_table()
    print("Emotion table created")