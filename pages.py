import pandas as pd
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow

from kasir import Kasir
from produk import Produk
from keuangan import Keuangan
from transaksi import Transaksi
from akun import Akun


# yang ada di Login.py kita pindah sini (LoginWindow)
# Halaman login sekarang berdiri sendiri / memiliki window sendiri (sebelumnya sebagai widget di MainWindow)
# kita ubah biar mudah mengatur pergantian halaman, jadi kalo login udah selesai, windownya ketutup diganti main window
# yang berisi menu2 aplikasi kita
class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('login.ui', self)  # load login.ui

        #  skip login page
        self.mainApp = MainWindow()
        self.mainApp.show()
        self.close()

        self.button_login.clicked.connect(self.authenticate)  # kalo tombol login diklik, jalankan fungsi authenticate

    # sama kayak sebelumnya
    def authenticate(self):
        username = self.input_username.text()
        password = self.input_password.text()

# ngambil data di database utk dicocokkan dgn yg diinput sama user
        df = pd.read_csv('data/user.csv')
        users = df[df["username"] == username] # searching yg namanya sesuai

# melakukan pencocokan data apakah sesuai
        if not users.empty:
            user = users.iloc[0] # gak kosong/ada
            if user.username == username and user.password == password:
                self.mainApp = MainWindow()  # untuk menginisiasi MainWindow
                self.mainApp.show()  # menampilkan mainWindow
                self.close()  # menutup LoginWindow
            else:
                print("wrong credentials")
        else:
            print("wrong credentials")


# semua menu aplikasi kita bakalan berada di sini, perpindahan halaman menggunakan stackedWidget
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

        self.kasir.createdNewTransaction.connect(self.transaksi.initTable)
        self.kasir.createdNewTransaction.connect(self.keuangan.initTable)

        self.produk.makeTransactions.connect(self.keuangan.initTable)


    def move_to(self, index):
        self.stackedWidget.setCurrentIndex(index)


if __name__ == '__main__':
    app = QApplication([])
    window = LoginWindow()  # Window pertama yang dijalanin adalah loginwindow
    window.show()
    app.exec()
