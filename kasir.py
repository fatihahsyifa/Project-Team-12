import pandas as pd
from PyQt6 import QtCore as Qtc
from PyQt6 import uic
from PyQt6.QtCore import Qt, QAbstractTableModel, QDateTime
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QWidget

from kasir_select_item import SelectItem
from transaksi_detail import DetailTransaksi


class SearchModel(QAbstractTableModel):
    def __init__(self, data):
        super(SearchModel, self).__init__()
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


class ItemModel(QAbstractTableModel):
    def __init__(self, data):
        super(ItemModel, self).__init__()
        self._data = data

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1] - 2

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if index.isValid():
            if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
                value = self._data.iloc[index.row(), index.column()]
                return str(value)

    def headerData(self, col, orientation, role):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self._data.columns[col]


class Kasir(QWidget):
    createdNewTransaction = Qtc.pyqtSignal(str)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('kasir.ui', self)
        self.df_temp_user = pd.read_csv('data/temp_user.csv')

        self.button_search.clicked.connect(self.search)
        self.button_select.clicked.connect(self.select)
        self.button_hapus.clicked.connect(self.hapusItem)
        self.button_simpan_transaksi.clicked.connect(self.simpanTransaksi)

        self.input_given_money.setValidator(QIntValidator(1, 1_999_999_999, self))
        self.input_given_money.editingFinished.connect(self.setChangeMoney)

        self.initItemTable()

    def initSearchTable(self, keyword):
        self.df_search = pd.read_csv('data/produk.csv')
        df = self.df_search
        query = (df["name"].str.contains(keyword, case=False)) | (df["merk"].str.contains(keyword, case=False))
        self.searchResult = df[query].reset_index(drop=True)

        self.searchModel = SearchModel(self.searchResult)
        self.tableView_search.setModel(self.searchModel)

    def initItemTable(self):
        self.df_temp_item = pd.read_csv('data/temp_item.csv')
        self.itemModel = ItemModel(self.df_temp_item)
        self.tableView_item.setModel(self.itemModel)
        self.total_price = self.df_temp_item["total_price"].sum()
        self.output_total_price.setText(str(self.total_price))

    def search(self):
        keyword = self.input_search.text()
        if keyword != "":
            self.initSearchTable(keyword)

    def select(self):
        if len(self.tableView_search.selectedIndexes()) > 0:
            rows = sorted(set(index.row() for index in self.tableView_search.selectedIndexes()))
            row = rows[0]
            data = self.searchResult.loc[row]
            self.selectItem = SelectItem(data["id"])
            self.selectItem.submitClicked.connect(self.initItemTable)
            self.selectItem.show()

    def hapusItem(self):
        if len(self.tableView_item.selectedIndexes()) > 0:
            rows = sorted(set(index.row() for index in self.tableView_item.selectedIndexes()))
            row = rows[0]

            # mengembalikan stok
            data_size = self.df_temp_item.loc[row]
            df_size = pd.read_csv('data/size.csv')
            df_size.loc[df_size["id"] == data_size["id_size"], "stok"] += data_size["qty"]
            df_size.to_csv('data/size.csv', index=False)

            # menghapus item
            self.df_temp_item = self.df_temp_item.drop(self.df_temp_item.index[row])
            self.df_temp_item.to_csv("data/temp_item.csv", index=False)
            self.initItemTable()

    def setChangeMoney(self):
        given_money = self.input_given_money.text()
        self.output_change_money.setText(str(int(given_money) - self.total_price))

    def simpanTransaksi(self):
        total_price = self.total_price
        given_money = self.input_given_money.text()
        change_money = int(given_money) - self.total_price
        date = QDateTime.currentDateTime().toString(Qt.DateFormat.ISODate)
        operator = self.df_temp_user.loc[0, "username"]
        df_transaksi = pd.read_csv('data/transaksi.csv')

        if len(df_transaksi) == 0:
            new_id = 1
        else:
            new_id = df_transaksi.iloc[-1]["id"] + 1

        new_row = [int(new_id), total_price, given_money, change_money, date, operator]
        df_transaksi.loc[len(df_transaksi)] = new_row
        df_transaksi.to_csv("data/transaksi.csv", index=False)

        self.makeTransaction(total_price)
        self.saveItems(new_id)
        self.removeTempItem()
        self.clearForm()
        self.detailTransaksi = DetailTransaksi(new_id)
        self.detailTransaksi.show()

    def saveItems(self, id_transaksi):
        df_item = pd.read_csv('data/item.csv')
        for i in range(len(self.df_temp_item)):
            if len(df_item) == 0:
                new_id = 1
            else:
                new_id = int(df_item.iloc[-1]["id"] + 1)
            id_transaction = int(id_transaksi)
            product_name = self.df_temp_item.loc[i, "name"]
            product_merk = self.df_temp_item.loc[i, "merk"]
            product_price = self.df_temp_item.loc[i, "price"]
            product_discount = self.df_temp_item.loc[i, "discount"]
            qty = self.df_temp_item.loc[i, "qty"]
            size = self.df_temp_item.loc[i, "size"]
            total_price = self.df_temp_item.loc[i, "total_price"]
            new_row = [new_id, id_transaction, product_name, product_merk, product_price, product_discount, qty, size,
                       total_price]
            df_item.loc[len(df_item)] = new_row
            df_item.to_csv("data/item.csv", index=False)

    def removeTempItem(self):
        self.df_temp_item.drop(self.df_temp_item.index, inplace=True)
        self.df_temp_item.to_csv('data/temp_item.csv', index=False)
        self.initItemTable()

    def clearForm(self):
        self.output_total_price.setText("0")
        self.input_given_money.clear()
        self.output_change_money.setText("-")

    def makeTransaction(self, amount):
        df = pd.read_csv('data/keuangan.csv')
        new_id = len(df) + 1
        date = QDateTime.currentDateTime().toString(Qt.DateFormat.ISODate)
        operator = self.df_temp_user.loc[0, "username"]
        new_row = [new_id, "in", amount, date, operator]
        df.loc[new_id] = new_row
        df.to_csv("data/keuangan.csv", index=False)
        self.createdNewTransaction.emit("ok")
