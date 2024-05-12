# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'interfaceDKvRxA.ui'
##
## Created by: Qt User Interface Compiler version 6.4.3
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QMainWindow, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

from Custom_Widgets.QCustomQPushButton import QCustomQPushButton
from Custom_Widgets.QCustomQStackedWidget import QCustomQStackedWidget
from Custom_Widgets.QCustomSlideMenu import QCustomSlideMenu
import image_rc
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1297, 782)
        icon = QIcon()
        icon.addFile(u":/newPrefix/Afbeeldingen/EEG.jpg", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet(u"*{\n"
"	background-color:transparent;\n"
"	background:none;\n"
"	padding:0;\n"
"	margin:0;\n"
"	color:#000;\n"
"	border-color: rgb(0, 0, 0);\n"
"}\n"
"\n"
"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.leftMenuContainer = QCustomSlideMenu(self.centralwidget)
        self.leftMenuContainer.setObjectName(u"leftMenuContainer")
        self.leftMenuContainer.setMaximumSize(QSize(39, 16777215))
        self.leftMenuContainer.setStyleSheet(u"*{\n"
"background-color: rgb(0, 166, 214);\n"
"border:none;\n"
"color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton{\n"
"	text-align:left;\n"
"}")
        self.verticalLayout = QVBoxLayout(self.leftMenuContainer)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 0, 0, 0)
        self.leftSubMenuContainer = QWidget(self.leftMenuContainer)
        self.leftSubMenuContainer.setObjectName(u"leftSubMenuContainer")
        self.verticalLayout_2 = QVBoxLayout(self.leftSubMenuContainer)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(self.leftSubMenuContainer)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.menuBtn = QPushButton(self.frame)
        self.menuBtn.setObjectName(u"menuBtn")
        font = QFont()
        font.setPointSize(22)
        font.setBold(True)
        self.menuBtn.setFont(font)
        icon1 = QIcon()
        icon1.addFile(u":/icons/icons/menu.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.menuBtn.setIcon(icon1)
        self.menuBtn.setIconSize(QSize(30, 30))

        self.horizontalLayout_2.addWidget(self.menuBtn)


        self.verticalLayout_2.addWidget(self.frame)

        self.frame_2 = QFrame(self.leftSubMenuContainer)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame_2)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 20, 0, 0)
        self.trainBtn = QPushButton(self.frame_2)
        self.trainBtn.setObjectName(u"trainBtn")
        font1 = QFont()
        font1.setPointSize(22)
        self.trainBtn.setFont(font1)
        self.trainBtn.setStyleSheet(u"background-color: rgb(0, 118, 194);")
        icon2 = QIcon()
        icon2.addFile(u":/icons/icons/sliders.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.trainBtn.setIcon(icon2)
        self.trainBtn.setIconSize(QSize(30, 30))

        self.verticalLayout_4.addWidget(self.trainBtn)

        self.testBtn = QPushButton(self.frame_2)
        self.testBtn.setObjectName(u"testBtn")
        self.testBtn.setFont(font1)
        self.testBtn.setStyleSheet(u"")
        icon3 = QIcon()
        icon3.addFile(u":/icons/icons/target.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.testBtn.setIcon(icon3)
        self.testBtn.setIconSize(QSize(30, 30))

        self.verticalLayout_4.addWidget(self.testBtn)

        self.usersBtn = QPushButton(self.frame_2)
        self.usersBtn.setObjectName(u"usersBtn")
        self.usersBtn.setFont(font1)
        icon4 = QIcon()
        icon4.addFile(u":/icons/icons/users.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.usersBtn.setIcon(icon4)
        self.usersBtn.setIconSize(QSize(30, 30))

        self.verticalLayout_4.addWidget(self.usersBtn)


        self.verticalLayout_2.addWidget(self.frame_2, 0, Qt.AlignTop)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.frame_3 = QFrame(self.leftSubMenuContainer)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame_3)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 10, 0, 10)
        self.infoBtn = QPushButton(self.frame_3)
        self.infoBtn.setObjectName(u"infoBtn")
        self.infoBtn.setFont(font1)
        icon5 = QIcon()
        icon5.addFile(u":/icons/icons/info.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.infoBtn.setIcon(icon5)
        self.infoBtn.setIconSize(QSize(30, 30))

        self.verticalLayout_5.addWidget(self.infoBtn)

        self.exitBtn = QPushButton(self.frame_3)
        self.exitBtn.setObjectName(u"exitBtn")
        self.exitBtn.setFont(font1)
        icon6 = QIcon()
        icon6.addFile(u":/icons/icons/x-circle.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.exitBtn.setIcon(icon6)
        self.exitBtn.setIconSize(QSize(30, 30))

        self.verticalLayout_5.addWidget(self.exitBtn)


        self.verticalLayout_2.addWidget(self.frame_3)


        self.verticalLayout.addWidget(self.leftSubMenuContainer)


        self.horizontalLayout.addWidget(self.leftMenuContainer, 0, Qt.AlignLeft)

        self.mainPages = QCustomQStackedWidget(self.centralwidget)
        self.mainPages.setObjectName(u"mainPages")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mainPages.sizePolicy().hasHeightForWidth())
        self.mainPages.setSizePolicy(sizePolicy)
        self.mainPages.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.mainBodyContainerTest = QWidget()
        self.mainBodyContainerTest.setObjectName(u"mainBodyContainerTest")
        self.mainBodyContainerTest.setStyleSheet(u"")
        self.gridLayout = QGridLayout(self.mainBodyContainerTest)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(-1, -1, -1, 9)
        self.userIDTest = QWidget(self.mainBodyContainerTest)
        self.userIDTest.setObjectName(u"userIDTest")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.userIDTest.sizePolicy().hasHeightForWidth())
        self.userIDTest.setSizePolicy(sizePolicy1)
        self.userIDTest.setMaximumSize(QSize(16777215, 70))
        self.userIDTest.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(0, 166, 214);\n"
"border:none;")
        self.verticalLayout_7 = QVBoxLayout(self.userIDTest)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.userID_test = QLineEdit(self.userIDTest)
        self.userID_test.setObjectName(u"userID_test")
        font2 = QFont()
        font2.setPointSize(28)
        font2.setBold(True)
        self.userID_test.setFont(font2)
        self.userID_test.setAlignment(Qt.AlignCenter)

        self.verticalLayout_7.addWidget(self.userID_test)


        self.gridLayout.addWidget(self.userIDTest, 0, 0, 1, 2)

        self.leftBodyFrameTest = QWidget(self.mainBodyContainerTest)
        self.leftBodyFrameTest.setObjectName(u"leftBodyFrameTest")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(50)
        sizePolicy2.setVerticalStretch(95)
        sizePolicy2.setHeightForWidth(self.leftBodyFrameTest.sizePolicy().hasHeightForWidth())
        self.leftBodyFrameTest.setSizePolicy(sizePolicy2)
        self.verticalLayout_3 = QVBoxLayout(self.leftBodyFrameTest)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.frame_4 = QFrame(self.leftBodyFrameTest)
        self.frame_4.setObjectName(u"frame_4")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(10)
        sizePolicy3.setHeightForWidth(self.frame_4.sizePolicy().hasHeightForWidth())
        self.frame_4.setSizePolicy(sizePolicy3)
        self.frame_4.setStyleSheet(u"background-color: rgb(0, 0, 0);\n"
"border:none;")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_4)
        self.horizontalLayout_3.setSpacing(3)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(3, 3, 3, 3)
        self.lineEdit_2 = QLineEdit(self.frame_4)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        sizePolicy4 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy4.setHorizontalStretch(25)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.lineEdit_2.sizePolicy().hasHeightForWidth())
        self.lineEdit_2.setSizePolicy(sizePolicy4)
        font3 = QFont()
        font3.setPointSize(24)
        self.lineEdit_2.setFont(font3)
        self.lineEdit_2.setCursor(QCursor(Qt.ArrowCursor))
        self.lineEdit_2.setStyleSheet(u"background-color: rgb(53, 227, 0);")
        self.lineEdit_2.setAlignment(Qt.AlignCenter)
        self.lineEdit_2.setReadOnly(True)

        self.horizontalLayout_3.addWidget(self.lineEdit_2)

        self.lineEdit_3 = QLineEdit(self.frame_4)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        sizePolicy5 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy5.setHorizontalStretch(50)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.lineEdit_3.sizePolicy().hasHeightForWidth())
        self.lineEdit_3.setSizePolicy(sizePolicy5)
        self.lineEdit_3.setFont(font3)
        self.lineEdit_3.setCursor(QCursor(Qt.ArrowCursor))
        self.lineEdit_3.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.lineEdit_3.setAlignment(Qt.AlignCenter)
        self.lineEdit_3.setReadOnly(True)

        self.horizontalLayout_3.addWidget(self.lineEdit_3)

        self.lineEdit_4 = QLineEdit(self.frame_4)
        self.lineEdit_4.setObjectName(u"lineEdit_4")
        sizePolicy4.setHeightForWidth(self.lineEdit_4.sizePolicy().hasHeightForWidth())
        self.lineEdit_4.setSizePolicy(sizePolicy4)
        self.lineEdit_4.setFont(font3)
        self.lineEdit_4.setCursor(QCursor(Qt.ArrowCursor))
        self.lineEdit_4.setStyleSheet(u"background-color: rgb(209, 0, 0);")
        self.lineEdit_4.setAlignment(Qt.AlignCenter)
        self.lineEdit_4.setReadOnly(True)

        self.horizontalLayout_3.addWidget(self.lineEdit_4)


        self.verticalLayout_3.addWidget(self.frame_4)

        self.frame_5 = QFrame(self.leftBodyFrameTest)
        self.frame_5.setObjectName(u"frame_5")
        sizePolicy6 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(15)
        sizePolicy6.setHeightForWidth(self.frame_5.sizePolicy().hasHeightForWidth())
        self.frame_5.setSizePolicy(sizePolicy6)
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_5)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.label = QLabel(self.frame_5)
        self.label.setObjectName(u"label")
        sizePolicy7 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy7)
        font4 = QFont()
        font4.setPointSize(16)
        self.label.setFont(font4)
        self.label.setStyleSheet(u"border:none;")
        self.label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout_8.addWidget(self.label)

        self.label_2 = QLabel(self.frame_5)
        self.label_2.setObjectName(u"label_2")
        sizePolicy7.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy7)
        self.label_2.setFont(font4)
        self.label_2.setStyleSheet(u"border:none;")
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout_8.addWidget(self.label_2)


        self.horizontalLayout_4.addLayout(self.verticalLayout_8)

        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.lineEdit_5 = QLineEdit(self.frame_5)
        self.lineEdit_5.setObjectName(u"lineEdit_5")
        sizePolicy.setHeightForWidth(self.lineEdit_5.sizePolicy().hasHeightForWidth())
        self.lineEdit_5.setSizePolicy(sizePolicy)
        self.lineEdit_5.setFont(font4)
        self.lineEdit_5.setCursor(QCursor(Qt.ArrowCursor))

        self.verticalLayout_9.addWidget(self.lineEdit_5)

        self.lineEdit_6 = QLineEdit(self.frame_5)
        self.lineEdit_6.setObjectName(u"lineEdit_6")
        sizePolicy.setHeightForWidth(self.lineEdit_6.sizePolicy().hasHeightForWidth())
        self.lineEdit_6.setSizePolicy(sizePolicy)
        self.lineEdit_6.setFont(font4)
        self.lineEdit_6.setCursor(QCursor(Qt.ArrowCursor))

        self.verticalLayout_9.addWidget(self.lineEdit_6)


        self.horizontalLayout_4.addLayout(self.verticalLayout_9)

        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.label_3 = QLabel(self.frame_5)
        self.label_3.setObjectName(u"label_3")
        sizePolicy7.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy7)
        self.label_3.setFont(font4)
        self.label_3.setStyleSheet(u"border:none;")
        self.label_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout_10.addWidget(self.label_3)

        self.label_4 = QLabel(self.frame_5)
        self.label_4.setObjectName(u"label_4")
        sizePolicy7.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy7)
        self.label_4.setFont(font4)
        self.label_4.setStyleSheet(u"border:none;")
        self.label_4.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout_10.addWidget(self.label_4)


        self.horizontalLayout_4.addLayout(self.verticalLayout_10)

        self.verticalLayout_11 = QVBoxLayout()
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.lineEdit_7 = QLineEdit(self.frame_5)
        self.lineEdit_7.setObjectName(u"lineEdit_7")
        sizePolicy.setHeightForWidth(self.lineEdit_7.sizePolicy().hasHeightForWidth())
        self.lineEdit_7.setSizePolicy(sizePolicy)
        self.lineEdit_7.setFont(font4)
        self.lineEdit_7.setCursor(QCursor(Qt.ArrowCursor))

        self.verticalLayout_11.addWidget(self.lineEdit_7)

        self.lineEdit_8 = QLineEdit(self.frame_5)
        self.lineEdit_8.setObjectName(u"lineEdit_8")
        sizePolicy.setHeightForWidth(self.lineEdit_8.sizePolicy().hasHeightForWidth())
        self.lineEdit_8.setSizePolicy(sizePolicy)
        self.lineEdit_8.setFont(font4)
        self.lineEdit_8.setCursor(QCursor(Qt.ArrowCursor))

        self.verticalLayout_11.addWidget(self.lineEdit_8)


        self.horizontalLayout_4.addLayout(self.verticalLayout_11)


        self.gridLayout_2.addLayout(self.horizontalLayout_4, 0, 0, 1, 1)


        self.verticalLayout_3.addWidget(self.frame_5)

        self.frame_6 = QFrame(self.leftBodyFrameTest)
        self.frame_6.setObjectName(u"frame_6")
        sizePolicy8 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(60)
        sizePolicy8.setHeightForWidth(self.frame_6.sizePolicy().hasHeightForWidth())
        self.frame_6.setSizePolicy(sizePolicy8)
        self.frame_6.setSizeIncrement(QSize(0, 0))
        self.frame_6.setBaseSize(QSize(0, 0))
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_6)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.widget_9 = QWidget(self.frame_6)
        self.widget_9.setObjectName(u"widget_9")
        sizePolicy9 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy9.setHorizontalStretch(90)
        sizePolicy9.setVerticalStretch(0)
        sizePolicy9.setHeightForWidth(self.widget_9.sizePolicy().hasHeightForWidth())
        self.widget_9.setSizePolicy(sizePolicy9)
        self.widget_9.setStyleSheet(u"image: url(:/newPrefix/Afbeeldingen/Graph with sample points.png);")

        self.gridLayout_3.addWidget(self.widget_9, 5, 1, 1, 1)

        self.label_7 = QLabel(self.frame_6)
        self.label_7.setObjectName(u"label_7")
        sizePolicy10 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy10.setHorizontalStretch(10)
        sizePolicy10.setVerticalStretch(0)
        sizePolicy10.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy10)
        self.label_7.setFont(font4)
        self.label_7.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.label_7, 7, 0, 1, 1)

        self.widget_3 = QWidget(self.frame_6)
        self.widget_3.setObjectName(u"widget_3")
        sizePolicy9.setHeightForWidth(self.widget_3.sizePolicy().hasHeightForWidth())
        self.widget_3.setSizePolicy(sizePolicy9)
        self.widget_3.setCursor(QCursor(Qt.ArrowCursor))
        self.widget_3.setStyleSheet(u"image: url(:/newPrefix/Afbeeldingen/Graph with sample points.png);")

        self.gridLayout_3.addWidget(self.widget_3, 0, 1, 1, 1)

        self.widget_6 = QWidget(self.frame_6)
        self.widget_6.setObjectName(u"widget_6")
        sizePolicy9.setHeightForWidth(self.widget_6.sizePolicy().hasHeightForWidth())
        self.widget_6.setSizePolicy(sizePolicy9)
        self.widget_6.setStyleSheet(u"image: url(:/newPrefix/Afbeeldingen/Graph with sample points.png);")

        self.gridLayout_3.addWidget(self.widget_6, 3, 1, 1, 1)

        self.label_6 = QLabel(self.frame_6)
        self.label_6.setObjectName(u"label_6")
        sizePolicy10.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy10)
        self.label_6.setFont(font4)
        self.label_6.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.label_6, 6, 0, 1, 1)

        self.label_5 = QLabel(self.frame_6)
        self.label_5.setObjectName(u"label_5")
        sizePolicy10.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy10)
        self.label_5.setFont(font4)
        self.label_5.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.label_5, 0, 0, 1, 1)

        self.widget_5 = QWidget(self.frame_6)
        self.widget_5.setObjectName(u"widget_5")
        sizePolicy9.setHeightForWidth(self.widget_5.sizePolicy().hasHeightForWidth())
        self.widget_5.setSizePolicy(sizePolicy9)
        self.widget_5.setStyleSheet(u"image: url(:/newPrefix/Afbeeldingen/Graph with sample points.png);")

        self.gridLayout_3.addWidget(self.widget_5, 7, 1, 1, 1)

        self.widget_7 = QWidget(self.frame_6)
        self.widget_7.setObjectName(u"widget_7")
        sizePolicy9.setHeightForWidth(self.widget_7.sizePolicy().hasHeightForWidth())
        self.widget_7.setSizePolicy(sizePolicy9)
        self.widget_7.setCursor(QCursor(Qt.ArrowCursor))
        self.widget_7.setStyleSheet(u"image: url(:/newPrefix/Afbeeldingen/Graph with sample points.png);")

        self.gridLayout_3.addWidget(self.widget_7, 2, 1, 1, 1)

        self.widget_8 = QWidget(self.frame_6)
        self.widget_8.setObjectName(u"widget_8")
        sizePolicy9.setHeightForWidth(self.widget_8.sizePolicy().hasHeightForWidth())
        self.widget_8.setSizePolicy(sizePolicy9)
        self.widget_8.setStyleSheet(u"image: url(:/newPrefix/Afbeeldingen/Graph with sample points.png);")

        self.gridLayout_3.addWidget(self.widget_8, 1, 1, 1, 1)

        self.widget_4 = QWidget(self.frame_6)
        self.widget_4.setObjectName(u"widget_4")
        sizePolicy9.setHeightForWidth(self.widget_4.sizePolicy().hasHeightForWidth())
        self.widget_4.setSizePolicy(sizePolicy9)
        self.widget_4.setStyleSheet(u"image: url(:/newPrefix/Afbeeldingen/Graph with sample points.png);")

        self.gridLayout_3.addWidget(self.widget_4, 6, 1, 1, 1)

        self.widget_10 = QWidget(self.frame_6)
        self.widget_10.setObjectName(u"widget_10")
        sizePolicy9.setHeightForWidth(self.widget_10.sizePolicy().hasHeightForWidth())
        self.widget_10.setSizePolicy(sizePolicy9)
        self.widget_10.setStyleSheet(u"image: url(:/newPrefix/Afbeeldingen/Graph with sample points.png);")

        self.gridLayout_3.addWidget(self.widget_10, 4, 1, 1, 1)

        self.label_8 = QLabel(self.frame_6)
        self.label_8.setObjectName(u"label_8")
        sizePolicy10.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy10)
        self.label_8.setFont(font4)
        self.label_8.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.label_8, 1, 0, 1, 1)

        self.label_9 = QLabel(self.frame_6)
        self.label_9.setObjectName(u"label_9")
        sizePolicy10.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy10)
        self.label_9.setFont(font4)
        self.label_9.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.label_9, 2, 0, 1, 1)

        self.label_10 = QLabel(self.frame_6)
        self.label_10.setObjectName(u"label_10")
        sizePolicy10.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy10)
        self.label_10.setFont(font4)
        self.label_10.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.label_10, 3, 0, 1, 1)

        self.label_11 = QLabel(self.frame_6)
        self.label_11.setObjectName(u"label_11")
        sizePolicy10.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy10)
        self.label_11.setFont(font4)
        self.label_11.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.label_11, 4, 0, 1, 1)

        self.label_12 = QLabel(self.frame_6)
        self.label_12.setObjectName(u"label_12")
        sizePolicy10.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy10)
        self.label_12.setFont(font4)
        self.label_12.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.label_12, 5, 0, 1, 1)


        self.verticalLayout_3.addWidget(self.frame_6)


        self.gridLayout.addWidget(self.leftBodyFrameTest, 1, 0, 1, 1)

        self.rightBodyFrameTest = QWidget(self.mainBodyContainerTest)
        self.rightBodyFrameTest.setObjectName(u"rightBodyFrameTest")
        sizePolicy2.setHeightForWidth(self.rightBodyFrameTest.sizePolicy().hasHeightForWidth())
        self.rightBodyFrameTest.setSizePolicy(sizePolicy2)
        self.rightBodyFrameTest.setStyleSheet(u"border:none;")
        self.verticalLayout_6 = QVBoxLayout(self.rightBodyFrameTest)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.frame_7 = QFrame(self.rightBodyFrameTest)
        self.frame_7.setObjectName(u"frame_7")
        sizePolicy11 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy11.setHorizontalStretch(0)
        sizePolicy11.setVerticalStretch(40)
        sizePolicy11.setHeightForWidth(self.frame_7.sizePolicy().hasHeightForWidth())
        self.frame_7.setSizePolicy(sizePolicy11)
        self.frame_7.setStyleSheet(u"image: url(:/newPrefix/Afbeeldingen/Graph with sample points.png);")
        self.frame_7.setFrameShape(QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Raised)

        self.verticalLayout_6.addWidget(self.frame_7)

        self.frame_8 = QFrame(self.rightBodyFrameTest)
        self.frame_8.setObjectName(u"frame_8")
        sizePolicy11.setHeightForWidth(self.frame_8.sizePolicy().hasHeightForWidth())
        self.frame_8.setSizePolicy(sizePolicy11)
        self.frame_8.setFrameShape(QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_8)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.widget_2 = QWidget(self.frame_8)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setStyleSheet(u"image: url(:/newPrefix/Afbeeldingen/column plot.png);")

        self.gridLayout_5.addWidget(self.widget_2, 0, 0, 1, 1)


        self.verticalLayout_6.addWidget(self.frame_8)

        self.frame_9 = QFrame(self.rightBodyFrameTest)
        self.frame_9.setObjectName(u"frame_9")
        sizePolicy12 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy12.setHorizontalStretch(0)
        sizePolicy12.setVerticalStretch(20)
        sizePolicy12.setHeightForWidth(self.frame_9.sizePolicy().hasHeightForWidth())
        self.frame_9.setSizePolicy(sizePolicy12)
        self.frame_9.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.frame_9.setFrameShape(QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_9)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(3, 3, 3, 3)
        self.widget = QWidget(self.frame_9)
        self.widget.setObjectName(u"widget")
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setCursor(QCursor(Qt.ArrowCursor))
        self.widget.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"image: url(:/newPrefix/Afbeeldingen/cursor.png);")

        self.gridLayout_4.addWidget(self.widget, 0, 0, 1, 1)


        self.verticalLayout_6.addWidget(self.frame_9)


        self.gridLayout.addWidget(self.rightBodyFrameTest, 1, 1, 1, 1)

        self.mainPages.addWidget(self.mainBodyContainerTest)
        self.mainBodyContainerUsers = QWidget()
        self.mainBodyContainerUsers.setObjectName(u"mainBodyContainerUsers")
        self.mainBodyContainerUsers.setStyleSheet(u"QPushButton{text-align:left; padding:5px 15px;}")
        self.gridLayout_6 = QGridLayout(self.mainBodyContainerUsers)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(-1, -1, -1, 9)
        self.listBtns = QVBoxLayout()
        self.listBtns.setObjectName(u"listBtns")
        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.listBtns.addItem(self.verticalSpacer_2)

        self.addBtn = QPushButton(self.mainBodyContainerUsers)
        self.addBtn.setObjectName(u"addBtn")
        font5 = QFont()
        font5.setPointSize(14)
        self.addBtn.setFont(font5)
        self.addBtn.setStyleSheet(u"background-color: rgb(0, 166, 214);\n"
"color: rgb(255, 255, 255);")

        self.listBtns.addWidget(self.addBtn)

        self.editBtn = QPushButton(self.mainBodyContainerUsers)
        self.editBtn.setObjectName(u"editBtn")
        self.editBtn.setFont(font5)
        self.editBtn.setStyleSheet(u"background-color: rgb(0, 166, 214);\n"
"color: rgb(255, 255, 255);")

        self.listBtns.addWidget(self.editBtn)

        self.removeBtn = QPushButton(self.mainBodyContainerUsers)
        self.removeBtn.setObjectName(u"removeBtn")
        self.removeBtn.setFont(font5)
        self.removeBtn.setStyleSheet(u"background-color: rgb(0, 166, 214);\n"
"color: rgb(255, 255, 255);")

        self.listBtns.addWidget(self.removeBtn)

        self.upBtn = QPushButton(self.mainBodyContainerUsers)
        self.upBtn.setObjectName(u"upBtn")
        self.upBtn.setFont(font5)
        self.upBtn.setStyleSheet(u"background-color: rgb(0, 166, 214);\n"
"color: rgb(255, 255, 255);")

        self.listBtns.addWidget(self.upBtn)

        self.downBtn = QPushButton(self.mainBodyContainerUsers)
        self.downBtn.setObjectName(u"downBtn")
        self.downBtn.setFont(font5)
        self.downBtn.setStyleSheet(u"background-color: rgb(0, 166, 214);\n"
"color: rgb(255, 255, 255);")

        self.listBtns.addWidget(self.downBtn)

        self.sortBtn = QPushButton(self.mainBodyContainerUsers)
        self.sortBtn.setObjectName(u"sortBtn")
        self.sortBtn.setFont(font5)
        self.sortBtn.setStyleSheet(u"background-color: rgb(0, 166, 214);\n"
"color: rgb(255, 255, 255);")

        self.listBtns.addWidget(self.sortBtn)


        self.gridLayout_6.addLayout(self.listBtns, 1, 1, 1, 1)

        self.usersList = QListWidget(self.mainBodyContainerUsers)
        self.usersList.setObjectName(u"usersList")
        sizePolicy13 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy13.setHorizontalStretch(0)
        sizePolicy13.setVerticalStretch(90)
        sizePolicy13.setHeightForWidth(self.usersList.sizePolicy().hasHeightForWidth())
        self.usersList.setSizePolicy(sizePolicy13)
        font6 = QFont()
        font6.setPointSize(18)
        self.usersList.setFont(font6)
        self.usersList.setAutoFillBackground(False)
        self.usersList.setStyleSheet(u"background-color: rgb(232, 232, 232);")
        self.usersList.setAlternatingRowColors(True)
        self.usersList.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.usersList.setSelectionRectVisible(True)

        self.gridLayout_6.addWidget(self.usersList, 1, 0, 1, 1)

        self.usersTitle = QLineEdit(self.mainBodyContainerUsers)
        self.usersTitle.setObjectName(u"usersTitle")
        sizePolicy14 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy14.setHorizontalStretch(0)
        sizePolicy14.setVerticalStretch(10)
        sizePolicy14.setHeightForWidth(self.usersTitle.sizePolicy().hasHeightForWidth())
        self.usersTitle.setSizePolicy(sizePolicy14)
        font7 = QFont()
        font7.setPointSize(50)
        self.usersTitle.setFont(font7)
        self.usersTitle.setStyleSheet(u"border:none;\n"
"color: rgb(12, 35, 64);")
        self.usersTitle.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_6.addWidget(self.usersTitle, 0, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer, 0, 1, 1, 1)

        self.mainPages.addWidget(self.mainBodyContainerUsers)
        self.mainBodyContainerTrain = QWidget()
        self.mainBodyContainerTrain.setObjectName(u"mainBodyContainerTrain")
        self.mainBodyContainerTrain.setMinimumSize(QSize(1122, 674))
        self.mainBodyContainerTrain.setStyleSheet(u"")
        self.gridLayout_24 = QGridLayout(self.mainBodyContainerTrain)
        self.gridLayout_24.setObjectName(u"gridLayout_24")
        self.gridLayout_24.setContentsMargins(-1, -1, -1, 9)
        self.leftBodyFrameTrain = QWidget(self.mainBodyContainerTrain)
        self.leftBodyFrameTrain.setObjectName(u"leftBodyFrameTrain")
        sizePolicy2.setHeightForWidth(self.leftBodyFrameTrain.sizePolicy().hasHeightForWidth())
        self.leftBodyFrameTrain.setSizePolicy(sizePolicy2)
        self.leftBodyFrameTrain.setStyleSheet(u"")
        self.verticalLayout_38 = QVBoxLayout(self.leftBodyFrameTrain)
        self.verticalLayout_38.setSpacing(0)
        self.verticalLayout_38.setObjectName(u"verticalLayout_38")
        self.verticalLayout_38.setContentsMargins(0, 0, 0, 0)
        self.frame_34 = QFrame(self.leftBodyFrameTrain)
        self.frame_34.setObjectName(u"frame_34")
        sizePolicy3.setHeightForWidth(self.frame_34.sizePolicy().hasHeightForWidth())
        self.frame_34.setSizePolicy(sizePolicy3)
        self.frame_34.setStyleSheet(u"background-color: rgb(0, 0, 0);\n"
"border:none;")
        self.frame_34.setFrameShape(QFrame.StyledPanel)
        self.frame_34.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_11 = QHBoxLayout(self.frame_34)
        self.horizontalLayout_11.setSpacing(3)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(3, 3, 3, 3)
        self.lineEdit_35 = QLineEdit(self.frame_34)
        self.lineEdit_35.setObjectName(u"lineEdit_35")
        sizePolicy4.setHeightForWidth(self.lineEdit_35.sizePolicy().hasHeightForWidth())
        self.lineEdit_35.setSizePolicy(sizePolicy4)
        self.lineEdit_35.setFont(font3)
        self.lineEdit_35.setCursor(QCursor(Qt.ArrowCursor))
        self.lineEdit_35.setStyleSheet(u"background-color: rgb(53, 227, 0);")
        self.lineEdit_35.setAlignment(Qt.AlignCenter)
        self.lineEdit_35.setReadOnly(True)

        self.horizontalLayout_11.addWidget(self.lineEdit_35)

        self.lineEdit_36 = QLineEdit(self.frame_34)
        self.lineEdit_36.setObjectName(u"lineEdit_36")
        sizePolicy5.setHeightForWidth(self.lineEdit_36.sizePolicy().hasHeightForWidth())
        self.lineEdit_36.setSizePolicy(sizePolicy5)
        self.lineEdit_36.setFont(font3)
        self.lineEdit_36.setCursor(QCursor(Qt.ArrowCursor))
        self.lineEdit_36.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.lineEdit_36.setAlignment(Qt.AlignCenter)
        self.lineEdit_36.setReadOnly(True)

        self.horizontalLayout_11.addWidget(self.lineEdit_36)

        self.lineEdit_37 = QLineEdit(self.frame_34)
        self.lineEdit_37.setObjectName(u"lineEdit_37")
        sizePolicy4.setHeightForWidth(self.lineEdit_37.sizePolicy().hasHeightForWidth())
        self.lineEdit_37.setSizePolicy(sizePolicy4)
        self.lineEdit_37.setFont(font3)
        self.lineEdit_37.setCursor(QCursor(Qt.ArrowCursor))
        self.lineEdit_37.setStyleSheet(u"background-color: rgb(209, 0, 0);")
        self.lineEdit_37.setAlignment(Qt.AlignCenter)
        self.lineEdit_37.setReadOnly(True)

        self.horizontalLayout_11.addWidget(self.lineEdit_37)


        self.verticalLayout_38.addWidget(self.frame_34)

        self.frame_35 = QFrame(self.leftBodyFrameTrain)
        self.frame_35.setObjectName(u"frame_35")
        sizePolicy6.setHeightForWidth(self.frame_35.sizePolicy().hasHeightForWidth())
        self.frame_35.setSizePolicy(sizePolicy6)
        self.frame_35.setFrameShape(QFrame.StyledPanel)
        self.frame_35.setFrameShadow(QFrame.Raised)
        self.gridLayout_22 = QGridLayout(self.frame_35)
        self.gridLayout_22.setObjectName(u"gridLayout_22")
        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.verticalLayout_39 = QVBoxLayout()
        self.verticalLayout_39.setObjectName(u"verticalLayout_39")
        self.label_29 = QLabel(self.frame_35)
        self.label_29.setObjectName(u"label_29")
        sizePolicy7.setHeightForWidth(self.label_29.sizePolicy().hasHeightForWidth())
        self.label_29.setSizePolicy(sizePolicy7)
        self.label_29.setFont(font4)
        self.label_29.setStyleSheet(u"border:none;")
        self.label_29.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout_39.addWidget(self.label_29)

        self.label_30 = QLabel(self.frame_35)
        self.label_30.setObjectName(u"label_30")
        sizePolicy7.setHeightForWidth(self.label_30.sizePolicy().hasHeightForWidth())
        self.label_30.setSizePolicy(sizePolicy7)
        self.label_30.setFont(font4)
        self.label_30.setStyleSheet(u"border:none;")
        self.label_30.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout_39.addWidget(self.label_30)


        self.horizontalLayout_12.addLayout(self.verticalLayout_39)

        self.verticalLayout_40 = QVBoxLayout()
        self.verticalLayout_40.setObjectName(u"verticalLayout_40")
        self.lineEdit_38 = QLineEdit(self.frame_35)
        self.lineEdit_38.setObjectName(u"lineEdit_38")
        sizePolicy.setHeightForWidth(self.lineEdit_38.sizePolicy().hasHeightForWidth())
        self.lineEdit_38.setSizePolicy(sizePolicy)
        self.lineEdit_38.setFont(font4)
        self.lineEdit_38.setCursor(QCursor(Qt.ArrowCursor))

        self.verticalLayout_40.addWidget(self.lineEdit_38)

        self.lineEdit_39 = QLineEdit(self.frame_35)
        self.lineEdit_39.setObjectName(u"lineEdit_39")
        sizePolicy.setHeightForWidth(self.lineEdit_39.sizePolicy().hasHeightForWidth())
        self.lineEdit_39.setSizePolicy(sizePolicy)
        self.lineEdit_39.setFont(font4)
        self.lineEdit_39.setCursor(QCursor(Qt.ArrowCursor))

        self.verticalLayout_40.addWidget(self.lineEdit_39)


        self.horizontalLayout_12.addLayout(self.verticalLayout_40)

        self.verticalLayout_41 = QVBoxLayout()
        self.verticalLayout_41.setObjectName(u"verticalLayout_41")
        self.label_31 = QLabel(self.frame_35)
        self.label_31.setObjectName(u"label_31")
        sizePolicy7.setHeightForWidth(self.label_31.sizePolicy().hasHeightForWidth())
        self.label_31.setSizePolicy(sizePolicy7)
        self.label_31.setFont(font4)
        self.label_31.setStyleSheet(u"border:none;")
        self.label_31.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout_41.addWidget(self.label_31)

        self.label_32 = QLabel(self.frame_35)
        self.label_32.setObjectName(u"label_32")
        sizePolicy7.setHeightForWidth(self.label_32.sizePolicy().hasHeightForWidth())
        self.label_32.setSizePolicy(sizePolicy7)
        self.label_32.setFont(font4)
        self.label_32.setStyleSheet(u"border:none;")
        self.label_32.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout_41.addWidget(self.label_32)


        self.horizontalLayout_12.addLayout(self.verticalLayout_41)

        self.verticalLayout_42 = QVBoxLayout()
        self.verticalLayout_42.setObjectName(u"verticalLayout_42")
        self.lineEdit_40 = QLineEdit(self.frame_35)
        self.lineEdit_40.setObjectName(u"lineEdit_40")
        sizePolicy.setHeightForWidth(self.lineEdit_40.sizePolicy().hasHeightForWidth())
        self.lineEdit_40.setSizePolicy(sizePolicy)
        self.lineEdit_40.setFont(font4)
        self.lineEdit_40.setCursor(QCursor(Qt.ArrowCursor))

        self.verticalLayout_42.addWidget(self.lineEdit_40)

        self.lineEdit_41 = QLineEdit(self.frame_35)
        self.lineEdit_41.setObjectName(u"lineEdit_41")
        sizePolicy.setHeightForWidth(self.lineEdit_41.sizePolicy().hasHeightForWidth())
        self.lineEdit_41.setSizePolicy(sizePolicy)
        self.lineEdit_41.setFont(font4)
        self.lineEdit_41.setCursor(QCursor(Qt.ArrowCursor))

        self.verticalLayout_42.addWidget(self.lineEdit_41)


        self.horizontalLayout_12.addLayout(self.verticalLayout_42)


        self.gridLayout_22.addLayout(self.horizontalLayout_12, 0, 0, 1, 1)


        self.verticalLayout_38.addWidget(self.frame_35)

        self.frame_36 = QFrame(self.leftBodyFrameTrain)
        self.frame_36.setObjectName(u"frame_36")
        sizePolicy8.setHeightForWidth(self.frame_36.sizePolicy().hasHeightForWidth())
        self.frame_36.setSizePolicy(sizePolicy8)
        self.frame_36.setSizeIncrement(QSize(0, 0))
        self.frame_36.setBaseSize(QSize(0, 0))
        self.frame_36.setFrameShape(QFrame.StyledPanel)
        self.frame_36.setFrameShadow(QFrame.Raised)
        self.gridLayout_23 = QGridLayout(self.frame_36)
        self.gridLayout_23.setObjectName(u"gridLayout_23")
        self.widget_25 = QWidget(self.frame_36)
        self.widget_25.setObjectName(u"widget_25")
        sizePolicy9.setHeightForWidth(self.widget_25.sizePolicy().hasHeightForWidth())
        self.widget_25.setSizePolicy(sizePolicy9)
        self.widget_25.setCursor(QCursor(Qt.ArrowCursor))
        self.widget_25.setStyleSheet(u"image: url(:/newPrefix/Afbeeldingen/Graph with sample points.png);")

        self.gridLayout_23.addWidget(self.widget_25, 0, 1, 1, 1)

        self.label_34 = QLabel(self.frame_36)
        self.label_34.setObjectName(u"label_34")
        sizePolicy10.setHeightForWidth(self.label_34.sizePolicy().hasHeightForWidth())
        self.label_34.setSizePolicy(sizePolicy10)
        self.label_34.setFont(font4)
        self.label_34.setAlignment(Qt.AlignCenter)

        self.gridLayout_23.addWidget(self.label_34, 6, 0, 1, 1)

        self.label_39 = QLabel(self.frame_36)
        self.label_39.setObjectName(u"label_39")
        sizePolicy10.setHeightForWidth(self.label_39.sizePolicy().hasHeightForWidth())
        self.label_39.setSizePolicy(sizePolicy10)
        self.label_39.setFont(font4)
        self.label_39.setAlignment(Qt.AlignCenter)

        self.gridLayout_23.addWidget(self.label_39, 4, 0, 1, 1)

        self.label_36 = QLabel(self.frame_36)
        self.label_36.setObjectName(u"label_36")
        sizePolicy10.setHeightForWidth(self.label_36.sizePolicy().hasHeightForWidth())
        self.label_36.setSizePolicy(sizePolicy10)
        self.label_36.setFont(font4)
        self.label_36.setAlignment(Qt.AlignCenter)

        self.gridLayout_23.addWidget(self.label_36, 1, 0, 1, 1)

        self.widget_26 = QWidget(self.frame_36)
        self.widget_26.setObjectName(u"widget_26")
        sizePolicy9.setHeightForWidth(self.widget_26.sizePolicy().hasHeightForWidth())
        self.widget_26.setSizePolicy(sizePolicy9)
        self.widget_26.setStyleSheet(u"image: url(:/newPrefix/Afbeeldingen/Graph with sample points.png);")

        self.gridLayout_23.addWidget(self.widget_26, 6, 1, 1, 1)

        self.label_37 = QLabel(self.frame_36)
        self.label_37.setObjectName(u"label_37")
        sizePolicy10.setHeightForWidth(self.label_37.sizePolicy().hasHeightForWidth())
        self.label_37.setSizePolicy(sizePolicy10)
        self.label_37.setFont(font4)
        self.label_37.setAlignment(Qt.AlignCenter)

        self.gridLayout_23.addWidget(self.label_37, 2, 0, 1, 1)

        self.label_35 = QLabel(self.frame_36)
        self.label_35.setObjectName(u"label_35")
        sizePolicy10.setHeightForWidth(self.label_35.sizePolicy().hasHeightForWidth())
        self.label_35.setSizePolicy(sizePolicy10)
        self.label_35.setFont(font4)
        self.label_35.setAlignment(Qt.AlignCenter)

        self.gridLayout_23.addWidget(self.label_35, 7, 0, 1, 1)

        self.widget_28 = QWidget(self.frame_36)
        self.widget_28.setObjectName(u"widget_28")
        sizePolicy9.setHeightForWidth(self.widget_28.sizePolicy().hasHeightForWidth())
        self.widget_28.setSizePolicy(sizePolicy9)
        self.widget_28.setCursor(QCursor(Qt.ArrowCursor))
        self.widget_28.setStyleSheet(u"image: url(:/newPrefix/Afbeeldingen/Graph with sample points.png);")

        self.gridLayout_23.addWidget(self.widget_28, 1, 1, 1, 1)

        self.widget_27 = QWidget(self.frame_36)
        self.widget_27.setObjectName(u"widget_27")
        sizePolicy9.setHeightForWidth(self.widget_27.sizePolicy().hasHeightForWidth())
        self.widget_27.setSizePolicy(sizePolicy9)
        self.widget_27.setStyleSheet(u"image: url(:/newPrefix/Afbeeldingen/Graph with sample points.png);")

        self.gridLayout_23.addWidget(self.widget_27, 7, 1, 1, 1)

        self.widget_31 = QWidget(self.frame_36)
        self.widget_31.setObjectName(u"widget_31")
        sizePolicy9.setHeightForWidth(self.widget_31.sizePolicy().hasHeightForWidth())
        self.widget_31.setSizePolicy(sizePolicy9)
        self.widget_31.setStyleSheet(u"image: url(:/newPrefix/Afbeeldingen/Graph with sample points.png);")

        self.gridLayout_23.addWidget(self.widget_31, 5, 1, 1, 1)

        self.label_33 = QLabel(self.frame_36)
        self.label_33.setObjectName(u"label_33")
        sizePolicy10.setHeightForWidth(self.label_33.sizePolicy().hasHeightForWidth())
        self.label_33.setSizePolicy(sizePolicy10)
        self.label_33.setFont(font4)
        self.label_33.setAlignment(Qt.AlignCenter)

        self.gridLayout_23.addWidget(self.label_33, 0, 0, 1, 1)

        self.label_40 = QLabel(self.frame_36)
        self.label_40.setObjectName(u"label_40")
        sizePolicy10.setHeightForWidth(self.label_40.sizePolicy().hasHeightForWidth())
        self.label_40.setSizePolicy(sizePolicy10)
        self.label_40.setFont(font4)
        self.label_40.setAlignment(Qt.AlignCenter)

        self.gridLayout_23.addWidget(self.label_40, 5, 0, 1, 1)

        self.widget_30 = QWidget(self.frame_36)
        self.widget_30.setObjectName(u"widget_30")
        sizePolicy9.setHeightForWidth(self.widget_30.sizePolicy().hasHeightForWidth())
        self.widget_30.setSizePolicy(sizePolicy9)
        self.widget_30.setCursor(QCursor(Qt.ArrowCursor))
        self.widget_30.setStyleSheet(u"image: url(:/newPrefix/Afbeeldingen/Graph with sample points.png);")

        self.gridLayout_23.addWidget(self.widget_30, 2, 1, 1, 1)

        self.label_38 = QLabel(self.frame_36)
        self.label_38.setObjectName(u"label_38")
        sizePolicy10.setHeightForWidth(self.label_38.sizePolicy().hasHeightForWidth())
        self.label_38.setSizePolicy(sizePolicy10)
        self.label_38.setFont(font4)
        self.label_38.setAlignment(Qt.AlignCenter)

        self.gridLayout_23.addWidget(self.label_38, 3, 0, 1, 1)

        self.widget_29 = QWidget(self.frame_36)
        self.widget_29.setObjectName(u"widget_29")
        sizePolicy9.setHeightForWidth(self.widget_29.sizePolicy().hasHeightForWidth())
        self.widget_29.setSizePolicy(sizePolicy9)
        self.widget_29.setCursor(QCursor(Qt.ArrowCursor))
        self.widget_29.setStyleSheet(u"image: url(:/newPrefix/Afbeeldingen/Graph with sample points.png);")

        self.gridLayout_23.addWidget(self.widget_29, 3, 1, 1, 1)

        self.widget_32 = QWidget(self.frame_36)
        self.widget_32.setObjectName(u"widget_32")
        sizePolicy9.setHeightForWidth(self.widget_32.sizePolicy().hasHeightForWidth())
        self.widget_32.setSizePolicy(sizePolicy9)
        self.widget_32.setStyleSheet(u"image: url(:/newPrefix/Afbeeldingen/Graph with sample points.png);")

        self.gridLayout_23.addWidget(self.widget_32, 4, 1, 1, 1)


        self.verticalLayout_38.addWidget(self.frame_36)


        self.gridLayout_24.addWidget(self.leftBodyFrameTrain, 1, 0, 1, 1)

        self.rightBodyFrameTrain = QWidget(self.mainBodyContainerTrain)
        self.rightBodyFrameTrain.setObjectName(u"rightBodyFrameTrain")
        sizePolicy2.setHeightForWidth(self.rightBodyFrameTrain.sizePolicy().hasHeightForWidth())
        self.rightBodyFrameTrain.setSizePolicy(sizePolicy2)
        self.rightBodyFrameTrain.setStyleSheet(u"border:none;")
        self.verticalLayout_37 = QVBoxLayout(self.rightBodyFrameTrain)
        self.verticalLayout_37.setSpacing(0)
        self.verticalLayout_37.setObjectName(u"verticalLayout_37")
        self.verticalLayout_37.setContentsMargins(0, 0, 0, 0)
        self.frame_31 = QFrame(self.rightBodyFrameTrain)
        self.frame_31.setObjectName(u"frame_31")
        sizePolicy11.setHeightForWidth(self.frame_31.sizePolicy().hasHeightForWidth())
        self.frame_31.setSizePolicy(sizePolicy11)
        self.frame_31.setStyleSheet(u"image: url(:/newPrefix/Afbeeldingen/Graph with sample points.png);")
        self.frame_31.setFrameShape(QFrame.StyledPanel)
        self.frame_31.setFrameShadow(QFrame.Raised)

        self.verticalLayout_37.addWidget(self.frame_31)

        self.frame_32 = QFrame(self.rightBodyFrameTrain)
        self.frame_32.setObjectName(u"frame_32")
        sizePolicy11.setHeightForWidth(self.frame_32.sizePolicy().hasHeightForWidth())
        self.frame_32.setSizePolicy(sizePolicy11)
        self.frame_32.setFrameShape(QFrame.StyledPanel)
        self.frame_32.setFrameShadow(QFrame.Raised)
        self.gridLayout_20 = QGridLayout(self.frame_32)
        self.gridLayout_20.setObjectName(u"gridLayout_20")
        self.widget_18 = QWidget(self.frame_32)
        self.widget_18.setObjectName(u"widget_18")
        self.widget_18.setStyleSheet(u"image: url(:/newPrefix/Afbeeldingen/column plot.png);")

        self.gridLayout_20.addWidget(self.widget_18, 0, 0, 1, 1)


        self.verticalLayout_37.addWidget(self.frame_32)

        self.frame_33 = QFrame(self.rightBodyFrameTrain)
        self.frame_33.setObjectName(u"frame_33")
        sizePolicy12.setHeightForWidth(self.frame_33.sizePolicy().hasHeightForWidth())
        self.frame_33.setSizePolicy(sizePolicy12)
        self.frame_33.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.frame_33.setFrameShape(QFrame.StyledPanel)
        self.frame_33.setFrameShadow(QFrame.Raised)
        self.gridLayout_21 = QGridLayout(self.frame_33)
        self.gridLayout_21.setObjectName(u"gridLayout_21")
        self.gridLayout_21.setContentsMargins(3, 3, 3, 3)
        self.widget_24 = QWidget(self.frame_33)
        self.widget_24.setObjectName(u"widget_24")
        sizePolicy.setHeightForWidth(self.widget_24.sizePolicy().hasHeightForWidth())
        self.widget_24.setSizePolicy(sizePolicy)
        self.widget_24.setCursor(QCursor(Qt.ArrowCursor))
        self.widget_24.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.gridLayout_25 = QGridLayout(self.widget_24)
        self.gridLayout_25.setSpacing(0)
        self.gridLayout_25.setObjectName(u"gridLayout_25")
        self.gridLayout_25.setContentsMargins(0, 0, 0, 0)
        self.startTrainBtn = QCustomQPushButton(self.widget_24)
        self.startTrainBtn.setObjectName(u"startTrainBtn")
        sizePolicy.setHeightForWidth(self.startTrainBtn.sizePolicy().hasHeightForWidth())
        self.startTrainBtn.setSizePolicy(sizePolicy)
        font8 = QFont()
        font8.setPointSize(24)
        font8.setBold(True)
        self.startTrainBtn.setFont(font8)
        self.startTrainBtn.setAutoFillBackground(False)
        self.startTrainBtn.setAutoDefault(False)
        self.startTrainBtn.setFlat(False)

        self.gridLayout_25.addWidget(self.startTrainBtn, 0, 0, 1, 1)


        self.gridLayout_21.addWidget(self.widget_24, 0, 0, 1, 1)


        self.verticalLayout_37.addWidget(self.frame_33)


        self.gridLayout_24.addWidget(self.rightBodyFrameTrain, 1, 1, 1, 1)

        self.userIDTrain = QWidget(self.mainBodyContainerTrain)
        self.userIDTrain.setObjectName(u"userIDTrain")
        sizePolicy1.setHeightForWidth(self.userIDTrain.sizePolicy().hasHeightForWidth())
        self.userIDTrain.setSizePolicy(sizePolicy1)
        self.userIDTrain.setMaximumSize(QSize(16777215, 70))
        self.userIDTrain.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(0, 166, 214);\n"
