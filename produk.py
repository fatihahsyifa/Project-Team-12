import pandas as pd
from PyQt6 import uic
from PyQt6 import QtCore as Qtc
from PyQt6.QtCore import Qt, QAbstractTableModel
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QWidget

from produk_edit import EditProduk
from produk_size import SizeProduk
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


class Produk(QWidget):
    makeTransactions = Qtc.pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('produk.ui', self)
        self.input_baru_buy_price.setValidator(QIntValidator(1, 1_999_999_999, self))
        self.input_baru_sell_price.setValidator(QIntValidator(1, 1_999_999_999, self))
        self.input_baru_discount.setValidator(QIntValidator(1, 1_999_999_999, self))

        self.button_tambah_produk.clicked.connect(self.tambahProduk)
        self.button_hapus_produk.clicked.connect(self.hapusProduk)
        self.button_edit_produk.clicked.connect(self.ubahProduk)
        self.button_stok_produk.clicked.connect(self.stokProduk)

        self.initTable()
        self.df_size = pd.read_csv('data/size.csv')

    def initTable(self):
        self.df_produk = pd.read_csv('data/produk.csv')
        self.model = PandasModel(self.df_produk)
        self.tableView.setModel(self.model)

    def clearForm(self):
        self.input_baru_name.clear()
        self.input_baru_merk.clear()
        self.input_baru_buy_price.clear()
        self.input_baru_sell_price.clear()
        self.input_baru_discount.clear()
        self.input_baru_color.clear()

    def tambahProduk(self):
        name = self.input_baru_name.text()
        merk = self.input_baru_merk.text()
        buy_price = self.input_baru_buy_price.text()
        sell_price = self.input_baru_sell_price.text()
        discount = self.input_baru_discount.text()
        color = self.input_baru_color.text()

        is_empty = name == "" or merk == "" or buy_price == "" or sell_price == "" or discount == "" or color == ""

        if is_empty:
            self.showWarning("Form tidak boleh kosong")
        else:
            buy_price = int(self.input_baru_buy_price.text())
            sell_price = int(self.input_baru_sell_price.text())
            discount = int(self.input_baru_discount.text())

            if len(self.df_produk) == 0:
                new_id = 1
            else:
                new_id = int(self.df_produk.iloc[-1]["id"] + 1)

            new_row = [new_id, name, merk, buy_price, sell_price, discount, color]

            self.df_produk.loc[len(self.df_produk)] = new_row
            self.clearForm()
            self.df_produk.to_csv("data/produk.csv", index=False)
            self.initTable()

    def hapusProduk(self):
        if len(self.tableView.selectedIndexes()) > 0:
            rows = sorted(set(index.row() for index in self.tableView.selectedIndexes()))
            row = rows[0]

            self.df_produk = self.df_produk.drop(self.df_produk.index[row])
            self.df_produk.to_csv("data/produk.csv", index=False)
            self.initTable()

    def ubahProduk(self):
        if len(self.tableView.selectedIndexes()) > 0:
            rows = sorted(set(index.row() for index in self.tableView.selectedIndexes()))
            row = rows[0]
            data = self.df_produk.loc[row]

            self.edit_produk = EditProduk()
            self.edit_produk.input_edit_row.setHidden(True)
            self.edit_produk.input_edit_row.setText(str(row))

            self.edit_produk.input_edit_name.setText(data["name"])
            self.edit_produk.input_edit_merk.setText(data["merk"])
            self.edit_produk.input_edit_sell_price.setText(str(data["sell_price"]))
            self.edit_produk.input_edit_discount.setText(str(data["discount"]))
            self.edit_produk.input_edit_color.setText(data["color"])

            self.edit_produk.submitClicked.connect(self.initTable)
            self.edit_produk.displayInfo()

    def stokProduk(self):
        if len(self.tableView.selectedIndexes()) > 0:
            rows = sorted(set(index.row() for index in self.tableView.selectedIndexes()))
            row = rows[0]
            data = self.df_produk.loc[row]
            self.sizeProduk = SizeProduk(data[0])
            self.sizeProduk.show()
            self.sizeProduk.makeRestock.connect(self.makeTransactions.emit("ok"))

    def showWarning(self, message):
        self.warning = Warning(message)
        self.warning.show()
