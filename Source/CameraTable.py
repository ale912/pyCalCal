__author__ = 'Алексей Галкин'

from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from Source.MainWidget import Data



class CameraTable(QTableWidget):
    def __init__(self, parent=None):
        QTableWidget.__init__(self, parent)

        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(['az', 'exp', 'gain'])

    def insertRow(self, p_int):
        QTableWidget.insertRow(self, p_int)
        r = p_int - 1
        if r >= 0:
            t0 = QTableWidgetItem(str(float(self.check_item(r, 0)) - 0.5))
            t1 = QTableWidgetItem(str(self.check_item(r, 1)))
            t2 = QTableWidgetItem(str(self.check_item(r, 2)))

            self.setItem(p_int, 0, t0)
            self.setItem(p_int, 1, t1)
            self.setItem(p_int, 2, t2)

    def check_item(self, r, c):
        item = self.item(r, c)
        try:
            if item.text():
                return item.text()
            else:
                return '0'
        except AttributeError:
            return '0'

    def get_data(self):
        data = Data([])
        for r in range(self.rowCount()):
            az = float(self.check_item(r, 0))
            exp = int(self.check_item(r, 1))
            gain = int(self.check_item(r, 2))
            data.append((az, exp, gain))
        return data

    def set_data(self, data):
        self.setRowCount(len(data))
        for r in range(self.rowCount()):
            t0 = QTableWidgetItem(str(data.el(r)))
            t1 = QTableWidgetItem(str(data.exp(r)))
            t2 = QTableWidgetItem(str(data.gain(r)))

            self.setItem(r, 0, t0)
            self.setItem(r, 1, t1)
            self.setItem(r, 2, t2)
        self.repaint()
