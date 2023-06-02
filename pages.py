import pandas as pd
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow

from login import Login
from kasir import Kasir


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('pages.ui', self)
        self.login = Login()
        self.stackedWidget.addWidget(self.login)
        self.login.button_login.clicked.connect(self.authenticate)

        self.kasir = Kasir()
        self.stackedWidget.addWidget(self.kasir)

    def authenticate(self):
        username = self.login.input_username.text() #ngambil teks yang ada di input
        password = self.login.input_password.text()

        df = pd.read_csv('data/user.csv')
        users = df[df["username"] == username] #yang ada di database sesuaiin dgn yg ada dinput bener ngga

        if not users.empty:
            user = users.iloc[0]
            if user.username == username and user.password == password:
                self.stackedWidget.setCurrentIndex(1)
        else:
            print("wrong credentials")


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
