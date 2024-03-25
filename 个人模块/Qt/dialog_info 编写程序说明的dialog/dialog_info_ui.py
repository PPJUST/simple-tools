# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_info_dialogusukGQ.ui'
##
## Created by: Qt User Interface Compiler version 6.1.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore


class Ui_dialog(object):
    def setupUi(self, dialog):
        if not dialog.objectName():
            dialog.setObjectName(u"dialog")
        dialog.resize(519, 339)
        self.verticalLayout_5 = QVBoxLayout(dialog)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.stackedWidget_show = QStackedWidget(dialog)
        self.stackedWidget_show.setObjectName(u"stackedWidget_show")
        self.info = QWidget()
        self.info.setObjectName(u"info")
        self.verticalLayout = QVBoxLayout(self.info)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.textBrowser = QTextBrowser(self.info)
        self.textBrowser.setObjectName(u"textBrowser")

        self.verticalLayout.addWidget(self.textBrowser)

        self.stackedWidget_show.addWidget(self.info)

        self.verticalLayout_5.addWidget(self.stackedWidget_show)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.toolButton_previous = QToolButton(dialog)
        self.toolButton_previous.setObjectName(u"toolButton_previous")

        self.horizontalLayout.addWidget(self.toolButton_previous)

        self.toolButton_next = QToolButton(dialog)
        self.toolButton_next.setObjectName(u"toolButton_next")

        self.horizontalLayout.addWidget(self.toolButton_next)

        self.label_current_page = QLabel(dialog)
        self.label_current_page.setObjectName(u"label_current_page")

        self.horizontalLayout.addWidget(self.label_current_page)

        self.label = QLabel(dialog)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.label_max_page = QLabel(dialog)
        self.label_max_page.setObjectName(u"label_max_page")

        self.horizontalLayout.addWidget(self.label_max_page)

        self.label_3 = QLabel(dialog)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout.addWidget(self.label_3)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout_5.addLayout(self.horizontalLayout)


        self.retranslateUi(dialog)

        self.stackedWidget_show.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(dialog)
    # setupUi

    def retranslateUi(self, dialog):
        dialog.setWindowTitle(QCoreApplication.translate("dialog", u"\u8bf4\u660e", None))
        self.textBrowser.setHtml(QCoreApplication.translate("dialog", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'\u5fae\u8f6f\u96c5\u9ed1'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u8bf4\u660e</p></body></html>", None))
        self.toolButton_previous.setText(QCoreApplication.translate("dialog", u"<", None))
        self.toolButton_next.setText(QCoreApplication.translate("dialog", u">", None))
        self.label_current_page.setText(QCoreApplication.translate("dialog", u"1", None))
        self.label.setText(QCoreApplication.translate("dialog", u"/", None))
        self.label_max_page.setText(QCoreApplication.translate("dialog", u"1", None))
        self.label_3.setText(QCoreApplication.translate("dialog", u"\u9875", None))
    # retranslateUi

