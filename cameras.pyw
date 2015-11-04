__author__ = 'Алексей Галкин'

import sys

from PyQt5.Qt import QApplication

from Source.CameraEdit import CameraEdit

app = QApplication(sys.argv)
c = CameraEdit()
c.show()
sys.exit(app.exec_())
