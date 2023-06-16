import pandas as pd
from PyQt6 import uic
from PyQt6.QtCore import Qt, QAbstractTableModel
from PyQt6.QtWidgets import QWidget


class PandasModel(QAbstractTableModel):
    def __init__(self, data, selected_id):
        super(PandasModel, self).__init__()
        self._data = data
        self.selected_id = selected_id

    def rowCount(self, index):
        return len(self._data.loc[self._data["id_transaction"] == self.selected_id])

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if index.isValid():
            if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
                value = self._data.loc[self._data["id_transaction"] == self.selected_id].iloc[index.row(), index.column()]
                return str(value)

    def headerData(self, col, orientation, role):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self._data.columns[col]


class DetailTransaksi(QWidget):
    def __init__(self, selected_id):
        super().__init__()
        self.selected_id = selected_id
        uic.loadUi('transaksi_detail.ui', self)
        self.initTable()
        self.initDetailInfo()

    def initTable(self):
        self.df_item = pd.read_csv('data/item.csv')
        self.model = PandasModel(self.df_item, self.selected_id)
        self.tableView.setModel(self.model)

    def initDetailInfo(self):
        self.df_transaksi = pd.read_csv('data/transaksi.csv')
        data = self.df_transaksi.loc[self.df_transaksi["id"] == self.selected_id].iloc[0]
        self.output_id.setText(str(data["id"]))
        self.output_total_price.setText(str(data["total_price"]))
        self.output_date.setText(str(data["date"]))
        self.output_given_money.setText(str(data["given_money"]))
        self.output_change_money.setText(str(data["change_money"]))
        self.output_operator.setText(str(data["operator"]))
