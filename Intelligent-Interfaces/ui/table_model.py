# This Python file uses the following encoding: utf-8
from PySide2.QtCore import Qt, QAbstractTableModel, QModelIndex
from PySide2.QtGui import QIntValidator, QColor


class TableModel(QAbstractTableModel):
    def __init__(self, data=None):
        QAbstractTableModel.__init__(self)
        self.loadData(data)


    def loadData(self, data):
        self.total_area = data[0]
        self.district_uk = data[1]
        self.room_count = data[2]
        self.subway_time = data[3]
        self.quality = data[4]
        self.estimation = data[5]
        self.price = data[6]

        self.column_count = 7
        self.row_count = len(self.total_area)


    def rowCount(self, parent=QModelIndex()):
        return self.row_count


    def columnCount(self, parent=QModelIndex()):
        return self.column_count


    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return ("Area, m2", "District", "Rooms", "Time to subway, minutes", "Quality, %", "Estimation", "Price")[section]
        else:
            return f"{section+1}"


    def data(self, index, role=Qt.DisplayRole):
        column = index.column()
        row = index.row()

        if role == Qt.DisplayRole:
            if column == 0:
                area = self.total_area[row]
                return str(int(area))
            elif column == 1:
                district = self.district_uk[row]
                return str(district)
            elif column == 2:
                rooms = self.room_count[row]
                return str(int(rooms))
            elif column == 3:
                time = self.subway_time[row]
                return str(int(time))
            elif column == 4:
                quality = self.quality[row]
                return str(int(quality))
            elif column == 5:
                estimation = self.estimation[row]
                return str(estimation)
            elif column == 6:
                price = self.price[row]
                return str(int(price))
        elif role == Qt.BackgroundRole:
            return QColor(Qt.white)
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignCenter

        return None
