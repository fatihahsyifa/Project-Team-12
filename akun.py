import pandas as pd
from PyQt6 import uic
from PyQt6.QtCore import Qt, QAbstractTableModel
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QWidget


class PandasModel(QAbstractTableModel):
    def __init__(self, data):
        super(PandasModel, self).__init__()
        self._data = data

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if index.isValid():
            if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
                value = self._data.iloc[index.row(), index.column()]
                return str(value)

    def headerData(self, col, orientation, role):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self._data.columns[col]


class Akun(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('akun.ui', self)
        self.groupBox_edit_akun.setVisible(False)
        self.df = pd.read_csv('data/user.csv')
        self.initTable()

    def initTable(self):
        self.model = PandasModel(self.df)
        self.tableView.setModel(self.model)
        self.button_tambah_akun.clicked.connect(self.tambahAkun)
        self.button_edit_akun.clicked.connect(self.ubahAkun)
        self.button_hapus_akun.clicked.connect(self.hapusAkun)

    def tambahAkun(self):
        name = self.input_tambah_name.text()
        username = self.input_tambah_username.text()
        password = self.input_tambah_password.text()
        if name == "" or username == "" or password == "":
            print("kosong")
        else:
            new_id = self.df.iloc[-1]["id"] + 1
            new_row = [new_id, "cashier", name, username, password]
            self.df.loc[len(self.df)] = new_row
            self.df.to_csv("data/user.csv", index=False)
            self.input_tambah_name.clear()
            self.input_tambah_username.clear()
            self.input_tambah_password.clear()
            self.initTable()

    def hapusAkun(self):
        if len(self.tableView.selectedIndexes()) > 0:
            rows = sorted(set(index.row() for index in self.tableView.selectedIndexes()))
            row = rows[0]

            self.df = self.df.drop(self.df.index[row])
            self.df.to_csv("data/user.csv", index=False)
            self.initTable()

    def ubahAkun(self):
        if len(self.tableView.selectedIndexes()) > 0:
            rows = sorted(set(index.row() for index in self.tableView.selectedIndexes()))
            row = rows[0]
            data = self.df.loc[row]
            self.input_edit_name.setText(data["name"])
            self.input_edit_username.setText(data["username"])
            self.input_edit_password.setText(data["password"])

            self.groupBox_edit_akun.setVisible(True)
            self.button_save_edit_akun.clicked.connect(self.editAkunSave)

    def editAkunSave(self):
        if len(self.tableView.selectedIndexes()) > 0:
            rows = sorted(set(index.row() for index in self.tableView.selectedIndexes()))
            row = rows[0]
            data = self.df.loc[row]

            name = self.input_edit_name.text()
            username = self.input_edit_username.text()
            password = self.input_edit_password.text()

            if name == "" or username == "" or password == "":
                print("kosong")
            else:
                edited_row = [data["id"], data["role"], name, username, password]
                self.df.loc[row] = edited_row
                self.df.to_csv("data/user.csv", index=False)
                self.input_edit_name.clear()
                self.input_edit_username.clear()
                self.input_edit_password.clear()
                self.groupBox_edit_akun.setVisible(False)
                self.initTable()
