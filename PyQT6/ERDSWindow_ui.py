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
from PySide6.QtWidgets import (QApplication, QGraphicsView, QHBoxLayout, QMainWindow,
    QSizePolicy, QVBoxLayout, QWidget)

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
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.ERDS1 = QGraphicsView(self.centralwidget)
        self.ERDS1.setObjectName(u"ERDS1")

        self.verticalLayout.addWidget(self.ERDS1)

        self.ERDS3 = QGraphicsView(self.centralwidget)
        self.ERDS3.setObjectName(u"ERDS3")

        self.verticalLayout.addWidget(self.ERDS3)

        self.ERDS5 = QGraphicsView(self.centralwidget)
        self.ERDS5.setObjectName(u"ERDS5")

        self.verticalLayout.addWidget(self.ERDS5)

        self.ERDS7 = QGraphicsView(self.centralwidget)
        self.ERDS7.setObjectName(u"ERDS7")

        self.verticalLayout.addWidget(self.ERDS7)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.ERDS2 = QGraphicsView(self.centralwidget)
        self.ERDS2.setObjectName(u"ERDS2")

        self.verticalLayout_2.addWidget(self.ERDS2)

        self.ERDS4 = QGraphicsView(self.centralwidget)
        self.ERDS4.setObjectName(u"ERDS4")

        self.verticalLayout_2.addWidget(self.ERDS4)

        self.ERDS6 = QGraphicsView(self.centralwidget)
        self.ERDS6.setObjectName(u"ERDS6")
        self.ERDS6.setStyleSheet(u"")

        self.verticalLayout_2.addWidget(self.ERDS6)

        self.ERDS8 = QGraphicsView(self.centralwidget)
        self.ERDS8.setObjectName(u"ERDS8")

        self.verticalLayout_2.addWidget(self.ERDS8)


        self.horizontalLayout.addLayout(self.verticalLayout_2)


        self.horizontalLayout_2.addLayout(self.horizontalLayout)

        ERDSWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(ERDSWindow)

        QMetaObject.connectSlotsByName(ERDSWindow)
    # setupUi

    def retranslateUi(self, ERDSWindow):
        ERDSWindow.setWindowTitle(QCoreApplication.translate("ERDSWindow", u"MainWindow", None))
    # retranslateUi

