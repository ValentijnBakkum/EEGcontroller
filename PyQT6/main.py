import os
import sys
import json
import csv
from ui_interface import *
from ui_splashscreen import *
from ui_ERDSWindow import Ui_ERDSWindow
from ui_userWindow import Ui_UserWindow
from Custom_Widgets import *
from PySide6.QtWidgets import QInputDialog, QMessageBox, QSplashScreen, QFrame
from PySide6.QtCore import Qt, QTimer, Slot, Signal, QEvent, QBasicTimer, QThread
from PySide6.QtGui import QPainter, QColor, QFont
import random
import numpy as np
import pandas as pd
import time
from datetime import datetime
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
from csv_to_tensor import cleaner

# =======================================================================
# Initialization Splashscreen
# =======================================================================
class SplashScreen(QSplashScreen):
    def __init__(self):
        super(SplashScreen, self).__init__()
        self.ui = Ui_SplashScreen()
        self.ui.setupUi(self)  # Load UI from ui_splashscreen.py
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)  # Make window frameless and without background

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


# =======================================================================
# Main Window from which everything can be called
# =======================================================================
class MainWindow(QMainWindow):
    # Signals to send to the Users Window to change the page
    userWindow_to_cursorPage = Signal()
    userWindow_to_trainingPage = Signal()
    userWindow_to_promptPage = Signal()
    userWindow_startRecording = Signal()
    userWindow_stopRecording = Signal()
    userWindow_startPromptTimer = Signal()

    def __init__(self):
        super(MainWindow, self).__init__()

        self.startFFT = False
        self.done_recording = False  # used to check if program is ready for training on data
        self.current_id = 0  # id 0 is set to be the "new user" without trained  data
        self.has_model = False
        self.in_training = False

        # For EEG cap connection and data
        self.simulate_data = False
        self.streams = resolve_stream()
        try:
            self.inlet = StreamInlet(self.streams[0])
        except:
            self.show_eeg_error("The EEG cap is not connected. Please connect the cap.")

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)  # Import UI from ui_interface.py

        # Set the control panel
        self.controlPanel = self.findChild(QWidget, "buttonsBox")
        self.controlPanel.installEventFilter(self)

        self.setWindowTitle("EEG-based BCI")

        # Apply style from the file style.json
        loadJsonStyle(self, self.ui, jsonFiles={"logs/style.json"})
        
        # Predefined colors
        colors = [
            QColor(255, 0, 0),      # Red
            QColor(255, 165, 0),    # Orange
            QColor(144, 238, 144),  # Light Green
            QColor(0, 128, 0),      # Green
            QColor(0, 128, 128),    # Blue-Green
            QColor(0, 255, 255),    # Cyan
            QColor(0, 0, 139),      # Dark Blue
            QColor(128, 0, 128),    # Purple
            QColor(255, 0, 255),    # Magenta
            QColor(255, 255, 0),    # Yellow
            QColor(0, 255, 0),      # Green
            QColor(0, 0, 255)       # Blue
        ]

        # Convert to pastel colors
        self.pastel_colors = [self.make_pastel(color) for color in colors]
        self.current_time = time.time()
        
        # Connect a function for if the buttons are clicked
        # User page:
        self.ui.addBtn.clicked.connect(self.addUser)
        self.ui.editBtn.clicked.connect(self.editUser)
        self.ui.removeBtn.clicked.connect(self.removeUser)
        self.ui.upBtn.clicked.connect(self.upUser)
        self.ui.downBtn.clicked.connect(self.downUser)
        self.ui.sortBtn.clicked.connect(self.sortUser)
        self.ui.usersList.itemClicked.connect(self.ChooseUser)
        # Menu
        self.ui.reconnectBtn.clicked.connect(self.reconnect_cap)
        self.ui.overviewBtn.clicked.connect(self.changeOverviewBtn)
        self.ui.usersBtn.clicked.connect(self.changeUsersBtn)
        self.ui.demosBtn.clicked.connect(self.changeDemosBtn)
        self.ui.exitBtn.clicked.connect(self.exitApp)
        # Demos submenu
        self.ui.cursorBtn.clicked.connect(self.setCursorPage)
        self.ui.trainBtn.clicked.connect(self.setTrainPage)
        self.ui.game1Btn.clicked.connect(self.openLavaGame)
        self.ui.game2Btn.clicked.connect(self.openAsteroid)
        # Button panel
        self.ui.startRecordingBtn.clicked.connect(self.startRecording)
        self.ui.stopRecordingBtn.clicked.connect(self.stopRecording)
        self.ui.openUserWindowBtn.clicked.connect(self.openUserWindow)
        self.ui.ERDSBtn.clicked.connect(self.openERDSWindow)
        self.ui.openPromptBtn.clicked.connect(self.setPromptPage)
        self.ui.startTimerBtn.clicked.connect(self.startPromptTimer)
        self.ui.dataTrainingBtn.clicked.connect(self.start_training)
        # Training values
        self.ui.batchSizeLine.textChanged.connect(self.bachtSizeChange)
        self.ui.marginLine.textChanged.connect(self.marginLineChange)
        self.ui.maxIterationLine.textChanged.connect(self.maxIterationLineChange)
        self.ui.learningRateLine.textChanged.connect(self.learningRateLineChange)

        # add users to user list from file
        with open('users.csv', newline='') as user_file:
            user_reader = csv.DictReader(user_file)
            for row in user_reader:
                self.ui.usersList.insertItem(self.ui.usersList.currentRow(), row["Name"])

        self.classify_result = ''

        # Data live plotting
        self.i = 0
        self.max_graph_width = 1000
        self.columns = 5
        self.av_height = int(self.max_graph_width/self.columns)
        self.channel = 1

        self.xdata = np.zeros(self.max_graph_width)
        self.ydata = [np.zeros(self.max_graph_width) for _ in range(8)]
        self.xf = np.zeros(251)
        self.y_fft2 = np.zeros(251)
        self.yBarGraph = np.zeros(self.columns)

        # FFT and band power plots
        # Window settings
        self.window = 500
        self.overlap = 0.25
        # calculate sample overlap
        self.overlap_win = int(self.overlap * self.window)
        # initial values
        self.y_win = np.zeros((self.window, 8))  # window array
        self.t_win = np.zeros(self.window)  # time array
        self.y_out = np.empty((0,8))
        self.t_out = np.array([])
        self.low = 8
        self.high = 30
        self.y_win_filt2 = np.zeros((self.window, 8))

        # Define frequency bands
        self.delta_band = (0.5, 4)
        self.theta_band = (4, 8)
        self.alpha_band = (8, 12)
        self.beta_band = (12, 30)
        self.gamma_band = (30, 50)

        # ML plots
        self.accuracy_data = np.array([0])
        self.loss_data = np.array([])

        # Create subplots and lines
        self.subplots = []
        self.lines = []

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
        self.xLabels = ['Delta', 'Theta', 'Alpha', 'Beta', 'Gamma']
        self.xBarGraph = list(range(1,len(self.xLabels)+1))

        self.power_band = pg.BarGraphItem(x=self.xBarGraph, height = self.yBarGraph, width = 1, brush = QColor(0, 166, 214), pen=QColor(255, 255, 255))
        self.ui.powerBandPlot.addItem(self.power_band)
        self.ui.powerBandPlot.getPlotItem().getAxis('bottom').setTicks([[(i, self.xLabels[i-1]) for i in self.xBarGraph]])
        self.ui.powerBandPlot.setYRange(0, 2)
        self.ui.powerBandPlot.setXRange(0.5, 5.5)
        self.ui.powerBandPlot.setMouseEnabled(x=False, y=True)
        self.ui.powerBandPlot.setMenuEnabled(False)
        self.ui.powerBandPlot.hideButtons()
        # Set axis labels after updating the data
        self.ui.powerBandPlot.getAxis('bottom').setLabel('Frequency Band')  # Set bottom axis label
        self.ui.powerBandPlot.getAxis('left').setLabel('Power Density [V^2/Hz]')  # Set left axis label
        self.ui.FFTPlot.getAxis('bottom').setLabel('Frequency [Hz]')
        self.ui.FFTPlot.getAxis('left').setLabel('Amplitude [uV]')

        self.start_time = time.time()

        # Check ERDS window
        self.check_timer = QTimer()
        self.check_timer.timeout.connect(self.check_plot_opened)

        self.signal_file = "plot_opened.signal"

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
            self.classification_thread = QThread()
            self.classification_worker = classificationWorker(self)
            self.classification_worker.moveToThread(self.classification_thread)
            self.classification_thread.started.connect(self.classification_worker.run)

            self.classification_worker.result.connect(self.reportProgress)

            self.classification_thread.start()

    def reportProgress(self, n):
        self.classify_result = n
    
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
        y_filtered_band= lfilter(b, a, np.array(y), axis =0)

        # Define the filter parameters
        lowcut = 48
        highcut = 52
        fs = 250  # Sampling frequency

        # Calculate the filter coefficients
        nyquist = 0.5 * fs
        low = lowcut / nyquist
        high = highcut / nyquist
        b, a = butter(4, [low, high], btype='bandstop')
        #zi = lfilter_zi(b,a)*y[0]

        # Apply the filter to each column of the DataFram
        y_filtered= lfilter(b, a, np.array(y_filtered_band), axis =0)

        return y_filtered
    
    
    # Function to calculate power in a specific frequency band
    def bandpower(self, frequencies, psd, band):
        band_freq_indices = np.logical_and(frequencies >= band[0], frequencies <= band[1])
        band_power = np.sum(psd[band_freq_indices])
        band_power_norm = band_power / (band[1] - band[0])
        return band_power_norm
        
    # Update graphs
    def update_plot(self):
        pen = pg.mkPen(self.pastel_colors[self.channel - 1], width = 2)
        plot_samples = 50
        # Gathering the data from the EEG cap
        if not self.simulate_data:
            sample, timestamp = self.inlet.pull_sample()
            sample_timestamp = (self.i) / 250
        else:
            sample, timestamp = self.generate_random_sample()  # For testing purposes when not connected to cap
            sample_timestamp = self.i / 250

        # Fill window for FFT plots

        # assign EEG data to array
        self.y_win[0] = sample[:8] # EEG data 1
        self.t_win[0] = (self.i)/250 # Counter from EEG cap in seconds

        # Shift the array with one index
        self.y_win = np.roll(self.y_win, -1, axis = 0)
        self.t_win = np.roll(self.t_win, -1)

        # When a new block of L is reached
        if self.i % self.overlap_win == 0 and self.i != self.overlap_win and self.i != 0:
            # # Apply a window function (Hamming window)
            window = np.hanning(len(self.y_win_filt2[:,self.channel - 1]))
            windowed_signal = self.y_win_filt2[:,self.channel - 1] * window      

            # zero pad the signal      
            #y_win_pad = np.pad(y_win_filt, int(0), 'constant')
            y_win_pad2 = np.pad(windowed_signal, int(261), 'constant') # pick the channel from the number key that is pressed
            # print(y_win_pad.shape) 

            self.xf = rfftfreq(y_win_pad2.shape[0], 1/250)
            #y_fft = np.abs(rfft(y_win_pad))
            self.y_fft2 = np.abs(rfft(y_win_pad2)) # Data to be plotted for FFT plot

            #  PSD
            # Compute the power spectral density using Welch's method
            frequencies, psd = welch(y_win_pad2, 250)

            # Powerbands            
            # Calculate power for each band
            delta_power = self.bandpower(frequencies, psd, self.delta_band)
            theta_power = self.bandpower(frequencies, psd, self.theta_band)
            alpha_power = self.bandpower(frequencies, psd, self.alpha_band)
            beta_power = self.bandpower(frequencies, psd, self.beta_band)
            gamma_power = self.bandpower(frequencies, psd, self.gamma_band)

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
                self.ui.FFTPlot.setXRange(0, 60)
                #self.ui.FFTPlot.setYRange(0, 50)
                self.ui.FFTPlot.setMouseEnabled(x=False, y=False)
                self.ui.FFTPlot.setMenuEnabled(False)
                self.ui.FFTPlot.hideButtons()

        # Only update the plot everytime it has collected plot update data sized data
        if self.i % plot_samples == 0 and self.i != 0:
            # filtered signal
            self.y_win_filt2 = self.filter(self.y_win, self.low, self.high)
            #self.y_win_filt2 = self.y_win

            self.xdata = np.roll(self.xdata, -plot_samples)
            self.xdata[-plot_samples:] = self.t_win[-plot_samples:]

            for k in range(8):
                self.ydata[k] = np.roll(self.ydata[k], -plot_samples)
                #self.ydata[k][-1] = sample[k]
                self.ydata[k][-plot_samples:] = self.y_win_filt2[-plot_samples:,k]
                self.lines[k].setData(self.xdata, self.ydata[k])


            if self.startFFT and not self.done_recording:
                self.FFT_plot.setData(self.xf, self.y_fft2)
                self.FFT_plot.setPen(pg.mkPen(self.pastel_colors[self.channel - 1], width = 2))
                self.power_band.setOpts(height=self.yBarGraph, brush=pg.mkBrush(self.pastel_colors[self.channel - 1]))

            print(time.time() - self.current_time)
            self.current_time = time.time()
        self.i += 1

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
            self.userWindow.show()

    # Set and open ERDS Window functions
    def openERDSWindow(self):
        self.ui.ERDSBtn.setText("Loading")
        self.ui.ERDSBtn.setEnabled(False)

        # Remove any existing signal file
        if os.path.exists(self.signal_file):
            os.remove(self.signal_file)

        self.ERDSplot_thread = QThread()
        self.ERDSplot_worker = ERDSplotWorker(self)
        self.ERDSplot_worker.moveToThread(self.ERDSplot_thread)
        self.ERDSplot_thread.started.connect(self.ERDSplot_worker.run)

        self.ERDSplot_thread.start()

        # Start a timer to check for the signal file
        self.check_timer.start(500)

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

    # Check ERDS window is opened
    def check_plot_opened(self):
        if os.path.exists(self.signal_file):
            self.ui.ERDSBtn.setText("ERDS")
            self.ui.ERDSBtn.setEnabled(True)
            self.check_timer.stop()
            os.remove(self.signal_file)

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

        new_directory = os.path.join(os.getcwd(), 'Data')
        new_directory = os.path.join(new_directory, str(self.current_id))
        new_directory = os.path.join(new_directory, "ICA")

        if not os.path.exists(new_directory):
            self.show_message("Train Error", "There are no recordings made for this user!")
            return
        
        full_file_path = os.path.join(new_directory, new_directory)

        self.train_thread = QThread()
        self.train_worker = trainWorker(int(self.ui.batchSizeLine.text()), float(self.ui.learningRateLine.text()),
                        int(self.ui.maxIterationLine.text()), 10, full_file_path, str(self.current_id), self, "Models/logits.pt", "Models/labels.pt")
        self.train_worker.moveToThread(self.train_thread)

        self.train_thread.started.connect(self.train_worker.load_train)
        self.train_worker.finished.connect(self.train_thread.quit)
        self.train_worker.finished.connect(self.train_worker.deleteLater)
        self.train_thread.finished.connect(self.train_thread.deleteLater)
        self.train_thread.finished.connect(self.resetPlots)
        self.train_worker.progress_to_main.connect(self.printProgress)
        self.train_worker.dataloading_to_main.connect(self.dataLoading)
        self.train_worker.training_started.connect(self.trainingStarted)
        self.train_worker.ML_to_main.connect(self.update_ML_plots)
        self.train_thread.start()
        self.in_training = True

        self.ui.dataTrainingBtn.setEnabled(False)
        self.train_thread.finished.connect(lambda: self.ui.dataTrainingBtn.setText("Train Data"))
        self.train_thread.finished.connect(lambda: self.ui.dataTrainingBtn.setEnabled(True))

    def printProgress(self, n):
        self.ui.dataTrainingBtn.setText(str(n))

    def dataLoading(self):
        self.ui.dataTrainingBtn.setText("Loading Data")

    def trainingStarted(self):
        self.ui.powerBandPlot.setAxisItems({
                'bottom': pg.AxisItem('bottom'),
                'left': pg.AxisItem('left')
                })
        self.ui.powerBandPlot.getAxis('bottom').setLabel('Progress')  # Set bottom axis label
        self.ui.powerBandPlot.getAxis('left').setLabel('Loss')  # Set left axis label
        self.ui.FFTPlot.getAxis('bottom').setLabel('Progress')
        self.ui.FFTPlot.getAxis('left').setLabel('Accuracy')

    def resetPlots(self):
        self.done_recording = False
        self.startFFT = False
        self.ui.FFTPlot.clear()
        self.ui.powerBandPlot.clear()
        self.ui.powerBandPlot.addItem(self.power_band)
        self.ui.powerBandPlot.getPlotItem().getAxis('bottom').setTicks([[(i, self.xLabels[i-1]) for i in self.xBarGraph]])
        self.ui.powerBandPlot.setYRange(0, 2)
        self.ui.powerBandPlot.setXRange(0.5, 5.5)
        self.ui.FFTPlot.setXRange(0, 60)
        self.ui.FFTPlot.enableAutoRange(axis='y', enable=True)
        self.ui.powerBandPlot.getAxis('bottom').setLabel('Frequency Band')  # Set bottom axis label
        self.ui.powerBandPlot.getAxis('left').setLabel('Power Density [V^2/Hz]')  # Set left axis label
        self.ui.FFTPlot.getAxis('bottom').setLabel('Frequency [Hz]')
        self.ui.FFTPlot.getAxis('left').setLabel('Amplitude [uV]')

    # updating the Machine Learning plots while training
    def update_ML_plots(self, accuracy, avgloss):
        # when it's the first time after recording we want to clear the previous plots
        self.accuracy_data = np.append(self.accuracy_data, accuracy)
        self.loss_data = np.append(self.loss_data, avgloss)

        if self.done_recording == False:
            pen = pg.mkPen(self.pastel_colors[self.channel - 1], width=2)
            # if the FFT and frequency band plots were used, clear them
            if self.startFFT:
                self.ui.FFTPlot.clear()
                self.ui.powerBandPlot.clear()
                # Reinitialize powerBandPlot axis
                self.ui.powerBandPlot.setYRange(0, 5)
                self.ui.powerBandPlot.setXRange(0, int(self.ui.maxIterationLine.text()) / 10)

            symbol_sign = None
            self.loss_plot = self.ui.powerBandPlot.plot(
                list(range(len(self.loss_data))),
                self.loss_data,
                name="Power Sensor",
                pen=pen,
                symbol=symbol_sign,
                symbolSize=5,
                symbolBrush="b",
            )
            self.accuracy_plot = self.ui.FFTPlot.plot(
                list(range(len(self.accuracy_data))),
                self.accuracy_data,
                name="Power Sensor",
                pen=pen,
                symbol=symbol_sign,
                symbolSize=5,
                symbolBrush="b",
            )
            self.ui.FFTPlot.setYRange(0, 100)
            self.ui.FFTPlot.setXRange(0, int(self.ui.maxIterationLine.text()) / 10)
            self.done_recording = True

        # update the plots with the new data
        self.accuracy_plot.setData(list(range(len(self.accuracy_data))), self.accuracy_data)
        self.loss_plot.setData(list(range(len(self.loss_data))), self.loss_data)

    # Functions that handles the user based interface
    def ChooseUser(self, item):
        self.ui.userID_test.setText(item.text())
        self.current_id = None
        with open('users.csv', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Name'] == item.text():
                    self.current_id = int(row['ID'])
        if not self.current_id:
            print("ERROR: USER " + item.text() + " HAS NO CORRESPONDING ID.")

        print("Current ID: ", self.current_id)

        if self.current_id == 0:
            self.has_model = False
        else:  # This checks if the selected user has a model trained.
            models_directory = os.path.join(os.getcwd(), 'Models')

            # if models folder does not exists, create it
            if not os.path.exists(models_directory):
                os.makedirs(models_directory)

            file_name = f"{self.current_id}.pt"
            # Construct the full file path
            full_file_path = os.path.join(models_directory, file_name)

            # Check if a file with the name exists in the 'models' directory
            file_exists = os.path.isfile(full_file_path)

            if not file_exists:
                self.show_message("No Model Error", "There currently is no model trained for this user. It is recommended" +
                                                    " to record and train on your own data for better accuracy.")
                self.has_model = False
            else:
                self.has_model = True

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

        if item.text() == "No user":
            self.show_message("Edit Error", "Cannot change the No user account!")
            return
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
        if(item.text() == "No user"):
            self.show_message("Deletion Error", "Cannot delete the No user account!")
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


# =======================================================================
# User Window class
# =======================================================================
class UserWindow(QMainWindow):
    go_signal = Signal()
    stop_signal = Signal()
    def __init__(self, main_window):
        super(UserWindow, self).__init__()
        self.ui = Ui_UserWindow()
        self.ui.setupUi(self) # Import UI from ui_userWindow.py
        self.main = main_window

        self.setWindowTitle("User Window")
        
        # Timer
        self.timer = QTimer()
        self.promptTimer = QTimer()

        # creating a timer
        self.timerupdate = QBasicTimer()
        self.timerupdate.start(80, self)

        self.stepsize = 10
        # Check clicked buttons and call their respective functions
        self.timer.timeout.connect(lambda: self.changePages())
        self.promptTimer.timeout.connect(lambda: self.changePrompt())

        self.classify_result = ''

        # Cap connection
        self.recording_thread = QThread()
        self.recording_worker = recordingWorker(self)
        self.recording_worker.moveToThread(self.recording_thread)
        self.recording_thread.started.connect(self.recording_worker.run)

        self.is_ready = False
        self.recording_worker.ready_signal.connect(self.set_ready)
        self.go_signal.connect(self.recording_worker.set_go_signal)
        self.stop_signal.connect(self.recording_worker.set_stop_signal)

        self.recording_thread.start()

    def set_ready(self):
        self.is_ready = True

    @Slot()
    def startRecording(self):
        global count
        global pageArray
        global i
        i = 0
        count = 0
        pageArray = [1,2,3,4 ,4,3,2,1 ,2,3,4,1 ,1,3,4,2 ,3,2,4,1 ,4,1,2,3, 0] # Fixed prompts for labeling
        while False == self.is_ready:
            time.sleep(0.1)
        self.go_signal.emit()  # emit go

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
        self.stop_signal.emit("Stop")
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
        #classifyProcess.kill()
    @Slot()
    def handle_signal_promptPage(self):
        self.ui.demosPages.setCurrentWidget(self.ui.promptPage)
        self.ui.promptTestWidget.setCurrentWidget(self.ui.calibrationPromptPage)
        self.promptTimer.stop()
        #classifyProcess.kill()

    def timerEvent(self, event):
        if event.timerId() == self.timerupdate.timerId():
            #prediction = classifyProcess.stdout.read1(1).decode("utf-8")
            self.classify_result = self.main.classify_result
            if self.classify_result == '':
                return

            self.classify_result = int(self.classify_result)

            self.step = 40  # Define step size for movement

            if self.classify_result == 3:
                if self.ui.mouseCursor.y() - self.stepsize > 0:
                    self.ui.mouseCursor.move(self.ui.mouseCursor.x(), self.ui.mouseCursor.y() - self.stepsize)
            elif self.classify_result == 0:
                if self.ui.mouseCursor.x() - self.stepsize > 0:
                    self.ui.mouseCursor.move(self.ui.mouseCursor.x() - self.stepsize, self.ui.mouseCursor.y())
            elif self.classify_result == 2:
                if self.ui.mouseCursor.y() + self.stepsize < (self.ui.cursorFrame.height() - self.ui.mouseCursor.height()):
                    self.ui.mouseCursor.move(self.ui.mouseCursor.x(), self.ui.mouseCursor.y() + self.stepsize)
            elif self.classify_result == 1:
                if self.ui.mouseCursor.x() + self.stepsize < (self.ui.cursorFrame.width() - self.ui.mouseCursor.width()):
                    self.ui.mouseCursor.move(self.ui.mouseCursor.x() + self.stepsize, self.ui.mouseCursor.y())

            # if self.main.classify_result != -1:
            #     self.main.classify_result = -1     

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


# =======================================================================
# Lava Game window class
# =======================================================================
class LavaGame(QMainWindow):
    def __init__(self, main):
        super().__init__()
        self.setWindowTitle("The Floor is Lava")
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.main = main

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

        # creating a timer
        self.timer = QBasicTimer()
        self.timer.start(80, self)

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

    # def timerEvent(self, event):
    #     if not self.game_over and event.timerId() == self.timer.timerId():
    #         #prediction = classifyProcess.stdout.read1(1).decode("utf-8")
    #         if prediction == '':
    #             return

    #         prediction = int(prediction)

    #         self.step = 40  # Define step size for movement

    #         if prediction == 3:
    #             if self.player.y() - self.step + 10 > 0:
    #                 self.player.move(self.player.x(), self.player.y() - self.step)
    #         elif prediction == 0:
    #             if self.player.x() - self.step > self.width()/6:
    #                 self.player.move(self.player.x() - self.step, self.player.y())
    #         elif prediction == 2:
    #             if self.player.y() + self.step < (self.height() - self.player.height()):
    #                 self.player.move(self.player.x(), self.player.y() + self.step)
    #         elif prediction == 1:
    #             if self.player.x() + self.step < (self.width() - self.player.width())-self.width()/6:
    #                 self.player.move(self.player.x() + self.step, self.player.y())


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

    # def keyPressEvent(self, event):
    #     if not self.game_over:
    #         prediction = int(classifyProcess.stdout.read1(1))
    
    #         self.step = 40  # Define step size for movement
    
    #         if prediction == 3:
    #             if self.player.y() - self.step + 10 > 0:
    #                 self.player.move(self.player.x(), self.player.y() - self.step)
    #         elif prediction == 0:
    #             if self.player.x() - self.step > self.width()/6:
    #                 self.player.move(self.player.x() - self.step, self.player.y())
    #         elif prediction == 2:
    #             if self.player.y() + self.step < (self.height() - self.player.height()):
    #                 self.player.move(self.player.x(), self.player.y() + self.step)
    #         elif prediction == 1:
    #             if self.player.x() + self.step < (self.width() - self.player.width())-self.width()/6:
    #                 self.player.move(self.player.x() + self.step, self.player.y())

    def keyPressEvent(self, event):

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
        #classifyProcess.kill()
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


# =======================================================================
# Asteroid Game window classes
# =======================================================================
class Asteroid(QMainWindow):
    def __init__(self, main):
        super(Asteroid, self).__init__()

        # creating a board object
        self.game = Game(self, main)

        # adding board as a central widget
        self.setCentralWidget(self.game)

        # setting title to the window
        self.setWindowTitle('Asteroid Shooter')

        # setting geometry to the window
        self.setGeometry(100, 100, 600, 400)

        # starting the board object
        self.game.start()


# =======================================================================
# Asteroid Game Frame classes
# =======================================================================
class Game(QFrame):
    # timer countdown time
    SPEED = 80

    # meteor settings
    MAXMETEORS = 3
    METEOR_SPEED = 3

    # constructor
    def __init__(self, parent, main):
        super(Game, self).__init__(parent)

        # creating a timer
        self.timer = QBasicTimer()

        # player location
        self.playerloc = 750

        self.main = main

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

    def read_prediction(self):
        prediction = self.main.classify_result
        print(prediction)
        if prediction == '':
            return

        prediction = int(prediction)

        if prediction == 0:
            self.direction = 0
        elif prediction == 1:
            self.direction = 1
        elif prediction != -1:
            self.spawn_bullet = True

        if self.main.classify_result != -1:
            self.main.classify_result = -1    

    # time event method
    def timerEvent(self, event):
        if self.width() < 500:
            pass
        else:
            # checking timer id
            if event.timerId() == self.timer.timerId():
                self.read_prediction()
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
                if pos_meteor[0] - 5 < pos[0] < pos_meteor[0] + self.cometSize and pos[1] < pos_meteor[1] + self.cometSize:
                    self.bullet.remove(pos)
                    self.meteor.remove(pos_meteor)
                    self.score += 1


# =======================================================================
# Training thread
# =======================================================================
class trainWorker(QObject):
    progress_to_main = Signal(int)
    dataloading_to_main = Signal()
    training_started = Signal()
    ML_to_main = Signal(float, float)
    finished = Signal()

    def __init__(self, batch_size: int, learning_rate: float, max_iters: int, eval_interval, load_cvs: str, user_ID: str, main: MainWindow, logits_train: str, targets_train: str):
        super().__init__()
        self.batch_size = batch_size
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.learning_rate = learning_rate
        self.max_iters = max_iters
        self.eval_interval = eval_interval
        self.load = load_cvs
        self.user_ID = user_ID
        self.main = main
        self.logits_train = logits_train
        self.targets_train = targets_train

    def train(self):
        logits_train = torch.load(self.logits_train)
        targets_train = torch.load(self.targets_train)
        targets_train = targets_train - 1
        #logits_train = logits_train[:, None, :, :]
        print(logits_train.shape)
        print(targets_train.shape)
        dataset = torch.utils.data.TensorDataset(logits_train, targets_train)
        train = DataLoader(dataset, batch_size=self.batch_size, shuffle=True)
        model = escargot().to(self.device)
        model.train()
        optimizer = torch.optim.Adam(model.parameters(), lr=self.learning_rate, weight_decay=1e-3)
        loss = torch.nn.CrossEntropyLoss()
        scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=30, gamma=0.7)
        llist = []
        tlist = []
        avloss = []
        acc_list = []
        # -----training loop-----#
        for itere in range(self.max_iters):
            f_list, t_list = next(iter(train))
            t_list = t_list.type(torch.LongTensor)
            if itere % self.eval_interval == 0 or itere == self.max_iters - 1:
                with torch.no_grad():
                    model.eval()
                    out = model(f_list.to(self.device, dtype=torch.float))  # tf_list.to(device),tff_list.to(device)
                    # print(torch.max(out,dim=1))
                    values, ind = torch.max(out, dim=1)
                    g = t_list.shape
                    # print(g)
                    a = np.sum((torch.eq(ind.to("cpu"), t_list.to("cpu")).numpy()))
                    # print(a)
                    accuracy = (a / g) * 100
                    tlist.append(accuracy)
                    avgloss = (np.sum(avloss) / (len(avloss)))
                    progress = (itere / self.max_iters) * 100
                    print("accuracy : {}, validation loss : {}, progress : {}%, lr : {}".format(accuracy, avgloss,
                                                                                                int(progress),
                                                                                                scheduler.get_last_lr()))
                    self.progress_to_main.emit(progress)
                    avloss = []
                    if itere == 0:
                        print(" ")
                    else:
                        llist.append(avgloss)
                        acc_list.append(accuracy)
                        self.ML_to_main.emit(float(accuracy), float(avgloss))
            else:
                model.train()
                inputs = model(f_list.to(self.device, dtype=torch.float))  # ,ff_list.to(device)batch_list.to(device)
                # print(inputs[0])
                with torch.no_grad():
                    val_input = model(
                        f_list.to(self.device, dtype=torch.float))  # test_list.to(device),tff_list.to(device)
                lossvalue = loss(inputs, t_list.to(self.device))
                # print(lossvalue)
                vallvalue = loss(val_input.to(self.device), t_list.to(self.device))
                avloss.append(vallvalue.data.cpu().numpy())
                optimizer.zero_grad(set_to_none=True)
                lossvalue.backward()
                optimizer.step()
                scheduler.step()
        # -----training loop-----#

        models_directory = os.path.join(os.getcwd(), 'Models')

        # if models folder does not exists, create it
        if not os.path.exists(models_directory):
            os.makedirs(models_directory)

        file_name = f"{self.user_ID}.pt"
        # Construct the full file path
        full_file_path = os.path.join(models_directory, file_name)

        # Check if a file with the same name already exists in the 'models' directory
        #file_exists = os.path.isfile(full_file_path)

        # if file_exists:
        #     reply = QMessageBox.question(
        #         None,
        #         "File Exist",
        #         "A model already exists for this user. Do you want to overwrite it?",
        #         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        #     if reply == QMessageBox.StandardButton.No:
        #         self.main.show_message("Save Canceled", "The existing model was not overwritten.")
        #         return

        torch.save(model.state_dict(), full_file_path)
        self.main.has_model = True
        self.finished.emit()
        # print(acc_list)
        # print(np.sum(acc_list)/10)

    def dataloader(self):
        combologits = torch.empty(0, 1, 529, 8)
        combolabels = torch.empty(0)

        input_directory = self.load
        output_directory = os.path.join(os.getcwd(), 'Models')

        for filename in os.listdir(input_directory):

            if filename.endswith(".csv"):
                filepath = os.path.join(input_directory, filename)
                data_csv = pd.read_csv(filepath, delimiter=',')
                data_csv = data_csv.iloc[:72000, :8]

                data_csv_detr = cleaner.detrend(data_csv)
                data_csv_filt = cleaner.filter(data_csv_detr)
                data_csv_np = np.array(data_csv_filt)
                (data_csv_res, lables) = cleaner.cursed_reshape(data_csv_np)

                print(data_csv_res.shape)
                print(lables.shape)

                data_torch = torch.from_numpy(data_csv_res)
                lables_torch = torch.from_numpy(lables)

                logits = data_torch.squeeze(1)
                data_torch = cleaner.CAR_filter(logits)
                logits = data_torch.unsqueeze(1)

                combologits = torch.cat((combologits, logits), dim=0)
                combolabels = torch.cat((combolabels, lables_torch), dim=0)

        user_logits_path = os.path.join(output_directory, 'logits.pt')
        user_labels_path = os.path.join(output_directory, 'labels.pt')

        torch.save(combologits, user_logits_path)
        torch.save(combolabels, user_labels_path)

    def load_train(self):
        self.dataloading_to_main.emit()
        self.dataloader()
        self.training_started.emit()
        self.train()


