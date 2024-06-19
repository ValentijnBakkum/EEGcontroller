import os
import sys
import json
import csv
import subprocess
from ui_interface import *
from ui_splashscreen import *
from ui_ERDSWindow import Ui_ERDSWindow
from ui_userWindow import Ui_UserWindow
from Custom_Widgets import *
from PySide6.QtWidgets import QInputDialog, QMessageBox, QSplashScreen, QFrame
from PySide6.QtCore import Qt, QTimer, Slot, Signal, QEvent, QBasicTimer
from PySide6.QtGui import QPainter, QColor, QFont
import random
import numpy as np
import pandas as pd
import time
import pyqtgraph as pg
import seaborn as sns
import matplotlib.pyplot as plt
import torch
from torch.utils.data import DataLoader
from escargot3 import escargot
from pylsl import StreamInlet, resolve_stream
from scipy.fft import rfft, rfftfreq 
from scipy.signal import welch
from scipy.signal import butter, lfilter, lfiltic
from scipy import signal

#=======================================================================
# Initialization Splashscreen
#=======================================================================
class SplashScreen(QSplashScreen):
    def __init__(self):
        super(SplashScreen, self).__init__()
        self.ui = Ui_SplashScreen()
        self.ui.setupUi(self) # Load UI from ui_splashscreen.py
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground) # Make window frameless and without background

        # Initialize progress bar for duration of splashscreen
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

    # Show screen until closed
    def showEvent(self, event):
        super().showEvent(event)
        self.centerSplash()

    # Center the splashscreen to the monitor screen
    def centerSplash(self):
        screen = self.screen()
        screen_geometry = screen.geometry()
        splash_geometry = self.geometry()

        x = (screen_geometry.width() - splash_geometry.width()) // 2
        y = (screen_geometry.height() - splash_geometry.height()) // 2

        self.move(x, y)

