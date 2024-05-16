import pyqtgraph.examples
from random import randint

import pyqtgraph as pg
from PyQt6.QtWidgets import QApplication, QMainWindow
import numpy as np

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create a plot widget
        self.plot_widget = pg.PlotWidget()
        self.setCentralWidget(self.plot_widget)

        # Generate some random data for demonstration
        x = np.linspace(0, 10, 1000)
        y = np.sin(x)

        # Plot the data
        self.plot_widget.plot(x, y)

        # Set FFT mode
        self.plot_widget.setFftMode(True)  # Set FFT mode to True

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()