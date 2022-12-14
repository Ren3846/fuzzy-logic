# This Python file uses the following encoding: utf-8
import sys


from PySide2.QtWidgets import QApplication
from ui.window import RentWindow


if __name__ == "__main__":
    app = QApplication([])
    widget = RentWindow()
    widget.show()
    sys.exit(app.exec_())