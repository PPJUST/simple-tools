"""
更新日期：
2023.11.21

功能：
移动QSlider后，将QSlider坐标设置为新值，并发送新值的信号
"""

from PySide6.QtCore import *
from PySide6.QtWidgets import *


class SliderMove(QSlider):
    """自定义QSlider控件
    移动QSlider后，将QSlider坐标设置为新值，并发送新值的int信号
    发送信号 signal_move_slider(int)"""
    signal_move_slider = Signal(int)  # 发送新值的int信号

    def __init__(self):
        super().__init__()

    def mousePressEvent(self, event):
        super(self).mousePressEvent(event)
        value = QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), event.x(), self.width())
        self.setValue(value)
        self.signal_move_slider.emit(value)