"border:none;")
        self.verticalLayout_36 = QVBoxLayout(self.userIDTrain)
        self.verticalLayout_36.setSpacing(0)
        self.verticalLayout_36.setObjectName(u"verticalLayout_36")
        self.verticalLayout_36.setContentsMargins(0, 0, 0, 0)
        self.userID_train = QLineEdit(self.userIDTrain)
        self.userID_train.setObjectName(u"userID_train")
        self.userID_train.setFont(font2)
        self.userID_train.setAlignment(Qt.AlignCenter)

        self.verticalLayout_36.addWidget(self.userID_train)


        self.gridLayout_24.addWidget(self.userIDTrain, 0, 0, 1, 2)

        self.infoWidgetTrain = QCustomSlideMenu(self.mainBodyContainerTrain)
        self.infoWidgetTrain.setObjectName(u"infoWidgetTrain")
        sizePolicy15 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy15.setHorizontalStretch(0)
        sizePolicy15.setVerticalStretch(0)
        sizePolicy15.setHeightForWidth(self.infoWidgetTrain.sizePolicy().hasHeightForWidth())
        self.infoWidgetTrain.setSizePolicy(sizePolicy15)
        self.infoWidgetTrain.setStyleSheet(u"background-color: rgb(0, 184, 200);\n"
"color: rgb(255, 255, 255);")
        self.verticalLayout_12 = QVBoxLayout(self.infoWidgetTrain)
        self.verticalLayout_12.setSpacing(9)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(9, 9, 9, 9)
        self.label_13 = QLabel(self.infoWidgetTrain)
        self.label_13.setObjectName(u"label_13")
        font9 = QFont()
        font9.setPointSize(12)
        font9.setBold(True)
        self.label_13.setFont(font9)

        self.verticalLayout_12.addWidget(self.label_13)

        self.frame_10 = QFrame(self.infoWidgetTrain)
        self.frame_10.setObjectName(u"frame_10")
        sizePolicy7.setHeightForWidth(self.frame_10.sizePolicy().hasHeightForWidth())
        self.frame_10.setSizePolicy(sizePolicy7)
        self.frame_10.setStyleSheet(u"")
        self.frame_10.setFrameShape(QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_10)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.label_14 = QLabel(self.frame_10)
        self.label_14.setObjectName(u"label_14")
        sizePolicy16 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy16.setHorizontalStretch(80)
        sizePolicy16.setVerticalStretch(0)
        sizePolicy16.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy16)
        font10 = QFont()
        font10.setPointSize(12)
        self.label_14.setFont(font10)

        self.horizontalLayout_5.addWidget(self.label_14)

        self.frame_11 = QFrame(self.frame_10)
        self.frame_11.setObjectName(u"frame_11")
        sizePolicy15.setHeightForWidth(self.frame_11.sizePolicy().hasHeightForWidth())
        self.frame_11.setSizePolicy(sizePolicy15)
        self.frame_11.setMinimumSize(QSize(169, 108))
        self.frame_11.setStyleSheet(u"")
        self.frame_11.setFrameShape(QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QFrame.Raised)
        self.verticalLayout_13 = QVBoxLayout(self.frame_11)
        self.verticalLayout_13.setSpacing(0)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.widget_11 = QWidget(self.frame_11)
        self.widget_11.setObjectName(u"widget_11")
        sizePolicy7.setHeightForWidth(self.widget_11.sizePolicy().hasHeightForWidth())
        self.widget_11.setSizePolicy(sizePolicy7)
        self.widget_11.setStyleSheet(u"image: url(:/newPrefix/Afbeeldingen/EEG cap.png);")

        self.verticalLayout_13.addWidget(self.widget_11)

        self.label_15 = QLabel(self.frame_11)
        self.label_15.setObjectName(u"label_15")
        font11 = QFont()
        font11.setPointSize(10)
        self.label_15.setFont(font11)

        self.verticalLayout_13.addWidget(self.label_15)


        self.horizontalLayout_5.addWidget(self.frame_11)


        self.verticalLayout_12.addWidget(self.frame_10)


        self.gridLayout_24.addWidget(self.infoWidgetTrain, 2, 0, 1, 2)

        self.mainPages.addWidget(self.mainBodyContainerTrain)

        self.horizontalLayout.addWidget(self.mainPages)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.mainPages.setCurrentIndex(2)
        self.startTrainBtn.setDefault(False)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.menuBtn.setText(QCoreApplication.translate("MainWindow", u"Menu", None))
        self.trainBtn.setText(QCoreApplication.translate("MainWindow", u"Train", None))
        self.testBtn.setText(QCoreApplication.translate("MainWindow", u"Test", None))
        self.usersBtn.setText(QCoreApplication.translate("MainWindow", u"Users", None))
        self.infoBtn.setText(QCoreApplication.translate("MainWindow", u"Info", None))
        self.exitBtn.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.userID_test.setText(QCoreApplication.translate("MainWindow", u"User ID", None))
        self.lineEdit_2.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.lineEdit_3.setText(QCoreApplication.translate("MainWindow", u"Direction", None))
        self.lineEdit_4.setText(QCoreApplication.translate("MainWindow", u"End", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"x:", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"y:", None))
        self.lineEdit_5.setText(QCoreApplication.translate("MainWindow", u"100", None))
        self.lineEdit_6.setText(QCoreApplication.translate("MainWindow", u"300", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"velocity (pixel/sec):", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"power (mW):", None))
        self.lineEdit_7.setText(QCoreApplication.translate("MainWindow", u"50", None))
        self.lineEdit_8.setText(QCoreApplication.translate("MainWindow", u"7", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Ch8", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Ch7", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Ch1", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Ch2", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Ch3", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Ch4", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Ch5", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Ch6", None))
        self.addBtn.setText(QCoreApplication.translate("MainWindow", u"ADD", None))
        self.editBtn.setText(QCoreApplication.translate("MainWindow", u"EDIT", None))
        self.removeBtn.setText(QCoreApplication.translate("MainWindow", u"REMOVE", None))
        self.upBtn.setText(QCoreApplication.translate("MainWindow", u"UP", None))
        self.downBtn.setText(QCoreApplication.translate("MainWindow", u"DOWN", None))
        self.sortBtn.setText(QCoreApplication.translate("MainWindow", u"SORT", None))
        self.usersTitle.setText(QCoreApplication.translate("MainWindow", u"Users", None))
        self.lineEdit_35.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.lineEdit_36.setText(QCoreApplication.translate("MainWindow", u"Direction", None))
        self.lineEdit_37.setText(QCoreApplication.translate("MainWindow", u"End", None))
        self.label_29.setText(QCoreApplication.translate("MainWindow", u"Batch size:", None))
        self.label_30.setText(QCoreApplication.translate("MainWindow", u"Learning rate:", None))
        self.lineEdit_38.setText(QCoreApplication.translate("MainWindow", u"1000", None))
        self.lineEdit_39.setText(QCoreApplication.translate("MainWindow", u"44100", None))
        self.label_31.setText(QCoreApplication.translate("MainWindow", u"Max iteration:", None))
        self.label_32.setText(QCoreApplication.translate("MainWindow", u"Window Length (>28)", None))
        self.lineEdit_40.setText(QCoreApplication.translate("MainWindow", u"10", None))
        self.lineEdit_41.setText(QCoreApplication.translate("MainWindow", u"1000", None))
        self.label_34.setText(QCoreApplication.translate("MainWindow", u"Ch7", None))
        self.label_39.setText(QCoreApplication.translate("MainWindow", u"Ch5", None))
        self.label_36.setText(QCoreApplication.translate("MainWindow", u"Ch2", None))
        self.label_37.setText(QCoreApplication.translate("MainWindow", u"Ch3", None))
        self.label_35.setText(QCoreApplication.translate("MainWindow", u"Ch8", None))
        self.label_33.setText(QCoreApplication.translate("MainWindow", u"Ch1", None))
        self.label_40.setText(QCoreApplication.translate("MainWindow", u"Ch6", None))
        self.label_38.setText(QCoreApplication.translate("MainWindow", u"Ch4", None))
        self.startTrainBtn.setText(QCoreApplication.translate("MainWindow", u"Start training!", None))
        self.userID_train.setText(QCoreApplication.translate("MainWindow", u"User ID", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Information", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Training page: Train the user's brain activity using the 'Start training!' button. A new window will appear\n"
" in which the user can record the brain activity according to the instruction given.\n"
" For help, click on the help button. While training, the brain waves and training values\n"
" can be seen on the main window and changed if necessary.\n"
"\n"
" Testing page: Test the user's brain commands. The resulting commands can be seen\n"
" in the bottom-right window. The brain waves and values are also displayed.\n"
"\n"
"Users page: Select the user that will train/test. Add or edit a user if necessary.", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Channel numbers with according position", None))
    # retranslateUi

