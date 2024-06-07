import os
import sys
import json
import csv
from random import randint
import subprocess
from ui_interface import *
from ui_splashscreen import *
from ui_ERDSWindow import Ui_ERDSWindow
from ui_userWindow import Ui_UserWindow
from Custom_Widgets import *
from PySide6.QtWidgets import QInputDialog, QMessageBox, QSplashScreen
#from PyQt6.QtCore import Qt
from PySide6.QtCore import Qt, QTimer, Slot, Signal
import random
import numpy as np
import time
import pyqtgraph as pg
from pylsl import StreamInlet, resolve_stream

class SplashScreen(QSplashScreen):
    def __init__(self):
        super(SplashScreen, self).__init__()
        self.ui = Ui_SplashScreen()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Initialize progress bar
        self.ui.progressBar.setMinimum(0)
        self.ui.progressBar.setMaximum(100)

        # Set up a timer to update the progress bar
        self.progress_timer = QTimer()
        self.progress_timer.timeout.connect(self.update_progress)
        self.progress_timer.start(100)

        # Counter for tracking progress
        self.progress_value = 0

    def update_progress(self):
        # Increment progress value
        self.progress_value += 1
        self.ui.progressBar.setValue(self.progress_value)

        # Check if progress is complete
        if self.progress_value >= 100:
            self.progress_timer.stop()

    
    def showEvent(self, event):
        super().showEvent(event)
        self.centerSplash()

    def centerSplash(self):
        screen = self.screen()
        screen_geometry = screen.geometry()
        splash_geometry = self.geometry()

        x = (screen_geometry.width() - splash_geometry.width()) // 2
        y = (screen_geometry.height() - splash_geometry.height()) // 2

        self.move(x, y)

