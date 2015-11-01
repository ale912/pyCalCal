__author__ = 'Алексей Галкин'

import shelve
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton, QInputDialog, QLineEdit, \
    QMessageBox, QLabel
from Application.CameraTable import CameraTable
from Application.MainWidget import Data


class CameraEdit(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.oldIndexCamera = 0
        self.nameLabel = QLabel('Название:')
        self.cameraViewComboBox = QComboBox()
        self.cameraViewComboBox.currentIndexChanged.connect(self.changeCamera)
        self.addCameraButton = QPushButton('Добавить камеру')
        self.addCameraButton.clicked.connect(self.addCamera)
        self.deleteCameraButton = QPushButton('Удалить камеру')
        self.deleteCameraButton.clicked.connect(self.delete_camera)

        layout0 = QHBoxLayout()
        layout0.addWidget(self.nameLabel)
        layout0.addWidget(self.cameraViewComboBox)
        layout0.addWidget(self.addCameraButton)
        layout0.addWidget(self.deleteCameraButton)

        self.cameraTable = CameraTable()
        self.addRow = QPushButton('Добавить строку')
        self.addRow.clicked.connect(self.addRowCameraTable)
        self.deleteRow = QPushButton('Удалить строку')
        self.deleteRow.clicked.connect(self.deleteRowCameraTable)

        layout1 = QVBoxLayout()
        layout1.addLayout(layout0)
        layout1.addWidget(self.cameraTable)
        layout1.addWidget(self.addRow)
        layout1.addWidget(self.deleteRow)

        self.setLayout(layout1)

        self.setWindowTitle('Камеры')

        self.setMinimumSize(370, 500)
        self.setMaximumSize(370, 500)

        self.load_camera()

    def closeEvent(self, QCloseEvent):
        self.save(self.cameraViewComboBox.currentIndex())

    def changeCamera(self, index):
        self.save(self.oldIndexCamera)
        self.load(index)
        self.oldIndexCamera = index

    def addRowCameraTable(self):
        self.cameraTable.insertRow(self.cameraTable.rowCount())

    def deleteRowCameraTable(self):
        self.cameraTable.removeRow(self.cameraTable.currentRow())

    def addCamera(self):
        res = QInputDialog.getText(None, 'Введите название камеры', 'Название камеры:', QLineEdit.Normal, '')
        if res[1] and res[0]:
            self.cameraViewComboBox.addItem(res[0])
            self.cameraViewComboBox.setCurrentIndex(self.cameraViewComboBox.count() - 1)
            self.cameraTable.setData(Data([]))

    def delete_camera(self):
        res = QMessageBox.warning(None, 'Предупреждение!', 'Удалить данные о камере?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if res == QMessageBox.Yes:
            with shelve.open('lovdat') as db:
                if self.cameraViewComboBox.currentText() in db:
                    del db[self.cameraViewComboBox.currentText()]
                self.cameraViewComboBox.removeItem(self.cameraViewComboBox.currentIndex())

    def save(self, index_camera):
        with shelve.open('lovdat') as db:
            text = self.cameraViewComboBox.itemText(index_camera)
            if text:
                data = self.cameraTable.getData()
                if data:
                    db[text] = data

    def load_camera(self):
        with shelve.open('lovdat') as db:
            for key in db.keys():
                self.cameraViewComboBox.addItem(key)
        self.load(self.cameraViewComboBox.currentIndex())

    def load(self, index_camera):
        self.cameraTable.clearContents()
        with shelve.open('lovdat') as db:
            text = self.cameraViewComboBox.itemText(index_camera)
            if text in db:
                data = db[text]
                if data:
                    self.cameraTable.setData(data)