# =======================================================================
# Classification QThread
# =======================================================================
class classificationWorker(QObject):
    result = Signal(int)

    def __init__(self, main: MainWindow):
        super().__init__()
        self.main = main

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
        y_filtered_band= lfilter(b, a, np.array(y), axis =0)

        # Define the filter parameters
        lowcut = 48
        highcut = 52
        fs = 250  # Sampling frequency

        # Calculate the filter coefficients
        nyquist = 0.5 * fs
        low = lowcut / nyquist
        high = highcut / nyquist
        b, a = butter(4, [low, high], btype='bandstop')
        #zi = lfilter_zi(b,a)*y[0]

        # Apply the filter to each column of the DataFram
        y_filtered= lfilter(b, a, np.array(y_filtered_band), axis =0)

        return y_filtered

    def run(self):
        #   Window settings
        window = 529
        overlap = 0

        #   ML settings

        # initial values:
        y_win = np.zeros((window, 8))  # window array
        t_win = np.zeros(window)  # time array
        t = 1
        i = 1
        y_out = np.empty((0, 8))
        t_out = np.array([])
        # step 0: initialize lsl 
        streams = resolve_stream()
        inlet = StreamInlet(streams[0])
        # step 1: read user id
        user_id = self.main.current_id
        # step 2: load corresponding model
        # *** up to machine learning group to implement
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model = escargot().to(device)

        if not self.main.has_model:
            user_id = 0

        models_directory = os.path.join(os.getcwd(), 'Models')

        # if models folder does not exists, create it
        if not os.path.exists(models_directory):
            os.makedirs(models_directory)

        file_name = f"{user_id}.pt"

        # Construct the full file path
        full_file_path = os.path.join(models_directory, file_name)
        print(full_file_path)

        model.load_state_dict(torch.load(full_file_path, map_location=torch.device('cpu')))
        #loop
        while True:
            # step 4: windowing
            sample,timestamp = inlet.pull_sample() 
            overlap_win = int((1 - overlap) * window)
            if overlap_win < 1:
                raise Exception("overlap is too large")
            y_win[0, :] = sample[0:8] # EEG data 1
            t_win[0] = (i)/250 # Counter from EEG cap in seconds
            y_win = np.roll(y_win, -1)
            t_win = np.roll(t_win, -1)
            if i % window == 0 and i != window and i != 0:
                # step 5: filtering
                y_win_filt = self.filter(y_win, 0.5, 38)
                # step 6: Send data to GUI
                # *** omited for testing *** Update: not necessary
                # step 7: Classify window
                with torch.no_grad():
                    torch_data = torch.from_numpy(y_win_filt).unsqueeze(0).unsqueeze(0)
                    model.eval()
                    output_vector = model(torch_data.to(device, dtype=torch.float))
                    print(output_vector)
                    self.classify_result = torch.max(output_vector, dim=1)[1][0].item() 
                    # step 8: Output classification
                    self.result.emit(self.classify_result)
                    if self.classify_result == 0:
                        self.main.ui.directionLine.setText('Left')
                    elif self.classify_result == 1:
                        self.main.ui.directionLine.setText('Right')
                    elif self.classify_result == 2:
                        self.main.ui.directionLine.setText('Down')
                    elif self.classify_result == 3:
                        self.main.ui.directionLine.setText('Up')
            i += 1


