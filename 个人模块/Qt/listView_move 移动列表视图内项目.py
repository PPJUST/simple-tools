"""
更新日期：
2023.11.21

功能：
支持移动QListview中的行项目，并发送行项目顺序的信号
"""

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class ListViewMove(QListView):
    """自定义QListview视图
    在移动视图中的行项目后发送移动信号（顺序的所有行项目的对象list）
    需要将行项目的UserRole设置为其名称
    发送信号：signal_listview_moved(list)
    """
    signal_moved = Signal(list)

    def __init__(self):
        super().__init__()
        self.setDragDropMode(self.InternalMove)

        self.old_items = []

    def mousePressEvent(self, event):
        super(self).mousePressEvent(event)

        self.old_items = []  # 拖动前的所有行项目
        model = self.model()
        for row in range(model.rowCount()):
            index = model.index(row, 0)  # 设置索引
            item = model.itemFromIndex(index)  # 从索引中获取行项目对象
            self.old_items.append(item)

    def dropEvent(self, event):
        super(self).dropEvent(event)

        new_items = []  # 拖动后的所有行项目，会比拖动前多1，因为先新建后删除
        model = self.model()
        for row in range(model.rowCount()):
            index = model.index(row, 0)  # 设置索引
            item = model.itemFromIndex(index)  # 从索引中获取行项目对象
            new_items.append(item)
        # 删除被复制的行项目，只保留新建的行项目
        final_items = new_items.copy()
        for i in new_items:
            if i not in self.old_items:  # 找到新建的行项目
                user_role = i.data(Qt.UserRole)  # 获取新行项目的名称
                for n in final_items:
                    if n.data(Qt.UserRole) == user_role and n in self.old_items:
                        final_items.remove(n)
                        break
                break
        self.signal_moved.emit(final_items)
