# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'interface.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QMainWindow, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

from Custom_Widgets.QCustomQStackedWidget import QCustomQStackedWidget
from Custom_Widgets.QCustomSlideMenu import QCustomSlideMenu
from pyqtgraph import (GraphicsLayoutWidget, PlotWidget)
import image_rc
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1595, 862)
        MainWindow.setMinimumSize(QSize(0, 0))
        icon = QIcon()
        icon.addFile(u":/newPrefix/pictures/EEG.jpg", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet(u"*{\n"
"	background-color:transparent;\n"
"	background:none;\n"
"	padding:0;\n"
"	margin:0;\n"
"	color:#000;\n"
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
        icon1.addFile(u":/icons/Qss/icons/menu.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.menuBtn.setIcon(icon1)
        self.menuBtn.setIconSize(QSize(30, 30))

        self.horizontalLayout_2.addWidget(self.menuBtn)


        self.verticalLayout_2.addWidget(self.frame)

        self.frame_2 = QFrame(self.leftSubMenuContainer)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setStyleSheet(u"border-radius: 10px;")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame_2)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 20, 0, 0)
        self.overviewBtn = QPushButton(self.frame_2)
        self.overviewBtn.setObjectName(u"overviewBtn")
        font1 = QFont()
        font1.setPointSize(22)
        self.overviewBtn.setFont(font1)
        self.overviewBtn.setStyleSheet(u"")
        icon2 = QIcon()
        icon2.addFile(u":/icons/Qss/icons/activity-svgrepo-com.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.overviewBtn.setIcon(icon2)
        self.overviewBtn.setIconSize(QSize(30, 30))

        self.verticalLayout_4.addWidget(self.overviewBtn)

        self.demosBtn = QPushButton(self.frame_2)
        self.demosBtn.setObjectName(u"demosBtn")
        self.demosBtn.setFont(font1)
        icon3 = QIcon()
        icon3.addFile(u":/icons/Qss/icons/console-controller-gamepad-play-svgrepo-com.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.demosBtn.setIcon(icon3)
        self.demosBtn.setIconSize(QSize(30, 30))

        self.verticalLayout_4.addWidget(self.demosBtn)

        self.usersBtn = QPushButton(self.frame_2)
        self.usersBtn.setObjectName(u"usersBtn")
        self.usersBtn.setFont(font1)
        self.usersBtn.setStyleSheet(u"background-color: rgb(0, 118, 194);")
        icon4 = QIcon()
        icon4.addFile(u":/icons/Qss/icons/users.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.usersBtn.setIcon(icon4)
        self.usersBtn.setIconSize(QSize(30, 30))

        self.verticalLayout_4.addWidget(self.usersBtn)


        self.verticalLayout_2.addWidget(self.frame_2, 0, Qt.AlignTop)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.frame_3 = QFrame(self.leftSubMenuContainer)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame_3)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 10, 0, 10)
        self.reconnectBtn = QPushButton(self.frame_3)
        self.reconnectBtn.setObjectName(u"reconnectBtn")
        self.reconnectBtn.setFont(font1)
        icon5 = QIcon()
        icon5.addFile(u":/icons/Qss/icons/download-cloud.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.reconnectBtn.setIcon(icon5)
        self.reconnectBtn.setIconSize(QSize(30, 30))

        self.verticalLayout_5.addWidget(self.reconnectBtn)

        self.infoBtn = QPushButton(self.frame_3)
        self.infoBtn.setObjectName(u"infoBtn")
        self.infoBtn.setFont(font1)
        icon6 = QIcon()
        icon6.addFile(u":/icons/Qss/icons/info.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.infoBtn.setIcon(icon6)
        self.infoBtn.setIconSize(QSize(30, 30))

        self.verticalLayout_5.addWidget(self.infoBtn)

        self.exitBtn = QPushButton(self.frame_3)
        self.exitBtn.setObjectName(u"exitBtn")
        self.exitBtn.setFont(font1)
        icon7 = QIcon()
        icon7.addFile(u":/icons/Qss/icons/x-circle.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.exitBtn.setIcon(icon7)
        self.exitBtn.setIconSize(QSize(30, 30))

        self.verticalLayout_5.addWidget(self.exitBtn)


        self.verticalLayout_2.addWidget(self.frame_3)


        self.verticalLayout.addWidget(self.leftSubMenuContainer)


        self.horizontalLayout.addWidget(self.leftMenuContainer, 0, Qt.AlignLeft)

        self.leftSubMenu = QCustomSlideMenu(self.centralwidget)
        self.leftSubMenu.setObjectName(u"leftSubMenu")
        self.leftSubMenu.setStyleSheet(u"*{\n"
"background-color: rgb(0, 118, 194);\n"
"border:none;\n"
"color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton{\n"
"	text-align:left;\n"
"}")
        self.verticalLayout_7 = QVBoxLayout(self.leftSubMenu)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.cursorBtn = QPushButton(self.leftSubMenu)
        self.cursorBtn.setObjectName(u"cursorBtn")
        self.cursorBtn.setFont(font1)
        icon8 = QIcon()
        icon8.addFile(u":/icons/Qss/icons/cursor-square-svgrepo-com.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.cursorBtn.setIcon(icon8)
        self.cursorBtn.setIconSize(QSize(30, 30))

        self.verticalLayout_7.addWidget(self.cursorBtn)

        self.trainBtn = QPushButton(self.leftSubMenu)
        self.trainBtn.setObjectName(u"trainBtn")
        self.trainBtn.setFont(font1)
        icon9 = QIcon()
        icon9.addFile(u":/icons/Qss/icons/target.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.trainBtn.setIcon(icon9)
        self.trainBtn.setIconSize(QSize(30, 30))

        self.verticalLayout_7.addWidget(self.trainBtn)

        self.game1Btn = QPushButton(self.leftSubMenu)
        self.game1Btn.setObjectName(u"game1Btn")
        self.game1Btn.setFont(font1)
        icon10 = QIcon()
        icon10.addFile(u":/icons/Qss/icons/fire-svgrepo-com.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.game1Btn.setIcon(icon10)
        self.game1Btn.setIconSize(QSize(30, 30))

        self.verticalLayout_7.addWidget(self.game1Btn)

        self.game2Btn = QPushButton(self.leftSubMenu)
        self.game2Btn.setObjectName(u"game2Btn")
        self.game2Btn.setFont(font1)
        icon11 = QIcon()
        icon11.addFile(u":/icons/Qss/icons/alien-gray-line-drawing-svgrepo-com.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.game2Btn.setIcon(icon11)
        self.game2Btn.setIconSize(QSize(30, 30))

        self.verticalLayout_7.addWidget(self.game2Btn)

        self.verticalSpacer_3 = QSpacerItem(20, 631, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer_3)


        self.horizontalLayout.addWidget(self.leftSubMenu)

        self.mainPages = QCustomQStackedWidget(self.centralwidget)
        self.mainPages.setObjectName(u"mainPages")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mainPages.sizePolicy().hasHeightForWidth())
        self.mainPages.setSizePolicy(sizePolicy)
        self.mainPages.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.mainBodyContainerGUI = QWidget()
        self.mainBodyContainerGUI.setObjectName(u"mainBodyContainerGUI")
        self.mainBodyContainerGUI.setStyleSheet(u"")
        self.gridLayout = QGridLayout(self.mainBodyContainerGUI)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(-1, -1, -1, 9)
        self.rightBodyFrameOverview = QWidget(self.mainBodyContainerGUI)
        self.rightBodyFrameOverview.setObjectName(u"rightBodyFrameOverview")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(50)
        sizePolicy1.setVerticalStretch(95)
        sizePolicy1.setHeightForWidth(self.rightBodyFrameOverview.sizePolicy().hasHeightForWidth())
        self.rightBodyFrameOverview.setSizePolicy(sizePolicy1)
        self.rightBodyFrameOverview.setStyleSheet(u"border:none;")
        self.verticalLayout_6 = QVBoxLayout(self.rightBodyFrameOverview)
        self.verticalLayout_6.setSpacing(9)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.buttonsBox = QWidget(self.rightBodyFrameOverview)
        self.buttonsBox.setObjectName(u"buttonsBox")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.buttonsBox.sizePolicy().hasHeightForWidth())
        self.buttonsBox.setSizePolicy(sizePolicy2)
        self.buttonsBox.setMinimumSize(QSize(600, 114))
        self.buttonsBox.setStyleSheet(u"*{\n"
"border:none;\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 10px;\n"
"background-color: rgb(0, 118, 194);\n"
"}\n"
"QPushButton{\n"
"	text-align:center;\n"
"	background-color: rgb(0, 166, 214);\n"
"}")
        self.gridLayout_3 = QGridLayout(self.buttonsBox)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_6 = QLabel(self.buttonsBox)
        self.label_6.setObjectName(u"label_6")
        font2 = QFont()
        font2.setPointSize(16)
        font2.setBold(True)
        self.label_6.setFont(font2)

        self.gridLayout_3.addWidget(self.label_6, 0, 0, 1, 1)

        self.openUserWindowBtn = QPushButton(self.buttonsBox)
        self.openUserWindowBtn.setObjectName(u"openUserWindowBtn")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(1)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.openUserWindowBtn.sizePolicy().hasHeightForWidth())
        self.openUserWindowBtn.setSizePolicy(sizePolicy3)
        font3 = QFont()
        font3.setPointSize(16)
        self.openUserWindowBtn.setFont(font3)

        self.gridLayout_3.addWidget(self.openUserWindowBtn, 1, 0, 1, 1)

        self.openPromptBtn = QPushButton(self.buttonsBox)
        self.openPromptBtn.setObjectName(u"openPromptBtn")
        sizePolicy3.setHeightForWidth(self.openPromptBtn.sizePolicy().hasHeightForWidth())
        self.openPromptBtn.setSizePolicy(sizePolicy3)
        self.openPromptBtn.setFont(font3)

        self.gridLayout_3.addWidget(self.openPromptBtn, 1, 1, 1, 1)

        self.startTimerBtn = QPushButton(self.buttonsBox)
        self.startTimerBtn.setObjectName(u"startTimerBtn")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(1)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.startTimerBtn.sizePolicy().hasHeightForWidth())
        self.startTimerBtn.setSizePolicy(sizePolicy4)
        self.startTimerBtn.setFont(font3)

        self.gridLayout_3.addWidget(self.startTimerBtn, 1, 2, 1, 1)

        self.promptTimeFrame = QFrame(self.buttonsBox)
        self.promptTimeFrame.setObjectName(u"promptTimeFrame")
        sizePolicy2.setHeightForWidth(self.promptTimeFrame.sizePolicy().hasHeightForWidth())
        self.promptTimeFrame.setSizePolicy(sizePolicy2)
        self.promptTimeFrame.setStyleSheet(u"background-color: rgb(0, 166, 214);")
        self.promptTimeFrame.setFrameShape(QFrame.StyledPanel)
        self.promptTimeFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.promptTimeFrame)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.stopwatch = QLabel(self.promptTimeFrame)
        self.stopwatch.setObjectName(u"stopwatch")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy5.setHorizontalStretch(75)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.stopwatch.sizePolicy().hasHeightForWidth())
        self.stopwatch.setSizePolicy(sizePolicy5)
        self.stopwatch.setFont(font3)
        self.stopwatch.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.stopwatch)

        self.unit_sec = QLabel(self.promptTimeFrame)
        self.unit_sec.setObjectName(u"unit_sec")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy6.setHorizontalStretch(25)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.unit_sec.sizePolicy().hasHeightForWidth())
        self.unit_sec.setSizePolicy(sizePolicy6)
        self.unit_sec.setFont(font3)

        self.horizontalLayout_4.addWidget(self.unit_sec)


        self.gridLayout_3.addWidget(self.promptTimeFrame, 1, 3, 1, 1)

        self.dataTrainingBtn = QPushButton(self.buttonsBox)
        self.dataTrainingBtn.setObjectName(u"dataTrainingBtn")
        sizePolicy4.setHeightForWidth(self.dataTrainingBtn.sizePolicy().hasHeightForWidth())
        self.dataTrainingBtn.setSizePolicy(sizePolicy4)
        self.dataTrainingBtn.setFont(font3)

        self.gridLayout_3.addWidget(self.dataTrainingBtn, 2, 0, 1, 1)

        self.startRecordingBtn = QPushButton(self.buttonsBox)
        self.startRecordingBtn.setObjectName(u"startRecordingBtn")
        sizePolicy4.setHeightForWidth(self.startRecordingBtn.sizePolicy().hasHeightForWidth())
        self.startRecordingBtn.setSizePolicy(sizePolicy4)
        self.startRecordingBtn.setFont(font3)

        self.gridLayout_3.addWidget(self.startRecordingBtn, 2, 1, 1, 1)

        self.stopRecordingBtn = QPushButton(self.buttonsBox)
        self.stopRecordingBtn.setObjectName(u"stopRecordingBtn")
        sizePolicy4.setHeightForWidth(self.stopRecordingBtn.sizePolicy().hasHeightForWidth())
        self.stopRecordingBtn.setSizePolicy(sizePolicy4)
        self.stopRecordingBtn.setFont(font3)

        self.gridLayout_3.addWidget(self.stopRecordingBtn, 2, 2, 1, 1)

        self.ERDSBtn = QPushButton(self.buttonsBox)
        self.ERDSBtn.setObjectName(u"ERDSBtn")
        sizePolicy4.setHeightForWidth(self.ERDSBtn.sizePolicy().hasHeightForWidth())
        self.ERDSBtn.setSizePolicy(sizePolicy4)
        self.ERDSBtn.setFont(font3)

        self.gridLayout_3.addWidget(self.ERDSBtn, 2, 3, 1, 1)


        self.verticalLayout_6.addWidget(self.buttonsBox)

        self.FFTFrame = QFrame(self.rightBodyFrameOverview)
        self.FFTFrame.setObjectName(u"FFTFrame")
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(40)
        sizePolicy7.setHeightForWidth(self.FFTFrame.sizePolicy().hasHeightForWidth())
        self.FFTFrame.setSizePolicy(sizePolicy7)
        self.FFTFrame.setStyleSheet(u"")
        self.FFTFrame.setFrameShape(QFrame.StyledPanel)
        self.FFTFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.FFTFrame)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.FFTPlot = PlotWidget(self.FFTFrame)
        self.FFTPlot.setObjectName(u"FFTPlot")
        brush = QBrush(QColor(255, 255, 255, 255))
        brush.setStyle(Qt.NoBrush)
        self.FFTPlot.setBackgroundBrush(brush)

        self.horizontalLayout_6.addWidget(self.FFTPlot)


        self.verticalLayout_6.addWidget(self.FFTFrame)

        self.powerBandFrame = QFrame(self.rightBodyFrameOverview)
        self.powerBandFrame.setObjectName(u"powerBandFrame")
        sizePolicy7.setHeightForWidth(self.powerBandFrame.sizePolicy().hasHeightForWidth())
        self.powerBandFrame.setSizePolicy(sizePolicy7)
        self.powerBandFrame.setFrameShape(QFrame.StyledPanel)
        self.powerBandFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_10 = QHBoxLayout(self.powerBandFrame)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.powerBandPlot = PlotWidget(self.powerBandFrame)
        self.powerBandPlot.setObjectName(u"powerBandPlot")
        brush1 = QBrush(QColor(255, 255, 255, 255))
        brush1.setStyle(Qt.NoBrush)
        self.powerBandPlot.setBackgroundBrush(brush1)

        self.horizontalLayout_10.addWidget(self.powerBandPlot)


        self.verticalLayout_6.addWidget(self.powerBandFrame)


        self.gridLayout.addWidget(self.rightBodyFrameOverview, 1, 1, 1, 1)

        self.UserIDBox = QWidget(self.mainBodyContainerGUI)
        self.UserIDBox.setObjectName(u"UserIDBox")
        sizePolicy2.setHeightForWidth(self.UserIDBox.sizePolicy().hasHeightForWidth())
        self.UserIDBox.setSizePolicy(sizePolicy2)
        self.UserIDBox.setMaximumSize(QSize(16777215, 70))
        self.UserIDBox.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(0, 166, 214);\n"
