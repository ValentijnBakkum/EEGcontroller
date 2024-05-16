import os
import sys
import json
import csv
from random import randint
from ui_interface import *
from ui_trainWindow import Ui_TrainWindow
from Custom_Widgets import *
from PyQt6.QtWidgets import QInputDialog, QMessageBox
from PySide6.QtCore import QTimer, Slot, Signal
import random
import numpy as np
import time
from pylsl import StreamInlet, resolve_stream



#Mainwindow from which everything can be called
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.stepsize = 5
        self.startFFT = False

        # for EEG cap data
        self.streams = resolve_stream()
        # self.inlet = StreamInlet(self.streams[0])

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

        self.ui.trainBtn.clicked.connect(self.changeTrainBtn)
        self.ui.testBtn.clicked.connect(self.changeTestBtn)
        self.ui.usersBtn.clicked.connect(self.changeUsersBtn)
        self.ui.exitBtn.clicked.connect(self.exitApp)
        #Training window
        self.app = TrainWindow()
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
        self.max_graph_width = 75
        self.plot_delay = 5

        self.xdata = np.zeros(self.max_graph_width)
        self.ydata = [np.zeros(self.max_graph_width) for _ in range(8)]
        symbol_sign = None

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

        # Add a timer to simulate new temperature measurements
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

        
        self.show()
        
    # Update graphs
    def update_plot(self):
        self.j = self.i // self.plot_delay

        if self.i % self.plot_delay:
            # gathering the data from the EEG cap
            # sample, timestamp = inlet.pull_sample()
            sample, timestamp = self.generate_random_sample()  # for testing purposes when not connected to cap
            sample_timestamp = sample[15]

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
            if self.startFFT:
                self.line_17.setData(self.xdata, self.ydata[0])
        if self.ui.mainPages.currentIndex() == 0:  # testing mode
            self.line_9.setData(self.xdata, self.ydata[0])
            self.line_10.setData(self.xdata, self.ydata[1])
            self.line_11.setData(self.xdata, self.ydata[2])
            self.line_12.setData(self.xdata, self.ydata[3])
            self.line_13.setData(self.xdata, self.ydata[4])
            self.line_14.setData(self.xdata, self.ydata[5])
            self.line_15.setData(self.xdata, self.ydata[6])
            self.line_16.setData(self.xdata, self.ydata[7])
            if self.startFFT:
                self.line_19.setData(self.xdata, self.ydata[0])

        self.i += 1

    # for testing purposes
    def generate_random_sample(self):
        # Simulate random data generation
        return random.sample(range(0, 100), 15) + [time.time()], 0

    #Call the training window
    def openTrainWindow(self):
        if self.app.isHidden():
            self.app.show()
        else:
            self.app.hide()

    def exitApp(self):
        QApplication.quit()    

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
        elif event.key() == Qt.Key_A:
            if self.ui.mouseCursor.x() - self.stepsize > 0:
                self.ui.mouseCursor.move(self.ui.mouseCursor.x() - self.stepsize, self.ui.mouseCursor.y())
        elif event.key() == Qt.Key_S:
            if self.ui.mouseCursor.y() + self.stepsize < (self.ui.frame_9.height() - self.ui.mouseCursor.height()):
                self.ui.mouseCursor.move(self.ui.mouseCursor.x(), self.ui.mouseCursor.y() + self.stepsize)
        elif event.key() == Qt.Key_D:
            if self.ui.mouseCursor.x() + self.stepsize < (self.ui.frame_9.width() - self.ui.mouseCursor.width()):
                self.ui.mouseCursor.move(self.ui.mouseCursor.x() + self.stepsize, self.ui.mouseCursor.y())
        self.ui.lineEdit_5.setText(str(self.ui.mouseCursor.x()))
        self.ui.lineEdit_6.setText(str(self.ui.mouseCursor.y()))
        self.update()


#Training window class
class TrainWindow(QMainWindow):
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

    def startRecording(self):
        self.timer.start(6000)
        global count
        global pageArray
        global i
        i = 0
        count = 0
        pageArray = [1,2,3,4 ,4,3,2,1 ,2,3,4,1 ,1,3,4,2 ,3,2,4,1 ,4,1,2,3, 0]

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

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())