#Mainwindow from which everything can be called
class MainWindow(QMainWindow):
    userWindow_to_cursorPage = Signal()
    userWindow_to_game1Page = Signal()
    userWindow_to_game2Page = Signal()
    userWindow_to_trainingPage = Signal()
    userWindow_to_promptPage = Signal()
    userWindow_startRecording = Signal()
    userWindow_stopRecording = Signal()
    userWindow_startPromptTimer = Signal()

    def __init__(self):
        super(MainWindow, self).__init__()

        self.startFFT = False
        self.done_recording = False

        # for EEG cap data
        self.simulate_data = False
        self.streams = resolve_stream()
        try:
            self.inlet = StreamInlet(self.streams[0])
            #Counter init
            # sample, timestamp = self.inlet.pull_sample()
            # self.counter_init = sample[15] 
        except:
            self.show_eeg_error("The EEG cap is not connected. Please connect the cap.")

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("EEG-based BCI")

        #Apply style from the file style.json
        loadJsonStyle(self, self.ui, jsonFiles = {
                        "logs/style.json"
                            }) 
        
        # Predefined colors
        colors = [
            QColor(255, 0, 0),    # Red
            QColor(255, 165, 0),  # Orange
            QColor(144, 238, 144),# Light Green
            QColor(0, 128, 0),    # Green
            QColor(0, 128, 128),  # Blue-Green
            QColor(0, 255, 255),  # Cyan
            QColor(0, 0, 139),    # Dark Blue
            QColor(128, 0, 128),  # Purple
            QColor(255, 0, 255),  # Magenta
            QColor(255, 255, 0),  # Yellow
            QColor(0, 255, 0),    # Green
            QColor(0, 0, 255)     # Blue
        ]

        # Convert to pastel colors
        self.pastel_colors = [self.make_pastel(color) for color in colors]
        
        #Check if the buttons are clicked and evoke their function
        #User page:
        self.ui.addBtn.clicked.connect(self.addUser)
        self.ui.editBtn.clicked.connect(self.editUser)
        self.ui.removeBtn.clicked.connect(self.removeUser)
        self.ui.upBtn.clicked.connect(self.upUser)
        self.ui.downBtn.clicked.connect(self.downUser)
        self.ui.sortBtn.clicked.connect(self.sortUser)
        self.ui.usersList.itemClicked.connect(self.ChooseUser)
        #Menu
        self.ui.reconnectBtn.clicked.connect(self.reconnect_cap)
        self.ui.overviewBtn.clicked.connect(self.changeOverviewBtn)
        self.ui.usersBtn.clicked.connect(self.changeUsersBtn)
        self.ui.demosBtn.clicked.connect(self.changeDemosBtn)
        self.ui.exitBtn.clicked.connect(self.exitApp)
        #Demos submenu
        self.ui.cursorBtn.clicked.connect(self.setCursorPage)
        self.ui.trainBtn.clicked.connect(self.setTrainPage)
        self.ui.game1Btn.clicked.connect(self.setGame1Page)
        self.ui.game2Btn.clicked.connect(self.setGame2Page)
        #Button panel
        self.ui.startRecordingBtn.clicked.connect(self.startRecording)
        self.ui.stopRecordingBtn.clicked.connect(self.stopRecording)
        self.ui.openUserWindowBtn.clicked.connect(self.openUserWindow)
        self.ui.ERDSBtn.clicked.connect(self.openERDSWindow)
        self.ui.openPromptBtn.clicked.connect(self.setPromptPage)
        self.ui.startTimerBtn.clicked.connect(self.startPromptTimer)

        # add users to user list from file
        with open('users.csv', newline='') as user_file:
            user_reader = csv.DictReader(user_file)
            for row in user_reader:
                currentIndex = self.ui.usersList.currentRow()
                self.ui.usersList.insertItem(currentIndex, row["Name"])

        
        #Data live plotting
        self.i = 0
        self.j = 0
        self.max_graph_width = 70
        self.plot_update_size = 10
        self.columns = 7
        self.av_height = int(self.max_graph_width/self.columns)
        self.channel = 1

        self.xdata = np.zeros(self.max_graph_width)
        self.ydata = [np.zeros(self.max_graph_width) for _ in range(8)]
        self.yBarGraph = np.zeros(self.columns)
        symbol_sign = None

        # ML plots
        self.accuracy_data = np.zeros(1)
        self.accuracy_data_iter = np.zeros(1)
        self.loss_data = np.array([100])
        self.loss_data_iter = np.zeros(1)

        # Create subplots and lines
        self.subplots = []
        self.lines = []

        self.j = 0

        self.ui.channelsPlot.setBackground(QColor(255, 255, 255))

        for i in range(8):
            p = self.ui.channelsPlot.addPlot(row=i, col=0)
            p.setMouseEnabled(x=False, y=False)
            p.setMenuEnabled(False)
            export = self.ui.channelsPlot.sceneObj.contextMenu
            del export[:]
            p.hideButtons()
            self.subplots.append(p)
            self.lines.append(p.plot(pen=pg.mkPen(self.pastel_colors[i], width = 2)))
            # p.hideAxis('bottom')
            # p.hideAxis('left')
        # self.subplots[0].setYRange(240500, 241300)
        # self.subplots[1].setYRange(249400, 249900)
        # self.subplots[2].setYRange(278700, 331200)
        # self.subplots[3].setYRange(259500, 296400)
        # self.subplots[4].setYRange(217000, 218000)
        # self.subplots[5].setYRange(239200, 240050)
        # self.subplots[6].setYRange(233100, 234300)
        # self.subplots[7].setYRange(222050, 223100)

        # Bar graph power band
        self.xBarGraph = np.array([2,6,10,14,18,25,40]) #Center points of the columns with according width /<--
        self.power_band_1= pg.BarGraphItem(x=self.xBarGraph[[0,1,2,3,4]], height = self.yBarGraph[[0,1,2,3,4]], width = 4, brush = QColor(0, 166, 214), pen=QColor(255, 255, 255))
        self.power_band_2 = pg.BarGraphItem(x=self.xBarGraph[[5]], height = self.yBarGraph[[5]], width = 10, brush = QColor(0, 166, 214), pen=QColor(255, 255, 255))
        self.power_band_3 = pg.BarGraphItem(x=self.xBarGraph[[6]], height = self.yBarGraph[[6]], width = 20, brush = QColor(0, 166, 214), pen=QColor(255, 255, 255))
        self.ui.powerBandPlot.addItem(self.power_band_1)
        self.ui.powerBandPlot.addItem(self.power_band_2)
        self.ui.powerBandPlot.addItem(self.power_band_3)
        self.ui.powerBandPlot.setYRange(10, 100)
        self.ui.powerBandPlot.setXRange(0, 50)
        self.ui.powerBandPlot.setMouseEnabled(x=False, y=False)
        self.ui.powerBandPlot.setMenuEnabled(False)
        self.ui.powerBandPlot.hideButtons()

        self.start_time = time.time()

        # Add a timer to simulate new temperature measurements
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(3)

        #Stopwatch variables
        self.count = 0
        self.flag = False
        self.ui.stopwatch.setText(str(self.count))
        self.stopwatch = QTimer()
        self.stopwatch.timeout.connect(self.showTime)
        self.stopwatch.start(100)
    
    def make_pastel(self, color, factor=0.5):
        white = QColor(255, 255, 255)
        color = QColor(color)
        return QColor(
            int(color.red() + (white.red() - color.red()) * factor),
            int(color.green() + (white.green() - color.green()) * factor),
            int(color.blue() + (white.blue() - color.blue()) * factor)
        )

    def showTime(self):
 
        # checking if flag is true
        if self.flag:
 
            # incrementing the counter
            self.count+= 1
        else:
            self.count=0
 
        # getting text from count
        if self.count < 47:
            text = "0.0"
        else:
            text = str(float("{:.1f}".format(self.count / 10 - 4.7)))
 
        # showing text
        self.ui.stopwatch.setText(text)

    def setCursorPage(self):
            self.userWindow_to_cursorPage.emit()

    def setGame1Page(self):
            self.userWindow_to_game1Page.emit()
    
    def setGame2Page(self):
            self.userWindow_to_game2Page.emit()
    
    def setTrainPage(self):
            self.userWindow_to_trainingPage.emit()

    def setPromptPage(self):
            self.userWindow_to_promptPage.emit()
            self.ui.stopwatch.setText("0.0")
            self.flag = False
    
    def startRecording(self):
            self.userWindow_startRecording.emit()

    def stopRecording(self):
            self.userWindow_stopRecording.emit()
            self.flag = False

    def startPromptTimer(self):
            self.flag = True
            self.userWindow_startPromptTimer.emit()

    
    def reconnect_cap(self):
        try:
            self.inlet = StreamInlet(self.streams[0])
            dlg = QMessageBox()
            dlg.setWindowTitle("EEG cap connected")
            dlg.setText("The EEG cap is succesfully connected. The data shown will now be the real data.")
            button = dlg.exec()
            self.simulate_data = False
            self.xdata = np.zeros(self.max_graph_width)
            self.ydata = [np.zeros(self.max_graph_width) for _ in range(8)]
            self.i = 0
        except:
            self.show_eeg_error("The EEG cap could not connect. Please try again.")
    
    def show_eeg_error(self, error_text):
        dlg = QMessageBox()
        dlg.setWindowTitle("ERROR")
        dlg.setStandardButtons(QMessageBox.StandardButton.Retry | QMessageBox.StandardButton.Ignore)
        dlg.setText(error_text)
        
        screen = self.screen()
        screen_geometry = screen.geometry()
        splash_geometry = self.geometry()

        x = (screen_geometry.width() - splash_geometry.width()) // 2
        y = 0#(screen_geometry.height() - 1.5*splash_geometry.height()) // 2

        dlg.move(x, y)
        button = dlg.exec()

        if button == QMessageBox.StandardButton.Retry:
            print("retrying....")
            try:
                self.inlet = StreamInlet(self.streams[0])
                self.simulate_data = False
            except:
                self.show_eeg_error(error_text)
        elif button == QMessageBox.StandardButton.Ignore:
            dlg = QMessageBox()
            dlg.setWindowTitle("Ignored")
            dlg.setText("The program will now run without the EEG cap data and will use simulated data. "
                        "To use the EEG cap restart the program.")
            dlg.move(x, y)
            button = dlg.exec()
            self.simulate_data = True
        
    # Update graphs
    def update_plot(self):
        pen = pg.mkPen(self.pastel_colors[self.channel - 1], width = 2)
        # gathering the data from the EEG cap
        if not self.simulate_data:
            sample, timestamp = self.inlet.pull_sample()
            sample_timestamp = (self.i) / 250
        else:
            sample, timestamp = self.generate_random_sample()  # for testing purposes when not connected to cap
            sample_timestamp = self.i / 250

        if self.i <= self.max_graph_width:
            self.xdata[self.j:] = sample_timestamp
            for k in range(8):
                self.ydata[k][self.j] = sample[k]
        else:
            if not self.startFFT:
                self.startFFT = True
                print(self.channel)
                symbol_sign = None
                self.FFT_plot = self.ui.FFTPlot.plot(
                    self.xdata,
                    self.ydata[self.channel - 1],
                    name="Power Sensor",
                    pen=pen,
                    symbol=symbol_sign,
                    symbolSize=5,
                    symbolBrush="b",
                )
                self.ui.FFTPlot.setXRange(5, 40)
                self.ui.FFTPlot.setYRange(0, 50)
                self.ui.FFTPlot.setMouseEnabled(x=False, y=False)
                self.ui.FFTPlot.setMenuEnabled(False)
                self.ui.FFTPlot.hideButtons()
                self.FFT_plot.setFftMode(True)

            self.xdata = np.roll(self.xdata, -1)
            self.xdata[-1] = sample_timestamp
            for k in range(8):
                self.ydata[k] = np.roll(self.ydata[k], -1)
                self.ydata[k][-1] = sample[k]

        #only update the plot everytime it has collected plot update data sized data
        if self.i % self.plot_update_size == 0:
            for i in range(8):
                self.lines[i].setData(self.xdata, self.ydata[i])
            self.power_band_1.setOpts(height=self.yBarGraph[[0, 1, 2, 3, 4]], brush=pg.mkBrush(self.pastel_colors[self.channel - 1]))
            self.power_band_2.setOpts(height=self.yBarGraph[[5]], brush=pg.mkBrush(self.pastel_colors[self.channel - 1]))
            self.power_band_3.setOpts(height=self.yBarGraph[[6]], brush=pg.mkBrush(self.pastel_colors[self.channel - 1]))

            if self.startFFT:
                self.FFT_plot.setData(self.xdata, self.ydata[self.channel - 1])
                self.FFT_plot.setPen(pg.mkPen(self.pastel_colors[self.channel - 1], width = 2))

            # change the power band plots from channel
            self.yBarGraph = np.array(
                [sum(self.ydata[self.channel - 1][i:i + self.av_height]) // self.av_height for i in
                 range(0, len(self.ydata[self.channel - 1]), self.av_height)])

        self.i += 1
        if self.i == 1000:
            print(time.time() - self.start_time)

    # for testing purposes
    def generate_random_sample(self):
        # Simulate random data generation
        return random.sample(range(0, 100), 15) + [time.time()], 0

    def setUserWindow(self, userWindow):
        self.userWindow = userWindow

    #Call the training window
    #def openUserWindow(self):
    #    #global recProcess
    #    #recProcess = subprocess.Popen(["python3", "-u", "MeasurementSubgroup/Streaming/LSL_csv.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,)
    #    
    #    self.userWindow.show()

    def setERDSWindow(self, ERDSWindow):
        self.ERDSWindow = ERDSWindow

    #Call the training window
    def openERDSWindow(self):
        #global recProcess
        #recProcess = subprocess.Popen(["python3", "-u", "MeasurementSubgroup/Streaming/LSL_csv.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,)
        
        self.ERDSWindow.show()

    def openUserWindow(self):
        global recProcess
        if self.userWindow.isVisible():
            pass
        else:
            recProcess = subprocess.Popen(["python3", "-u", "MeasurementSubgroup/Streaming/LSL_csv.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,)
            self.userWindow.show()

    def exitApp(self):
        QApplication.quit()
    '''
    @Slot()
    def handle_signal_trainData(self):  # will start training the ML model on the new data
        # TODO sent signal and data to ML part to actually start the training
        self.accuracy_data = np.append(self.accuracy_data, random.sample(range(int(self.accuracy_data[-1]), 100), 1))
        self.accuracy_data_iter = np.append(self.accuracy_data_iter, self.accuracy_data_iter[-1] + 1)
        self.loss_data = np.append(self.loss_data, random.sample(range(0, self.loss_data[-1] + 1), 1))
        self.loss_data_iter = np.append(self.loss_data_iter, self.loss_data_iter[-1] + 1)
        self.update_ML_plots()
    '''
    #Function that handles the user based interface
    def ChooseUser(self, item):
        if type(item) is str:
            self.ui.userID_test.setText(item)
            self.current_id = None
            with open('users.csv', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['Name'] == item:
                        self.current_id = row['ID']
            if not self.current_id:
                print("ERROR: USER " + item + " HAS NO CORRESPONDING ID.")

        else:
            self.ui.userID_test.setText(item.text())
            self.current_id = None
            with open('users.csv', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['Name'] == item.text():
                        self.current_id = row['ID']
            if not self.current_id:
                print("ERROR: USER " + item.text() + " HAS NO CORRESPONDING ID.")
        print(self.current_id)

    #Functions for the buttons on the user page
    def changeOverviewBtn(self):
        if self.ui.mainPages.currentIndex() == 0:
            self.ui.overviewBtn.setStyleSheet("background-color: rgb(0, 118, 194);")
            self.ui.usersBtn.setStyleSheet("background-color: rgb(0, 166, 214);")
            self.ui.demosBtn.setStyleSheet("background-color: rgb(0, 166, 214);")

    def changeUsersBtn(self):
        if self.ui.mainPages.currentIndex() == 1:
            self.ui.usersBtn.setStyleSheet("background-color: rgb(0, 118, 194);")
            self.ui.overviewBtn.setStyleSheet("background-color: rgb(0, 166, 214);")
            self.ui.demosBtn.setStyleSheet("background-color: rgb(0, 166, 214);")

    def changeDemosBtn(self):
        self.ui.demosBtn.setStyleSheet("background-color: rgb(0, 118, 194);")

    def addUser(self):
        currentIndex = self.ui.usersList.currentRow()
        error = ""
        while True:
            if error:
                text, ok = QInputDialog.getText(None, "New User", error)
            else:
                text, ok = QInputDialog.getText(None, "New User", "User Name")
            error = ""
            if ok and text is not None:
                if text == "":
                    error = "Please fill in a valid username"
                with open('users.csv', newline='') as user_file:
                    reader = csv.DictReader(user_file)
                    highest_id = 0
                    for row in reader:
                        if int(row["ID"]) > highest_id:
                            highest_id = int(row["ID"])
                        if row["Name"] == text:
                            error = "This user already exists"
                if not error:
                    with open('users.csv', 'a+', newline='') as user_file:
                        writer = csv.writer(user_file)
                        writer.writerow([text, highest_id + 1])
                    self.ui.usersList.insertItem(currentIndex, text)
                    self.ChooseUser(text)
                    return
            else:
                return
            

    def editUser(self):
        currentIndex = self.ui.usersList.currentRow()
        item = self.ui.usersList.item(currentIndex)
        if item is not None:
            error = ""
            while True:
                if error:
                    text, ok = QInputDialog.getText(None, "Change Username", error)
                else:
                    text, ok = QInputDialog.getText(None, "Change Username", "User Name")
                error = ""
                if ok and text is not None:
                    if text == "":
                        error = "Please fill in a valid username"

                    rows = []
                    with open('users.csv', newline='') as file:
                        reader = csv.DictReader(file)
                        for row in reader:
                            if row["Name"] == text and text != item.text():
                                error = "This user already exists"
                            elif row['Name'] == item.text():  # Update the name for the corresponding user
                                row['Name'] = text
                            rows.append(row)
                    if not error:
                        with open('users.csv', 'w', newline='') as file:
                            writer = csv.DictWriter(file, fieldnames=['Name', 'ID'])
                            writer.writeheader()
                            writer.writerows(rows)
                        item.setText(text)
                        self.ChooseUser(text)
                        return
                else:
                    return
            
    def removeUser(self):
        currentIndex = self.ui.usersList.currentRow()
        item = self.ui.usersList.item(currentIndex)
        if item is None:
            return

        question = QMessageBox.question(None,"Remove User",
             "Do you want to remove user: " + item.text(),
             QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if question == QMessageBox.StandardButton.Yes:
            rows = []
            with open('users.csv', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['Name'] != item.text():  # Update the name for the corresponding user
                        rows.append(row)
            with open('users.csv', 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['Name', 'ID'])
                writer.writeheader()
                writer.writerows(rows)
            item = self.ui.usersList.takeItem(currentIndex)
            del item
            del item

    def upUser(self):
        index = self.ui.usersList.currentRow()
        if index >= 1:
            item = self.ui.usersList.takeItem(index)
            self.ui.usersList.insertItem(index-1,item)
            self.ui.usersList.setCurrentItem(item)

    def downUser(self):
        index = self.ui.usersList.currentRow()
        if index < self.ui.usersList.count()-1:
            item = self.ui.usersList.takeItem(index)
            self.ui.usersList.insertItem(index + 1, item)
            self.ui.usersList.setCurrentItem(item)

    def sortUser(self):
        self.ui.usersList.sortItems()
    
    # for test controlling the "mouse"
    # TODO make the ML output prediction do this
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_1:
            self.yBarGraph = np.array([sum(self.ydata[0][i:i+self.av_height])//self.av_height for i in range(0,len(self.ydata[0]),self.av_height)])
            self.channel = 1
        elif event.key() == Qt.Key.Key_2:
            self.yBarGraph = np.array([sum(self.ydata[1][i:i+self.av_height])//self.av_height for i in range(0,len(self.ydata[1]),self.av_height)])
            self.channel = 2
        elif event.key() == Qt.Key.Key_3:
            self.yBarGraph = np.array([sum(self.ydata[2][i:i+self.av_height])//self.av_height for i in range(0,len(self.ydata[2]),self.av_height)])
            self.channel = 3
        elif event.key() == Qt.Key.Key_4:
            self.yBarGraph = np.array([sum(self.ydata[3][i:i+self.av_height])//self.av_height for i in range(0,len(self.ydata[3]),self.av_height)])
            self.channel = 4
        elif event.key() == Qt.Key.Key_5:
            self.yBarGraph = np.array([sum(self.ydata[4][i:i+self.av_height])//self.av_height for i in range(0,len(self.ydata[4]),self.av_height)])
            self.channel = 5
        elif event.key() == Qt.Key.Key_6:
            self.yBarGraph = np.array([sum(self.ydata[5][i:i+self.av_height])//self.av_height for i in range(0,len(self.ydata[5]),self.av_height)])
            self.channel = 6
        elif event.key() == Qt.Key.Key_7:
            self.yBarGraph = np.array([sum(self.ydata[6][i:i+self.av_height])//self.av_height for i in range(0,len(self.ydata[6]),self.av_height)])
            self.channel = 7
        elif event.key() == Qt.Key.Key_8:
            self.yBarGraph = np.array([sum(self.ydata[7][i:i+self.av_height])//self.av_height for i in range(0,len(self.ydata[7]),self.av_height)])
            self.channel = 8
        '''

        # to simulate the accuracy plot
        if event.key() == Qt.Key_P:
            self.accuracy_data = np.append(self.accuracy_data, random.sample(range(int(self.accuracy_data[-1]), 100), 1))
            self.accuracy_data_iter = np.append(self.accuracy_data_iter, self.accuracy_data_iter[-1] + 1)
            self.loss_data = np.append(self.loss_data, random.sample(range(0, self.loss_data[-1] + 1), 1))
            self.loss_data_iter = np.append(self.loss_data_iter, self.loss_data_iter[-1] + 1)
            self.update_ML_plots()

        self.update()

    # updating the Machine Learning plots while training
    def update_ML_plots(self):
        # when it's the first time after recording we want to clear the previous plots
        if self.done_recording == False:
            # if the FFT and frequency band plots were used, clear them
            if self.startFFT:
                self.line_17.clear()
                self.ui.graphicsView_18.clear()
                self.line_19.clear()
                self.ui.graphicsView_20.clear()
            self.done_recording = True
            pen = pg.mkPen(color=(255, 0, 0))
            symbol_sign = None
            self.line_17 = self.ui.graphicsView_17.plot(
                self.accuracy_data_iter,
                self.accuracy_data,
                name="Power Sensor",
                pen=pen,
                symbol=symbol_sign,
                symbolSize=5,
                symbolBrush="b",
            )
            self.line_18 = self.ui.graphicsView_18.plot(
                self.loss_data_iter,
                self.loss_data,
                name="Power Sensor",
                pen=pen,
                symbol=symbol_sign,
                symbolSize=5,
                symbolBrush="b",
            )
            self.line_19 = self.ui.graphicsView_19.plot(
                self.accuracy_data_iter,
                self.accuracy_data,
                name="Power Sensor",
                pen=pen,
                symbol=symbol_sign,
                symbolSize=5,
                symbolBrush="b",
            )
            self.line_20 = self.ui.graphicsView_20.plot(
                self.loss_data_iter,
                self.loss_data,
                name="Power Sensor",
                pen=pen,
                symbol=symbol_sign,
                symbolSize=5,
                symbolBrush="b",
            )

        # update the plots with the new data
        self.line_17.setData(self.accuracy_data_iter, self.accuracy_data)
        self.line_18.setData(self.loss_data_iter, self.loss_data)
        self.line_19.setData(self.accuracy_data_iter, self.accuracy_data)
        self.line_20.setData(self.loss_data_iter, self.loss_data)
    '''

#User window class
class UserWindow(QMainWindow):
    signal_to_trainData = Signal()

    def __init__(self):
        super(UserWindow, self).__init__()
        self.ui = Ui_UserWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("User Window")
        
        #Timer
        self.timer = QTimer()
        self.promptTimer = QTimer()

        self.stepsize = 10
        #Check clicked buttons and call their respective functions
        self.timer.timeout.connect(lambda: self.changePages())
        self.promptTimer.timeout.connect(lambda: self.changePrompt())

        #self.ui.dataTrainingBtn.clicked.connect(self.trainingData)

        #cap
        self.streams = resolve_stream()
        self.inlet = StreamInlet(self.streams[0])

        self.grid_layout = QGridLayout(self.ui.game1Widget)

        #Tic Tac Toe
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_over = False

        for row in range(3):
            for col in range(3):
                button = QPushButton("")
                button.setFixedSize(QSize(100, 100))
                font = button.font()
                font.setPointSize(24)
                button.setFont(font)
                button.clicked.connect(lambda _, r=row, c=col: self.on_button_clicked(r, c))
                self.grid_layout.addWidget(button, row, col)
                self.buttons[row][col] = button

    def on_button_clicked(self, row, col):
        if self.game_over or self.buttons[row][col].text():
            return

        self.buttons[row][col].setText(self.current_player)
        if self.check_winner():
            self.show_winner(self.current_player)
            self.game_over = True
        elif self.is_draw():
            self.show_winner("No one")
            self.game_over = True
        else:
            self.current_player = 'O' if self.current_player == 'X' else 'X'

    def check_winner(self):
        for row in range(3):
            if self.buttons[row][0].text() == self.buttons[row][1].text() == self.buttons[row][2].text() != '':
                return True
        for col in range(3):
            if self.buttons[0][col].text() == self.buttons[1][col].text() == self.buttons[2][col].text() != '':
                return True
        if self.buttons[0][0].text() == self.buttons[1][1].text() == self.buttons[2][2].text() != '':
            return True
        if self.buttons[0][2].text() == self.buttons[1][1].text() == self.buttons[2][0].text() != '':
            return True
        return False

    def is_draw(self):
        for row in range(3):
            for col in range(3):
                if not self.buttons[row][col].text():
                    return False
        return True

    def show_winner(self, winner):
        msg = QMessageBox()
        msg.setWindowTitle("Game Over")
        msg.setText(f"{winner} wins!")
        msg.exec()

    def trainingData(self):
        self.signal_to_trainData.emit()
        self.close()

    @Slot()
    def startRecording(self):
        global count
        global pageArray
        global i
        i = 0
        count = 0
        pageArray = [1,2,3,4 ,4,3,2,1 ,2,3,4,1 ,1,3,4,2 ,3,2,4,1 ,4,1,2,3, 0]
        recProcess.stdout.read1(1)
        if count == 0:
            recProcess.stdin.write(b"G\n") # G for go
        else:
            recProcess.stdin.write(b"S\n") # G for go
        recProcess.stdin.flush()
        self.timer.start(100)



    @Slot()
    def startPromptTimer(self):
            self.promptTimer.start(5000)

    def changePrompt(self):
            self.ui.promptTestWidget.setCurrentWidget(self.ui.promptPromptPage)
            self.promptTimer.stop()

    def changePages(self):
        if self.ui.demosPages.currentWidget() == self.ui.trainingPage:
            global count
            global pageArray
            global i

            pageNumber = pageArray[i]

            if count % 2 != 0:
                self.ui.promptsWidgets.setCurrentWidget(self.ui.calibrationPage)
            else:
                self.ui.promptsWidgets.setCurrentIndex(pageNumber)
                i = i + 1
            if count == 47:
                self.timer.stop()

            count = count + 1

    @Slot()
    def stopRecording(self):
        self.count = 47
        recProcess.stdin.write(b"Stop\n")
        self.timer.stop()
        self.ui.promptsWidgets.setCurrentWidget(self.ui.calibrationPage)

    def help(self):
        QMessageBox.information(None,"Help",
        "Instructions and their respective outputs:\nleft hand -> left\nright hand -> right\nfeet -> down\ntongue -> up",
        QMessageBox.StandardButton.Ok)

    @Slot()
    def handle_signal_cursorPage(self):
        self.ui.demosPages.setCurrentWidget(self.ui.cursorPage)
    @Slot()
    def handle_signal_trainingPage(self):
        self.ui.demosPages.setCurrentWidget(self.ui.trainingPage)
    @Slot()
    def handle_signal_promptPage(self):
        self.ui.demosPages.setCurrentWidget(self.ui.promptPage)
        self.ui.promptTestWidget.setCurrentWidget(self.ui.calibrationPromptPage)
        self.promptTimer.stop()
    @Slot()
    def handle_signal_game1Page(self):
        self.ui.demosPages.setCurrentWidget(self.ui.game1Page)
    @Slot()
    def handle_signal_game2Page(self):
        self.ui.demosPages.setCurrentWidget(self.ui.game2Page)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_W:
            if self.ui.mouseCursor.y() - self.stepsize > 0:
                self.ui.mouseCursor.move(self.ui.mouseCursor.x(), self.ui.mouseCursor.y() - self.stepsize)
        elif event.key() == Qt.Key_A:
            if self.ui.mouseCursor.x() - self.stepsize > 0:
                self.ui.mouseCursor.move(self.ui.mouseCursor.x() - self.stepsize, self.ui.mouseCursor.y())
        elif event.key() == Qt.Key_S:
            if self.ui.mouseCursor.y() + self.stepsize < (self.ui.cursorFrame.height() - self.ui.mouseCursor.height()):
                self.ui.mouseCursor.move(self.ui.mouseCursor.x(), self.ui.mouseCursor.y() + self.stepsize)
        elif event.key() == Qt.Key_D:
            if self.ui.mouseCursor.x() + self.stepsize < (self.ui.cursorFrame.width() - self.ui.mouseCursor.width()):
                self.ui.mouseCursor.move(self.ui.mouseCursor.x() + self.stepsize, self.ui.mouseCursor.y())


#ERDS window class
class ERDSWindow(QMainWindow):

    def __init__(self):
        super(ERDSWindow, self).__init__()
        self.ui = Ui_ERDSWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("ERDS Window")
        
def show_main_window():
    window1.showMaximized()
    window1.show()

    splash.finish(window1)

#Creates the app and runs the Mainwindow
if __name__ == "__main__":

    path = './users.csv'
    if not os.path.isfile(path):
        with open('users.csv', 'w') as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "ID"])

    app = QApplication(sys.argv)

    
    splash = SplashScreen()
    splash.show()

    window1 = MainWindow()
    window2 = UserWindow()
    window3 = ERDSWindow()

    window1.setUserWindow(window2)
    window1.setERDSWindow(window3)
    
    #window2.signal_to_trainData.connect(window1.handle_signal_trainData)
    window1.userWindow_to_cursorPage.connect(window2.handle_signal_cursorPage)
    window1.userWindow_to_promptPage.connect(window2.handle_signal_promptPage)
    window1.userWindow_to_trainingPage.connect(window2.handle_signal_trainingPage)
    window1.userWindow_to_game1Page.connect(window2.handle_signal_game1Page)
    window1.userWindow_to_game2Page.connect(window2.handle_signal_game2Page)
    window1.userWindow_startRecording.connect(window2.startRecording)
    window1.userWindow_stopRecording.connect(window2.stopRecording)
    window1.userWindow_startPromptTimer.connect(window2.startPromptTimer)

    QTimer.singleShot(3000, show_main_window)
    
    sys.exit(app.exec_())