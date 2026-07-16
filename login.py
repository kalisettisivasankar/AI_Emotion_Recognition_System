import sys

from auth import login_user
from dashboard import DashboardWindow
from register import RegisterWindow

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QFrame,
    QMessageBox
)


class LoginWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("AI Emotion Recognition")
        self.resize(1200,700)


        self.setStyleSheet("""
        QWidget{
            background:#0F172A;
            color:white;
            font-family:Segoe UI;
        }

        QFrame#card{
            background:#1E293B;
            border-radius:20px;
        }

        QLabel#title{
            font-size:30px;
            font-weight:bold;
        }

        QLabel#subtitle{
            font-size:14px;
            color:#CBD5E1;
        }

        QLineEdit{
            background:white;
            color:black;
            border:none;
            border-radius:12px;
            padding:12px;
            font-size:15px;
        }

        QPushButton#login{
            background:#2563EB;
            color:white;
            border:none;
            border-radius:12px;
            padding:12px;
            font-size:16px;
            font-weight:bold;
        }

        QPushButton#link{
            background:transparent;
            color:#60A5FA;
            border:none;
            font-size:13px;
        }
        """)


        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(60,40,60,40)


        left = QVBoxLayout()


        logo = QLabel("🤖")
        logo.setAlignment(Qt.AlignCenter)
        logo.setFont(QFont("Arial",60))


        heading = QLabel("AI Emotion\nRecognition")
        heading.setObjectName("title")


        desc = QLabel(
            "Professional Desktop Application\n"
            "Built using Python + PySide6\n"
            "with AI Emotion Detection."
        )

        desc.setObjectName("subtitle")


        left.addStretch()
        left.addWidget(logo)
        left.addSpacing(20)
        left.addWidget(heading)
        left.addSpacing(15)
        left.addWidget(desc)
        left.addStretch()


        card = QFrame()
        card.setObjectName("card")
        card.setFixedWidth(420)


        card_layout = QVBoxLayout(card)

        card_layout.setContentsMargins(
            40,40,40,40
        )

        card_layout.setSpacing(18)


        welcome = QLabel("Welcome Back")
        welcome.setObjectName("title")
        welcome.setAlignment(Qt.AlignCenter)


        subtitle = QLabel("Sign in to continue")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignCenter)


        self.email = QLineEdit()
        self.email.setPlaceholderText(
            "📧 Email or Phone"
        )


        self.password = QLineEdit()
        self.password.setPlaceholderText(
            "🔒 Password"
        )

        self.password.setEchoMode(
            QLineEdit.Password
        )


        self.show_btn = QPushButton("👁 Show")
        self.show_btn.setObjectName("link")

        self.show_btn.clicked.connect(
            self.toggle_password
        )


        login_btn = QPushButton("Sign In")
        login_btn.setObjectName("login")

        login_btn.clicked.connect(
            self.login
        )
        forgot_btn = QPushButton(
            "Forgot Password?"
        )

        forgot_btn.setObjectName(
            "link"
        )


        register_btn = QPushButton(
            "Create Account"
        )

        register_btn.setObjectName(
            "link"
        )

        register_btn.clicked.connect(
            self.open_register
        )


        card_layout.addWidget(welcome)
        card_layout.addWidget(subtitle)

        card_layout.addSpacing(20)

        card_layout.addWidget(self.email)
        card_layout.addWidget(self.password)
        card_layout.addWidget(self.show_btn)

        card_layout.addSpacing(10)

        card_layout.addWidget(login_btn)

        card_layout.addSpacing(15)

        card_layout.addWidget(forgot_btn)
        card_layout.addWidget(register_btn)


        main_layout.addLayout(left,1)
        main_layout.addWidget(card,1)



    def login(self):

        email_phone = self.email.text()
        password = self.password.text()


        if not email_phone or not password:

            QMessageBox.warning(
                self,
                "Error",
                "Enter Email/Phone and Password"
            )

            return


        success, user = login_user(
            email_phone,
            password
        )


        if success:

            QMessageBox.information(
                self,
                "Success",
                "Login Successful"
            )


            self.dashboard = DashboardWindow()
            self.dashboard.show()

            self.close()


        else:

            QMessageBox.warning(
                self,
                "Failed",
                "Invalid Email/Phone or Password"
            )



    def open_register(self):

        self.register_window = RegisterWindow()
        self.register_window.show()

        self.close()



    def toggle_password(self):

        if self.password.echoMode() == QLineEdit.Password:

            self.password.setEchoMode(
                QLineEdit.Normal
            )

            self.show_btn.setText(
                "🙈 Hide"
            )


        else:

            self.password.setEchoMode(
                QLineEdit.Password
            )

            self.show_btn.setText(
                "👁 Show"
            )



if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = LoginWindow()

    window.show()

    sys.exit(app.exec())