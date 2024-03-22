"""
更新日期：
2023.11.21

功能：
自定义Qt项目视图委托QStyledItemDelegate，在QStandardItem中显示自适应大小的图像
"""

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class StyledItemDelegateImage(QStyledItemDelegate):
    """自定义Qt项目视图委托QStyledItemDelegate
    在QStandardItem中显示自适应大小的图像（图像路径需在QStandardItem的UserRole中）
    """

    def __init__(self):
        super().__init__()

    def paint(self, painter, option, index):
        # 获取QStandardItem中的图片数据
        pixmap = index.data(Qt.UserRole)

        # 创建绘制工具
        item_rect = option.rect
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(Qt.NoBrush)

        # 缩放图片以适应QStandardItem
        scaled_pixmap = pixmap.scaled(QSize(item_rect.width(), item_rect.height()),
                                      Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # 在QStandardItem上绘制图片
        painter.drawPixmap(item_rect.x() + (item_rect.width() - scaled_pixmap.width()) / 2,
                           item_rect.y() + (item_rect.height() - scaled_pixmap.height()) / 2,
                           scaled_pixmap.width(), scaled_pixmap.height(),
                           scaled_pixmap)
