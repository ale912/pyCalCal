__author__ = 'Алексей Галкин'

import sys

from PyQt5.Qt import QApplication
from Application.MainWidget import MainWidget

app = QApplication(sys.argv)

w = MainWidget()

sys.exit(app.exec_())
