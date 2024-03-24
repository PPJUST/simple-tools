"""
更新日期：
2024.03.24

功能：
在程序中显示一个淡入淡出的置顶文本提示框
"""
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QMainWindow, QGraphicsOpacityEffect, QLabel


class TopTip(QMainWindow):
    def __init__(self, show_text: str):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)  # 无边框窗口
        self.setAttribute(Qt.WA_TranslucentBackground)  # 透明背景
        self.show()

        # 居中显示
        screen = QGuiApplication.primaryScreen().availableGeometry()
        size = self.geometry()
        x = int((screen.width() - size.width()) / 2)
        y = int((screen.height() - size.height()) / 2)
        self.move(x, y)

        # 创建label并添加到窗口中
        label = QLabel(str(show_text))
        label.setStyleSheet("font-size: 15pt; color: blue")
        self.setCentralWidget(label)

        # 淡入效果
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(500)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setEasingCurve(QEasingCurve.InOutCubic)
        self.animation.start()

        # 设置定时器结束后开始淡出
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.start_fade_out)
        self.timer.start(1000)

    def start_fade_out(self):
        # 淡出效果
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.finished.connect(self.close)
        self.animation.start()