"border-radius: 10px;")
        self.horizontalLayout_15 = QHBoxLayout(self.UserIDBox)
        self.horizontalLayout_15.setSpacing(0)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_15.setContentsMargins(0, 0, 100, 0)
        self.logoFrame = QFrame(self.UserIDBox)
        self.logoFrame.setObjectName(u"logoFrame")
        sizePolicy8 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy8.setHorizontalStretch(10)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.logoFrame.sizePolicy().hasHeightForWidth())
        self.logoFrame.setSizePolicy(sizePolicy8)
        self.logoFrame.setStyleSheet(u"image: url(:/newPrefix/pictures/TUDelft-logo_white.png);")
        self.logoFrame.setFrameShape(QFrame.StyledPanel)
        self.logoFrame.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_15.addWidget(self.logoFrame)

        self.userID_test = QLineEdit(self.UserIDBox)
        self.userID_test.setObjectName(u"userID_test")
        sizePolicy9 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy9.setHorizontalStretch(90)
        sizePolicy9.setVerticalStretch(0)
        sizePolicy9.setHeightForWidth(self.userID_test.sizePolicy().hasHeightForWidth())
        self.userID_test.setSizePolicy(sizePolicy9)
        font4 = QFont()
        font4.setPointSize(28)
        font4.setBold(True)
        self.userID_test.setFont(font4)
        self.userID_test.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_15.addWidget(self.userID_test)


        self.gridLayout.addWidget(self.UserIDBox, 0, 0, 1, 2)

        self.leftBodyFrameOverview = QWidget(self.mainBodyContainerGUI)
        self.leftBodyFrameOverview.setObjectName(u"leftBodyFrameOverview")
        sizePolicy10 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy10.setHorizontalStretch(50)
        sizePolicy10.setVerticalStretch(95)
        sizePolicy10.setHeightForWidth(self.leftBodyFrameOverview.sizePolicy().hasHeightForWidth())
        self.leftBodyFrameOverview.setSizePolicy(sizePolicy10)
        self.leftBodyFrameOverview.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.verticalLayout_3 = QVBoxLayout(self.leftBodyFrameOverview)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.directionFrame = QFrame(self.leftBodyFrameOverview)
        self.directionFrame.setObjectName(u"directionFrame")
        sizePolicy11 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy11.setHorizontalStretch(0)
        sizePolicy11.setVerticalStretch(10)
        sizePolicy11.setHeightForWidth(self.directionFrame.sizePolicy().hasHeightForWidth())
        self.directionFrame.setSizePolicy(sizePolicy11)
        self.directionFrame.setStyleSheet(u"background-color: rgb(0, 0, 0);\n"
"border-radius: 10px")
        self.directionFrame.setFrameShape(QFrame.StyledPanel)
        self.directionFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.directionFrame)
        self.horizontalLayout_3.setSpacing(3)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(3, 3, 3, 3)
        self.directionLine = QLineEdit(self.directionFrame)
        self.directionLine.setObjectName(u"directionLine")
        sizePolicy12 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy12.setHorizontalStretch(50)
        sizePolicy12.setVerticalStretch(0)
        sizePolicy12.setHeightForWidth(self.directionLine.sizePolicy().hasHeightForWidth())
        self.directionLine.setSizePolicy(sizePolicy12)
        font5 = QFont()
        font5.setPointSize(24)
        self.directionLine.setFont(font5)
        self.directionLine.setCursor(QCursor(Qt.ArrowCursor))
        self.directionLine.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.directionLine.setAlignment(Qt.AlignCenter)
        self.directionLine.setReadOnly(True)

        self.horizontalLayout_3.addWidget(self.directionLine)


        self.verticalLayout_3.addWidget(self.directionFrame)

        self.valuesFrame = QFrame(self.leftBodyFrameOverview)
        self.valuesFrame.setObjectName(u"valuesFrame")
        sizePolicy13 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy13.setHorizontalStretch(0)
        sizePolicy13.setVerticalStretch(15)
        sizePolicy13.setHeightForWidth(self.valuesFrame.sizePolicy().hasHeightForWidth())
        self.valuesFrame.setSizePolicy(sizePolicy13)
        self.valuesFrame.setMaximumSize(QSize(16777215, 107))
        self.valuesFrame.setStyleSheet(u"background-color: rgb(0, 118, 194);\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 10px;")
        self.valuesFrame.setFrameShape(QFrame.StyledPanel)
        self.valuesFrame.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.valuesFrame)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(9, 9, 9, 9)
        self.valuesBox = QHBoxLayout()
        self.valuesBox.setObjectName(u"valuesBox")
        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.label = QLabel(self.valuesFrame)
        self.label.setObjectName(u"label")
        sizePolicy14 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy14.setHorizontalStretch(0)
        sizePolicy14.setVerticalStretch(0)
        sizePolicy14.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy14)
        self.label.setFont(font3)
        self.label.setStyleSheet(u"border:none;")
        self.label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout_8.addWidget(self.label)

        self.label_2 = QLabel(self.valuesFrame)
        self.label_2.setObjectName(u"label_2")
        sizePolicy14.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy14)
        self.label_2.setFont(font3)
        self.label_2.setStyleSheet(u"border:none;")
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout_8.addWidget(self.label_2)


        self.valuesBox.addLayout(self.verticalLayout_8)

        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.learningRateLine = QLineEdit(self.valuesFrame)
        self.learningRateLine.setObjectName(u"learningRateLine")
        sizePolicy.setHeightForWidth(self.learningRateLine.sizePolicy().hasHeightForWidth())
        self.learningRateLine.setSizePolicy(sizePolicy)
        self.learningRateLine.setFont(font3)
        self.learningRateLine.setCursor(QCursor(Qt.ArrowCursor))
        self.learningRateLine.setStyleSheet(u"")

        self.verticalLayout_9.addWidget(self.learningRateLine)

        self.batchSizeLine = QLineEdit(self.valuesFrame)
        self.batchSizeLine.setObjectName(u"batchSizeLine")
        sizePolicy.setHeightForWidth(self.batchSizeLine.sizePolicy().hasHeightForWidth())
        self.batchSizeLine.setSizePolicy(sizePolicy)
        self.batchSizeLine.setFont(font3)
        self.batchSizeLine.setCursor(QCursor(Qt.ArrowCursor))

        self.verticalLayout_9.addWidget(self.batchSizeLine)


        self.valuesBox.addLayout(self.verticalLayout_9)

        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.label_3 = QLabel(self.valuesFrame)
        self.label_3.setObjectName(u"label_3")
        sizePolicy14.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy14)
        self.label_3.setFont(font3)
        self.label_3.setStyleSheet(u"border:none;")
        self.label_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout_10.addWidget(self.label_3)

        self.label_4 = QLabel(self.valuesFrame)
        self.label_4.setObjectName(u"label_4")
        sizePolicy14.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy14)
        self.label_4.setFont(font3)
        self.label_4.setStyleSheet(u"border:none;")
        self.label_4.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout_10.addWidget(self.label_4)


        self.valuesBox.addLayout(self.verticalLayout_10)

        self.verticalLayout_11 = QVBoxLayout()
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.maxIterationLine = QLineEdit(self.valuesFrame)
        self.maxIterationLine.setObjectName(u"maxIterationLine")
        sizePolicy.setHeightForWidth(self.maxIterationLine.sizePolicy().hasHeightForWidth())
        self.maxIterationLine.setSizePolicy(sizePolicy)
        self.maxIterationLine.setFont(font3)
        self.maxIterationLine.setCursor(QCursor(Qt.ArrowCursor))

        self.verticalLayout_11.addWidget(self.maxIterationLine)

        self.marginLine = QLineEdit(self.valuesFrame)
        self.marginLine.setObjectName(u"marginLine")
        sizePolicy.setHeightForWidth(self.marginLine.sizePolicy().hasHeightForWidth())
        self.marginLine.setSizePolicy(sizePolicy)
        self.marginLine.setFont(font3)
        self.marginLine.setCursor(QCursor(Qt.ArrowCursor))

        self.verticalLayout_11.addWidget(self.marginLine)


        self.valuesBox.addLayout(self.verticalLayout_11)


        self.gridLayout_2.addLayout(self.valuesBox, 1, 0, 1, 1)

        self.label_5 = QLabel(self.valuesFrame)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font2)

        self.gridLayout_2.addWidget(self.label_5, 0, 0, 1, 1)


        self.verticalLayout_3.addWidget(self.valuesFrame)

        self.channelsFrame = QFrame(self.leftBodyFrameOverview)
        self.channelsFrame.setObjectName(u"channelsFrame")
        sizePolicy15 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy15.setHorizontalStretch(0)
        sizePolicy15.setVerticalStretch(60)
        sizePolicy15.setHeightForWidth(self.channelsFrame.sizePolicy().hasHeightForWidth())
        self.channelsFrame.setSizePolicy(sizePolicy15)
        self.channelsFrame.setSizeIncrement(QSize(0, 0))
        self.channelsFrame.setBaseSize(QSize(0, 0))
        self.channelsFrame.setStyleSheet(u"")
        self.channelsFrame.setFrameShape(QFrame.StyledPanel)
        self.channelsFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.channelsFrame)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.verticalLayout_14 = QVBoxLayout()
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.ch1Label = QLabel(self.channelsFrame)
        self.ch1Label.setObjectName(u"ch1Label")
        sizePolicy8.setHeightForWidth(self.ch1Label.sizePolicy().hasHeightForWidth())
        self.ch1Label.setSizePolicy(sizePolicy8)
        self.ch1Label.setFont(font3)
        self.ch1Label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_14.addWidget(self.ch1Label)

        self.ch2Label = QLabel(self.channelsFrame)
        self.ch2Label.setObjectName(u"ch2Label")
        sizePolicy8.setHeightForWidth(self.ch2Label.sizePolicy().hasHeightForWidth())
        self.ch2Label.setSizePolicy(sizePolicy8)
        self.ch2Label.setFont(font3)
        self.ch2Label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_14.addWidget(self.ch2Label)

        self.ch3Label = QLabel(self.channelsFrame)
        self.ch3Label.setObjectName(u"ch3Label")
        sizePolicy8.setHeightForWidth(self.ch3Label.sizePolicy().hasHeightForWidth())
        self.ch3Label.setSizePolicy(sizePolicy8)
        self.ch3Label.setFont(font3)
        self.ch3Label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_14.addWidget(self.ch3Label)

        self.ch4Label = QLabel(self.channelsFrame)
        self.ch4Label.setObjectName(u"ch4Label")
        sizePolicy8.setHeightForWidth(self.ch4Label.sizePolicy().hasHeightForWidth())
        self.ch4Label.setSizePolicy(sizePolicy8)
        self.ch4Label.setFont(font3)
        self.ch4Label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_14.addWidget(self.ch4Label)

        self.ch5Label = QLabel(self.channelsFrame)
        self.ch5Label.setObjectName(u"ch5Label")
        sizePolicy8.setHeightForWidth(self.ch5Label.sizePolicy().hasHeightForWidth())
        self.ch5Label.setSizePolicy(sizePolicy8)
        self.ch5Label.setFont(font3)
        self.ch5Label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_14.addWidget(self.ch5Label)

        self.ch6Label = QLabel(self.channelsFrame)
        self.ch6Label.setObjectName(u"ch6Label")
        sizePolicy8.setHeightForWidth(self.ch6Label.sizePolicy().hasHeightForWidth())
        self.ch6Label.setSizePolicy(sizePolicy8)
        self.ch6Label.setFont(font3)
        self.ch6Label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_14.addWidget(self.ch6Label)

        self.ch7Label = QLabel(self.channelsFrame)
        self.ch7Label.setObjectName(u"ch7Label")
        sizePolicy8.setHeightForWidth(self.ch7Label.sizePolicy().hasHeightForWidth())
        self.ch7Label.setSizePolicy(sizePolicy8)
        self.ch7Label.setFont(font3)
        self.ch7Label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_14.addWidget(self.ch7Label)

        self.ch8Label = QLabel(self.channelsFrame)
        self.ch8Label.setObjectName(u"ch8Label")
        sizePolicy8.setHeightForWidth(self.ch8Label.sizePolicy().hasHeightForWidth())
        self.ch8Label.setSizePolicy(sizePolicy8)
        self.ch8Label.setFont(font3)
        self.ch8Label.setStyleSheet(u"")
        self.ch8Label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_14.addWidget(self.ch8Label)


        self.horizontalLayout_8.addLayout(self.verticalLayout_14)

        self.widget = QWidget(self.channelsFrame)
        self.widget.setObjectName(u"widget")

        self.horizontalLayout_8.addWidget(self.widget)

        self.channelsPlot = GraphicsLayoutWidget(self.channelsFrame)
        self.channelsPlot.setObjectName(u"channelsPlot")
        self.channelsPlot.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.horizontalLayout_8.addWidget(self.channelsPlot)


        self.horizontalLayout_9.addLayout(self.horizontalLayout_8)


        self.verticalLayout_3.addWidget(self.channelsFrame)


        self.gridLayout.addWidget(self.leftBodyFrameOverview, 1, 0, 1, 1)

        self.infoWidgetContainer = QWidget(self.mainBodyContainerGUI)
        self.infoWidgetContainer.setObjectName(u"infoWidgetContainer")
        sizePolicy16 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy16.setHorizontalStretch(0)
        sizePolicy16.setVerticalStretch(0)
        sizePolicy16.setHeightForWidth(self.infoWidgetContainer.sizePolicy().hasHeightForWidth())
        self.infoWidgetContainer.setSizePolicy(sizePolicy16)
        self.infoWidgetContainer.setStyleSheet(u"border-radius: 10px;")
        self.horizontalLayout_7 = QHBoxLayout(self.infoWidgetContainer)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.infoWidgetTrain = QCustomSlideMenu(self.infoWidgetContainer)
        self.infoWidgetTrain.setObjectName(u"infoWidgetTrain")
        sizePolicy16.setHeightForWidth(self.infoWidgetTrain.sizePolicy().hasHeightForWidth())
        self.infoWidgetTrain.setSizePolicy(sizePolicy16)
        self.infoWidgetTrain.setMinimumSize(QSize(0, 0))
        self.infoWidgetTrain.setMaximumSize(QSize(0, 0))
        self.infoWidgetTrain.setStyleSheet(u"background-color: rgb(0, 184, 200);\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 10px;")
        self.verticalLayout_12 = QVBoxLayout(self.infoWidgetTrain)
        self.verticalLayout_12.setSpacing(0)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(9, 9, 9, 9)
        self.label_13 = QLabel(self.infoWidgetTrain)
        self.label_13.setObjectName(u"label_13")
        font6 = QFont()
        font6.setPointSize(12)
        font6.setBold(True)
        self.label_13.setFont(font6)

        self.verticalLayout_12.addWidget(self.label_13)

        self.frame_10 = QFrame(self.infoWidgetTrain)
        self.frame_10.setObjectName(u"frame_10")
        sizePolicy16.setHeightForWidth(self.frame_10.sizePolicy().hasHeightForWidth())
        self.frame_10.setSizePolicy(sizePolicy16)
        self.frame_10.setStyleSheet(u"border-radius: 10px;")
        self.frame_10.setFrameShape(QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_10)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.label_14 = QLabel(self.frame_10)
        self.label_14.setObjectName(u"label_14")
        sizePolicy17 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy17.setHorizontalStretch(80)
        sizePolicy17.setVerticalStretch(0)
        sizePolicy17.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy17)
        font7 = QFont()
        font7.setPointSize(12)
        self.label_14.setFont(font7)

        self.horizontalLayout_5.addWidget(self.label_14)

        self.frame_11 = QFrame(self.frame_10)
        self.frame_11.setObjectName(u"frame_11")
        sizePolicy16.setHeightForWidth(self.frame_11.sizePolicy().hasHeightForWidth())
        self.frame_11.setSizePolicy(sizePolicy16)
        self.frame_11.setMinimumSize(QSize(0, 0))
        self.frame_11.setStyleSheet(u"border-radius: 10px;")
        self.frame_11.setFrameShape(QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QFrame.Raised)
        self.verticalLayout_13 = QVBoxLayout(self.frame_11)
        self.verticalLayout_13.setSpacing(0)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.widget_11 = QWidget(self.frame_11)
        self.widget_11.setObjectName(u"widget_11")
        sizePolicy14.setHeightForWidth(self.widget_11.sizePolicy().hasHeightForWidth())
        self.widget_11.setSizePolicy(sizePolicy14)
        self.widget_11.setStyleSheet(u"image: url(:/newPrefix/pictures/EEG cap.png);")

        self.verticalLayout_13.addWidget(self.widget_11)

        self.label_15 = QLabel(self.frame_11)
        self.label_15.setObjectName(u"label_15")
        font8 = QFont()
        font8.setPointSize(10)
        self.label_15.setFont(font8)

        self.verticalLayout_13.addWidget(self.label_15)


        self.horizontalLayout_5.addWidget(self.frame_11)


        self.verticalLayout_12.addWidget(self.frame_10)


        self.horizontalLayout_7.addWidget(self.infoWidgetTrain)


        self.gridLayout.addWidget(self.infoWidgetContainer, 2, 0, 1, 1)

        self.mainPages.addWidget(self.mainBodyContainerGUI)
        self.mainBodyContainerUsers = QWidget()
        self.mainBodyContainerUsers.setObjectName(u"mainBodyContainerUsers")
        self.mainBodyContainerUsers.setStyleSheet(u"QPushButton{text-align:left; padding:5px 15px;border-radius: 10px;}")
        self.gridLayout_6 = QGridLayout(self.mainBodyContainerUsers)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(-1, -1, -1, 9)
        self.listBtns = QVBoxLayout()
        self.listBtns.setObjectName(u"listBtns")
        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.listBtns.addItem(self.verticalSpacer_2)

        self.addBtn = QPushButton(self.mainBodyContainerUsers)
        self.addBtn.setObjectName(u"addBtn")
        font9 = QFont()
        font9.setPointSize(14)
        self.addBtn.setFont(font9)
        self.addBtn.setStyleSheet(u"background-color: rgb(0, 166, 214);\n"
"color: rgb(255, 255, 255);")

        self.listBtns.addWidget(self.addBtn)

        self.editBtn = QPushButton(self.mainBodyContainerUsers)
        self.editBtn.setObjectName(u"editBtn")
        self.editBtn.setFont(font9)
        self.editBtn.setStyleSheet(u"background-color: rgb(0, 166, 214);\n"
"color: rgb(255, 255, 255);")

        self.listBtns.addWidget(self.editBtn)

        self.removeBtn = QPushButton(self.mainBodyContainerUsers)
        self.removeBtn.setObjectName(u"removeBtn")
        self.removeBtn.setFont(font9)
        self.removeBtn.setStyleSheet(u"background-color: rgb(0, 166, 214);\n"
"color: rgb(255, 255, 255);")

        self.listBtns.addWidget(self.removeBtn)

        self.upBtn = QPushButton(self.mainBodyContainerUsers)
        self.upBtn.setObjectName(u"upBtn")
        self.upBtn.setFont(font9)
        self.upBtn.setStyleSheet(u"background-color: rgb(0, 166, 214);\n"
"color: rgb(255, 255, 255);")

        self.listBtns.addWidget(self.upBtn)

        self.downBtn = QPushButton(self.mainBodyContainerUsers)
        self.downBtn.setObjectName(u"downBtn")
        self.downBtn.setFont(font9)
        self.downBtn.setStyleSheet(u"background-color: rgb(0, 166, 214);\n"
"color: rgb(255, 255, 255);")

        self.listBtns.addWidget(self.downBtn)

        self.sortBtn = QPushButton(self.mainBodyContainerUsers)
        self.sortBtn.setObjectName(u"sortBtn")
        self.sortBtn.setFont(font9)
        self.sortBtn.setStyleSheet(u"background-color: rgb(0, 166, 214);\n"
"color: rgb(255, 255, 255);")

        self.listBtns.addWidget(self.sortBtn)


        self.gridLayout_6.addLayout(self.listBtns, 1, 1, 1, 1)

        self.usersList = QListWidget(self.mainBodyContainerUsers)
        self.usersList.setObjectName(u"usersList")
        sizePolicy18 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy18.setHorizontalStretch(0)
        sizePolicy18.setVerticalStretch(90)
        sizePolicy18.setHeightForWidth(self.usersList.sizePolicy().hasHeightForWidth())
        self.usersList.setSizePolicy(sizePolicy18)
        font10 = QFont()
        font10.setPointSize(18)
        self.usersList.setFont(font10)
        self.usersList.setAutoFillBackground(False)
        self.usersList.setStyleSheet(u"background-color: rgb(232, 232, 232);")
        self.usersList.setAlternatingRowColors(True)
        self.usersList.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.usersList.setSelectionRectVisible(True)

        self.gridLayout_6.addWidget(self.usersList, 1, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer, 0, 1, 1, 1)

        self.usersBox = QWidget(self.mainBodyContainerUsers)
        self.usersBox.setObjectName(u"usersBox")
        self.usersBox.setStyleSheet(u"background-color:transparent;")
        self.horizontalLayout_16 = QHBoxLayout(self.usersBox)
        self.horizontalLayout_16.setSpacing(0)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.logo2Frame = QFrame(self.usersBox)
        self.logo2Frame.setObjectName(u"logo2Frame")
        sizePolicy8.setHeightForWidth(self.logo2Frame.sizePolicy().hasHeightForWidth())
        self.logo2Frame.setSizePolicy(sizePolicy8)
        self.logo2Frame.setStyleSheet(u"image: url(:/newPrefix/pictures/flame logo.png);")
        self.logo2Frame.setFrameShape(QFrame.StyledPanel)
        self.logo2Frame.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_16.addWidget(self.logo2Frame)

        self.usersTitle = QLineEdit(self.usersBox)
        self.usersTitle.setObjectName(u"usersTitle")
        sizePolicy9.setHeightForWidth(self.usersTitle.sizePolicy().hasHeightForWidth())
        self.usersTitle.setSizePolicy(sizePolicy9)
        font11 = QFont()
        font11.setPointSize(50)
        self.usersTitle.setFont(font11)
        self.usersTitle.setStyleSheet(u"border:none;\n"
"color: rgb(12, 35, 64);")
        self.usersTitle.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.usersTitle.setReadOnly(True)

        self.horizontalLayout_16.addWidget(self.usersTitle)


        self.gridLayout_6.addWidget(self.usersBox, 0, 0, 1, 1)

        self.mainPages.addWidget(self.mainBodyContainerUsers)

        self.horizontalLayout.addWidget(self.mainPages)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.mainPages.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
