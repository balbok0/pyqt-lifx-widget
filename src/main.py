from PyQt5 import QtCore, QtGui, QtWidgets
from lights_panel import LightsPanel


app = QtWidgets.QApplication([])
volume = LightsPanel()
volume.show()
app.exec_()
