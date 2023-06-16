import pandas as pd
from PyQt6 import uic
from PyQt6.QtCore import Qt, QAbstractTableModel
from PyQt6 import QtCore as Qtc
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QWidget

class PandasModel(QAbstractTableModel):
    def __init__(self, data, keyword):
        super(PandasModel, self).__init__()
        self._data = data
        self.keyword = keyword

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


class SelectItem(QWidget):
    submitClicked = Qtc.pyqtSignal(str)
    def __init__(self, selected_id):
        super().__init__()
        self.selected_id = selected_id
        uic.loadUi('kasir_select_item.ui', self)
        self.initTable()
        self.button_tambah_item.clicked.connect(self.tambahItem)
        self.input_qty.setValidator(QIntValidator(1, 1_999_999_999, self))

    def initTable(self):
        self.df = pd.read_csv('data/size.csv')
        self.data_model = self.df[self.df["id_product"] == self.selected_id].reset_index(drop=True)
        self.model = PandasModel(self.data_model, self.selected_id)
        self.tableView.setModel(self.model)

    def tambahItem(self):
        if len(self.tableView.selectedIndexes()) > 0:
            rows = sorted(set(index.row() for index in self.tableView.selectedIndexes()))
            row = rows[0]
            data_size = self.data_model.loc[row]
            df_produk = pd.read_csv('data/produk.csv')
            data_produk = df_produk.loc[df_produk["id"] == self.selected_id].iloc[0]
            qty = self.input_qty.text()
            if qty == "":
                print("kosong")
            else:
                qty = int(self.input_qty.text())
                if qty > data_size["stok"]:
                    print("stok tidak cukup")
                else:
                    final_total_price = ((100 - data_produk["discount"]) / 100) * qty * data_produk["sell_price"]

                    new_row = [data_produk["name"],
                               data_produk["merk"],
                               data_size["size"],
                               qty,
                               data_produk["discount"],
                               data_produk["sell_price"],
                               "{:.2f}".format(final_total_price),
                               self.selected_id,
                               data_size["id"]]

                    # menyimpan ke temp item
                    df_temp_item = pd.read_csv('data/temp_item.csv')
                    df_temp_item.loc[len(df_temp_item)] = new_row
                    df_temp_item.to_csv('data/temp_item.csv', index=False)
                    # mengurangi stok
                    self.df.loc[self.df["id"] == data_size["id"], "stok"] -= qty
                    self.df.to_csv('data/size.csv', index=False)

                    self.submitClicked.emit("ok")
                    self.close()
