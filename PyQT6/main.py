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



#Mainwindow from which everything can be called
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.stepsize = 5

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
        x_axis_range = 80
        symbol_sign = None

        pen = pg.mkPen(color=(255, 0, 0))
        self.time = list(range(x_axis_range))
        self.power = [randint(20, 40) for _ in range(x_axis_range)]
        self.power_2 = [randint(20, 40) for _ in range(x_axis_range)]
        self.power_3 = [randint(20, 40) for _ in range(x_axis_range)]
        self.power_4 = [randint(20, 40) for _ in range(x_axis_range)]
        self.power_5 = [randint(20, 40) for _ in range(x_axis_range)]
        self.power_6 = [randint(20, 40) for _ in range(x_axis_range)]
        self.power_7 = [randint(20, 40) for _ in range(x_axis_range)]
        self.power_8 = [randint(20, 40) for _ in range(x_axis_range)]
        # Get a line reference
        self.line = self.ui.graphicsView.plot(
            self.time,
            self.power,
            name="Power Sensor",
            pen=pen,
            symbol=symbol_sign,
            symbolSize=5,
            symbolBrush="b",
        )
        self.line_2 = self.ui.graphicsView_2.plot(
            self.time,
            self.power_2,
            name="Power Sensor",
            pen=pen,
            symbol=symbol_sign,
            symbolSize=5,
            symbolBrush="b",
        )
        self.line_3 = self.ui.graphicsView_3.plot(
            self.time,
            self.power_3,
            name="Power Sensor",
            pen=pen,
            symbol=symbol_sign,
            symbolSize=5,
            symbolBrush="b",
        )
        self.line_4 = self.ui.graphicsView_4.plot(
            self.time,
            self.power_4,
            name="Power Sensor",
            pen=pen,
            symbol=symbol_sign,
            symbolSize=5,
            symbolBrush="b",
        )
        self.line_5 = self.ui.graphicsView_5.plot(
            self.time,
            self.power_5,
            name="Power Sensor",
            pen=pen,
            symbol=symbol_sign,
            symbolSize=5,
            symbolBrush="b",
        )
        self.line_6 = self.ui.graphicsView_6.plot(
            self.time,
            self.power_6,
            name="Power Sensor",
            pen=pen,
            symbol=symbol_sign,
            symbolSize=5,
            symbolBrush="b",
        )
        self.line_7 = self.ui.graphicsView_7.plot(
            self.time,
            self.power_7,
            name="Power Sensor",
            pen=pen,
            symbol=symbol_sign,
            symbolSize=5,
            symbolBrush="b",
        )
        self.line_8 = self.ui.graphicsView_8.plot(
            self.time,
            self.power_8,
            name="Power Sensor",
            pen=pen,
            symbol=symbol_sign,
            symbolSize=5,
            symbolBrush="b",
        )
        self.line_17 = self.ui.graphicsView_17.plot(
            self.time,
            self.power,
            name="Power Sensor",
            pen=pen,
            symbol=symbol_sign,
            symbolSize=5,
            symbolBrush="b",
        )
        self.line_17.setFftMode(True)
        # Add a timer to simulate new temperature measurements
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

        
        self.show()
        
    # Update graphs
    def update_plot(self):
        self.time = self.time[1:]

        self.time.append(self.time[-1] + 1)
        self.power = self.power[1:]
        self.power.append(randint(20, 40))
        self.power_2 = self.power_2[1:]
        self.power_2.append(randint(20, 40))
        self.power_3 = self.power_3[1:]
        self.power_3.append(randint(20, 40))
        self.power_4 = self.power_4[1:]
        self.power_4.append(randint(20, 40))
        self.power_5 = self.power_5[1:]
        self.power_5.append(randint(20, 40))
        self.power_6 = self.power_6[1:]
        self.power_6.append(randint(20, 40))
        self.power_7 = self.power_7[1:]
        self.power_7.append(randint(20, 40))
        self.power_8 = self.power_8[1:]
        self.power_8.append(randint(20, 40))

        self.line.setData(self.time, self.power)
        self.line_2.setData(self.time, self.power_2)
        self.line_3.setData(self.time, self.power_3)
        self.line_4.setData(self.time, self.power_4)
        self.line_5.setData(self.time, self.power_5)
        self.line_6.setData(self.time, self.power_6)
        self.line_7.setData(self.time, self.power_7)
        self.line_8.setData(self.time, self.power_8)
        self.line_17.setData(self.time, self.power)

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