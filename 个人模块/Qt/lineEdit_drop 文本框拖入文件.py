"""
更新日期：
2023.11.21

功能：
文本框支持拖入文件或文件夹，并将其文本设置为对应路径
"""
import os

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class LineEditDrop(QLineEdit):
    """自定义QLineEdit控件
    拖入【文件夹】/【文件】到QLineEdit中，将QLineEdit的文本设置为相应的路径
    发送信号 signal_dropped(list) 所有拖入的文件夹/文件所在文件夹路径列表"""

    signal_dropped = Signal(list)

    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls:
            dirpath_list = set()
            for index in range(len(urls)):
                path = urls[index].toLocalFile()  # 获取路径
                if os.path.isdir(path):
                    dirpath = path
                else:
                    dirpath = os.path.split(path)[0]
                dirpath_list.add(dirpath)
            dirpath_list = list(dirpath_list)
            self.setText(dirpath_list[0])
            self.signal_dropped.emit(dirpath_list)
