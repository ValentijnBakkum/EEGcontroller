import os
import sys
import json
import csv
from random import randint
import subprocess
from ui_interface import *
from ui_trainWindow import Ui_TrainWindow
from Custom_Widgets import *
from PyQt6.QtWidgets import QInputDialog, QMessageBox
from PySide6.QtCore import QTimer, Slot, Signal
import random
import numpy as np
import time
import pyqtgraph as pg
from pylsl import StreamInlet, resolve_stream

#Mainwindow from which everything can be called
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.stepsize = 5
        self.startFFT = False
        self.done_recording = False

        # for EEG cap data
        self.simulate_data = False
        try:
            self.streams = resolve_stream()
            self.inlet = StreamInlet(self.streams[0])

            # Counter init
            sample, timestamp = self.inlet.pull_sample()
            self.counter_init = sample[15] 

        except:
            self.show_eeg_error("The EEG cap is not connected. Please connect the cap.")
            self.counter_init = 0

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("EEG-based BCI")

        #Apply style from the file style.json
        loadJsonStyle(self, self.ui, jsonFiles = {
                        "logs/style.json"
                            }) 
        
        #Check if the buttons are clicked and evoke their function
        #User page:
        self.ui.addBtn.clicked.connect(self.addUser)
        self.ui.editBtn.clicked.connect(self.editUser)
        self.ui.removeBtn.clicked.connect(self.removeUser)
        self.ui.upBtn.clicked.connect(self.upUser)
        self.ui.downBtn.clicked.connect(self.downUser)
        self.ui.sortBtn.clicked.connect(self.sortUser)
        self.ui.usersList.itemClicked.connect(self.ChooseUser)
        #menu
        self.ui.reconnectBtn.clicked.connect(self.reconnect_cap)
        self.ui.trainBtn.clicked.connect(self.changeTrainBtn)
        self.ui.testBtn.clicked.connect(self.changeTestBtn)
        self.ui.usersBtn.clicked.connect(self.changeUsersBtn)
        self.ui.exitBtn.clicked.connect(self.exitApp)
        #Training window
        self.ui.startTrainBtn.clicked.connect(self.openTrainWindow)

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
        self.plot_delay = 5
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

        pen = pg.mkPen(color=(255, 0, 0))
        # Get a line reference
        self.line = self.ui.graphicsView.plot(
            self.xdata,
            self.ydata[0],
            name="Power Sensor",
            pen=pen,
            symbol=symbol_sign,
            symbolSize=5,
            symbolBrush="b",
        )
        self.line_2 = self.ui.graphicsView_2.plot(
            self.xdata,
            self.ydata[1],
            name="Power Sensor",
            pen=pen,
            symbol=symbol_sign,
            symbolSize=5,
            symbolBrush="b",
        )
        self.line_3 = self.ui.graphicsView_3.plot(
            self.xdata,
            self.ydata[2],
            name="Power Sensor",
            pen=pen,
            symbol=symbol_sign,
            symbolSize=5,
            symbolBrush="b",
        )
        self.line_4 = self.ui.graphicsView_4.plot(
            self.xdata,
            self.ydata[3],
            name="Power Sensor",
            pen=pen,
            symbol=symbol_sign,
            symbolSize=5,
            symbolBrush="b",
        )
        self.line_5 = self.ui.graphicsView_5.plot(
            self.xdata,
            self.ydata[4],
            name="Power Sensor",
            pen=pen,
            symbol=symbol_sign,
            symbolSize=5,
            symbolBrush="b",
        )
        self.line_6 = self.ui.graphicsView_6.plot(
            self.xdata,
            self.ydata[5],
            name="Power Sensor",
            pen=pen,
            symbol=symbol_sign,
            symbolSize=5,
            symbolBrush="b",
        )
        self.line_7 = self.ui.graphicsView_7.plot(
            self.xdata,
            self.ydata[6],
            name="Power Sensor",
            pen=pen,
            symbol=symbol_sign,
            symbolSize=5,
            symbolBrush="b",
        )
        self.line_8 = self.ui.graphicsView_8.plot(
            self.xdata,
            self.ydata[7],
            name="Power Sensor",
            pen=pen,
            symbol=symbol_sign,
            symbolSize=5,
            symbolBrush="b",
        )
        self.line_9 = self.ui.graphicsView_9.plot(
            self.xdata,
            self.ydata[0],
            name="Power Sensor",
            pen=pen,
            symbol=symbol_sign,
            symbolSize=5,
            symbolBrush="b",
        )
        self.line_10 = self.ui.graphicsView_10.plot(
            self.xdata,
            self.ydata[1],
            name="Power Sensor",
            pen=pen,
            symbol=symbol_sign,
            symbolSize=5,
            symbolBrush="b",
        )
        self.line_11 = self.ui.graphicsView_11.plot(
            self.xdata,
            self.ydata[2],
            name="Power Sensor",
            pen=pen,
            symbol=symbol_sign,
            symbolSize=5,
            symbolBrush="b",
        )
        self.line_12 = self.ui.graphicsView_12.plot(
            self.xdata,
            self.ydata[3],
            name="Power Sensor",
            pen=pen,
            symbol=symbol_sign,
            symbolSize=5,
            symbolBrush="b",
        )
        self.line_13 = self.ui.graphicsView_13.plot(
            self.xdata,
            self.ydata[4],
            name="Power Sensor",
            pen=pen,
            symbol=symbol_sign,
            symbolSize=5,
            symbolBrush="b",
        )
        self.line_14 = self.ui.graphicsView_14.plot(
            self.xdata,
            self.ydata[5],
            name="Power Sensor",
            pen=pen,
            symbol=symbol_sign,
            symbolSize=5,
            symbolBrush="b",
        )
        self.line_15 = self.ui.graphicsView_15.plot(
            self.xdata,
            self.ydata[6],
            name="Power Sensor",
            pen=pen,
            symbol=symbol_sign,
            symbolSize=5,
            symbolBrush="b",
        )
        self.line_16 = self.ui.graphicsView_16.plot(
            self.xdata,
            self.ydata[7],
            name="Power Sensor",
            pen=pen,
            symbol=symbol_sign,
            symbolSize=5,
            symbolBrush="b",
        )
        # Bar graph power band
        self.xBarGraph = np.array([2,6,10,14,18,25,40]) #Center points of the columns with according width /<--
        self.line_18_1 = pg.BarGraphItem(x=self.xBarGraph[[0,1,2,3,4]], height = self.yBarGraph[[0,1,2,3,4]], width = 4, brush = QColor(0, 166, 214), pen=QColor(255, 255, 255))
        self.line_18_2 = pg.BarGraphItem(x=self.xBarGraph[[5]], height = self.yBarGraph[[5]], width = 10, brush = QColor(0, 166, 214), pen=QColor(255, 255, 255))
        self.line_18_3 = pg.BarGraphItem(x=self.xBarGraph[[6]], height = self.yBarGraph[[6]], width = 20, brush = QColor(0, 166, 214), pen=QColor(255, 255, 255))
        self.ui.graphicsView_18.addItem(self.line_18_1)
        self.ui.graphicsView_18.addItem(self.line_18_2)
        self.ui.graphicsView_18.addItem(self.line_18_3)
        self.ui.graphicsView_18.setYRange(10,100)
        self.ui.graphicsView_18.setXRange(0,50)

        self.line_20_1 = pg.BarGraphItem(x=self.xBarGraph[[0,1,2,3,4]], height = self.yBarGraph[[0,1,2,3,4]], width = 4, brush = QColor(0, 166, 214), pen=QColor(255, 255, 255))
        self.line_20_2 = pg.BarGraphItem(x=self.xBarGraph[[5]], height = self.yBarGraph[[5]], width = 10, brush = QColor(0, 166, 214), pen=QColor(255, 255, 255))
        self.line_20_3 = pg.BarGraphItem(x=self.xBarGraph[[6]], height = self.yBarGraph[[6]], width = 20, brush = QColor(0, 166, 214), pen=QColor(255, 255, 255))
        self.ui.graphicsView_20.addItem(self.line_20_1)
        self.ui.graphicsView_20.addItem(self.line_20_2)
        self.ui.graphicsView_20.addItem(self.line_20_3)
        self.ui.graphicsView_20.setYRange(10,100)
        self.ui.graphicsView_20.setXRange(0,50)

        # Add a timer to simulate new temperature measurements
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

        
        self.show()

    def reconnect_cap(self):
        try:
            self.streams = resolve_stream()
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
        button = dlg.exec()

        if button == QMessageBox.StandardButton.Retry:
            print("retrying....")
            try:
                self.streams = resolve_stream()
                self.inlet = StreamInlet(self.streams[0])
                self.simulate_data = False
            except:
                self.show_eeg_error(error_text)
        elif button == QMessageBox.StandardButton.Ignore:
            dlg = QMessageBox()
            dlg.setWindowTitle("Ignored")
            dlg.setText("The program will now run without the EEG cap data and will use simulated data. "
                        "To use the EEG cap restart the program.")
            button = dlg.exec()
            self.simulate_data = True
        
    # Update graphs
    def update_plot(self):
        self.j = self.i // self.plot_delay

        if self.i % self.plot_delay:
            # gathering the data from the EEG cap
            if not self.simulate_data:
                sample, timestamp = self.inlet.pull_sample()
            else:
                sample, timestamp = self.generate_random_sample()  # for testing purposes when not connected to cap
            sample_timestamp = (sample[15] - self.counter_init)

            if self.j < self.ydata[0].size:
                self.xdata[self.j:] = sample_timestamp
            else:
                self.xdata = np.append(self.xdata[1:], sample_timestamp)
                # start creating the FFT plot
                if self.startFFT == False:
                    pen = pg.mkPen(color=(255, 0, 0))
                    symbol_sign = None
                    self.line_17 = self.ui.graphicsView_17.plot(
                        self.xdata,
                        self.ydata[0],
                        name="Power Sensor",
                        pen=pen,
                        symbol=symbol_sign,
                        symbolSize=5,
                        symbolBrush="b",
                    )
                    self.ui.graphicsView_17.setXRange(0,60)
                    self.line_17.setFftMode(True)
                    self.line_19 = self.ui.graphicsView_19.plot(
                        self.xdata,
                        self.ydata[0],
                        name="Power Sensor",
                        pen=pen,
                        symbol=symbol_sign,
                        symbolSize=5,
                        symbolBrush="b",
                    )
                    self.ui.graphicsView_19.setXRange(0,60)
                    self.line_19.setFftMode(True)
                    self.startFFT = True

            # update the data arrays
            k = 0
            while k < 8:
                if self.j < self.ydata[0].size:
                    self.ydata[k][self.j:] = sample[k]
                else:
                    self.ydata[k] = np.append(self.ydata[k][1:], sample[k])
                k += 1

            if self.channel == 1:
                self.yBarGraph = np.array([sum(self.ydata[0][i:i+self.av_height])//self.av_height for i in range(0,len(self.ydata[0]),self.av_height)])
            elif self.channel == 2:
                self.yBarGraph = np.array([sum(self.ydata[1][i:i+self.av_height])//self.av_height for i in range(0,len(self.ydata[1]),self.av_height)])
            elif self.channel == 3:
                self.yBarGraph = np.array([sum(self.ydata[2][i:i+self.av_height])//self.av_height for i in range(0,len(self.ydata[2]),self.av_height)])
            elif self.channel == 4:
                self.yBarGraph = np.array([sum(self.ydata[3][i:i+self.av_height])//self.av_height for i in range(0,len(self.ydata[3]),self.av_height)])
            elif self.channel == 5:
                self.yBarGraph = np.array([sum(self.ydata[4][i:i+self.av_height])//self.av_height for i in range(0,len(self.ydata[4]),self.av_height)])
            elif self.channel == 6:
                self.yBarGraph = np.array([sum(self.ydata[5][i:i+self.av_height])//self.av_height for i in range(0,len(self.ydata[5]),self.av_height)])
            elif self.channel == 7:
                self.yBarGraph = np.array([sum(self.ydata[6][i:i+self.av_height])//self.av_height for i in range(0,len(self.ydata[6]),self.av_height)])
            elif self.channel == 8:
                self.yBarGraph = np.array([sum(self.ydata[7][i:i+self.av_height])//self.av_height for i in range(0,len(self.ydata[7]),self.av_height)])

        # update the plots with the new data
        # depending on which screen is active
        if self.ui.mainPages.currentIndex() == 2:  # training mode
            self.line.setData(self.xdata, self.ydata[0])
            self.line_2.setData(self.xdata, self.ydata[1])
            self.line_3.setData(self.xdata, self.ydata[2])
            self.line_4.setData(self.xdata, self.ydata[3])
            self.line_5.setData(self.xdata, self.ydata[4])
            self.line_6.setData(self.xdata, self.ydata[5])
            self.line_7.setData(self.xdata, self.ydata[6])
            self.line_8.setData(self.xdata, self.ydata[7])
            if self.startFFT and not self.done_recording:
                if self.channel == 1:
                    self.line_17.setData(self.xdata, self.ydata[0])
                elif self.channel == 2:
                    self.line_17.setData(self.xdata, self.ydata[1])
                elif self.channel == 3:
                    self.line_17.setData(self.xdata, self.ydata[2])
                elif self.channel == 4:
                    self.line_17.setData(self.xdata, self.ydata[3])
                elif self.channel == 5:
                    self.line_17.setData(self.xdata, self.ydata[4])
                elif self.channel == 6:
                    self.line_17.setData(self.xdata, self.ydata[5])
                elif self.channel == 7:
                    self.line_17.setData(self.xdata, self.ydata[6])
                elif self.channel == 8:
                    self.line_17.setData(self.xdata, self.ydata[7])
                self.line_18_1.setOpts(height = self.yBarGraph[[0,1,2,3,4]])
                self.line_18_2.setOpts(height = self.yBarGraph[[5]])
                self.line_18_3.setOpts(height = self.yBarGraph[[6]])
        if self.ui.mainPages.currentIndex() == 0:  # testing mode
            self.line_9.setData(self.xdata, self.ydata[0])
            self.line_10.setData(self.xdata, self.ydata[1])
            self.line_11.setData(self.xdata, self.ydata[2])
            self.line_12.setData(self.xdata, self.ydata[3])
            self.line_13.setData(self.xdata, self.ydata[4])
            self.line_14.setData(self.xdata, self.ydata[5])
            self.line_15.setData(self.xdata, self.ydata[6])
            self.line_16.setData(self.xdata, self.ydata[7])
            if self.startFFT and not self.done_recording:
                if self.channel == 1:
                    self.line_19.setData(self.xdata, self.ydata[0])
                elif self.channel == 2:
                    self.line_19.setData(self.xdata, self.ydata[1])
                elif self.channel == 3:
                    self.line_19.setData(self.xdata, self.ydata[2])
                elif self.channel == 4:
                    self.line_19.setData(self.xdata, self.ydata[3])
                elif self.channel == 5:
                    self.line_19.setData(self.xdata, self.ydata[4])
                elif self.channel == 6:
                    self.line_19.setData(self.xdata, self.ydata[5])
                elif self.channel == 7:
                    self.line_19.setData(self.xdata, self.ydata[6])
                elif self.channel == 8:
                    self.line_19.setData(self.xdata, self.ydata[7])
                self.line_20_1.setOpts(height = self.yBarGraph[[0,1,2,3,4]])
                self.line_20_2.setOpts(height = self.yBarGraph[[5]])
                self.line_20_3.setOpts(height = self.yBarGraph[[6]])

        self.i += 1

    # for testing purposes
    def generate_random_sample(self):
        # Simulate random data generation
        return random.sample(range(0, 100), 15) + [time.time()], 0

    def setTrainWindow(self, trainWindow):
        self.trainWindow = trainWindow

    #Call the training window
    def openTrainWindow(self):
        global recProcess
        recProcess = subprocess.Popen(["python3", "-u", "MeasurementSubgroup/Streaming/LSL_csv.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,)
        
        self.trainWindow.show()

    def exitApp(self):
        QApplication.quit()

    @Slot()
    def handle_signal_trainData(self):  # will start training the ML model on the new data
        # TODO sent signal and data to ML part to actually start the training
        self.accuracy_data = np.append(self.accuracy_data, random.sample(range(int(self.accuracy_data[-1]), 100), 1))
        self.accuracy_data_iter = np.append(self.accuracy_data_iter, self.accuracy_data_iter[-1] + 1)
        self.loss_data = np.append(self.loss_data, random.sample(range(0, self.loss_data[-1] + 1), 1))
        self.loss_data_iter = np.append(self.loss_data_iter, self.loss_data_iter[-1] + 1)
        self.update_ML_plots()

    #Function that handles the user based interface
    def ChooseUser(self, item):
        if type(item) is str:
            self.ui.userID_test.setText(item)
            self.ui.userID_train.setText(item)
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
            self.ui.userID_train.setText(item.text())
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
    def changeTrainBtn(self):
        if self.ui.mainPages.currentIndex() == 2:
            self.ui.trainBtn.setStyleSheet("background-color: rgb(0, 118, 194);")
            self.ui.testBtn.setStyleSheet("background-color: rgb(0, 166, 214);")
            self.ui.usersBtn.setStyleSheet("background-color: rgb(0, 166, 214);")

    def changeTestBtn(self):
        if self.ui.mainPages.currentIndex() == 0:
            self.ui.testBtn.setStyleSheet("background-color: rgb(0, 118, 194);")
            self.ui.trainBtn.setStyleSheet("background-color: rgb(0, 166, 214);")
            self.ui.usersBtn.setStyleSheet("background-color: rgb(0, 166, 214);")

    def changeUsersBtn(self):
        if self.ui.mainPages.currentIndex() == 1:
            self.ui.usersBtn.setStyleSheet("background-color: rgb(0, 118, 194);")
            self.ui.trainBtn.setStyleSheet("background-color: rgb(0, 166, 214);")
            self.ui.testBtn.setStyleSheet("background-color: rgb(0, 166, 214);")

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
        if event.key() == Qt.Key_W:
            if self.ui.mouseCursor.y() - self.stepsize > 0:
                self.ui.mouseCursor.move(self.ui.mouseCursor.x(), self.ui.mouseCursor.y() - self.stepsize)
                self.ui.lineEdit_3.setText("Up")
        elif event.key() == Qt.Key_A:
            if self.ui.mouseCursor.x() - self.stepsize > 0:
                self.ui.mouseCursor.move(self.ui.mouseCursor.x() - self.stepsize, self.ui.mouseCursor.y())
                self.ui.lineEdit_3.setText("Left")
        elif event.key() == Qt.Key_S:
            if self.ui.mouseCursor.y() + self.stepsize < (self.ui.frame_9.height() - self.ui.mouseCursor.height()):
                self.ui.mouseCursor.move(self.ui.mouseCursor.x(), self.ui.mouseCursor.y() + self.stepsize)
                self.ui.lineEdit_3.setText("Down")
        elif event.key() == Qt.Key_D:
            if self.ui.mouseCursor.x() + self.stepsize < (self.ui.frame_9.width() - self.ui.mouseCursor.width()):
                self.ui.mouseCursor.move(self.ui.mouseCursor.x() + self.stepsize, self.ui.mouseCursor.y())
                self.ui.lineEdit_3.setText("Right")
        elif event.key() == Qt.Key_1:
            self.yBarGraph = np.array([sum(self.ydata[0][i:i+self.av_height])//self.av_height for i in range(0,len(self.ydata[0]),self.av_height)])
            self.channel = 1
        elif event.key() == Qt.Key_2:
            self.yBarGraph = np.array([sum(self.ydata[1][i:i+self.av_height])//self.av_height for i in range(0,len(self.ydata[1]),self.av_height)])
            self.channel = 2
        elif event.key() == Qt.Key_3:
            self.yBarGraph = np.array([sum(self.ydata[2][i:i+self.av_height])//self.av_height for i in range(0,len(self.ydata[2]),self.av_height)])
            self.channel = 3
        elif event.key() == Qt.Key_4:
            self.yBarGraph = np.array([sum(self.ydata[3][i:i+self.av_height])//self.av_height for i in range(0,len(self.ydata[3]),self.av_height)])
            self.channel = 4
        elif event.key() == Qt.Key_5:
            self.yBarGraph = np.array([sum(self.ydata[4][i:i+self.av_height])//self.av_height for i in range(0,len(self.ydata[4]),self.av_height)])
            self.channel = 5
        elif event.key() == Qt.Key_6:
            self.yBarGraph = np.array([sum(self.ydata[5][i:i+self.av_height])//self.av_height for i in range(0,len(self.ydata[5]),self.av_height)])
            self.channel = 6
        elif event.key() == Qt.Key_7:
            self.yBarGraph = np.array([sum(self.ydata[6][i:i+self.av_height])//self.av_height for i in range(0,len(self.ydata[6]),self.av_height)])
            self.channel = 7
        elif event.key() == Qt.Key_8:
            self.yBarGraph = np.array([sum(self.ydata[7][i:i+self.av_height])//self.av_height for i in range(0,len(self.ydata[7]),self.av_height)])
            self.channel = 8

        self.ui.lineEdit_5.setText(str(self.ui.mouseCursor.x()))
        self.ui.lineEdit_6.setText(str(self.ui.mouseCursor.y()))

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


#Training window class
class TrainWindow(QMainWindow):
    signal_to_trainData = Signal()

    def __init__(self):
        super(TrainWindow, self).__init__()
        self.ui = Ui_TrainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("Training Window")

        #Timer
        self.timer = QTimer()

        #Check clicked buttons and call their respective functions
        self.ui.startRecordingBtn.clicked.connect(self.startRecording)
        self.ui.stopRecordingBtn.clicked.connect(self.stopRecording)
        self.ui.helpBtn.clicked.connect(self.help)
        self.timer.timeout.connect(lambda: self.changePages())

        self.ui.dataTrainingBtn.clicked.connect(self.trainingData)

    def trainingData(self):
        self.signal_to_trainData.emit()
        self.close()


    def startRecording(self):
        recProcess.stdout.read1(1)
        recProcess.stdin.write(b"G\n") # G for go
        recProcess.stdin.flush()
        self.timer.start(6000)
        global count
        global pageArray
        global i
        i = 0
        count = 0
        pageArray = [1,2,3,4 ,4,3,2,1 ,2,3,4,1 ,1,3,4,2 ,3,2,4,1 ,4,1,2,3, 0]

        # 1. Right hand, 2. Left hand, 3. Tongue, 4. Feet, 0. Rest

    def changePages(self):
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

    def stopRecording(self):
        recProcess.kill()
        self.timer.stop()
        self.ui.promptsWidgets.setCurrentWidget(self.ui.calibrationPage)
    
    def help(self):
        QMessageBox.information(None,"Help",
        "Instructions and their respective outputs:\nleft hand -> left\nright hand -> right\nfeet -> down\ntongue -> up",
        QMessageBox.StandardButton.Ok)

#Creates the app and runs the Mainwindow
if __name__ == "__main__":

    path = './users.csv'
    if not os.path.isfile(path):
        with open('users.csv', 'w') as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "ID"])

    app = QApplication(sys.argv)

    window1 = MainWindow()
    window2 = TrainWindow()

    window1.setTrainWindow(window2)
    
    window2.signal_to_trainData.connect(window1.handle_signal_trainData)
    window1.showMaximized()
    window1.show()
    sys.exit(app.exec_())