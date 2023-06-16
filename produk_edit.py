import pandas as pd
from PyQt6 import uic
from PyQt6 import QtCore as Qtc
from PyQt6.QtWidgets import QWidget

from warning import Warning

class EditProduk(QWidget):
    submitClicked = Qtc.pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('produk_edit.ui', self)
        self.df = pd.read_csv('data/produk.csv')
        self.button_edit_produk.clicked.connect(self.saveProduk)

    def displayInfo(self):
        self.show()

    def saveProduk(self):
        row = self.input_edit_row.text()
        data = self.df.loc[int(row)]
        name = self.input_edit_name.text()
        merk = self.input_edit_merk.text()
        sell_price = self.input_edit_sell_price.text()
        discount = self.input_edit_discount.text()
        color = self.input_edit_color.text()

        is_empty = name == "" or merk == "" or sell_price == "" or discount == "" or color == ""

        if is_empty:
            self.showWarning("Form tidak boleh kosong")
        else:
            sell_price = int(self.input_edit_sell_price.text())
            discount = int(self.input_edit_discount.text())
            edited_row = [data["id"], name, merk, data["buy_price"], sell_price, discount, color]
            self.df.loc[int(row)] = edited_row
            self.df.to_csv("data/produk.csv", index=False)
            self.submitClicked.emit("ok")
            self.close()

    def showWarning(self, message):
        self.warning = Warning(message)
        self.warning.show()