# =======================================================================
# Recording QThread
# =======================================================================
class recordingWorker(QObject):
    ready_signal = Signal()
    go_signal = False
    stop_signal = "Continue"

    def __init__(self, main: MainWindow):
        super().__init__()
        self.main = main

    def set_go_signal(self):
        self.go_signal = True

    def set_stop_signal(self):
        self.stop_signal = "Stop"

    def run(self):
        finished = False

        # initialize the colomns of your data and your dictionary to capture the data.
        # columns=['Time','FZ', 'C3', 'CZ', 'C4', 'PZ', 'PO7', 'OZ', 'PO8','AccX','AccY','AccZ','Gyro1','Gyro2','Gyro3', 'Battery','Counter','Validation']
        columns = ['FZ', 'C3', 'CZ', 'C4', 'PZ', 'PO7', 'OZ', 'PO8', 'Counter', 'Validation']
        columns_index_dict = {'FZ': 0, 'C3': 1, 'CZ': 2, 'C4': 3, 'PZ': 4, 'PO7': 5, 'OZ': 6, 'PO8': 7, 'Counter': 15,
                            'Validation': 16}

        pageArray = [1, 2, 3, 4, 4, 3, 2, 1, 2, 3, 4, 1, 1, 3, 4, 2, 3, 2, 4, 1, 4, 1, 2, 3, 0]
        pageNumber = 0

        # prompt time settings
        prompt_time = 6  # time of each prompt in seconds
        promptsamples = prompt_time * 48 * 250  # amount of samples of each recording (time * amount of prompts * sampling rate + 5 samples as buffer)

        # 1. Right hand, 2. Left hand, 3. Tongue, 4. Feet, 0. Rest

        while True:

            data_dict = dict((k, []) for k in columns)
            label = []

            streams = resolve_stream()
            inlet = StreamInlet(streams[0])

            self.ready_signal.emit()  # ready signal
            while False == self.go_signal:
                time.sleep(0.1)

            current_id = self.main.current_id  # Convert the received input to an integer

            i = 0
            pageNumber = 0

            while not finished:
                # get the streamed data. Columns of sample are equal to the columns variable, only the first element being timestamp
                # concatenate timestamp and data in 1 list

                sample, timestamp = inlet.pull_sample()
                all_data = sample

                # logger.info(len(data_dict['Counter']))

                # print(all_data) # print the data coming from the EEG cap

                # updating data dictionary with newly transmitted samples   
                for column in data_dict.keys():  # iterate over the columns of the data dictionary
                    data_dict[column].append(all_data[columns_index_dict[column]])  # append the data to the corresponding column

                ### Add label column
                if len(data_dict['Counter']) % int(250 * (
                        prompt_time * 2)) == 0:  # Each prompt takes 12 seconds in total. Set pageNumber to 0 which is the rest state
                    pageNumber = 0
                elif len(data_dict['Counter']) % int(250 * (
                prompt_time)) == 0:  # After 6 seconds the action will appear. Set pageNumber to pageArray[i] which is the action
                    pageNumber = pageArray[i]
                else:  # Else assign the same pageNumber
                    pageNumber = pageNumber

                label.append(pageNumber)  # Append to list label

                # After 12 seconds add 1 to i, which goes to the next prompt
                if len(data_dict['Counter']) % int(250 * (prompt_time * 2)) == 0 and len(data_dict['Counter']) != 0:
                    i += 1

                # data is collected at 250 Hz. Let's stop data collection after 60 seconds. Meaning we stop when we collected 250*60 samples.
                if len(data_dict['Counter']) >= (
                        promptsamples + 5):  # 72005 = sampling_rate * seconds_per_prompt * num_prompts + 5_seconds_leeway
                    finished = True  # 72005 = 250*(6+6)*(4*6)+5

                if len(data_dict['Counter']) % int(promptsamples / 48) == 0:
                    recieved_loop = self.stop_signal()
                    if recieved_loop == "Stop":
                        finished = True
                        inlet.close_stream()

                        # lastly, we can save our data to a CSV format.
            data_df = pd.DataFrame.from_dict(data_dict)
            now = datetime.now()

            if recieved_loop != "Stop":

                # Add column to the data_df called label
                data_df["Label"] = label  # add new column to the Dataframe
                data_df.to_csv(
                    'Data/' + str(current_id) + '/EEGdata-' + now.strftime("%Y-%j--%H-%M-%S") + '.csv',
                    index=False)

                # ICA filtering
                # ICA_filtering(current_id, 'EEGdata-' + now.strftime("%Y-%j--%H-%M-%S"))

            else:
                # Add column to the data_df called label
                data_df["Label"] = label # add new column to the Dataframe
                data_df.to_csv('MeasurementSubgroup/Our_measurements/Measurement_prompt/EEGdata-' + now.strftime("%Y-%j--%H-%M-%S") + '_STOP.csv', index = False)

            inlet.close_stream()

            finished = False

