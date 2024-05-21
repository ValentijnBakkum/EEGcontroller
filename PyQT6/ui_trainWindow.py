# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'trainWindownNPMkv.ui'
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
    QLabel, QMainWindow, QPushButton, QSizePolicy,
    QSpacerItem, QStackedWidget, QVBoxLayout, QWidget)
import image_rc
import resources_rc

class Ui_TrainWindow(object):
    def setupUi(self, TrainWindow):
        if not TrainWindow.objectName():
            TrainWindow.setObjectName(u"TrainWindow")
        TrainWindow.resize(945, 671)
        icon = QIcon()
        icon.addFile(u":/newPrefix/pictures/EEG.jpg", QSize(), QIcon.Normal, QIcon.Off)
        TrainWindow.setWindowIcon(icon)
        TrainWindow.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")
        self.centralwidget = QWidget(TrainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.startRecordingBtn = QPushButton(self.widget)
        self.startRecordingBtn.setObjectName(u"startRecordingBtn")
        icon1 = QIcon()
        icon1.addFile(u":/icons/Qss/icons/red circle.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.startRecordingBtn.setIcon(icon1)
        self.startRecordingBtn.setIconSize(QSize(25, 25))

        self.horizontalLayout.addWidget(self.startRecordingBtn)

        self.stopRecordingBtn = QPushButton(self.widget)
        self.stopRecordingBtn.setObjectName(u"stopRecordingBtn")
        icon2 = QIcon()
        icon2.addFile(u":/icons/Qss/icons/black square.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.stopRecordingBtn.setIcon(icon2)
        self.stopRecordingBtn.setIconSize(QSize(25, 25))

        self.horizontalLayout.addWidget(self.stopRecordingBtn)

        self.helpBtn = QPushButton(self.widget)
        self.helpBtn.setObjectName(u"helpBtn")
        font = QFont()
        font.setPointSize(14)
        self.helpBtn.setFont(font)
        icon3 = QIcon()
        icon3.addFile(u":/icons/Qss/icons/black help-circle.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.helpBtn.setIcon(icon3)
        self.helpBtn.setIconSize(QSize(25, 25))

        self.horizontalLayout.addWidget(self.helpBtn)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.dataTrainingBtn = QPushButton(self.widget)
        self.dataTrainingBtn.setObjectName(u"dataTrainingBtn")

        self.horizontalLayout.addWidget(self.dataTrainingBtn)


        self.verticalLayout.addWidget(self.widget)

        self.promptsWidgets = QStackedWidget(self.centralwidget)
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

        self.frame_10 = QFrame(self.calibrationPage)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setMaximumSize(QSize(199, 187))
        self.frame_10.setFrameShape(QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QFrame.Raised)
        self.gridLayout_6 = QGridLayout(self.frame_10)
        self.gridLayout_6.setSpacing(0)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.frame_7 = QFrame(self.frame_10)
        self.frame_7.setObjectName(u"frame_7")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_7.sizePolicy().hasHeightForWidth())
        self.frame_7.setSizePolicy(sizePolicy)
        self.frame_7.setMaximumSize(QSize(20, 16777215))
        self.frame_7.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.frame_7.setFrameShape(QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Raised)

        self.gridLayout_6.addWidget(self.frame_7, 0, 1, 1, 1)

        self.frame_8 = QFrame(self.frame_10)
        self.frame_8.setObjectName(u"frame_8")
        sizePolicy.setHeightForWidth(self.frame_8.sizePolicy().hasHeightForWidth())
        self.frame_8.setSizePolicy(sizePolicy)
        self.frame_8.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.frame_8.setFrameShape(QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Raised)

        self.gridLayout_6.addWidget(self.frame_8, 1, 0, 1, 1)

        self.frame_6 = QFrame(self.frame_10)
        self.frame_6.setObjectName(u"frame_6")
        sizePolicy.setHeightForWidth(self.frame_6.sizePolicy().hasHeightForWidth())
        self.frame_6.setSizePolicy(sizePolicy)
        self.frame_6.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)

        self.gridLayout_6.addWidget(self.frame_6, 1, 1, 1, 1)

        self.frame_9 = QFrame(self.frame_10)
        self.frame_9.setObjectName(u"frame_9")
        sizePolicy.setHeightForWidth(self.frame_9.sizePolicy().hasHeightForWidth())
        self.frame_9.setSizePolicy(sizePolicy)
        self.frame_9.setMaximumSize(QSize(16777215, 20))
        self.frame_9.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.frame_9.setFrameShape(QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QFrame.Raised)

        self.gridLayout_6.addWidget(self.frame_9, 1, 2, 1, 1)

        self.frame = QFrame(self.frame_10)
        self.frame.setObjectName(u"frame")
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)

        self.gridLayout_6.addWidget(self.frame, 2, 1, 1, 1)


        self.gridLayout.addWidget(self.frame_10, 1, 1, 1, 1)

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

        self.frame_2 = QFrame(self.rightPage)
        self.frame_2.setObjectName(u"frame_2")
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setStyleSheet(u"")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(self.frame_2)
        self.label.setObjectName(u"label")
        font1 = QFont()
        font1.setPointSize(40)
        font1.setBold(False)
        self.label.setFont(font1)
        self.label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.label)


        self.gridLayout_2.addWidget(self.frame_2, 1, 1, 1, 1)

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

        self.frame_3 = QFrame(self.leftPage)
        self.frame_3.setObjectName(u"frame_3")
        sizePolicy.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy)
        self.frame_3.setStyleSheet(u"")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_2 = QLabel(self.frame_3)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font1)
        self.label_2.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.label_2)


        self.gridLayout_3.addWidget(self.frame_3, 1, 1, 1, 1)

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

        self.frame_4 = QFrame(self.upPage)
        self.frame_4.setObjectName(u"frame_4")
        sizePolicy.setHeightForWidth(self.frame_4.sizePolicy().hasHeightForWidth())
        self.frame_4.setSizePolicy(sizePolicy)
        self.frame_4.setStyleSheet(u"")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_4)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_3 = QLabel(self.frame_4)
        self.label_3.setObjectName(u"label_3")
        font2 = QFont()
        font2.setPointSize(50)
        font2.setBold(False)
        self.label_3.setFont(font2)
        self.label_3.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.label_3)


        self.gridLayout_4.addWidget(self.frame_4, 1, 1, 1, 1)

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

        self.frame_5 = QFrame(self.downPage)
        self.frame_5.setObjectName(u"frame_5")
        sizePolicy.setHeightForWidth(self.frame_5.sizePolicy().hasHeightForWidth())
        self.frame_5.setSizePolicy(sizePolicy)
        self.frame_5.setStyleSheet(u"")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_5)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_4 = QLabel(self.frame_5)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font2)
        self.label_4.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_5.addWidget(self.label_4)


        self.gridLayout_5.addWidget(self.frame_5, 1, 1, 1, 1)

        self.horizontalSpacer_11 = QSpacerItem(294, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_11, 1, 2, 1, 1)

        self.verticalSpacer_10 = QSpacerItem(20, 185, QSizePolicy.Minimum, QSizePolicy.Preferred)

        self.gridLayout_5.addItem(self.verticalSpacer_10, 2, 1, 1, 1)

        self.promptsWidgets.addWidget(self.downPage)

        self.verticalLayout.addWidget(self.promptsWidgets)

        TrainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(TrainWindow)

        self.promptsWidgets.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(TrainWindow)
    # setupUi

    def retranslateUi(self, TrainWindow):
        TrainWindow.setWindowTitle(QCoreApplication.translate("TrainWindow", u"MainWindow", None))
        self.startRecordingBtn.setText("")
        self.stopRecordingBtn.setText("")
        self.helpBtn.setText("")
        self.dataTrainingBtn.setText(QCoreApplication.translate("TrainWindow", u"Start training data!", None))
        self.label.setText(QCoreApplication.translate("TrainWindow", u"Right Hand", None))
        self.label_2.setText(QCoreApplication.translate("TrainWindow", u"Left Hand", None))
        self.label_3.setText(QCoreApplication.translate("TrainWindow", u"Tongue", None))
        self.label_4.setText(QCoreApplication.translate("TrainWindow", u"Feet", None))
    # retranslateUi

