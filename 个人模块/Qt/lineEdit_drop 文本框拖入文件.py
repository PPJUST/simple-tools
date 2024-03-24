"""
更新日期：
2024.03.24

功能：
文本框支持拖入文件或文件夹，并将其文本设置为对应路径（定时检查路径有效性）
"""
import os

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

_ERROR_STYLESHEET = 'border: 1px solid red;'


class LineEditDrop(QLineEdit):
    """自定义QLineEdit控件
    拖入【文件夹】/【文件】到QLineEdit中，将QLineEdit的文本设置为相应的路径
    发送信号 signal_dropped(list) 所有拖入的文件夹/文件所在文件夹路径列表"""

    signal_dropped = Signal(list)
    signal_is_exist = Signal(bool)

    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setReadOnly(True)
        self.setPlaceholderText('拖入文件到此处...')

        # 设置一个QTime定时更新检查路径有效性
        self.qtimer_check_path = QTimer()
        self.qtimer_check_path.timeout.connect(self._check_path)
        self.qtimer_check_path.setInterval(1000)
        self.qtimer_check_path.start()

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls:
            paths = []
            for index in range(len(urls)):
                path = urls[index].toLocalFile()
                paths.append(path)
            paths = list(set(paths))
            self.setText(paths[0])
            self.signal_dropped.emit(paths)

    def reset_path(self, path: str):
        """设置文本框的文本"""
        self.setText(path)
        self.setToolTip(path)
        self.signal_dropped.emit(path)

    def _check_path(self):
        """检查路径规范"""
        path = self.text()
        if path:
            is_exists = os.path.exists(path)
            self.signal_is_exist.emit(is_exists)
            if is_exists:
                self.setStyleSheet('')
            else:
                self.setStyleSheet(_ERROR_STYLESHEET)
        else:
            self.signal_is_exist.emit(False)
