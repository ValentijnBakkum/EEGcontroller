# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'userWindowuAqIuf.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QMainWindow, QSizePolicy, QSpacerItem,
    QStackedWidget, QWidget)
import image_rc
import resources_rc

class Ui_UserWindow(object):
    def setupUi(self, UserWindow):
        if not UserWindow.objectName():
            UserWindow.setObjectName(u"UserWindow")
        UserWindow.resize(1228, 737)
        icon = QIcon()
        icon.addFile(u":/newPrefix/pictures/EEG.jpg", QSize(), QIcon.Normal, QIcon.Off)
        UserWindow.setWindowIcon(icon)
        UserWindow.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")
        self.centralwidget = QWidget(UserWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_12 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_12.setSpacing(0)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.demosPages = QStackedWidget(self.centralwidget)
        self.demosPages.setObjectName(u"demosPages")
        self.trainingPage = QWidget()
        self.trainingPage.setObjectName(u"trainingPage")
        self.trainingPage.setStyleSheet(u"*{\n"
"	background-color:rgb(0, 0, 0);\n"
"	color: rgb(200,200,200);\n"
"}")
        self.horizontalLayout = QHBoxLayout(self.trainingPage)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.promptsWidgets = QStackedWidget(self.trainingPage)
        self.promptsWidgets.setObjectName(u"promptsWidgets")
        self.promptsWidgets.setStyleSheet(u"")
        self.calibrationPage = QWidget()
        self.calibrationPage.setObjectName(u"calibrationPage")
        self.calibrationPage.setStyleSheet(u"")
        self.gridLayout = QGridLayout(self.calibrationPage)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalSpacer = QSpacerItem(20, 185, QSizePolicy.Minimum, QSizePolicy.Preferred)

        self.gridLayout.addItem(self.verticalSpacer, 0, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(348, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 1, 0, 1, 1)

        self.calibrationCross = QFrame(self.calibrationPage)
        self.calibrationCross.setObjectName(u"calibrationCross")
        self.calibrationCross.setMaximumSize(QSize(199, 187))
        self.calibrationCross.setFrameShape(QFrame.StyledPanel)
        self.calibrationCross.setFrameShadow(QFrame.Raised)
        self.gridLayout_6 = QGridLayout(self.calibrationCross)
        self.gridLayout_6.setSpacing(0)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.frame_7 = QFrame(self.calibrationCross)
        self.frame_7.setObjectName(u"frame_7")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_7.sizePolicy().hasHeightForWidth())
        self.frame_7.setSizePolicy(sizePolicy)
        self.frame_7.setMaximumSize(QSize(20, 16777215))
        self.frame_7.setStyleSheet(u"background-color: rgb(200, 200, 200);")
        self.frame_7.setFrameShape(QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Raised)

        self.gridLayout_6.addWidget(self.frame_7, 0, 1, 1, 1)

        self.frame_8 = QFrame(self.calibrationCross)
        self.frame_8.setObjectName(u"frame_8")
        sizePolicy.setHeightForWidth(self.frame_8.sizePolicy().hasHeightForWidth())
        self.frame_8.setSizePolicy(sizePolicy)
        self.frame_8.setStyleSheet(u"background-color: rgb(200, 200, 200);")
        self.frame_8.setFrameShape(QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Raised)

        self.gridLayout_6.addWidget(self.frame_8, 1, 0, 1, 1)

        self.frame_6 = QFrame(self.calibrationCross)
        self.frame_6.setObjectName(u"frame_6")
        sizePolicy.setHeightForWidth(self.frame_6.sizePolicy().hasHeightForWidth())
        self.frame_6.setSizePolicy(sizePolicy)
        self.frame_6.setStyleSheet(u"background-color: rgb(200, 200, 200);")
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)

        self.gridLayout_6.addWidget(self.frame_6, 1, 1, 1, 1)

        self.frame_9 = QFrame(self.calibrationCross)
        self.frame_9.setObjectName(u"frame_9")
        sizePolicy.setHeightForWidth(self.frame_9.sizePolicy().hasHeightForWidth())
        self.frame_9.setSizePolicy(sizePolicy)
        self.frame_9.setMaximumSize(QSize(16777215, 20))
        self.frame_9.setStyleSheet(u"background-color: rgb(200, 200, 200);")
        self.frame_9.setFrameShape(QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QFrame.Raised)

        self.gridLayout_6.addWidget(self.frame_9, 1, 2, 1, 1)

        self.frame = QFrame(self.calibrationCross)
        self.frame.setObjectName(u"frame")
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setStyleSheet(u"background-color: rgb(200, 200, 200);")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)

        self.gridLayout_6.addWidget(self.frame, 2, 1, 1, 1)


        self.gridLayout.addWidget(self.calibrationCross, 1, 1, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(338, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_3, 1, 2, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 185, QSizePolicy.Minimum, QSizePolicy.Preferred)

        self.gridLayout.addItem(self.verticalSpacer_2, 2, 1, 1, 1)

        self.promptsWidgets.addWidget(self.calibrationPage)
        self.rightPage = QWidget()
        self.rightPage.setObjectName(u"rightPage")
        self.rightPage.setStyleSheet(u"")
        self.gridLayout_2 = QGridLayout(self.rightPage)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalSpacer_3 = QSpacerItem(20, 185, QSizePolicy.Minimum, QSizePolicy.Preferred)

        self.gridLayout_2.addItem(self.verticalSpacer_3, 0, 1, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(294, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_4, 1, 0, 1, 1)

        self.rightFrame = QFrame(self.rightPage)
        self.rightFrame.setObjectName(u"rightFrame")
        sizePolicy.setHeightForWidth(self.rightFrame.sizePolicy().hasHeightForWidth())
        self.rightFrame.setSizePolicy(sizePolicy)
        self.rightFrame.setStyleSheet(u"")
        self.rightFrame.setFrameShape(QFrame.StyledPanel)
        self.rightFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.rightFrame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.rightLabel = QLabel(self.rightFrame)
        self.rightLabel.setObjectName(u"rightLabel")
        font = QFont()
        font.setPointSize(40)
        font.setBold(False)
        self.rightLabel.setFont(font)
        self.rightLabel.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.rightLabel)


        self.gridLayout_2.addWidget(self.rightFrame, 1, 1, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(294, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_5, 1, 2, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(20, 185, QSizePolicy.Minimum, QSizePolicy.Preferred)

        self.gridLayout_2.addItem(self.verticalSpacer_4, 2, 1, 1, 1)

        self.promptsWidgets.addWidget(self.rightPage)
        self.leftPage = QWidget()
        self.leftPage.setObjectName(u"leftPage")
        self.gridLayout_3 = QGridLayout(self.leftPage)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.verticalSpacer_5 = QSpacerItem(20, 185, QSizePolicy.Minimum, QSizePolicy.Preferred)

        self.gridLayout_3.addItem(self.verticalSpacer_5, 0, 1, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(294, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_6, 1, 0, 1, 1)

        self.leftFrame = QFrame(self.leftPage)
        self.leftFrame.setObjectName(u"leftFrame")
        sizePolicy.setHeightForWidth(self.leftFrame.sizePolicy().hasHeightForWidth())
        self.leftFrame.setSizePolicy(sizePolicy)
        self.leftFrame.setStyleSheet(u"")
        self.leftFrame.setFrameShape(QFrame.StyledPanel)
        self.leftFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.leftFrame)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.leftLabel = QLabel(self.leftFrame)
        self.leftLabel.setObjectName(u"leftLabel")
        self.leftLabel.setFont(font)
        self.leftLabel.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.leftLabel)


        self.gridLayout_3.addWidget(self.leftFrame, 1, 1, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(294, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_7, 1, 2, 1, 1)

        self.verticalSpacer_6 = QSpacerItem(20, 185, QSizePolicy.Minimum, QSizePolicy.Preferred)

        self.gridLayout_3.addItem(self.verticalSpacer_6, 2, 1, 1, 1)

        self.promptsWidgets.addWidget(self.leftPage)
        self.upPage = QWidget()
        self.upPage.setObjectName(u"upPage")
        self.gridLayout_4 = QGridLayout(self.upPage)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.verticalSpacer_7 = QSpacerItem(20, 185, QSizePolicy.Minimum, QSizePolicy.Preferred)

        self.gridLayout_4.addItem(self.verticalSpacer_7, 0, 1, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(294, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_8, 1, 0, 1, 1)

        self.tongueFrame = QFrame(self.upPage)
        self.tongueFrame.setObjectName(u"tongueFrame")
        sizePolicy.setHeightForWidth(self.tongueFrame.sizePolicy().hasHeightForWidth())
        self.tongueFrame.setSizePolicy(sizePolicy)
        self.tongueFrame.setStyleSheet(u"")
        self.tongueFrame.setFrameShape(QFrame.StyledPanel)
        self.tongueFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.tongueFrame)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.tongueLabel = QLabel(self.tongueFrame)
        self.tongueLabel.setObjectName(u"tongueLabel")
        font1 = QFont()
        font1.setPointSize(50)
        font1.setBold(False)
        self.tongueLabel.setFont(font1)
        self.tongueLabel.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.tongueLabel)


        self.gridLayout_4.addWidget(self.tongueFrame, 1, 1, 1, 1)

        self.horizontalSpacer_9 = QSpacerItem(294, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_9, 1, 2, 1, 1)

        self.verticalSpacer_8 = QSpacerItem(20, 185, QSizePolicy.Minimum, QSizePolicy.Preferred)

        self.gridLayout_4.addItem(self.verticalSpacer_8, 2, 1, 1, 1)

        self.promptsWidgets.addWidget(self.upPage)
        self.downPage = QWidget()
        self.downPage.setObjectName(u"downPage")
        self.gridLayout_5 = QGridLayout(self.downPage)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.verticalSpacer_9 = QSpacerItem(20, 185, QSizePolicy.Minimum, QSizePolicy.Preferred)

        self.gridLayout_5.addItem(self.verticalSpacer_9, 0, 1, 1, 1)

        self.horizontalSpacer_10 = QSpacerItem(294, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_10, 1, 0, 1, 1)

        self.feetFrame = QFrame(self.downPage)
        self.feetFrame.setObjectName(u"feetFrame")
        sizePolicy.setHeightForWidth(self.feetFrame.sizePolicy().hasHeightForWidth())
        self.feetFrame.setSizePolicy(sizePolicy)
        self.feetFrame.setStyleSheet(u"")
        self.feetFrame.setFrameShape(QFrame.StyledPanel)
        self.feetFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.feetFrame)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.feetLabel = QLabel(self.feetFrame)
        self.feetLabel.setObjectName(u"feetLabel")
        self.feetLabel.setFont(font1)
        self.feetLabel.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_5.addWidget(self.feetLabel)


        self.gridLayout_5.addWidget(self.feetFrame, 1, 1, 1, 1)

        self.horizontalSpacer_11 = QSpacerItem(294, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_11, 1, 2, 1, 1)

        self.verticalSpacer_10 = QSpacerItem(20, 185, QSizePolicy.Minimum, QSizePolicy.Preferred)

        self.gridLayout_5.addItem(self.verticalSpacer_10, 2, 1, 1, 1)

        self.promptsWidgets.addWidget(self.downPage)

        self.horizontalLayout.addWidget(self.promptsWidgets)

        self.demosPages.addWidget(self.trainingPage)
        self.promptPage = QWidget()
        self.promptPage.setObjectName(u"promptPage")
        self.horizontalLayout_7 = QHBoxLayout(self.promptPage)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.promptTestWidget = QStackedWidget(self.promptPage)
        self.promptTestWidget.setObjectName(u"promptTestWidget")
        self.calibrationPromptPage = QWidget()
        self.calibrationPromptPage.setObjectName(u"calibrationPromptPage")
        self.calibrationPromptPage.setStyleSheet(u"background-color: rgb(0,0,0);")
        self.gridLayout_8 = QGridLayout(self.calibrationPromptPage)
        self.gridLayout_8.setSpacing(0)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(0, 0, 0, 0)
        self.frame_2 = QFrame(self.calibrationPromptPage)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_9 = QGridLayout(self.frame_2)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.verticalSpacer_12 = QSpacerItem(20, 247, QSizePolicy.Minimum, QSizePolicy.Preferred)

        self.gridLayout_9.addItem(self.verticalSpacer_12, 0, 1, 1, 1)

        self.horizontalSpacer_13 = QSpacerItem(487, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.gridLayout_9.addItem(self.horizontalSpacer_13, 1, 0, 1, 1)

        self.calibrationCross_2 = QFrame(self.frame_2)
        self.calibrationCross_2.setObjectName(u"calibrationCross_2")
        self.calibrationCross_2.setMaximumSize(QSize(199, 187))
        self.calibrationCross_2.setFrameShape(QFrame.StyledPanel)
        self.calibrationCross_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_7 = QGridLayout(self.calibrationCross_2)
        self.gridLayout_7.setSpacing(0)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.frame_11 = QFrame(self.calibrationCross_2)
        self.frame_11.setObjectName(u"frame_11")
        sizePolicy.setHeightForWidth(self.frame_11.sizePolicy().hasHeightForWidth())
        self.frame_11.setSizePolicy(sizePolicy)
        self.frame_11.setMaximumSize(QSize(20, 16777215))
        self.frame_11.setStyleSheet(u"background-color: rgb(200, 200, 200);")
        self.frame_11.setFrameShape(QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QFrame.Raised)

        self.gridLayout_7.addWidget(self.frame_11, 0, 1, 1, 1)

        self.frame_12 = QFrame(self.calibrationCross_2)
        self.frame_12.setObjectName(u"frame_12")
        sizePolicy.setHeightForWidth(self.frame_12.sizePolicy().hasHeightForWidth())
        self.frame_12.setSizePolicy(sizePolicy)
        self.frame_12.setStyleSheet(u"background-color: rgb(200, 200, 200);")
        self.frame_12.setFrameShape(QFrame.StyledPanel)
        self.frame_12.setFrameShadow(QFrame.Raised)

        self.gridLayout_7.addWidget(self.frame_12, 1, 0, 1, 1)

        self.frame_13 = QFrame(self.calibrationCross_2)
        self.frame_13.setObjectName(u"frame_13")
        sizePolicy.setHeightForWidth(self.frame_13.sizePolicy().hasHeightForWidth())
        self.frame_13.setSizePolicy(sizePolicy)
        self.frame_13.setStyleSheet(u"background-color: rgb(200, 200, 200);")
        self.frame_13.setFrameShape(QFrame.StyledPanel)
        self.frame_13.setFrameShadow(QFrame.Raised)

        self.gridLayout_7.addWidget(self.frame_13, 1, 1, 1, 1)

        self.frame_14 = QFrame(self.calibrationCross_2)
        self.frame_14.setObjectName(u"frame_14")
        sizePolicy.setHeightForWidth(self.frame_14.sizePolicy().hasHeightForWidth())
        self.frame_14.setSizePolicy(sizePolicy)
        self.frame_14.setMaximumSize(QSize(16777215, 20))
        self.frame_14.setStyleSheet(u"background-color: rgb(200, 200, 200);")
        self.frame_14.setFrameShape(QFrame.StyledPanel)
        self.frame_14.setFrameShadow(QFrame.Raised)

        self.gridLayout_7.addWidget(self.frame_14, 1, 2, 1, 1)

        self.frame_3 = QFrame(self.calibrationCross_2)
        self.frame_3.setObjectName(u"frame_3")
        sizePolicy.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy)
        self.frame_3.setStyleSheet(u"background-color: rgb(200, 200, 200);")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)

        self.gridLayout_7.addWidget(self.frame_3, 2, 1, 1, 1)


        self.gridLayout_9.addWidget(self.calibrationCross_2, 1, 1, 1, 1)

        self.horizontalSpacer_12 = QSpacerItem(486, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.gridLayout_9.addItem(self.horizontalSpacer_12, 1, 2, 1, 1)

        self.verticalSpacer_11 = QSpacerItem(20, 247, QSizePolicy.Minimum, QSizePolicy.Preferred)

        self.gridLayout_9.addItem(self.verticalSpacer_11, 2, 1, 1, 1)


        self.gridLayout_8.addWidget(self.frame_2, 0, 0, 1, 1)

        self.promptTestWidget.addWidget(self.calibrationPromptPage)
        self.promptPromptPage = QWidget()
        self.promptPromptPage.setObjectName(u"promptPromptPage")
        self.promptPromptPage.setStyleSheet(u"color: rgb(200,200,200);")
        self.horizontalLayout_8 = QHBoxLayout(self.promptPromptPage)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.frame_4 = QFrame(self.promptPromptPage)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setStyleSheet(u"background-color: rgb(0,0,0);")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.gridLayout_10 = QGridLayout(self.frame_4)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.verticalSpacer_13 = QSpacerItem(20, 220, QSizePolicy.Minimum, QSizePolicy.Preferred)

        self.gridLayout_10.addItem(self.verticalSpacer_13, 0, 1, 1, 1)

        self.horizontalSpacer_14 = QSpacerItem(384, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.gridLayout_10.addItem(self.horizontalSpacer_14, 1, 0, 1, 1)

        self.rightFrame_2 = QFrame(self.frame_4)
        self.rightFrame_2.setObjectName(u"rightFrame_2")
        sizePolicy.setHeightForWidth(self.rightFrame_2.sizePolicy().hasHeightForWidth())
        self.rightFrame_2.setSizePolicy(sizePolicy)
        self.rightFrame_2.setStyleSheet(u"")
        self.rightFrame_2.setFrameShape(QFrame.StyledPanel)
        self.rightFrame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_11 = QHBoxLayout(self.rightFrame_2)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.rightLabel_2 = QLabel(self.rightFrame_2)
        self.rightLabel_2.setObjectName(u"rightLabel_2")
        self.rightLabel_2.setFont(font)
        self.rightLabel_2.setStyleSheet(u"")
        self.rightLabel_2.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_11.addWidget(self.rightLabel_2)


        self.gridLayout_10.addWidget(self.rightFrame_2, 1, 1, 1, 1)

        self.horizontalSpacer_15 = QSpacerItem(384, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.gridLayout_10.addItem(self.horizontalSpacer_15, 1, 2, 1, 1)

        self.verticalSpacer_14 = QSpacerItem(20, 220, QSizePolicy.Minimum, QSizePolicy.Preferred)

        self.gridLayout_10.addItem(self.verticalSpacer_14, 2, 1, 1, 1)


        self.horizontalLayout_8.addWidget(self.frame_4)

        self.promptTestWidget.addWidget(self.promptPromptPage)

        self.horizontalLayout_7.addWidget(self.promptTestWidget)

        self.demosPages.addWidget(self.promptPage)
        self.cursorPage = QWidget()
        self.cursorPage.setObjectName(u"cursorPage")
        self.horizontalLayout_6 = QHBoxLayout(self.cursorPage)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.cursorFrame = QFrame(self.cursorPage)
        self.cursorFrame.setObjectName(u"cursorFrame")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(20)
        sizePolicy1.setHeightForWidth(self.cursorFrame.sizePolicy().hasHeightForWidth())
        self.cursorFrame.setSizePolicy(sizePolicy1)
        self.cursorFrame.setStyleSheet(u"")
        self.cursorFrame.setFrameShape(QFrame.StyledPanel)
        self.cursorFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_13 = QHBoxLayout(self.cursorFrame)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(3, 3, 3, 3)
        self.mouseCursor = QWidget(self.cursorFrame)
        self.mouseCursor.setObjectName(u"mouseCursor")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.mouseCursor.sizePolicy().hasHeightForWidth())
        self.mouseCursor.setSizePolicy(sizePolicy2)
        self.mouseCursor.setMaximumSize(QSize(20, 20))
        self.mouseCursor.setCursor(QCursor(Qt.ArrowCursor))
        self.mouseCursor.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"image: url(:/newPrefix/pictures/cursor.png);")

        self.horizontalLayout_13.addWidget(self.mouseCursor)


        self.horizontalLayout_6.addWidget(self.cursorFrame)

        self.demosPages.addWidget(self.cursorPage)
        self.game1Page = QWidget()
        self.game1Page.setObjectName(u"game1Page")
        self.horizontalLayout_9 = QHBoxLayout(self.game1Page)
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.game1Widget = QWidget(self.game1Page)
        self.game1Widget.setObjectName(u"game1Widget")
        sizePolicy3 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(10)
        sizePolicy3.setVerticalStretch(10)
        sizePolicy3.setHeightForWidth(self.game1Widget.sizePolicy().hasHeightForWidth())
        self.game1Widget.setSizePolicy(sizePolicy3)
        self.game1Widget.setMinimumSize(QSize(400, 400))

        self.horizontalLayout_9.addWidget(self.game1Widget)

        self.demosPages.addWidget(self.game1Page)
        self.game2Page = QWidget()
        self.game2Page.setObjectName(u"game2Page")
        self.horizontalLayout_10 = QHBoxLayout(self.game2Page)
        self.horizontalLayout_10.setSpacing(0)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.game2Widget = QWidget(self.game2Page)
        self.game2Widget.setObjectName(u"game2Widget")
        self.gridLayout_11 = QGridLayout(self.game2Widget)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.game2Label = QLabel(self.game2Widget)
        self.game2Label.setObjectName(u"game2Label")
        sizePolicy4 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.game2Label.sizePolicy().hasHeightForWidth())
        self.game2Label.setSizePolicy(sizePolicy4)
        font2 = QFont()
        font2.setPointSize(22)
        self.game2Label.setFont(font2)

        self.gridLayout_11.addWidget(self.game2Label, 0, 0, 1, 1)


        self.horizontalLayout_10.addWidget(self.game2Widget)

        self.demosPages.addWidget(self.game2Page)

        self.horizontalLayout_12.addWidget(self.demosPages)

        UserWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(UserWindow)

        self.demosPages.setCurrentIndex(2)
        self.promptsWidgets.setCurrentIndex(0)
        self.promptTestWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(UserWindow)
    # setupUi

    def retranslateUi(self, UserWindow):
        UserWindow.setWindowTitle(QCoreApplication.translate("UserWindow", u"MainWindow", None))
        self.rightLabel.setText(QCoreApplication.translate("UserWindow", u"Right Hand", None))
        self.leftLabel.setText(QCoreApplication.translate("UserWindow", u"Left Hand", None))
        self.tongueLabel.setText(QCoreApplication.translate("UserWindow", u"Tongue", None))
        self.feetLabel.setText(QCoreApplication.translate("UserWindow", u"Feet", None))
        self.rightLabel_2.setText(QCoreApplication.translate("UserWindow", u"Right Hand", None))
        self.game2Label.setText(QCoreApplication.translate("UserWindow", u"Game 2 Page", None))
    # retranslateUi

