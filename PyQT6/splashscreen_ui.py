# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'splashscreen.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QMainWindow,
    QProgressBar, QSizePolicy, QWidget)
import image_rc

class Ui_SplashScreen(object):
    def setupUi(self, SplashScreen):
        if not SplashScreen.objectName():
            SplashScreen.setObjectName(u"SplashScreen")
        SplashScreen.resize(690, 425)
        self.centralwidget = QWidget(SplashScreen)
        self.centralwidget.setObjectName(u"centralwidget")
        self.mainFrame = QFrame(self.centralwidget)
        self.mainFrame.setObjectName(u"mainFrame")
        self.mainFrame.setGeometry(QRect(0, 54, 500, 200))
        self.mainFrame.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:0, y1:0.273, x2:1, y2:0.711, stop:0 rgba(6, 196, 249, 255), stop:1 rgba(0, 23, 132, 255));\n"
"border-radius: 20px;\n"
"border-bottom: 5px solid rgb(68, 161, 208);\n"
"border-right: 5px solid rgb(0, 23, 131);\n"
"border-top: 5px solid rgb(68, 161, 208);\n"
"border-left: 5px solid rgb(68, 161, 208);")
        self.mainFrame.setFrameShape(QFrame.StyledPanel)
        self.mainFrame.setFrameShadow(QFrame.Raised)
        self.logoDelft = QFrame(self.mainFrame)
        self.logoDelft.setObjectName(u"logoDelft")
        self.logoDelft.setGeometry(QRect(0, 0, 181, 151))
        self.logoDelft.setStyleSheet(u"image: url(:/newPrefix/pictures/TUDelftFlame_white.png);\n"
"background-color:none;\n"
"border:none;")
        self.logoDelft.setFrameShape(QFrame.StyledPanel)
        self.logoDelft.setFrameShadow(QFrame.Raised)
        self.frame = QFrame(self.mainFrame)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(70, 10, 550, 550))
        self.frame.setStyleSheet(u"background-color:none;\n"
"border: 10px solid rgb(0, 16, 80);\n"
"border-radius:275px;")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 133, 401, 71))
        font = QFont()
        font.setFamilies([u"Copperplate Gothic Bold"])
        font.setPointSize(35)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setStyleSheet(u"border-top:none;\n"
"border-bottom:20px solid rgb(0, 16, 80);\n"
"border-left:none;\n"
"border-right:none;")
        self.label.setAlignment(Qt.AlignCenter)
        self.logoBorderFrame = QFrame(self.centralwidget)
        self.logoBorderFrame.setObjectName(u"logoBorderFrame")
        self.logoBorderFrame.setGeometry(QRect(440, 0, 250, 250))
        self.logoBorderFrame.setStyleSheet(u"border: 7px solid rgb(68, 161, 208);\n"
"border-radius: 20px;\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:0, stop:0 rgba(1, 84, 158, 237), stop:1 rgba(192, 230, 255, 255));")
        self.logoBorderFrame.setFrameShape(QFrame.StyledPanel)
        self.logoBorderFrame.setFrameShadow(QFrame.Raised)
        self.EEGFrame = QFrame(self.centralwidget)
        self.EEGFrame.setObjectName(u"EEGFrame")
        self.EEGFrame.setGeometry(QRect(440, 0, 250, 250))
        self.EEGFrame.setStyleSheet(u"image: url(:/newPrefix/pictures/EEG-removebg.png);\n"
"background-color:none;\n"
"border:none;")
        self.EEGFrame.setFrameShape(QFrame.StyledPanel)
        self.EEGFrame.setFrameShadow(QFrame.Raised)
        self.moreInfoFrame = QFrame(self.centralwidget)
        self.moreInfoFrame.setObjectName(u"moreInfoFrame")
        self.moreInfoFrame.setGeometry(QRect(1, 234, 500, 191))
        self.moreInfoFrame.setStyleSheet(u"background-color: rgb(0, 16, 80);\n"
"border-radius:20px;\n"
"border: 5px solid rgb(68, 161, 208);")
        self.moreInfoFrame.setFrameShape(QFrame.StyledPanel)
        self.moreInfoFrame.setFrameShadow(QFrame.Raised)
        self.label_2 = QLabel(self.moreInfoFrame)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(50, 40, 431, 51))
        font1 = QFont()
        font1.setFamilies([u"Rockwell Extra Bold"])
        font1.setPointSize(20)
        font1.setBold(True)
        self.label_2.setFont(font1)
        self.label_2.setStyleSheet(u"border:none;\n"
"color: rgb(255, 255, 255);")
        self.label_3 = QLabel(self.moreInfoFrame)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(300, 90, 131, 20))
        font2 = QFont()
        font2.setFamilies([u"Rockwell"])
        font2.setPointSize(16)
        font2.setBold(False)
        self.label_3.setFont(font2)
        self.label_3.setStyleSheet(u"border:none;\n"
"color: rgb(255, 255, 255);")
        self.label_4 = QLabel(self.moreInfoFrame)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(140, 160, 231, 20))
        font3 = QFont()
        font3.setFamilies([u"Arial"])
        font3.setPointSize(12)
        font3.setBold(False)
        self.label_4.setFont(font3)
        self.label_4.setStyleSheet(u"border:none;\n"
"color: rgb(154, 154, 154);")
        self.progressBar = QProgressBar(self.moreInfoFrame)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(70, 110, 0, 0))
        self.progressBar.setStyleSheet(u"border:none;")
        self.progressBar.setValue(24)
        self.progressBar.raise_()
        self.label_2.raise_()
        self.label_3.raise_()
        self.label_4.raise_()
        SplashScreen.setCentralWidget(self.centralwidget)
        self.logoBorderFrame.raise_()
        self.moreInfoFrame.raise_()
        self.mainFrame.raise_()
        self.EEGFrame.raise_()

        self.retranslateUi(SplashScreen)

        QMetaObject.connectSlotsByName(SplashScreen)
    # setupUi

    def retranslateUi(self, SplashScreen):
        SplashScreen.setWindowTitle(QCoreApplication.translate("SplashScreen", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("SplashScreen", u"WELCOME", None))
        self.label_2.setText(QCoreApplication.translate("SplashScreen", u"Initializing BCI-Desk App", None))
        self.label_3.setText(QCoreApplication.translate("SplashScreen", u"Please wait...", None))
        self.label_4.setText(QCoreApplication.translate("SplashScreen", u"Designed by Group I (TU Delft)", None))
    # retranslateUi

