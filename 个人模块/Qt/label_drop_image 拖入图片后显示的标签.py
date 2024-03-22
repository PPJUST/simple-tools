"""
更新日期：
2023.11.21

功能：
拖入图片文件到QLabel，在QLabel上保持纵横比显示该图片
"""
import os

import filetype
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class LabelDropImage(QLabel):
    """自定义QLabel控件
    拖入图片文件到QLabel，在QLabel上保持纵横比显示该图片
    发送信号 signal_dropped(str)
    注意：仅支持单个图片文件路径"""
    signal_dropped = Signal(str)  # 发送获取的文件夹路径str信号

    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)  # 设置可拖入

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls:
            path = urls[0].toLocalFile()  # 获取路径
            if os.path.isfile(path) and filetype.is_image(path):
                self.setProperty('pic_path', path)
                pixmap = QPixmap(path)
                resize = self.calculate_resize(self.size(), pixmap.size())
                pixmap = pixmap.scaled(resize, spectRatioMode=Qt.KeepAspectRatio)  # 保持纵横比
                self.setPixmap(pixmap)
                self.signal_dropped.emit(path)
