__author__ = 'Алексей Галкин'

import sys
from PyQt5.Qt import QApplication
from Application.CameraEdit import CameraEdit

import shelve
from Application.MainWidget import Data

app = QApplication(sys.argv)
c = CameraEdit()
c.show()
sys.exit(app.exec_())