from PyQt6 import uic
from PyQt6.QtWidgets import QWidget


class Warning(QWidget):
    def __init__(self, message):
        super().__init__()
        self.message = message
        print(self.message)
        uic.loadUi('warning.ui', self)
        self.label_warning.setText(str(self.message))
        self.button_close.clicked.connect(self.close)
