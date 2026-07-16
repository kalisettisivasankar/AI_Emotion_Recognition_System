from flask import Flask, render_template, Response
import cv2
from deepface import DeepFace
import sqlite3
from datetime import datetime

app = Flask(__name__)

camera = cv2.VideoCapture(0)

current_emotion = "Waiting..."
last_saved_emotion = ""


def save_emotion(emotion):
    conn = sqlite3.connect("emotion_app.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS emotion_history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        emotion TEXT,
        date_time TEXT
    )
    """)

    cursor.execute(
        "INSERT INTO emotion_history (emotion, date_time) VALUES (?, ?)",
        (emotion, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )

    conn.commit()
    conn.close()


def generate_frames():
    global current_emotion
    global last_saved_emotion

    while True:

        success, frame = camera.read()

        if not success:
            break

        try:
            result = DeepFace.analyze(
                img_path=frame,
                actions=["emotion"],
                detector_backend="opencv",
                enforce_detection=False,
                silent=True
            )

            if isinstance(result, list):
                emotion = result[0]["dominant_emotion"]
            else:
                emotion = result["dominant_emotion"]

            current_emotion = emotion

            if current_emotion != last_saved_emotion:
                save_emotion(current_emotion)
                last_saved_emotion = current_emotion

        except Exception as e:
            print("ERROR:", e)

        cv2.putText(
            frame,
            f"Emotion: {current_emotion}",
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        ret, buffer = cv2.imencode(".jpg", frame)

        if not ret:
            continue

        frame = buffer.tobytes()

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' +
            frame +
            b'\r\n'
        )


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/video")
def video():
    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )