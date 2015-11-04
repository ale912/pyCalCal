__author__ = 'Алексей Галкин'

import shelve
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton, QInputDialog, QLineEdit, \
    QMessageBox, QLabel
from Source.CameraTable import CameraTable
from Source.MainWidget import Data

path_lovdat = 'data/lovdat'


class CameraEdit(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.oldIndexCamera = 0
        self.nameLabel = QLabel('Название:')
        self.cameraViewComboBox = QComboBox()
        self.cameraViewComboBox.currentIndexChanged.connect(self.change_camera)
        self.addCameraButton = QPushButton('Добавить камеру')
        self.addCameraButton.clicked.connect(self.addcamera_click)
        self.deleteCameraButton = QPushButton('Удалить камеру')
        self.deleteCameraButton.clicked.connect(self.deletecamera_click)

        layout0 = QHBoxLayout()
        layout0.addWidget(self.nameLabel)
        layout0.addWidget(self.cameraViewComboBox)
        layout0.addWidget(self.addCameraButton)
        layout0.addWidget(self.deleteCameraButton)

        self.cameraTable = CameraTable()
        self.addRowButton = QPushButton('Добавить строку')
        self.addRowButton.clicked.connect(self.addrow_click)
        self.deleteRowButton = QPushButton('Удалить строку')
        self.deleteRowButton.clicked.connect(self.deleterow_click)

        layout1 = QVBoxLayout()
        layout1.addLayout(layout0)
        layout1.addWidget(self.cameraTable)
        layout1.addWidget(self.addRowButton)
        layout1.addWidget(self.deleteRowButton)

        self.setLayout(layout1)

        self.setWindowTitle('Камеры')

        self.setMinimumSize(500, 500)
        self.setMaximumSize(500, 500)

        self.loadcamera()

    def closeEvent(self, qcloseevent):
        self.save(self.cameraViewComboBox.currentIndex())

    def change_camera(self, index):
        self.save(self.oldIndexCamera)
        self.load(index)
        self.oldIndexCamera = index

    def addrow_click(self):
        self.cameraTable.insertRow(self.cameraTable.rowCount())

    def deleterow_click(self):
        self.cameraTable.removeRow(self.cameraTable.currentRow())

    def addcamera_click(self):
        res = QInputDialog.getText(None, 'Введите название камеры', 'Название камеры:', QLineEdit.Normal, '')
        if res[1] and res[0]:
            self.cameraViewComboBox.addItem(res[0])
            self.cameraViewComboBox.setCurrentIndex(self.cameraViewComboBox.count() - 1)
            self.cameraTable.set_data(Data([]))

    def deletecamera_click(self):
        res = QMessageBox.warning(None, 'Предупреждение!', 'Удалить данные о камере?', QMessageBox.Yes | QMessageBox.No,
                                  QMessageBox.No)
        if res == QMessageBox.Yes:
            with shelve.open(path_lovdat) as db:
                if self.cameraViewComboBox.currentText() in db:
                    del db[self.cameraViewComboBox.currentText()]
                self.cameraViewComboBox.removeItem(self.cameraViewComboBox.currentIndex())

    def save(self, index_camera):
        with shelve.open(path_lovdat) as db:
            text = self.cameraViewComboBox.itemText(index_camera)
            if text:
                data = self.cameraTable.get_data()
                if data:
                    db[text] = data

    def loadcamera(self):
        with shelve.open(path_lovdat) as db:
            for key in db.keys():
                self.cameraViewComboBox.addItem(key)
        self.load(self.cameraViewComboBox.currentIndex())

    def load(self, index_camera):
        self.cameraTable.clearContents()
        with shelve.open(path_lovdat) as db:
            text = self.cameraViewComboBox.itemText(index_camera)
            if text in db:
                data = db[text]
                if data:
                    self.cameraTable.set_data(data)