#if QT_CONFIG(tooltip)
        self.menuBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Menu", None))
#endif // QT_CONFIG(tooltip)
        self.menuBtn.setText(QCoreApplication.translate("MainWindow", u"Menu", None))
#if QT_CONFIG(tooltip)
        self.overviewBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Train", None))
#endif // QT_CONFIG(tooltip)
        self.overviewBtn.setText(QCoreApplication.translate("MainWindow", u"Dashboard", None))
#if QT_CONFIG(tooltip)
        self.demosBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Demos", None))
#endif // QT_CONFIG(tooltip)
        self.demosBtn.setText(QCoreApplication.translate("MainWindow", u"Demos", None))
#if QT_CONFIG(tooltip)
        self.usersBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Users", None))
#endif // QT_CONFIG(tooltip)
        self.usersBtn.setText(QCoreApplication.translate("MainWindow", u"Users", None))
#if QT_CONFIG(tooltip)
        self.reconnectBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Reconnect", None))
#endif // QT_CONFIG(tooltip)
        self.reconnectBtn.setText(QCoreApplication.translate("MainWindow", u"Reconnect", None))
#if QT_CONFIG(tooltip)
        self.infoBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Information", None))
#endif // QT_CONFIG(tooltip)
        self.infoBtn.setText(QCoreApplication.translate("MainWindow", u"Info", None))
