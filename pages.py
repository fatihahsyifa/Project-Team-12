import pandas as pd
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget

from kasir import Kasir
from produk import Produk
from keuangan import Keuangan
from transaksi import Transaksi
from akun import Akun

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('login.ui', self)

        self.mainApp = MainWindow()
        self.mainApp.show()
        self.close()

        self.button_login.clicked.connect(self.authenticate)

    def authenticate(self):
        username = self.input_username.text()
        password = self.input_password.text()

        df = pd.read_csv('data/user.csv')
        users = df[df["username"] == username]

        if not users.empty:
            user = users.iloc[0]
            if user.username == username and user.password == password:
                self.mainApp = MainWindow()
                self.mainApp.show()
                self.close()
            else:
                print("wrong credentials")
        else:
            print("wrong credentials")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('pages.ui', self)

        self.kasir = Kasir()
        self.stackedWidget.addWidget(self.kasir)
        self.button_kasir.clicked.connect(lambda: self.move_to(0))

        self.produk = Produk()
        self.stackedWidget.addWidget(self.produk)
        self.button_produk.clicked.connect(lambda: self.move_to(1))

        self.keuangan = Keuangan()
        self.stackedWidget.addWidget(self.keuangan)
        self.button_keuangan.clicked.connect(lambda: self.move_to(2))

        self.transaksi = Transaksi()
        self.stackedWidget.addWidget(self.transaksi)
        self.button_transaksi.clicked.connect(lambda: self.move_to(3))

        self.akun = Akun()
        self.stackedWidget.addWidget(self.akun)
        self.button_akun.clicked.connect(lambda: self.move_to(4))

        self.button_keluar.clicked.connect(self.close)

    def move_to(self, index):
        print(index)
        self.stackedWidget.setCurrentIndex(index)


if __name__ == '__main__':
    app = QApplication([])
    window = LoginWindow()
    window.show()
    app.exec()
