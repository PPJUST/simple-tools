"""
更新日期：
2024.03.24

功能：
拖入文件/文件夹至控件中（拖入时变更label图标），发送所有拖入路径的列表的信号
"""

from PySide6.QtCore import *
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import *

_ICON_DEFAULT = ''
_ICON_DROP = ''


class LabelDrop(QLabel):
    """自定义QLabel控件
    拖入【文件夹】/【文件】到QLabel中后，发送所有拖入路径的list信号
    发送信号 signal_dropped(list)"""

    signal_dropped = Signal(list)  # 发送拖入的所有路径list

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setScaledContents(True)

        self.icon = _ICON_DEFAULT
        self.last_icon = None

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
            self.last_icon = self.pixmap()
            self.setPixmap(QPixmap(_ICON_DROP))
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        self.setPixmap(QPixmap(self.last_icon))

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            drop_paths = [url.toLocalFile() for url in urls]
            self.signal_dropped.emit(drop_paths)
