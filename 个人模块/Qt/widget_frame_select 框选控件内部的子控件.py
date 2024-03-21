"""
更新日期：
2023.11.21

功能：
框选控件内部的子控件，发送所有选中子控件对象的列表信号
"""
import time

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class WidgetFrameSelect(QWidget):
    """自定义QWidget控件，在QWidget内实现框选操作，并发送框选范围内的所有内部控件对象的列表信号
    发送信号：
    signal_selected_widgets(list) 框选对象
    Signal_start_selected = Signal(str) 开始框选
    Signal_double_click = Signal(list) 双击时，选中的控件对象list
    """
    signal_selected_widgets = Signal(list)  # 发送选中的控件对象
    Signal_start_selected = Signal()  # 发送开始框选信号
    Signal_double_click = Signal(list)  # 发送双击时选中的控件对象list

    def __init__(self):
        super().__init__()
        self.last_left_click_time = 0  # 左键点击时间，用于响应双击操作
        self.widgets = []  # 所有内部控件
        self.selected_widgets = []  # 选中的控件
        self.state_is_selecting = False  # 框选状态
        self.start_pos = None  # 开始坐标
        self.end_pos = None  # 结束坐标

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:  # 左键按下的操作
            # 通过前后两次左键点击时间判断是否是双击操作
            left_click_time = time.time()  # 获取当前左键点击时间
            if left_click_time - self.last_left_click_time < 0.25:  # 设置双击时间为250毫秒
                self.Signal_double_click.emit(self.selected_widgets)  # 发送选中的控件
            self.last_left_click_time = left_click_time  # 更新上一次点击左键的时间
            # 一般单击情况下执行的操作
            self.Signal_start_selected.emit()
            self.widgets = []  # 点击左键时重置内部控件
            self.selected_widgets = []  # 点击左键时重置选中控件
            self.add_child_widgets()
            if event.button() == Qt.LeftButton:
                self.state_is_selecting = True
                self.start_pos = event.pos()
                self.end_pos = event.pos()
        if event.button() == Qt.RightButton:  # 右键按下的操作
            pass

    def mouseMoveEvent(self, event):
        if self.state_is_selecting:
            self.end_pos = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.state_is_selecting = False

            self.selected_widgets = self.get_selected_widgets()
            self.signal_selected_widgets.emit(self.selected_widgets)  # 发送获取到的控件列表

            self.widgets = []
            self.start_pos = None
            self.end_pos = None
            self.update()

    def get_selected_widgets(self):
        selected_widgets = []
        selection_rect = self.get_selection_rect()
        for widget in self.widgets:
            intersect_rect = selection_rect.intersected(widget.geometry())
            if not intersect_rect.isNull() and intersect_rect.width() >= 0 and intersect_rect.height() >= 0:
                selected_widgets.append(widget)  # 存储widget的内存对象，可以更换成widget的属性（例如widget.text()）
        return selected_widgets

    def get_selection_rect(self):
        if self.start_pos != self.end_pos:
            return QRect(self.start_pos, self.end_pos).normalized()
        else:
            return QRect(self.start_pos, self.end_pos + QPoint(1, 1)).normalized()

    def paintEvent(self, event):
        if self.state_is_selecting:
            painter = QPainter(self)
            painter.setPen(QPen(QColor(0, 0, 255), 1, Qt.DashLine))
            painter.drawRect(self.get_selection_rect())

    def add_child_widgets(self):
        for index in range(self.layout().count()):  # 将widget内的所有控件添加到全局变量中
            child_widget = self.layout().itemAt(index).widget()
            if child_widget not in self.widgets:
                self.widgets.append(child_widget)
