# 说明、教程的dialog控件
"""
更新日期：
2024.03.25

功能：
用于编写说明的dialog控件，可以插入图片页，自带切页功能
"""
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QDialog, QWidget, QVBoxLayout, QLabel

from dialog_info_ui import Ui_dialog


class DialogInfo(QDialog):
    """编写教程的dialog控件"""

    def __init__(self):
        super().__init__()
        self.ui = Ui_dialog()
        self.ui.setupUi(self)

        self.ui.textBrowser.setOpenExternalLinks(True)  # 设置允许打开外部链接

        # 设置槽函数
        self.ui.toolButton_next.clicked.connect(lambda: self._to_page(1))
        self.ui.toolButton_previous.clicked.connect(lambda: self._to_page(-1))

    def _to_page(self, index):
        """切页"""
        page_index = self.ui.stackedWidget_show.currentIndex() + index
        max_page = self.ui.stackedWidget_show.count()
        if page_index >= max_page:
            page_index = 0
        if page_index < 0:
            page_index = max_page - 1

        self.ui.stackedWidget_show.setCurrentIndex(page_index)
        self.ui.label_current_page.setText(str(page_index + 1))

    def add_information(self, info: str):
        """添加文本信息"""
        self.ui.textBrowser.setText(info)

    def add_image_page(self, image_file):
        """插入图片页"""
        new_page = QWidget()
        layout = QVBoxLayout()

        label = QLabel()
        pixmap = QPixmap(image_file)
        label.setPixmap(pixmap)

        layout.addWidget(label)
        new_page.setLayout(layout)

        self.ui.stackedWidget_show.addWidget(new_page)

        self.ui.label_max_page.setText(str(self.ui.stackedWidget_show.count()))
