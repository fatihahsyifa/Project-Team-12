import pandas as pd
from PyQt6 import uic
from PyQt6.QtCore import Qt, QAbstractTableModel
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QWidget


class PandasModel(QAbstractTableModel):
    def __init__(self, data, selected_id):
        super(PandasModel, self).__init__()
        self._data = data
        self.selected_id = selected_id

    def rowCount(self, index):
        return len(self._data.loc[self._data["id_product"] == self.selected_id])

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if index.isValid():
            if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
                value = self._data.loc[self._data["id_product"] == self.selected_id].iloc[index.row(), index.column()]
                return str(value)

    def headerData(self, col, orientation, role):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self._data.columns[col]


class SizeProduk(QWidget):
    def __init__(self, selected_id):
        super().__init__()
        self.selected_id = selected_id
        uic.loadUi('produk_size.ui', self)
        self.initTable()

        self.input_baru_size.setValidator(QIntValidator(1, 1_999_999_999, self))
        self.input_baru_stok.setValidator(QIntValidator(1, 1_999_999_999, self))
        self.input_restock.setValidator(QIntValidator(1, 1_999_999_999, self))
        self.groupBox_restock.setVisible(False)

        self.button_tambah_size.clicked.connect(self.tambahSize)
        self.button_restock.clicked.connect(self.restock)

        df_produk = pd.read_csv('data/produk.csv')
        self.buy_price = df_produk.loc[df_produk["id"] == selected_id].iloc[0]["buy_price"]

    def initTable(self):
        self.df = pd.read_csv('data/size.csv')
        self.model = PandasModel(self.df, self.selected_id)
        self.tableView.setModel(self.model)

    def tambahSize(self):
        size = self.input_baru_size.text()
        stok = self.input_baru_stok.text()

        if size == "" or stok == "":
            print("kosong")
        elif len(self.df.loc[self.df["id_product"] == self.selected_id].loc[self.df["size"] == int(size)]) > 0:
            print("size sudah ada")
        else:
            size = int(self.input_baru_size.text())
            stok = int(self.input_baru_stok.text())

            current_saldo = int(self.getSaldo())

            if current_saldo < int(stok * self.buy_price):
                print("saldo tidak cukup")
            else:
                new_id = self.df.iloc[-1][0] + 1
                new_row = [new_id, self.selected_id, size, stok]

                self.df.loc[len(self.df)] = new_row
                self.makeTransaction(int(stok * self.buy_price))
                self.input_baru_size.clear()
                self.input_baru_stok.clear()
                self.df.to_csv("data/size.csv", index=False)
                self.initTable()

    def restock(self):
        if len(self.tableView.selectedIndexes()) > 0:
            self.groupBox_restock.setVisible(True)
            self.button_restock_save.clicked.connect(self.restockSave)

    def restockSave(self):
        if len(self.tableView.selectedIndexes()) > 0:
            rows = sorted(set(index.row() for index in self.tableView.selectedIndexes()))
            row = rows[0]
            temp_df = self.df.sort_values(by=['id_product'])
            temp_id = temp_df.loc[temp_df["id_product"] == self.selected_id].reset_index(drop=True).loc[row]["id"]
            data = self.df.loc[self.df["id"] == temp_id].iloc[0]

            added_stock = self.input_restock.text()
            if added_stock == "":
                print("kosong")
            else:
                added_stock = int(self.input_restock.text())
                current_saldo = int(self.getSaldo())

                if current_saldo < int(added_stock * self.buy_price):
                    print("saldo tidak cukup")
                else:
                    edited_row = [data["id"], data["id_product"], data["size"], int(data["stok"] + added_stock)]

                    self.df.loc[self.df["id"] == data["id"]] = edited_row
                    self.df.to_csv("data/size.csv", index=False)
                    self.makeTransaction(int(added_stock * self.buy_price))
                    self.input_restock.clear()
                    self.groupBox_restock.setVisible(False)
                    self.initTable()

    def getSaldo(self):
        df = pd.read_csv('data/keuangan.csv')
        return df["amount"].sum()

    def makeTransaction(self, amount):
        df = pd.read_csv('data/keuangan.csv')
        new_id = len(df) + 1
        new_row = [new_id, "out", 0-amount, None]
        df.loc[new_id] = new_row
        df.to_csv("data/keuangan.csv", index=False)
