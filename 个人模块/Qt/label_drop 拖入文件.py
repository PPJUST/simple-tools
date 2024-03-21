"""
更新日期：
2023.11.21

功能：
拖入文件/文件夹至控件中，发送所有拖入路径的列表的信号
"""

from PySide6.QtCore import *
from PySide6.QtWidgets import *


class LabelDrop(QLabel):
    """自定义QLabel控件
    拖入【文件夹】/【文件】到QLabel中后，发送所有拖入路径的list信号
    发送信号 signal_dropped(list)"""

    signal_dropped = Signal(list)  # 发送拖入的所有路径list

    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            drop_path_list = [url.toLocalFile() for url in urls]  # 获取多个文件的路径的列表
            self.signal_dropped.emit(drop_path_list)
