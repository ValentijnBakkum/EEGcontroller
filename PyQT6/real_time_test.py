import os
import sys
import json
import csv
from random import randint
from ui_interface import *
from Custom_Widgets import *
from PySide6.QtWidgets import QInputDialog, QMessageBox, QSplashScreen
#from PyQt6.QtCore import Qt
from PySide6.QtCore import Qt, QTimer, Slot, Signal
import random
import numpy as np
import time
import pyqtgraph as pg
from pylsl import StreamInlet, resolve_stream

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.ticker as ticker
import queue
import numpy as np
import sounddevice as sd

from PyQt6 import QtCore, QtWidgets,QtGui
from PyQt6 import uic
from PyQt6.QtCore import pyqtSlot

class MplCanvas(FigureCanvas):
	def __init__(self, parent=None, width=5, height=4, dpi=100):
		fig = Figure(figsize=(width, height), dpi=dpi)
		self.axes = fig.add_subplot(111)
		super(MplCanvas, self).__init__(fig)
		fig.tight_layout()

#Mainwindow from which everything can be called
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("EEG-based BCI")

        #Apply style from the file style.json
        loadJsonStyle(self, self.ui, jsonFiles = {
                        "logs/style.json"
                            })

        
        #Real-time plotting
        self.threadpool = QtCore.QThreadPool()

        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.ui.plotsWidget.addWidget(self.canvas, 2, 1, 1, 1)
        self.reference_plot = None
        self.q = queue.Queue(maxsize=20)

        self.window_length = 1000
        self.downsample = 1
        self.channels = [1]
        self.interval = 30 

        self.samplerate = 250
        length  = int(self.window_length*self.samplerate/(1000*self.downsample))
        sd.default.samplerate = self.samplerate

        self.plotdata =  np.zeros((length,len(self.channels)))
        self.timer = QtCore.QTimer()
        self.timer.setInterval(self.interval) #msec
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()
        self.data=[0]
        self.ui.startRecordingBtn.clicked.connect(self.start_worker)
        self.worker = None
        self.go_on = False

        self.start_time = time.time()

    def getData(self):
        self.streams = resolve_stream()
        try:
            self.inlet = StreamInlet(self.streams[0])
            #Counter init
            sample, timestamp = self.inlet.pull_sample()
            self.counter_init = sample[15] 
        except:
            self.show_eeg_error("The EEG cap is not connected. Please connect the cap.")

    def start_worker(self):
        worker = Worker(self.start_stream, )
        self.threadpool.start(worker)

    def start_stream(self):
        self.getData()

    def update_plot(self):
        try:
            data=[0]
            
            while True:
                try: 
                    data = self.q.get_nowait()
                except queue.Empty:
                    break
                shift = len(data)
                self.plotdata = np.roll(self.plotdata, -shift,axis = 0)
                self.plotdata[-shift:,:] = data
                self.ydata = self.plotdata[:]
                self.canvas.axes.set_facecolor((0,0,0))
                
        
                if self.reference_plot is None:
                    plot_refs = self.canvas.axes.plot( self.ydata, color=(0,1,0.29))
                    self.reference_plot = plot_refs[0]				
                else:
                    self.reference_plot.set_ydata(self.ydata)

            
            self.canvas.axes.yaxis.grid(True,linestyle='--')
            start, end = self.canvas.axes.get_ylim()
            self.canvas.axes.yaxis.set_ticks(np.arange(start, end, 0.1))
            self.canvas.axes.yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.1f'))
            self.canvas.axes.set_ylim( ymin=-0.5, ymax=0.5)		
            self.canvas.draw()
        except:
            pass

class Worker(QtCore.QRunnable):

	def __init__(self, function, *args, **kwargs):
		super(Worker, self).__init__()
		self.function = function
		self.args = args
		self.kwargs = kwargs

	@pyqtSlot()
	def run(self):

		self.function(*self.args, **self.kwargs)
          
#Creates the app and runs the Mainwindow
app = QApplication(sys.argv)
window1 = MainWindow()
window1.show()

sys.exit(app.exec_())