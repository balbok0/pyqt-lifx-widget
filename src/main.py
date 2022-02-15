from PyQt5 import QtCore, QtGui, QtWidgets
from main_panel import MainPanel


app = QtWidgets.QApplication([])
volume = MainPanel()
volume.show()
app.exec_()