# =======================================================================
# ERDS plots QThread
# =======================================================================
class ERDSplotWorker(QObject):
    def __init__(self, main: MainWindow):
        super().__init__()
        self.main = main
    
    def run(self):
        # Modified from code by: Clemens Brunner <clemens.brunner@gmail.com>
        #                        Felix Klotzsche <klotzsche@cbs.mpg.de>
        #
        # License: BSD-3-Clause
        # Copyright the MNE-Python contributors.

        import os
        import matplotlib.pyplot as plt
        import numpy as np
        import pandas as pd
        import seaborn as sns
        from matplotlib.colors import TwoSlopeNorm

        import mne
        from mne.datasets import eegbci
        from mne.io import concatenate_raws, read_raw_edf
        from mne.stats import permutation_cluster_1samp_test as pcluster_test

        # config
        mne.set_log_level('WARNING')

        def singlefile(filename):
            output = np.genfromtxt('MeasurementSubgroup/Our_measurements/Measurement_prompt/' + filename, delimiter=',')[1:, :]
            events = np.array([[ 1500, 0, 1],
                                [ 4500, 0, 2],
                                [ 7500, 0, 3],
                                [10500, 0, 4],
                                [13500, 0, 4],
                                [16500, 0, 3],
                                [19500, 0, 2],
                                [22500, 0, 1],
                                [25500, 0, 2],
                                [28500, 0, 3],
                                [31500, 0, 4],
                                [34500, 0, 1],
                                [37500, 0, 1],
                                [40500, 0, 3],
                                [43500, 0, 4],
                                [46500, 0, 2],
                                [49500, 0, 3],
                                [52500, 0, 2],
                                [55500, 0, 4],
                                [58500, 0, 1],
                                [61500, 0, 4],
                                [64500, 0, 1],
                                [67500, 0, 2],
                                [70500, 0, 3]])

            return (output, events)
            

        #———————————————————————————————————————————————————————————————————————
        #(allOutputs, events) = multifile(["EEGdata-2024-149--16-41-44.csv"])
        #———————————————————————————————————————————————————————————————————————
        recordings_list = os.listdir('MeasurementSubgroup/Our_measurements/Measurement_prompt')
        (allOutputs, events) = singlefile(recordings_list[-2])
        #———————————————————————————————————————————————————————————————————————

        channels = allOutputs[:, 0:8].transpose()

        # create mne_info object
        ch_names =        ['Fz', 
                    'C3',  'Cz',  'C4', 
                        'Pz', 
                    'PO7', 'Oz',  'PO8'] 

        ch_type = ['eeg' for i in range(8)]
        mne_info = mne.create_info(ch_names, float(250), ch_types=ch_type)

        #create mne.raw object
        raw = mne.io.RawArray(channels, mne_info)
        raw.set_montage(mne.channels.make_standard_montage("standard_1005"))

        tmin, tmax = -1, 4
        event_ids = {'right': 1, "left": 2, 'tongue': 3, 'feet': 4}  # map event IDs to tasks

        epochs = mne.Epochs(
            raw,
            events = events,
            event_id=[1, 2, 3, 4],
            tmin=tmin - 0.5,
            tmax=tmax + 0.5,
            picks=(    'Fz', 
                'C3',  'Cz',  'C4', 
                    'Pz', 
                'PO7', 'Oz',  'PO8'),
            baseline=None,
            preload=True,
        )

        freqs = np.arange(2, 36)  # frequencies from 2-35Hz
        vmin, vmax = -1, 1.5  # set min and max ERDS values in plot
        baseline = (-1, 0)  # baseline interval (in s)
        cnorm = TwoSlopeNorm(vmin=vmin, vcenter=0, vmax=vmax)  # min, center & max ERDS

        kwargs = dict(
            n_permutations=100, step_down_p=0.05, seed=1, buffer_size=None, out_type="mask"
        )  # for cluster test

        # Finally, we perform time/frequency decomposition over all epochs.
        tfr = epochs.compute_tfr(
            method="multitaper",
            freqs=freqs,
            n_cycles=freqs,
            use_fft=True,
            return_itc=False,
            average=False,
            decim=2,
        )
        tfr.crop(tmin, tmax).apply_baseline(baseline, mode="percent")

        df = tfr.to_data_frame(time_format=None)
        df.head()

        df = tfr.to_data_frame(time_format=None, long_format=True)

        # Map to frequency bands:
        freq_bounds = {"_": 0, "delta": 3, "theta": 7, "alpha": 13, "beta": 35, "gamma": 140}
        df["band"] = pd.cut(
            df["freq"], list(freq_bounds.values()), labels=list(freq_bounds)[1:]
        )

        # Filter to retain only relevant frequency bands:
        freq_bands_of_interest = ["delta", "theta", "alpha", "beta"]
        df = df[df.band.isin(freq_bands_of_interest)]
        df["band"] = df["band"].cat.remove_unused_categories()

        # Order channels for plotting:
        df["channel"] = df["channel"].cat.reorder_categories(('Fz', 'C3', 'Cz', 'C4', 'Pz', 'PO7', 'Oz', 'PO8'), ordered=True)

        df = df.drop(df.index[df['time'].isin([-1.004])], axis=0)

        g = sns.FacetGrid(df, row="band", col="channel", margin_titles=True)
        g.map(sns.lineplot, "time", "value", "condition", n_boot=10)
        axline_kw = dict(color="black", linestyle="dashed", linewidth=0.5, alpha=0.5)
        g.map(plt.axhline, y=0, **axline_kw)
        g.map(plt.axvline, x=0, **axline_kw)
        g.set(ylim=(None, 1.5))
        g.set_axis_labels("Time (s)", "ERDS")
        g.set_titles(col_template="{col_name}", row_template="{row_name}")
        g.add_legend(ncol=2, loc="lower center")
        g.figure.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.08)


        plt.show()


def show_main_window():
    window1.showMaximized()
    window1.show()

    splash.finish(window1)


# Creates the app and runs the Mainwindow
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
    window2 = UserWindow(window1)
    window3 = LavaGame(window1)
    window4 = Asteroid(window1)

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