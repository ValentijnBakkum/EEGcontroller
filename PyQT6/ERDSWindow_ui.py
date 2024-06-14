# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ERDSWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QMainWindow, QSizePolicy,
    QWidget)

class Ui_ERDSWindow(object):
    def setupUi(self, ERDSWindow):
        if not ERDSWindow.objectName():
            ERDSWindow.setObjectName(u"ERDSWindow")
        ERDSWindow.resize(1053, 1032)
        self.centralwidget = QWidget(ERDSWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"*{\n"
"	background-color: rgb(12, 35, 64);\n"
"}\n"
"QGraphicsView{\n"
"	background-color: rgb(255, 255, 255);\n"
"}")
        self.horizontalLayout_2 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.plotWidget = QWidget(self.centralwidget)
        self.plotWidget.setObjectName(u"plotWidget")

        self.horizontalLayout_2.addWidget(self.plotWidget)

        ERDSWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(ERDSWindow)

        QMetaObject.connectSlotsByName(ERDSWindow)
    # setupUi

    def retranslateUi(self, ERDSWindow):
        ERDSWindow.setWindowTitle(QCoreApplication.translate("ERDSWindow", u"MainWindow", None))
    # retranslateUi

