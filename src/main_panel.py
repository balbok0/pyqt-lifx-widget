from single_light_widget import SingleLightWidget
from utils import load_icon
from themes import Theme

from collections import defaultdict
import time
from typing import Dict, Optional

from PyQt5.QtGui import QPalette
from PyQt5.QtCore import (
    Qt,
    QEvent,
    QTimer,
)
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QSystemTrayIcon,
    QScrollArea,
    QMenu,
)

from lifxlan import LifxLAN, Light


class MainPanel(QWidget):
    def __init__(
        self,
        *args,
        **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)

        # Close through tray
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)

        self.title = "LifX Control"
        self.setWindowTitle(self.title)
        self.setWindowIcon(load_icon("lightbulb", self.palette().windowText().color()))

        # Tray icon
        self.tray_icon = self.create_system_tray_icon(self.title, self.palette())

        # Timestamp for hide/show action
        self.last_change_timestamp = 0.0

        # Slot
        self.tray_icon.activated.connect(self.toggle_visibility)

        # Data handling
        self.lan = LifxLAN()
        self.lights_dict: Dict[str, Dict[str, Light]] = defaultdict(dict)
        for light in self.lan.get_lights():
            self.lights_dict[light.get_group()][light.get_label()] = light

        lights_list_layout = QVBoxLayout()
        lights_list_layout.setAlignment(Qt.AlignTop)

        self.light_widgets: Dict[str, Dict[str, SingleLightWidget]] = defaultdict(dict)
        for group_name, group in self.lights_dict.items():
            for light_name, light in group.items():
                self.light_widgets[group_name][light_name] = SingleLightWidget(group_name, light_name, light)
                lights_list_layout.addWidget(self.light_widgets[group_name][light_name])

        lights_list_area = QScrollArea()
        lights_list_area.setLayout(lights_list_layout)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(lights_list_area)
        self.setLayout(layout)

    def changeEvent(self, event: QEvent):
        if event.type() == QEvent.WindowStateChange and time.time() - self.last_change_timestamp > 0.1:
            QTimer.singleShot(0, self.toggle_visibility)

    def toggle_visibility(self, activation_reason: Optional[QSystemTrayIcon.ActivationReason] = None):
        self.last_change_timestamp = time.time()
        if activation_reason is None or activation_reason == QSystemTrayIcon.Trigger:
            if self.isVisible():
                self.hide()
            else:
                state = Qt.WindowStates(Qt.WindowActive)
                state |= not Qt.WindowMinimized
                self.setWindowState(state)
                self.show()

    def create_system_tray_icon(self, title: str, palette: QPalette):
        # Create tray_icon
        tray_icon = QSystemTrayIcon(load_icon("lightbulb", palette.windowText().color()))
        tray_icon.setToolTip(title)
        tray_icon.show()

        # Create context menu
        tray_icon_menu = QMenu()
        # Theme submenu
        theme_menu = tray_icon_menu.addMenu("Theme")
        for theme in Theme:
            theme_menu.addAction(theme.name, lambda: self.setPalette(theme.value))
        tray_icon_menu.addSeparator()
        tray_icon_menu.addAction("Quit", lambda: self.close)
        tray_icon.setContextMenu(tray_icon_menu)

        return tray_icon