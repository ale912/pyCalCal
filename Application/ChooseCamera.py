__author__ = 'Алексей Галкин'

from PyQt5.QtWidgets import QDialog, QCheckBox, QPushButton, QVBoxLayout
from PyQt5.Qt import Qt

class ChooseCamera(QDialog):
    def __init__(self, cameras,parent=None):
        QDialog.__init__(self, parent, Qt.WindowTitleHint)

        self.checks = []
        layout = QVBoxLayout()
        for cam in sorted(cameras):
            check = QCheckBox(cam)
            check.setChecked(True)
            self.checks.append(check)
            layout.addWidget(check)
        button = QPushButton('Выбрать')
        button.clicked.connect(self.click)
        layout.addWidget(button)

        self.setLayout(layout)

        self.setMinimumSize(200,200)
        self.setWindowTitle('Камеры')

        self.cameras = []

    def click(self):
        self.cameras = [c.text() for c in self.checks if c.isChecked()]
        self.close()