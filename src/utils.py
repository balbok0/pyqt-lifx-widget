from functools import lru_cache
from pathlib import Path
from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QColor, QIcon

@lru_cache(10)
def _load_icon_file(icon_name: str):
    path = Path(__file__).parent.parent / "icons" / f"{icon_name}.png"
    if not path.exists():
        raise ValueError(
            f"Given incorrect icon name. Please see valid names in folder (ignore file extensions): {path.parent}"
        )
    return QPixmap(str(path))


def load_icon(icon_name: str, color: QColor):

    pixmap = _load_icon_file(icon_name)
    colored_pixmap = QPixmap(pixmap.size())
    colored_pixmap.fill(color)
    colored_pixmap.setMask( pixmap.createMaskFromColor(Qt.transparent) )

    return QIcon(colored_pixmap)
