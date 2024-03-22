"""
更新日期：
2023.11.21

功能：
计算将一张图片显示在一个控件上时，保持图片纵横比时计算出来的控件大小
"""
from PySide6.QtCore import QSize


def calculate_resize(qsize_widget: QSize, qsize_pic: QSize) -> QSize:
    """计算将一张图片显示在一个控件上时，保持图片纵横比时计算出来的控件大小"""
    label_width = qsize_widget.width()
    label_height = qsize_widget.height()
    pic_width = qsize_pic.width()
    pic_height = qsize_pic.height()

    label_rate = label_width / label_height
    pic_rate = pic_width / pic_height

    if label_rate >= pic_rate:  # 符合则按高缩放
        resize_height = label_height
        resize_width = int(pic_width / pic_height * resize_height)
        resize_qsize = QSize(resize_width, resize_height)
    else:  # 否则按宽缩放
        resize_width = label_width
        resize_height = int(pic_height / pic_width * resize_width)
        resize_qsize = QSize(resize_width, resize_height)

    """
    后续操作示例
    pixmap = pixmap.scaled(resize_qsize, spectRatioMode=Qt.KeepAspectRatio)  # 保持纵横比
    label.setPixmap(pixmap)
    """

    return resize_qsize
