import sys

from auth import register_user

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QMessageBox
)

from PySide6.QtCore import Qt


class RegisterWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Create Account")
        self.resize(500, 650)


        self.setStyleSheet("""
            QWidget{
                background:#0F172A;
                color:white;
                font-family:Segoe UI;
            }

            QLabel#title{
                font-size:24px;
                font-weight:bold;
            }

            QLineEdit{
                background:white;
                color:black;
                border-radius:10px;
                padding:12px;
            }

            QPushButton{
                background:#2563EB;
                color:white;
                border-radius:10px;
                padding:12px;
                font-weight:bold;
            }

            QPushButton:hover{
                background:#1D4ED8;
            }
        """)


        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)


        title = QLabel("Create Account")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)


        self.name = QLineEdit()
        self.name.setPlaceholderText("Full Name")


        self.email = QLineEdit()
        self.email.setPlaceholderText("Email Address")


        self.phone = QLineEdit()
        self.phone.setPlaceholderText("Phone Number")


        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)


        self.confirm = QLineEdit()
        self.confirm.setPlaceholderText("Confirm Password")
        self.confirm.setEchoMode(QLineEdit.Password)


        register_btn = QPushButton("Register")
        register_btn.clicked.connect(self.register)


        login_btn = QPushButton("Back to Login")


        layout.addWidget(title)
        layout.addSpacing(20)

        layout.addWidget(self.name)
        layout.addWidget(self.email)
        layout.addWidget(self.phone)
        layout.addWidget(self.password)
        layout.addWidget(self.confirm)

        layout.addSpacing(10)

        layout.addWidget(register_btn)
        layout.addWidget(login_btn)


        self.setLayout(layout)



    def register(self):

        name = self.name.text()
        email = self.email.text()
        phone = self.phone.text()
        password = self.password.text()
        confirm = self.confirm.text()


        if not name or not email or not phone or not password:

            QMessageBox.warning(
                self,
                "Error",
                "Please fill all fields"
            )
            return


        if password != confirm:

            QMessageBox.warning(
                self,
                "Error",
                "Passwords do not match"
            )
            return


        success, message = register_user(
            name,
            email,
            phone,
            password
        )


        if success:

            QMessageBox.information(
                self,
                "Success",
                message
            )

            self.name.clear()
            self.email.clear()
            self.phone.clear()
            self.password.clear()
            self.confirm.clear()


        else:

            QMessageBox.warning(
                self,
                "Error",
                message
            )



if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = RegisterWindow()
    window.show()

    sys.exit(app.exec())