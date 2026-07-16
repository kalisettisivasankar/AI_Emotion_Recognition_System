import cv2
from deepface import DeepFace

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QPushButton
)

from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QImage, QPixmap


class DashboardWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("AI Emotion Recognition Dashboard")
        self.resize(1000, 700)


        layout = QVBoxLayout()


        self.title = QLabel(
            "AI Emotion Recognition Dashboard"
        )
        self.title.setAlignment(Qt.AlignCenter)


        self.camera_label = QLabel()

        self.camera_label.setFixedSize(
            700,
            450
        )

        self.camera_label.setAlignment(
            Qt.AlignCenter
        )


        self.emotion_label = QLabel(
            "Emotion: Waiting..."
        )

        self.emotion_label.setAlignment(
            Qt.AlignCenter
        )


        self.start_btn = QPushButton(
            "Start Camera"
        )

        self.start_btn.clicked.connect(
            self.start_camera
        )


        layout.addWidget(self.title)
        layout.addWidget(self.camera_label)
        layout.addWidget(self.emotion_label)
        layout.addWidget(self.start_btn)


        self.setLayout(layout)


        self.camera = None

        self.current_emotion = "Waiting..."

        self.frame_count = 0


        self.timer = QTimer()

        self.timer.timeout.connect(
            self.update_frame
        )



    def start_camera(self):

        self.camera = cv2.VideoCapture(0)

        self.timer.start(30)



    def update_frame(self):

        ret, frame = self.camera.read()


        if ret:

            self.frame_count += 1


            # Emotion detection every 30 frames
            if self.frame_count % 30 == 0:

                try:

                    result = DeepFace.analyze(
                        frame,
                        actions=['emotion'],
                        detector_backend="opencv",
                        enforce_detection=False
                    )


                    if isinstance(result, list):

                        self.current_emotion = result[0]["dominant_emotion"]

                    else:

                        self.current_emotion = result["dominant_emotion"]


                    print(
                        "Detected Emotion:",
                        self.current_emotion
                    )


                except Exception as e:

                    print(e)



            self.emotion_label.setText(
                "Emotion: " + self.current_emotion
            )



            frame = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )


            h,w,ch = frame.shape


            image = QImage(
                frame.data,
                w,
                h,
                ch*w,
                QImage.Format_RGB888
            )


            self.camera_label.setPixmap(
                QPixmap.fromImage(image)
            )



    def closeEvent(self, event):

        if self.camera:

            self.camera.release()

        event.accept()