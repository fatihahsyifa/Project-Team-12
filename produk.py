from PyQt6 import uic
from PyQt6.QtWidgets import QWidget


class Produk(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('produk.ui', self)
