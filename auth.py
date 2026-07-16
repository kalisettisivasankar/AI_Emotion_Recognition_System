import sqlite3


DATABASE = "database/emotion_app.db"


def register_user(full_name, email, phone, password):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users (full_name, email, phone, password)
            VALUES (?, ?, ?, ?)
        """, (full_name, email, phone, password))

        conn.commit()
        conn.close()

        return True, "Registration Successful!"

    except sqlite3.IntegrityError:
        return False, "Email or Phone Number already exists."

    except Exception as e:
        return False, str(e)


def login_user(email_or_phone, password):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM users
        WHERE (email=? OR phone=?) AND password=?
    """, (email_or_phone, email_or_phone, password))

    user = cursor.fetchone()

    conn.close()

    if user:
        return True, user
    else:
        return False, None