from collections import defaultdict
from typing import Dict, List, Optional, Union
from PyQt5 import QtCore, QtGui, QtWidgets
from lifxlan import LifxLAN, Light


class SingleLightWidget(QtWidgets.QWidget):
    def __init__(self, group: str, name: str, light_handle: Light , *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.handle = light_handle
        features = self.handle.get_product_features()

        # Light Color chooser - Changes H, S, B(V)
        if features["color"]:
            self.light_chooser = QtWidgets.QColorDialog()
            self.light_chooser_button = QtWidgets.QPushButton('Color')

            # Slot
            self.light_chooser_button.clicked.connect(self.toggle_color_panel_visibility)
            self.light_chooser.currentColorChanged[QtGui.QColor].connect(self.change_color)

        # Temperature chooser - Changes (K)
        if features["temperature"]:
            self.kelvin_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)

            # Settings
            self.kelvin_slider.setMinimum(features["min_kelvin"])
            self.kelvin_slider.setMaximum(features["max_kelvin"])
            self.kelvin_slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
            self.kelvin_slider.setTickInterval(500)
            print(self.handle.get_color()[-1])
            self.kelvin_slider.setValue(self.handle.get_color()[-1])

            # Slot
            self.kelvin_slider.valueChanged.connect(
                lambda: self.change_color(kelvin=self.kelvin_slider.value())
            )

        # TODO: I think this is always on? -- Double-check
        # Power button - Turns light on or off
        self.power_on_button = QtWidgets.QPushButton(QtGui.QIcon("icons/lightbulb.png"), "")
        self.update_power_button()
        # Slot
        self.power_on_button.clicked.connect(self.change_power)

        # Layout stuff
        name_layout = QtWidgets.QVBoxLayout()
        name_layout.addWidget(QtWidgets.QLabel(f"{name}<br><small>{group}</small>"))

        layout = QtWidgets.QHBoxLayout()
        layout.addLayout(name_layout)
        if features["color"]:
            layout.addWidget(self.light_chooser_button)
        layout.addWidget(self.power_on_button)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(layout)
        if features["temperature"]:
            main_layout.addWidget(self.kelvin_slider)

        self.setLayout(main_layout)

    def toggle_color_panel_visibility(self):
        h, s, b, _ = self.handle.get_color()  # Ignore kelvin's for now

        self.light_chooser.setCurrentColor(QtGui.QColor.fromHsvF(h / 65535.0, s / 65535.0, b / 65535.0))
        self.light_chooser.setVisible(not self.light_chooser.isVisible())

    def change_color(self, color: Optional[QtGui.QColor] = None, kelvin: Optional[int] = None):
        if color is None and kelvin is None:
            return

        if color is None:
            h, s, b, _ = self.handle.get_color()
        else:
            h, s, b, _ = color.getHsvF()
            if not color.isValid():
                return

            h = int(h * 65535)
            s = int(s * 65535)
            b = int(b * 65535)

        if kelvin is None:
            kelvin = self.handle.get_color()[-1]

        if h < 0 or s < 0 or b < 0:
            return

        self.handle.set_color((h, s, b, kelvin))

    def change_power(self):
        cur_power = not bool(self.handle.get_power())
        self.handle.set_power(cur_power)
        self.update_power_button(cur_power)

    def update_power_button(self, power: bool = None):
        if power is None:
            power = bool(self.handle.get_power())
        self.power_on_button.setStyleSheet(
            f"background-color: {'yellowgreen' if power else 'tomato'};"
        )


class LightsPanel(QtWidgets.QWidget):
    def __init__(
        self,
        *args,
        **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)

        # Data handling
        self.lan = LifxLAN()
        self.lights_dict: Dict[str, Dict[str, Light]] = defaultdict(dict)
        for light in self.lan.get_lights():
            self.lights_dict[light.get_group()][light.get_label()] = light

        lights_list_layout = QtWidgets.QVBoxLayout()
        lights_list_layout.setAlignment(QtCore.Qt.AlignTop)

        self.light_widgets: Dict[str, Dict[str, SingleLightWidget]] = defaultdict(dict)
        for group_name, group in self.lights_dict.items():
            for light_name, light in group.items():
                self.light_widgets[group_name][light_name] = SingleLightWidget(group_name, light_name, light)
                lights_list_layout.addWidget(self.light_widgets[group_name][light_name])

        lights_list_area = QtWidgets.QScrollArea()
        lights_list_area.setLayout(lights_list_layout)

        # Layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(lights_list_area)
        self.setLayout(layout)
