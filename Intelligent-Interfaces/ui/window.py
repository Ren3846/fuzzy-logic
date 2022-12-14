# This Python file uses the following encoding: utf-8
import sys
import os

from PySide2.QtWidgets import QWidget, QHeaderView, QSizePolicy, QTableView
from PySide2.QtCore import QFile, Slot, Qt, QAbstractTableModel, QModelIndex
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QIntValidator

from ui.table_model import TableModel
from ui.data_provider import DataProvider
from ui.processor import Processor


class RentWindow(QWidget):
    def __init__(self):
        super(RentWindow, self).__init__()
        self.load_ui()
        self.setWindowTitle('Rent  estimator')
        self.setFixedSize(800, 600)

        input_validator = QIntValidator()
        input_validator.setRange(1, 100)

        self.ui_widget.areaEditBox.setValidator(input_validator)
        self.ui_widget.comfortEditBox.setValidator(input_validator)
        self.ui_widget.subwayTimeEditBox.setValidator(input_validator)

        self.ui_widget.estimateButton.clicked.connect(self.estimate_click)
        self.ui_widget.filterButton.clicked.connect(self.filter_click)

        self.data_provider = DataProvider()
        self.table_model = TableModel(self.data_provider.getData())
        self.ui_widget.flatsTableView.setModel(self.table_model)
        self.ui_widget.flatsTableView.setColumnWidth(0, 80)
        self.ui_widget.flatsTableView.setColumnWidth(1, 120)
        self.ui_widget.flatsTableView.setColumnWidth(2, 60)
        self.ui_widget.flatsTableView.setColumnWidth(3, 160)
        self.ui_widget.flatsTableView.setColumnWidth(6, 80)
        self.ui_widget.flatsTableView.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.ui_widget.flatsTableView.setWordWrap(True)

        self.processor = Processor()

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.ui_widget = loader.load(ui_file, self)
        ui_file.close()

    @Slot()
    def estimate_click(self):
        area_text = self.ui_widget.areaEditBox.text()
        district_text = self.ui_widget.districtComboBox.currentText()
        rooms_text = self.ui_widget.roomComboBox.currentText()
        subway_text = self.ui_widget.subwayTimeEditBox.text()
        comfort_text = self.ui_widget.comfortEditBox.text()

        if area_text == '' or district_text == '' or rooms_text == '' or subway_text == '' or comfort_text == '':
            return

        output = self.processor.process(
            float(self.normalize_input(area_text, 100, self.ui_widget.areaEditBox)),
            district_text,
            float(rooms_text),
            float(self.normalize_input(subway_text, 60, self.ui_widget.subwayTimeEditBox)),
            float(self.normalize_input(comfort_text, 100, self.ui_widget.comfortEditBox)),
        )
        self.ui_widget.estimateResultLabel.setText(
            "Estimation result: {}   | price: {}".format(output.price_fuzz, output.price))

    @staticmethod
    def normalize_input(variable_text, max_bound, ui_component):
        if float(variable_text) > max_bound:
            ui_component.setText(str(max_bound))
            return max_bound
        else:
            return float(variable_text)

    @Slot()
    def filter_click(self):
        self.table_model = TableModel(self.data_provider.filter(self.ui_widget.filterComboBox.currentText()))
        self.ui_widget.flatsTableView.setModel(self.table_model)