#if QT_CONFIG(tooltip)
        self.exitBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Exit Window", None))
#endif // QT_CONFIG(tooltip)
        self.exitBtn.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.cursorBtn.setText(QCoreApplication.translate("MainWindow", u"Cursor", None))
        self.trainBtn.setText(QCoreApplication.translate("MainWindow", u"Train", None))
        self.game1Btn.setText(QCoreApplication.translate("MainWindow", u"Game 1", None))
        self.game2Btn.setText(QCoreApplication.translate("MainWindow", u"Game 2", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Control Panel", None))
        self.openUserWindowBtn.setText(QCoreApplication.translate("MainWindow", u"Open Window", None))
        self.openPromptBtn.setText(QCoreApplication.translate("MainWindow", u"Open Prompt", None))
        self.startTimerBtn.setText(QCoreApplication.translate("MainWindow", u"Start Timer", None))
        self.stopwatch.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.unit_sec.setText(QCoreApplication.translate("MainWindow", u"s", None))
        self.dataTrainingBtn.setText(QCoreApplication.translate("MainWindow", u"Train Data", None))
        self.startRecordingBtn.setText(QCoreApplication.translate("MainWindow", u"Start Recording", None))
        self.stopRecordingBtn.setText(QCoreApplication.translate("MainWindow", u"Stop Recording", None))
        self.ERDSBtn.setText(QCoreApplication.translate("MainWindow", u"ERDS", None))
        self.userID_test.setText(QCoreApplication.translate("MainWindow", u"No User selected", None))
        self.directionLine.setText(QCoreApplication.translate("MainWindow", u"Direction", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Learning rate:   ", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Batch size:   ", None))
        self.learningRateLine.setText(QCoreApplication.translate("MainWindow", u"0.01", None))
        self.batchSizeLine.setText(QCoreApplication.translate("MainWindow", u"64", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Max iteration:   ", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Margin:   ", None))
        self.maxIterationLine.setText(QCoreApplication.translate("MainWindow", u"1000", None))
        self.marginLine.setText(QCoreApplication.translate("MainWindow", u"0.6", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Training Panel", None))
        self.ch1Label.setText(QCoreApplication.translate("MainWindow", u"Ch1", None))
        self.ch2Label.setText(QCoreApplication.translate("MainWindow", u"Ch2", None))
        self.ch3Label.setText(QCoreApplication.translate("MainWindow", u"Ch3", None))
        self.ch4Label.setText(QCoreApplication.translate("MainWindow", u"Ch4", None))
        self.ch5Label.setText(QCoreApplication.translate("MainWindow", u"Ch5", None))
        self.ch6Label.setText(QCoreApplication.translate("MainWindow", u"Ch6", None))
        self.ch7Label.setText(QCoreApplication.translate("MainWindow", u"Ch7", None))
        self.ch8Label.setText(QCoreApplication.translate("MainWindow", u"Ch8", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Information", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Welcome to this BCI app!\n"
"The dashboard window contains numerous data and parameters for a better understanding of EEG data!\n"
" Plots: eight channel plots for each electrode of the cap and an FFT and power band plot\n"
" of the chosen channel. The channel can be changed using the numbers key.\n"
" In the training panel you can change the training values according to your liking.\n"
" Lastly, the buttons panel gives you control over the user's window and other features.\n"
"\n"
" The demos button opens a submenu which contains the possible demo you would like to run.\n"
"\n"
" Lastly, the user's window allows you to choose and edit users that are going to be trained or tested.", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Channel numbers with according position", None))
#if QT_CONFIG(tooltip)
        self.addBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Add user", None))
#endif // QT_CONFIG(tooltip)
        self.addBtn.setText(QCoreApplication.translate("MainWindow", u"ADD", None))
#if QT_CONFIG(tooltip)
        self.editBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Edit user", None))
#endif // QT_CONFIG(tooltip)
        self.editBtn.setText(QCoreApplication.translate("MainWindow", u"EDIT", None))
#if QT_CONFIG(tooltip)
        self.removeBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Remove user", None))
#endif // QT_CONFIG(tooltip)
        self.removeBtn.setText(QCoreApplication.translate("MainWindow", u"REMOVE", None))
#if QT_CONFIG(tooltip)
        self.upBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Put user a position above", None))
#endif // QT_CONFIG(tooltip)
        self.upBtn.setText(QCoreApplication.translate("MainWindow", u"UP", None))
#if QT_CONFIG(tooltip)
        self.downBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Put user a position above", None))
#endif // QT_CONFIG(tooltip)
        self.downBtn.setText(QCoreApplication.translate("MainWindow", u"DOWN", None))
#if QT_CONFIG(tooltip)
        self.sortBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Sort users", None))
#endif // QT_CONFIG(tooltip)
        self.sortBtn.setText(QCoreApplication.translate("MainWindow", u"SORT", None))
        self.usersTitle.setText(QCoreApplication.translate("MainWindow", u"Users", None))
    # retranslateUi

