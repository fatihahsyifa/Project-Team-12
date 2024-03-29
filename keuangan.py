import pandas as pd
from PyQt6 import uic
from PyQt6.QtCore import Qt, QAbstractTableModel, QDateTime
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QWidget

from warning import Warning


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


class Keuangan(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('keuangan.ui', self)
        self.df_temp_user = pd.read_csv('data/temp_user.csv')
        self.initTable()

    def initTable(self):
        self.df = pd.read_csv('data/keuangan.csv')
        self.model = PandasModel(self.df)
        self.tableView.setModel(self.model)

        self.input_tambah_saldo.setValidator(QIntValidator(1, 1_999_999_999, self))
        self.input_tarik_saldo.setValidator(QIntValidator(1, 1_999_999_999, self))

        self.button_tambah_saldo.clicked.connect(self.tambahSaldo)
        self.button_tarik_saldo.clicked.connect(self.tarikSaldo)

        self.label_saldo.setText(str(self.hitungSaldo()))

    def tambahSaldo(self):
        amount = self.input_tambah_saldo.text()
        if amount is None or amount == "":
            self.showWarning("Amount tidak boleh kosong")
        else:
            amount = int(self.input_tambah_saldo.text())
            new_id = len(self.df) + 1
            date = QDateTime.currentDateTime().toString(Qt.DateFormat.ISODate)
            operator = self.df_temp_user.loc[0, "username"]
            new_row = [new_id, "in", amount, date, operator]
            self.df.loc[new_id] = new_row
            self.input_tambah_saldo.clear()
            self.df.to_csv("data/keuangan.csv", index=False)
            self.initTable()

    def tarikSaldo(self):
        amount = self.input_tarik_saldo.text()
        if amount is None or amount == "":
            self.showWarning("Amount tidak boleh kosong")
        else:
            amount = 0 - int(self.input_tarik_saldo.text())
            new_id = len(self.df) + 1
            date = QDateTime.currentDateTime().toString(Qt.DateFormat.ISODate)
            operator = self.df_temp_user.loc[0, "username"]
            new_row = [new_id, "out", amount, date, operator]
            self.df.loc[new_id] = new_row
            self.input_tarik_saldo.clear()
            self.df.to_csv("data/keuangan.csv", index=False)
            self.initTable()

    def hitungSaldo(self):
        return self.df["amount"].sum()

    def showWarning(self, message):
        self.warning = Warning(message)
        self.warning.show()
