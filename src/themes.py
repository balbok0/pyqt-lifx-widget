from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QApplication, qApp
import PyQt5


from copy import deepcopy
from enum import Enum

default_palette = QPalette()
for attr in [
    "Window",
    "WindowText",
    "Base",
    "AlternateBase",
    "ToolTipBase",
    "ToolTipText",
    "Text",
    "Button",
    "ButtonText",
    "Link",
    "Highlight",
    "HighlightedText",
]:
    setattr(default_palette, attr, getattr(QPalette(), attr))

# Dark -- credits: https://gist.github.com/QuantumCD/6245215?permalink_comment_id=3619360#gistcomment-3619360
darkGray = QColor(53, 53, 53)
gray = QColor(128, 128, 128)
black = QColor(25, 25, 25)
blue = QColor(42, 130, 218)

darkPalette = QPalette()
darkPalette.setColor(QPalette.Window, darkGray)
darkPalette.setColor(QPalette.WindowText, Qt.white)
darkPalette.setColor(QPalette.Base, black)
darkPalette.setColor(QPalette.AlternateBase, darkGray)
darkPalette.setColor(QPalette.ToolTipBase, blue)
darkPalette.setColor(QPalette.ToolTipText, Qt.white)
darkPalette.setColor(QPalette.Text, Qt.white)
darkPalette.setColor(QPalette.Button, darkGray)
darkPalette.setColor(QPalette.ButtonText, Qt.white)
darkPalette.setColor(QPalette.Link, blue)
darkPalette.setColor(QPalette.Highlight, blue)
darkPalette.setColor(QPalette.HighlightedText, Qt.black)

darkPalette.setColor(QPalette.Active, QPalette.Button, gray.darker())
darkPalette.setColor(QPalette.Disabled, QPalette.ButtonText, gray)
darkPalette.setColor(QPalette.Disabled, QPalette.WindowText, gray)
darkPalette.setColor(QPalette.Disabled, QPalette.Text, gray)
darkPalette.setColor(QPalette.Disabled, QPalette.Light, darkGray)
darkPalette.setColor(QPalette.Disabled, QPalette.Button, QColor(35, 35, 35))



class Theme(Enum):
    light = QPalette()  # TODO: Make light pallete
    dark = darkPalette