#=======================================================================
# Main Window from which everything can be called
#=======================================================================
class MainWindow(QMainWindow):
    #Signals to send to the Users Window to change the page
    userWindow_to_cursorPage = Signal()
    userWindow_to_trainingPage = Signal()
    userWindow_to_promptPage = Signal()
    userWindow_startRecording = Signal()
    userWindow_stopRecording = Signal()
    userWindow_startPromptTimer = Signal()

    def __init__(self):
        super(MainWindow, self).__init__()

        self.startFFT = False
        self.done_recording = False
        self.current_id = 0 # id 0 is set to be the "new user" without trained  data
        self.in_training = False

        # For EEG cap connection and data
        self.simulate_data = False
        self.streams = resolve_stream()
        try:
            self.inlet = StreamInlet(self.streams[0])
        except:
            self.show_eeg_error("The EEG cap is not connected. Please connect the cap.")

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self) # Import UI from ui_interface.py

        # Set the control panel
        self.controlPanel = self.findChild(QWidget, "buttonsBox")
        self.controlPanel.installEventFilter(self)

        self.setWindowTitle("EEG-based BCI")

        # Apply style from the file style.json
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
        self.ui.game1Btn.clicked.connect(self.openLavaGame)
        self.ui.game2Btn.clicked.connect(self.openAsteroid)
        #Button panel
        self.ui.startRecordingBtn.clicked.connect(self.startRecording)
        self.ui.stopRecordingBtn.clicked.connect(self.stopRecording)
        self.ui.openUserWindowBtn.clicked.connect(self.openUserWindow)
        self.ui.ERDSBtn.clicked.connect(self.openERDSWindow)
        self.ui.openPromptBtn.clicked.connect(self.setPromptPage)
        self.ui.startTimerBtn.clicked.connect(self.startPromptTimer)
        self.ui.dataTrainingBtn.clicked.connect(self.start_training)
        #Training values
        self.ui.batchSizeLine.textChanged.connect(self.bachtSizeChange)
        self.ui.marginLine.textChanged.connect(self.marginLineChange)
        self.ui.maxIterationLine.textChanged.connect(self.maxIterationLineChange)
        self.ui.learningRateLine.textChanged.connect(self.learningRateLineChange)

        # add users to user list from file
        with open('users.csv', newline='') as user_file:
            user_reader = csv.DictReader(user_file)
            for row in user_reader:
                currentIndex = self.ui.usersList.currentRow()
                self.ui.usersList.insertItem(currentIndex, row["Name"])

        
        #Data live plotting
        self.i = 0
        self.j = 0
        self.max_graph_width = 50
        self.plot_update_size = 2
        self.columns = 5
        self.av_height = int(self.max_graph_width/self.columns)
        self.channel = 1

        self.xdata = np.zeros(self.max_graph_width)
        self.ydata = [np.zeros(self.max_graph_width) for _ in range(8)]
        self.xf = np.zeros(251)
        self.y_fft2 = np.zeros(251)
        self.yBarGraph = np.zeros(self.columns)
        symbol_sign = None

        # FFT and powerbands plots
        # Window settings
        self.window = 500
        self.overlap = 0.25
        # initial values
        self.y_win = np.zeros(self.window)  # window array
        self.t_win = np.zeros(self.window)  # time array
        self.y_out = np.array([])
        self.t_out = np.array([])
        self.low = 8
        self.high = 30

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
            #p.hideAxis('bottom')
            #p.hideAxis('left')

        # Bar graph band power
        self.xBarGraph = np.array([2,6,10,21,40]) #Center points of the columns with according width
        self.power_band_1= pg.BarGraphItem(x=self.xBarGraph[0:3], height = self.yBarGraph[0:3], width = 4, brush = QColor(0, 166, 214), pen=QColor(255, 255, 255))
        self.power_band_2 = pg.BarGraphItem(x=self.xBarGraph[3], height = self.yBarGraph[3], width = 18, brush = QColor(0, 166, 214), pen=QColor(255, 255, 255))
        self.power_band_3 = pg.BarGraphItem(x=self.xBarGraph[4], height = self.yBarGraph[4], width = 20, brush = QColor(0, 166, 214), pen=QColor(255, 255, 255))
        self.ui.powerBandPlot.addItem(self.power_band_1)
        self.ui.powerBandPlot.addItem(self.power_band_2)
        self.ui.powerBandPlot.addItem(self.power_band_3)
        #self.ui.powerBandPlot.setYRange(10, 100)
        self.ui.powerBandPlot.setXRange(0, 50)
        self.ui.powerBandPlot.setMouseEnabled(x=False, y=False)
        self.ui.powerBandPlot.setMenuEnabled(False)
        self.ui.powerBandPlot.hideButtons()

        self.start_time = time.time()

        # Add a timer to simulate new temperature measurements
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(0.04)

        # Stopwatch variables
        self.count = 0
        self.flag = False
        self.ui.stopwatch.setText(str(self.count))
        self.stopwatch = QTimer()
        self.stopwatch.timeout.connect(self.showTime)
        self.stopwatch.start(100)

        #Threshold of minimum width of window
        self.min_width = 1000
        self.original_geometry = self.geometry()

    # Handle Batch size text change
    def bachtSizeChange(self):
        self.batchSize = self.ui.batchSizeLine.text()

    # Handle Batch size text change
    def marginLineChange(self):
        self.margin = self.ui.marginLine.text()

    # Handle Batch size text change
    def maxIterationLineChange(self):
        self.maxIteration = self.ui.maxIterationLine.text()

    # Handle Batch size text change
    def learningRateLineChange(self):
        self.learningRate = self.ui.learningRateLine.text()

    # Check if double clicked on control panel, if true minimze window around the control panel
    def eventFilter(self, obj, event):
        if obj == self.controlPanel and event.type() == QEvent.MouseButtonDblClick:
            self.minimizeWindow()
            return True
        return super().eventFilter(obj, event)
    
    def minimizeWindow(self):
        if self.width() > self.min_width: # Check state of window
            # Hide other components
            self.ui.leftMenuContainer.hide()
            self.ui.frame_2.hide()
            self.ui.frame_3.hide()
            self.ui.leftSubMenu.expandMenu()
            self.ui.UserIDBox.hide()
            self.ui.infoWidgetContainer.hide()
            self.ui.leftBodyFrameOverview.hide()
            self.ui.FFTFrame.hide()
            self.ui.powerBandFrame.hide()

            # Resize the window to the size of the control panel widget
            self.setFixedSize(900,200)
            self.setWindowFlags(Qt.Widget | Qt.WindowStaysOnTopHint)

            # Set background to transparent
            self.setAttribute(Qt.WA_TranslucentBackground, True)
            self.show()

        else:
            self.setFixedSize(1595, 831)
            self.setMinimumSize(0, 0)
            self.setMaximumSize(16777215, 16777215)

            # Restore window frame and background
            self.setWindowFlags(Qt.Widget)
            self.setAttribute(Qt.WA_TranslucentBackground, False)
            self.setGeometry(self.original_geometry)
            #Show other components
            self.ui.leftMenuContainer.show()
            self.ui.frame_2.show()
            self.ui.frame_3.show()
            self.ui.leftSubMenu.show()
            self.ui.leftSubMenu.collapseMenu()
            self.ui.UserIDBox.show()
            self.ui.infoWidgetContainer.show()
            self.ui.leftBodyFrameOverview.show()
            self.ui.FFTFrame.show()
            self.ui.powerBandFrame.show()

            self.showMaximized()

    # Make plot colors pastel
    def make_pastel(self, color, factor=0.3):
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
            self.count += 1
        else:
            self.count = 0

        # Getting text from count
        if self.count < 47:
            text = "0.0"
        else:
            text = str(float("{:.1f}".format(self.count / 10 - 4.7)))
 
        # Show text
        self.ui.stopwatch.setText(text)

    # Emit the signals to the User Window to change page
    def setCursorPage(self):
            self.userWindow_to_cursorPage.emit()
    
    def setTrainPage(self):
            self.userWindow_to_trainingPage.emit()

    def setPromptPage(self):
            self.userWindow_to_promptPage.emit()
            self.ui.stopwatch.setText("0.0") # Reset timer
            self.flag = False
    
    def startRecording(self):
            self.userWindow_startRecording.emit()

    def stopRecording(self):
            self.userWindow_stopRecording.emit()
            self.flag = False

    def startPromptTimer(self):
            self.flag = True
            self.userWindow_startPromptTimer.emit()

    # Try to reconnect with cap again
    def reconnect_cap(self):
        try:
            self.inlet = StreamInlet(self.streams[0], max_buflen=0)
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
    
    # Show error if no cap connected
    def show_eeg_error(self, error_text):
        dlg = QMessageBox()
        dlg.setWindowTitle("ERROR")
        dlg.setStandardButtons(QMessageBox.StandardButton.Retry | QMessageBox.StandardButton.Ignore)
        dlg.setText(error_text)
        
        screen = self.screen()
        screen_geometry = screen.geometry()
        splash_geometry = self.geometry()

        x = (screen_geometry.width() - splash_geometry.width()) // 2
        y = 0

        dlg.move(x, y)
        button = dlg.exec()

        if button == QMessageBox.StandardButton.Retry:
            print("retrying....")
            try:
                self.inlet = StreamInlet(self.streams[0], max_buflen=0)
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

    # Filter raw signal
    def filter(self, y, low, high):
        # Remove the DC component
        y = signal.detrend(y, axis=0)

        # Define the filter parameters
        lowcut = low
        highcut = high
        fs = 250  # Sampling frequency

        # Calculate the filter coefficients
        nyquist = 0.5 * fs
        low = lowcut / nyquist
        high = highcut / nyquist
        b, a = butter(4, [low, high], btype='band')
        #zi = lfilter_zi(b,a)*y[0]

        # Apply the filter to each column of the DataFram
        y_filtered_band= lfilter(b, a, np.array(y))

        # Define the filter parameters
        lowcut = 49
        highcut = 51
        fs = 250  # Sampling frequency

        # Calculate the filter coefficients
        nyquist = 0.5 * fs
        low = lowcut / nyquist
        high = highcut / nyquist
        b, a = butter(4, [low, high], btype='bandstop')
        #zi = lfilter_zi(b,a)*y[0]

        # Apply the filter to each column of the DataFram
        y_filtered= lfilter(b, a, np.array(y_filtered_band))

        return y_filtered
        
    # Update graphs
    def update_plot(self):
        pen = pg.mkPen(self.pastel_colors[self.channel - 1], width = 2)
        # Gathering the data from the EEG cap
        if not self.simulate_data:
            sample, timestamp = self.inlet.pull_sample()
            sample_timestamp = (self.i) / 250
        else:
            sample, timestamp = self.generate_random_sample()  # For testing purposes when not connected to cap
            sample_timestamp = self.i / 250

        # Fill window for FFT plots
        #calculate sample overlap
        overlap_win = int(self.overlap * self.window)

        # assign EEG data to array
        self.y_win[0] = sample[self.channel - 1] # EEG data 1
        self.t_win[0] = (self.i)/250 # Counter from EEG cap in seconds

        # Shift the array with one index
        self.y_win = np.roll(self.y_win, -1)
        self.t_win = np.roll(self.t_win, -1)

        # When a new block of L is reached
        if self.i % overlap_win == 0 and self.i != overlap_win and self.i != 0:
            #print(self.i/250, "sec")
            # apply filter to window
            #y_win_filt = filter(y_win, 0.5, 38)
            y_win_filt2 = self.filter(self.y_win, self.low, self.high)
            
            #y_win_pad = np.pad(y_win_filt, int(0), 'constant')
            y_win_pad2 = np.pad(y_win_filt2, int(0), 'constant')
            # print(y_win_pad.shape)

            self.xf = rfftfreq(y_win_pad2.shape[0], 1/250)
            #y_fft = np.abs(rfft(y_win_pad))
            self.y_fft2 = np.abs(rfft(y_win_pad2)) # Data to be plotted for FFT plot

            #  PSD
            # Compute the power spectral density using Welch's method
            frequencies, psd = welch(y_win_pad2, 250)

            # Powerbands
            # Define frequency bands
            delta_band = (0.5, 4)
            theta_band = (4, 8)
            alpha_band = (8, 12)
            beta_band = (12, 30)
            gamma_band = (30, 50)

            # Function to calculate power in a specific frequency band
            def bandpower(frequencies, psd, band):
                band_freq_indices = np.logical_and(frequencies >= band[0], frequencies <= band[1])
                band_power = np.sum(psd[band_freq_indices])
                band_power_norm = band_power / (band[1] - band[0])
                return band_power_norm
            
            # Calculate power for each band
            delta_power = bandpower(frequencies, psd, delta_band)
            theta_power = bandpower(frequencies, psd, theta_band)
            alpha_power = bandpower(frequencies, psd, alpha_band)
            beta_power = bandpower(frequencies, psd, beta_band)
            gamma_power = bandpower(frequencies, psd, gamma_band)

            # Power values 
            self.yBarGraph = [delta_power, theta_power, alpha_power, beta_power, gamma_power] # Data to be plotted for powerbands

        if self.i <= self.max_graph_width:
            pass
        else:
            if not self.startFFT:
                self.startFFT = True
                symbol_sign = None
                self.FFT_plot = self.ui.FFTPlot.plot(
                    self.xf,
                    self.y_fft2,
                    name="Power Sensor",
                    pen=pen,
                    symbol=symbol_sign,
                    symbolSize=5,
                    symbolBrush="b",
                )
                #self.ui.FFTPlot.setXRange(5, 35)
                #self.ui.FFTPlot.setYRange(0, 50)
                self.ui.FFTPlot.setMouseEnabled(x=False, y=False)
                self.ui.FFTPlot.setMenuEnabled(False)
                self.ui.FFTPlot.hideButtons()

        # Only update the plot everytime it has collected plot update data sized data
        if self.i % 50 == 0:
            self.xdata = np.roll(self.xdata, -1)
            self.xdata[-1] = sample_timestamp

            for k in range(8):
                self.ydata[k] = np.roll(self.ydata[k], -1)
                self.ydata[k][-1] = sample[k]
                self.lines[k].setData(self.xdata, self.ydata[k])

            self.power_band_1.setOpts(height=self.yBarGraph[0:3], brush=pg.mkBrush(self.pastel_colors[self.channel - 1]))
            self.power_band_2.setOpts(height=self.yBarGraph[3], brush=pg.mkBrush(self.pastel_colors[self.channel - 1]))
            self.power_band_3.setOpts(height=self.yBarGraph[4], brush=pg.mkBrush(self.pastel_colors[self.channel - 1]))

            if self.startFFT:
                self.FFT_plot.setData(self.xf, self.y_fft2)
                self.FFT_plot.setPen(pg.mkPen(self.pastel_colors[self.channel - 1], width = 2))

            # Change the power band plots from channel
            #self.yBarGraph = np.array(
            #    [sum(self.ydata[self.channel - 1][i:i + self.av_height]) // self.av_height for i in
            #     range(0, len(self.ydata[self.channel - 1]), self.av_height)])

        self.i += 1

        if self.i == 1000:
            print(time.time() - self.start_time)


    # For testing purposes
    def generate_random_sample(self):
        # Simulate random data generation
        return random.sample(range(0, 100), 15) + [time.time()], 0
    
    # Set and open User Window functions
    def setUserWindow(self, userWindow):
        self.userWindow = userWindow

    def openUserWindow(self):
        global recProcess
        if self.userWindow.isVisible():
            pass
        else:
            recProcess = subprocess.Popen(["python3", "-u", "MeasurementSubgroup/Streaming/LSL_csv.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,)
            self.userWindow.show()

    # Set and open ERDS Window functions
    def openERDSWindow(self):
        global ERDS_process
        ERDS_process = subprocess.Popen(["python", "-u", "MeasurementSubgroup/ERDS_plots/ERDS_for_GUI.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,)

    # Set and open Lava Game Window functions
    def setLavaGameWindow(self, LavaGame):
        self.LavaGame = LavaGame

    def openLavaGame(self):
        self.LavaGame.showMaximized()
        self.userWindow.hide()

    # Set and open Asteroid Widnow functions
    def setAsteroidWindow(self, Asteroid):
        self.Asteroid = Asteroid

    def openAsteroid(self):
        self.Asteroid.showMaximized()
        self.userWindow.hide()

    # Exit the app
    def exitApp(self):
        QApplication.quit()

    def show_message(self, window_title: str, message: str):
        dlg = QMessageBox()
        dlg.setWindowTitle(window_title)
        dlg.setText(message)
        button = dlg.exec()

    # Will start training the ML model on the new data
    def start_training(self):
        if self.in_training:
            self.show_message("Train Error", "Already in training!")
            return

        if self.current_id == 0:
            self.show_message("Train Error", "No user selected!")
            return

        #parent_directory = os.path.dirname(os.getcwd())
        new_directory = os.path.join(os.getcwd(), 'MeasurementSubgroup\\Our_measurements')
        file_name = f"{self.current_id}.csv"
        file_exists = any(file for file in os.listdir(new_directory) if file == file_name)

        if not file_exists:
            self.show_message("Train Error", "There are no recordings made for this user!")
            return

        full_file_path = os.path.join(new_directory, file_name)
        trainer = train(int(self.ui.batchSizeLine.text()), int(self.ui.learningRateLine.text()),
                        int(self.ui.maxIterationLine.text()), 10, full_file_path, self.current_id, self)
        trainer.dataloader()
        trainer.train("own.pt","owntargets.pt")

    # updating the Machine Learning plots while training
    def update_ML_plots(self):
        # when it's the first time after recording we want to clear the previous plots
        if self.done_recording == False:
            pen = pg.mkPen(self.pastel_colors[self.channel - 1], width=2)
            # if the FFT and frequency band plots were used, clear them
            if self.startFFT:
                self.FFT_plot.clear()
                self.ui.powerBandPlot.clear()
            symbol_sign = None
            self.loss_plot = self.ui.powerBandPlot.plot(
                self.loss_data_iter,
                self.loss_data,
                name="Power Sensor",
                pen=pen,
                symbol=symbol_sign,
                symbolSize=5,
                symbolBrush="b",
            )
            self.ui.powerBandPlot.setYRange(0, 100)
            self.ui.powerBandPlot.setXRange(0, int(self.ui.maxIterationLine.text()))
            self.accuracy_plot = self.ui.FFTPlot.plot(
                self.accuracy_data_iter,
                self.accuracy_data,
                name="Power Sensor",
                pen=pen,
                symbol=symbol_sign,
                symbolSize=5,
                symbolBrush="b",
            )
            self.ui.FFTPlot.setYRange(0, 100)
            self.ui.FFTPlot.setXRange(0, int(self.ui.maxIterationLine.text()))
            self.done_recording = True

        # update the plots with the new data
        self.accuracy_plot.setData(self.accuracy_data_iter, self.accuracy_data)
        self.loss_plot.setData(self.loss_data_iter, self.loss_data)


    #Functions that handles the user based interface
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

    # Add user name
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
            
    # Edit user name
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

    # Remove user        
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

    # Move user up
    def upUser(self):
        index = self.ui.usersList.currentRow()
        if index >= 1:
            item = self.ui.usersList.takeItem(index)
            self.ui.usersList.insertItem(index-1,item)
            self.ui.usersList.setCurrentItem(item)

    # Move user down
    def downUser(self):
        index = self.ui.usersList.currentRow()
        if index < self.ui.usersList.count()-1:
            item = self.ui.usersList.takeItem(index)
            self.ui.usersList.insertItem(index + 1, item)
            self.ui.usersList.setCurrentItem(item)

    # Sort user names
    def sortUser(self):
        self.ui.usersList.sortItems()

    # Change color of menu buttons according to the page
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
    
    # Functions when clicking on keys
    def keyPressEvent(self, event):
        # Functions to change FFT and band power when clicking on 1-8
        if event.key() == Qt.Key.Key_1:
            #self.yBarGraph = np.array([sum(self.ydata[0][i:i+self.av_height])//self.av_height for i in range(0,len(self.ydata[0]),self.av_height)])
            self.channel = 1
        elif event.key() == Qt.Key.Key_2:
            #self.yBarGraph = np.array([sum(self.ydata[1][i:i+self.av_height])//self.av_height for i in range(0,len(self.ydata[1]),self.av_height)])
            self.channel = 2
        elif event.key() == Qt.Key.Key_3:
            #self.yBarGraph = np.array([sum(self.ydata[2][i:i+self.av_height])//self.av_height for i in range(0,len(self.ydata[2]),self.av_height)])
            self.channel = 3
        elif event.key() == Qt.Key.Key_4:
            #self.yBarGraph = np.array([sum(self.ydata[3][i:i+self.av_height])//self.av_height for i in range(0,len(self.ydata[3]),self.av_height)])
            self.channel = 4
        elif event.key() == Qt.Key.Key_5:
            #self.yBarGraph = np.array([sum(self.ydata[4][i:i+self.av_height])//self.av_height for i in range(0,len(self.ydata[4]),self.av_height)])
            self.channel = 5
        elif event.key() == Qt.Key.Key_6:
            #self.yBarGraph = np.array([sum(self.ydata[5][i:i+self.av_height])//self.av_height for i in range(0,len(self.ydata[5]),self.av_height)])
            self.channel = 6
        elif event.key() == Qt.Key.Key_7:
            #self.yBarGraph = np.array([sum(self.ydata[6][i:i+self.av_height])//self.av_height for i in range(0,len(self.ydata[6]),self.av_height)])
            self.channel = 7
        elif event.key() == Qt.Key.Key_8:
            #self.yBarGraph = np.array([sum(self.ydata[7][i:i+self.av_height])//self.av_height for i in range(0,len(self.ydata[7]),self.av_height)])
            self.channel = 8
        

        # to simulate the accuracy plot
        if event.key() == Qt.Key_P:
            self.accuracy_data = np.append(self.accuracy_data, random.sample(range(int(self.accuracy_data[-1]), 100), 1))
            self.accuracy_data_iter = np.append(self.accuracy_data_iter, self.accuracy_data_iter[-1] + 1)
            self.loss_data = np.append(self.loss_data, random.sample(range(0, self.loss_data[-1] + 1), 1))
            self.loss_data_iter = np.append(self.loss_data_iter, self.loss_data_iter[-1] + 1)
            self.update_ML_plots()

        self.update()

    def closeEvent(self, event):
        try:
            ERDS_process.kill()
        except:
            pass

#=======================================================================
# User Window class
#=======================================================================
class UserWindow(QMainWindow):
    def __init__(self):
        super(UserWindow, self).__init__()
        self.ui = Ui_UserWindow()
        self.ui.setupUi(self) # Import UI from ui_userWindow.py

        self.setWindowTitle("User Window")
        
        # Timer
        self.timer = QTimer()
        self.promptTimer = QTimer()

        self.stepsize = 10
        # Check clicked buttons and call their respective functions
        self.timer.timeout.connect(lambda: self.changePages())
        self.promptTimer.timeout.connect(lambda: self.changePrompt())

        # Cap connection
        self.streams = resolve_stream()
        #self.inlet = StreamInlet(self.streams[0])
        recProcess = subprocess.Popen(["python3", "-u", "MeasurementSubgroup/Streaming/LSL_csv.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,)

    @Slot()
    def startRecording(self):
        global count
        global pageArray
        global i
        i = 0
        count = 0
        pageArray = [1,2,3,4 ,4,3,2,1 ,2,3,4,1 ,1,3,4,2 ,3,2,4,1 ,4,1,2,3, 0] # Fixed prompts for labeling
        recProcess.stdout.read1(1)
        recProcess.stdin.write(b"G\n") # G for go
        recProcess.stdin.flush()
        self.timer.start(6000)

    def changePages(self):
        if self.ui.demosPages.currentWidget() == self.ui.trainingPage:
            global count
            global pageArray
            global i

            pageNumber = pageArray[i]

            recProcess.stdin.write(b"Prompt\n") # G for go
            recProcess.stdin.flush()

            if count % 2 != 0:
                self.ui.promptsWidgets.setCurrentWidget(self.ui.calibrationPage)
            else:
                self.ui.promptsWidgets.setCurrentIndex(pageNumber)
                i = i + 1
            if count == 47:
                recProcess.stdin.write(b"Done\n") # G for go
                recProcess.stdin.flush()
                self.timer.stop()

            count = count + 1

    @Slot()
    def stopRecording(self):
        recProcess.stdin.write(b"Stop\n") # G for go
        recProcess.stdin.flush()
        self.timer.stop()
        self.ui.promptsWidgets.setCurrentWidget(self.ui.calibrationPage)

    @Slot()
    def startPromptTimer(self):
            self.promptTimer.start(5000) # Countdown to show prompt

    def changePrompt(self):
            self.ui.promptTestWidget.setCurrentWidget(self.ui.promptPromptPage)
            self.promptTimer.stop()

    # Change pages according to signal received from MainWindow
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

    # Simulate cursor movements with WASD keys
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_W:
            if self.ui.mouseCursor.y() - self.stepsize > 0:
                self.ui.mouseCursor.move(self.ui.mouseCursor.x(), self.ui.mouseCursor.y() - self.stepsize)
        elif event.key() == Qt.Key.Key_A:
            if self.ui.mouseCursor.x() - self.stepsize > 0:
                self.ui.mouseCursor.move(self.ui.mouseCursor.x() - self.stepsize, self.ui.mouseCursor.y())
        elif event.key() == Qt.Key.Key_S:
            if self.ui.mouseCursor.y() + self.stepsize < (self.ui.cursorFrame.height() - self.ui.mouseCursor.height()):
                self.ui.mouseCursor.move(self.ui.mouseCursor.x(), self.ui.mouseCursor.y() + self.stepsize)
        elif event.key() == Qt.Key.Key_D:
            if self.ui.mouseCursor.x() + self.stepsize < (self.ui.cursorFrame.width() - self.ui.mouseCursor.width()):
                self.ui.mouseCursor.move(self.ui.mouseCursor.x() + self.stepsize, self.ui.mouseCursor.y())

    def closeEvent(self, event):
        recProcess.kill()

#=======================================================================
# Lava Game window class
#=======================================================================
class LavaGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("The Floor is Lava")
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.grid_layout = QGridLayout(self.central_widget)
        self.central_widget.setLayout(self.grid_layout)

        self.create_grid()
        self.create_player()
        # Timer to check collision with red tiles
        self.check_collision_timer = QTimer(self)
        self.check_collision_timer.timeout.connect(self.check_collision)

        self.game_over = False

        # Countdown setup
        self.countdown_label = QLabel(self.central_widget)
        self.countdown_label.setAlignment(Qt.AlignCenter)
        self.countdown_label.setStyleSheet("font-size: 100px; color: red;")
        self.countdown_label.setGeometry(0, 0, self.width(), self.height())
        self.countdown_timer = QTimer(self)
        self.countdown_timer.timeout.connect(self.update_countdown)
        self.countdown_value = 5        

        # Start the game with countdown
        self.start_countdown()

    def start_countdown(self):
        if self.isHidden():
            pass
        else:
            self.countdown_value = 5  # Start countdown from 5
            self.countdown_label.setText(str(self.countdown_value))
            self.countdown_label.show()
            self.countdown_timer.start(1000)

    def update_countdown(self):
        self.countdown_value -= 1
        if self.countdown_value > 0:
            self.countdown_label.setText(str(self.countdown_value))
        else:
            self.countdown_timer.stop()
            self.countdown_label.hide()
            self.generate_warning()

    def start_game(self):
        if self.isHidden():
            pass
        else:
            QTimer.singleShot(3000, self.generate_warning)  # Schedule turning new warning tiles after 3 seconds

    def create_grid(self):
        grid_size = 8
        self.red_tiles = set()
        self.empty_cells = set()  # Store the empty cells separately

        # Add empty cells to the left
        for row in range(grid_size):
            empty_cell_widget = QWidget()
            empty_cell_widget.setStyleSheet("border: none;")  # No border or background color
            self.grid_layout.addWidget(empty_cell_widget, row, 0)
            self.empty_cells.add(empty_cell_widget)  # Add empty cells to the set

        for row in range(grid_size):
            empty_cell_widget = QWidget()
            empty_cell_widget.setStyleSheet("border: none;")  # No border or background color
            self.grid_layout.addWidget(empty_cell_widget, row, 1)
            self.empty_cells.add(empty_cell_widget)  # Add empty cells to the set

        # Add empty cells to the right
        for row in range(grid_size):
            empty_cell_widget = QWidget()
            empty_cell_widget.setStyleSheet("border: none;")  # No border or background color
            self.grid_layout.addWidget(empty_cell_widget, row, grid_size + 1)
            self.empty_cells.add(empty_cell_widget)  # Add empty cells to the set

        for row in range(grid_size):
            empty_cell_widget = QWidget()
            empty_cell_widget.setStyleSheet("border: none;")  # No border or background color
            self.grid_layout.addWidget(empty_cell_widget, row, grid_size + 2)
            self.empty_cells.add(empty_cell_widget)  # Add empty cells to the set

        for row in range(grid_size):
            empty_cell_widget = QWidget()
            empty_cell_widget.setStyleSheet("border: none;")  # No border or background color
            self.grid_layout.addWidget(empty_cell_widget, row, grid_size + 3)
            self.empty_cells.add(empty_cell_widget)  # Add empty cells to the set

        # Add game cells
        for row in range(grid_size):
            for col in range(grid_size):
                cell_widget = QWidget()
                cell_widget.setStyleSheet("background-color: white; border: 1px solid black;")
                self.grid_layout.addWidget(cell_widget, row, col + 2)  # Offset by 2 to skip the empty columns

    def create_player(self):
        self.player = QWidget(self.central_widget)
        self.player.setFixedSize(120, 120)
        self.player.setStyleSheet("background-color: blue; border: 1px solid black;")
        self.player.move(1220, 640)  # Position the player initially

    def generate_warning(self):
        if self.isHidden():
            pass
        else:
            self.check_collision_timer.start(50)  # Check collision every 50 milliseconds
            if self.game_over:
                return
            for tile in self.red_tiles:
                tile.setStyleSheet("background-color: white; border: 1px solid black;")
            self.red_tiles.clear()

            num_warning_tiles = random.randint(4, 6)
            available_cells = [self.grid_layout.itemAt(i).widget() for i in range(self.grid_layout.count()) if self.grid_layout.itemAt(i).widget() not in self.empty_cells]
            warning_tiles = random.sample(available_cells, num_warning_tiles)
            for tile in warning_tiles:
                tile.setStyleSheet("background-color: yellow; border: 1px solid black;")
                self.red_tiles.add(tile)

            QTimer.singleShot(6000, self.generate_lava)  # Schedule turning warning tiles to lava after 6 seconds

    def generate_lava(self):
        if self.isHidden():
            pass
        else:
            for tile in self.red_tiles:
                tile.setStyleSheet("background-color: red; border: 1px solid black;")
            QTimer.singleShot(3000, self.revert_lava)  # Schedule reverting lava tiles to white after 3 seconds

    def revert_lava(self):
        for tile in self.red_tiles:
            tile.setStyleSheet("background-color: white; border: 1px solid black;")
        self.start_game()  # Start a new cycle of the game

    # Check if there is a collision between player and lava tile
    def check_collision(self):
        if not self.game_over:
            player_rect = self.player.geometry()
            for tile in self.red_tiles:
                if tile.styleSheet() == "background-color: red; border: 1px solid black;" and player_rect.intersects(tile.geometry()):
                    self.game_over = True
                    self.game_over_label = QLabel("Game Over", self.central_widget) 
                    self.game_over_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.game_over_label.setGeometry(0, 0, self.width(), self.height())
                    self.game_over_label.setStyleSheet("font-size: 100px; color: red;")
                    self.game_over_label.raise_()
                    self.game_over_label.show()

    def keyPressEvent(self, event):
        if not self.game_over:
            self.step = 40  # Define step size for movement
            if event.key() == Qt.Key.Key_W:
                if self.player.y() - self.step + 10 > 0:
                    self.player.move(self.player.x(), self.player.y() - self.step)
            elif event.key() == Qt.Key.Key_A:
                if self.player.x() - self.step > self.width()/6:
                    self.player.move(self.player.x() - self.step, self.player.y())
            elif event.key() == Qt.Key.Key_S:
                if self.player.y() + self.step < (self.height() - self.player.height()):
                    self.player.move(self.player.x(), self.player.y() + self.step)
            elif event.key() == Qt.Key.Key_D:
                if self.player.x() + self.step < (self.width() - self.player.width())-self.width()/6:
                    self.player.move(self.player.x() + self.step, self.player.y())

    def closeEvent(self, event):
        # Stop all game timers and reset game state
        self.check_collision_timer.stop()
        self.countdown_timer.stop()
        self.game_over = False  # Reset game over flag
        self.countdown_label.hide()
        if hasattr(self, 'game_over_label'):
            self.game_over_label.hide()
        event.accept()  # Accept the close event

    def showEvent(self, event):
        # Restart the game when the window is shown
        self.start_countdown()
        event.accept()  # Accept the show event

#=======================================================================
# Asteroid Game window classes
#=======================================================================
class Asteroid(QMainWindow):
    def __init__(self):
        super(Asteroid, self).__init__()

        # creating a board object
        self.game = Game(self)

        # adding board as a central widget
        self.setCentralWidget(self.game)

        # setting title to the window
        self.setWindowTitle('Asteroid Shooter')

        # setting geometry to the window
        self.setGeometry(100, 100, 600, 400)

        # starting the board object
        self.game.start()

#=======================================================================
# Asteroid Game Frame classes
#=======================================================================
class Game(QFrame):
    # timer countdown time
    SPEED = 80

    # meteor settings
    MAXMETEORS = 3
    METEOR_SPEED = 3

    # constructor
    def __init__(self, parent):
        super(Game, self).__init__(parent)

        # creating a timer
        self.timer = QBasicTimer()

        # player location
        self.playerloc = 750

        # meteor list
        self.meteor = []
        # bullet list
        self.bullet = []

        self.spawn_bullet = False

        # keeps track of score
        self.score = 0
        self.lives = 3

        # sizes of objects
        self.playerSize = 70
        self.cometSize = 70
        self.border_size = 470

        # direction of player
        self.direction = -1

        self.game_active = True

        # setting focus
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    # start method
    def start(self):
        # starting timer
        self.timer.start(Game.SPEED, self)

    # paint event
    def paintEvent(self, event):
        painter = QPainter(self)

        # draw side panels
        self.draw_side_panels(painter)

        # draw the meteors
        for pos in self.meteor:
            self.draw_square(painter, pos[0], pos[1], self.cometSize, self.cometSize, QColor(0xFF0000))

        # draw the bullets
        for pos in self.bullet:
            self.draw_square(painter, pos[0], pos[1], 5, 10, QColor(0xFF0000))

        # draw the score (if the game is active, not active when player is gameOver)
        if self.game_active:
            self.draw_score(painter)

            # drawing player
            self.draw_square(painter, self.playerloc, self.height() - self.playerSize,
                             self.playerSize, self.playerSize, QColor(0x228B22))
        else:
            self.draw_game_over(painter)

    # drawing side panels
    def draw_side_panels(self, painter):
        # left panel
        painter.fillRect(0, 0, self.border_size, self.height(), QColor(0x404040))
        # right panel
        painter.fillRect(self.width() - self.border_size, 0, self.border_size, self.height(), QColor(0x404040))

    # drawing score
    def draw_score(self, painter):
        painter.setPen(QColor(0xFFFFFF))
        painter.setFont(QFont('Arial', 50))
        score_text = f"Score: {self.score}"
        painter.drawText(10, 70, score_text)
        painter.setFont(QFont('Arial', 40))
        lives_text = f"Lives: {self.lives}"
        painter.drawText(10, 120, lives_text)

    # drawing square
    def draw_square(self, painter, x, y, width, height, color):
        painter.fillRect(x, y, width, height, color)

    # draw Game Over text with score
    def draw_game_over(self, painter):
        painter.setPen(QColor(0xFF0000))
        painter.setFont(QFont('Arial', 50))
        game_over_text = f"GAME OVER"
        text_width = painter.fontMetrics().horizontalAdvance(game_over_text)
        painter.drawText((self.width() - text_width) // 2, self.height() // 2, game_over_text)
        painter.setPen(QColor(0x000000))
        painter.setFont(QFont('Arial', 30))
        score_text = f"Score: {self.score}"
        text_width = painter.fontMetrics().horizontalAdvance(score_text)
        painter.drawText((self.width() - text_width) // 2, self.height() // 2 + 50, score_text)

    # key press event
    def keyPressEvent(self, event):
        key = event.key()
        # if left key is pressed
        if key == Qt.Key.Key_A:
            # if direction is not right
            self.direction = 0

        # if right key is pressed
        elif key == Qt.Key.Key_D:
            # if direction is not left
            self.direction = 1

        # if space key is pressed
        elif key == Qt.Key.Key_Space:
            self.spawn_bullet = True

    # method to move the player
    def move_player(self):
        # if direction is left
        if self.direction == 0:
            if self.playerloc > self.border_size + self.playerSize // 2:
                self.playerloc -= self.playerSize
            # reset direction until new move button is pressed
            self.direction = -1
        # if direction is right
        elif self.direction == 1:
            if self.playerloc < self.width() - self.border_size - self.playerSize * 2:
                self.playerloc += self.playerSize
            # reset direction until new move button is pressed
            self.direction = -1


    # time event method
    def timerEvent(self, event):
        if self.width() < 500:
            pass
        else:
            # checking timer id
            if event.timerId() == self.timer.timerId():
                # if the player is not gameover
                if self.game_active:
                    # move the player and spawn meteors and bullets if needed
                    self.move_player()
                    self.spawn_meteor()
                    if self.spawn_bullet:
                        self.bullet.append([self.playerloc + self.playerSize // 2, self.height() - self.playerSize])
                        self.spawn_bullet = False
                    # call update meteor and bullet methods
                    self.update_meteor()
                    self.update_bullet()
                    # update the window
                    self.update()

    # spawns a meteor
    def spawn_meteor(self):
        # if there are less than the max amount of meteors, spawn one
        if len(self.meteor) < self.MAXMETEORS:
            # getting new random x location until its not the same as an already existing meteor's location
            while True:
                # creating random x coord for the meteor within vertical field
                x = random.randint(self.border_size, self.width() - self.border_size - self.cometSize)
                # extract x-coordinates of existing meteors and check for overlap
                overlapping = False
                for pos in self.meteor:
                    if abs(x - pos[0]) < self.cometSize:
                        overlapping = True
                        break
                if not overlapping:
                    break
            self.meteor.append([x, 0])

    # move the meteors down
    def update_meteor(self):
        for index, pos in enumerate(self.meteor[:]):
            pos[1] += Game.METEOR_SPEED
            # if it hits the ground, remove a life and the meteor
            if pos[1] > self.height() - self.playerSize:
                self.lives -= 1
                self.meteor.remove(pos)
                # call Game over method when no lives are left
                if self.lives <= 0:
                    self.game_over()

    # when no lives are left, destroy all bullets and meteors
    def game_over(self):
        self.game_active = False
        for index, pos in enumerate(self.meteor[:]):
            self.meteor.remove(pos)
        for index, pos in enumerate(self.meteor[:]):
            self.bullet.remove(pos)

    # move all bullets up and check for collision
    def update_bullet(self):
        for pos in self.bullet[:]:
            pos[1] -= self.playerSize
            # if bullet is too high, destroy it
            if pos[1] < 0:
                self.bullet.remove(pos)
            # if bullet collides with meteor, remove the bullet and meteor and add a point to the players score
            for pos_meteor in self.meteor[:]:
                if pos[0] > pos_meteor[0] and pos[0] < pos_meteor[0] + self.cometSize and pos[1] < pos_meteor[1] + self.cometSize:
                    self.bullet.remove(pos)
                    self.meteor.remove(pos_meteor)
                    self.score += 1


class train():
    def __init__(self,batch_size,learning_rate,max_iters,eval_interval,load_cvs):
        self.batch_size = batch_size
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.learning_rate = learning_rate
        self.max_iters = max_iters
        self.eval_interval = eval_interval
        self.load = load_cvs
    def train(self,logits_train,targets_train):
        logits_train = torch.load(logits_train)
        targets_train = torch.load(targets_train)
        logits_train = logits_train[:,None,:,:]
        print(logits_train.shape)
        print(targets_train.shape)
        dataset = torch.utils.data.TensorDataset(logits_train,targets_train)
        train = DataLoader(dataset,batch_size = self.batch_size,shuffle = True)
        model = escargot().to(self.device)
        model.train()
        optimizer = torch.optim.Adam(model.parameters(), lr=self.learning_rate, weight_decay=1e-3)
        loss = torch.nn.CrossEntropyLoss()
        scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=30, gamma=0.7)
        llist = []
        tlist = []
        avloss = []
        acc_list = []
        #-----training loop-----#
        for itere in range(self.max_iters):
            f_list,t_list = next(iter(train))
            t_list = t_list.type(torch.LongTensor)
            if itere % self.eval_interval == 0 or itere == self.max_iters - 1:
                with torch.no_grad():
                    model.eval()
                    out = model(f_list.to(self.device,dtype=torch.float))#tf_list.to(device),tff_list.to(device)
                    #print(torch.max(out,dim=1))
                    values,ind = torch.max(out,dim = 1)
                    g = t_list.shape
                    #print(g)
                    a = np.sum((torch.eq(ind.to("cpu"),t_list.to("cpu")).numpy()))
                    #print(a)
                    accuracy = (a/g)*100
                    tlist.append(accuracy)
                    avgloss = (np.sum(avloss)/(len(avloss)))
                    progress = (itere/self.max_iters) * 100
                    print("accuracy : {}, validation loss : {}, progress : {}%, lr : {}".format(accuracy, avgloss, int(progress), scheduler.get_last_lr()))
                    avloss = []
                    if itere == 0:
                        print(" ")
                    else:
                        llist.append(avgloss)
                        acc_list.append(accuracy)
            else:
                model.train()
                inputs = model(f_list.to(self.device,dtype=torch.float))#,ff_list.to(device)batch_list.to(device)
                #print(inputs[0])
                with torch.no_grad():
                    val_input = model(f_list.to(self.device,dtype=torch.float))#test_list.to(device),tff_list.to(device)
                lossvalue = loss(inputs, t_list.to(self.device))
                #print(lossvalue)
                vallvalue = loss(val_input.to(self.device),t_list.to(self.device))
                avloss.append(vallvalue.data.cpu().numpy())
                optimizer.zero_grad(set_to_none=True)
                lossvalue.backward()
                optimizer.step()
                scheduler.step()
        #-----training loop-----#    
                
        torch.save(model.state_dict(),'blockblock.pt')
        #print(acc_list)
        #print(np.sum(acc_list)/10)
    def dataloader(self):
        df = pd.read_csv(self.load)
        label_1 = df.loc[df['Label'] == 0]
        label_2 = df.loc[df['Label'] == 1]
        label_3 = df.loc[df['Label'] == 2]
        label_4 = df.loc[df['Label'] == 3]
        label_5 = df.loc[df['Label'] == 4]
        label_1mod = label_2.drop(columns=["Counter", "Validation","Label"])
        label_2mod = label_3.drop(columns=["Counter", "Validation","Label"])
        label_3mod = label_4.drop(columns=["Counter", "Validation","Label"])
        label_4mod = label_5.drop(columns=["Counter", "Validation","Label"])
        label_1mod = label_1mod.to_numpy()
        label_2mod = label_2mod.to_numpy()
        label_3mod = label_3mod.to_numpy()
        label_4mod = label_4mod.to_numpy()
        
        list_class = [label_1mod,label_2mod,label_3mod,label_4mod]
        g = 0
        output_list = []
        label_list = []
        #print(label_1mod)
        for i in list_class:
            for _ in range(6):
                index = _ *1500
                for waa in range(30):
                    a = i[index+25*waa:index + 529+25*waa]
                    a = torch.tensor(a)
                    #print(a.shape)
                    #a = torch.mul(a,0.00001)
                    #print(a.shape)
                    
                    if g == 0:
                        output_list.append(a)
                        label_list.append(0)
                    elif g == 1:
                        output_list.append(a)
                        label_list.append(1)
                        pass
                    elif g == 2:
                        output_list.append(a)
                        label_list.append(2)
                        pass
                    elif g == 3:
                        output_list.append(a)
                        label_list.append(1)
            g = g + 1
        output_label1 = np.stack(output_list)  
        output_label1 = torch.tensor(output_label1)   
        targets = torch.tensor(label_list) 
        print(output_label1.shape)    
        torch.save(output_label1,"own.pt")
        torch.save(targets,"owntargets.pt")
        return True

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
    window3 = LavaGame()
    window4 = Asteroid()

    window1.setUserWindow(window2)
    window1.setLavaGameWindow(window3)
    window1.setAsteroidWindow(window4)
    
    window1.userWindow_to_cursorPage.connect(window2.handle_signal_cursorPage)
    window1.userWindow_to_promptPage.connect(window2.handle_signal_promptPage)
    window1.userWindow_to_trainingPage.connect(window2.handle_signal_trainingPage)
    window1.userWindow_startRecording.connect(window2.startRecording)
    window1.userWindow_stopRecording.connect(window2.stopRecording)
    window1.userWindow_startPromptTimer.connect(window2.startPromptTimer)

    QTimer.singleShot(3000, show_main_window)
    
    sys.exit(app.exec_())