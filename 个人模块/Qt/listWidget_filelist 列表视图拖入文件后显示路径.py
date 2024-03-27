"""
更新日期：
2024.03.27

功能：
拖入文件到列表视图后，显示路径，并附带一些基本功能
"""

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class ListWidgetFolderList(QListWidget):
    """拖入文件夹列表显示控件，附带一些基本功能"""
    signal_list = Signal(list)

    def __init__(self):
        super().__init__()
        self.path_list = []

        self.setAcceptDrops(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setSpacing(3)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        path_list = []
        if urls:
            for index in range(len(urls)):
                path = urls[index].toLocalFile()
                path_list.append(path)

        self._add_item(path_list)

    def _add_item(self, path_list: list):
        """新增行项目"""
        for path in path_list:
            if path not in self.path_list:
                self.path_list.append(path)

        self._refresh_list()

    def _refresh_list(self):
        """刷新列表项目"""
        self.clear()
        for path in self.path_list:
            end_index = self.count()
            item = QListWidgetItem()
            item_widget = WidgetFolderLine()
            item_widget.set_dirpath(path)
            item_widget.signal_del.connect(self._del_item)

            self.insertItem(end_index + 1, item)
            self.setItemWidget(item, item_widget)

        self.signal_list.emit(self.path_list)

    def _del_item(self):
        """删除行项目"""
        del_item_widget = self.sender()
        # 删除全局变量中的对应数据
        for i in range(self.count()):
            item = self.item(i)
            item_widget = self.itemWidget(item)
            dirpath = item_widget.label_dirpath.toolTip()
            if del_item_widget is item_widget:
                self.path_list.remove(dirpath)
                break

        self._refresh_list()


class WidgetFolderLine(QWidget):
    """单行路径控件，用于插入至主控件中"""
    signal_del = Signal()

    def __init__(self):
        super().__init__()
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setStretch(1, 1)

        self.toolButton_del = QToolButton()
        self.toolButton_del.setText('X')
        self.toolButton_del.setStyleSheet("background-color: white; border: none;")
        self.horizontalLayout.addWidget(self.toolButton_del)

        self.label_dirpath = QLabel()
        self.label_dirpath.setText('显示路径')
        self.horizontalLayout.addWidget(self.label_dirpath)

        """连接信号与槽函数"""
        self.toolButton_del.clicked.connect(self._click_del_button)

    def set_dirpath(self, path):
        """设置文本"""
        self.label_dirpath.setText(path)
        self.label_dirpath.setToolTip(path)

    def _click_del_button(self):
        self.signal_del.emit()


def _test_widget():
    # 测试显示效果
    app = QApplication([])
    window = QWidget()
    # --------------
    test = ListWidgetFolderList()
    # -------------
    layout = QVBoxLayout()
    layout.addWidget(test)
    window.setLayout(layout)
    window.show()
    app.exec()


if __name__ == "__main__":
    _test_widget()