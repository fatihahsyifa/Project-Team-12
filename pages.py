import pandas as pd
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow

from kasir import Kasir
from produk import Produk
from keuangan import Keuangan
from transaksi import Transaksi
from akun import Akun
from warning import Warning


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('login.ui', self)
        self.df_temp_user = pd.read_csv('data/temp_user.csv')
        self.button_login.clicked.connect(self.authenticate)

    def showWarning(self, message):
        self.warning = Warning(message)
        self.warning.show()

    def authenticate(self):
        username = self.input_username.text()
        password = self.input_password.text()

        df = pd.read_csv('data/user.csv')
        users = df[df["username"] == username]

        if not users.empty:
            user = users.iloc[0]
            if user.username == username and user.password == password:
                new_row = [user.id, user.role, user.name, user.username]
                self.df_temp_user.drop(self.df_temp_user.index, inplace=True)
                self.df_temp_user.loc[0] = new_row
                self.df_temp_user.to_csv('data/temp_user.csv', index=False)

                self.mainApp = MainWindow()
                self.mainApp.show()
                self.close()
            else:
                self.showWarning("Username / Password salah")
        else:
            self.showWarning("Username / Password salah")


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

        self.showMenu()
        self.button_keluar.clicked.connect(self.close)

        self.kasir.createdNewTransaction.connect(self.transaksi.initTable)
        self.kasir.createdNewTransaction.connect(self.keuangan.initTable)

        self.produk.makeTransactions.connect(self.keuangan.initTable)

    def move_to(self, index):
        self.stackedWidget.setCurrentIndex(index)

    def showMenu(self):
        self.df_temp_user = pd.read_csv('data/temp_user.csv')
        if self.df_temp_user.loc[0]["role"] == "cashier":
            self.button_keuangan.setVisible(False)
            self.button_akun.setVisible(False)


if __name__ == '__main__':
    app = QApplication([])
    window = LoginWindow()
    window.show()
    app.exec()
