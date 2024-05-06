import os
import sys
import json
from ui_interface import *
from Custom_Widgets import *
from PyQt6.QtWidgets import QInputDialog, QMessageBox

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        loadJsonStyle(self, self.ui, jsonFiles = {
                        "logs/style.json"
                            }) 
        self.ui.addBtn.clicked.connect(self.addUser)
        self.ui.editBtn.clicked.connect(self.editUser)
        self.ui.removeBtn.clicked.connect(self.removeUser)
        self.ui.upBtn.clicked.connect(self.upUser)
        self.ui.downBtn.clicked.connect(self.downUser)
        self.ui.sortBtn.clicked.connect(self.sortUser)
        

        self.show()

    def addUser(self):
        currentIndex = self.ui.usersList.currentRow()
        text, ok = QInputDialog.getText(None, "New User", "User Name")
        if ok and text is not None:
            self.ui.usersList.insertItem(currentIndex, text)

    def editUser(self):
        currentIndex = self.ui.usersList.currentRow()
        item = self.ui.usersList.item(currentIndex)
        if item is not None:
            text, ok = QInputDialog.getText(None, "New User", "User Name")
            if ok and text is not None:
                item.setText(text)
            
    def removeUser(self):
        currentIndex = self.ui.usersList.currentRow()
        item = self.ui.usersList.item(currentIndex)
        if item is None:
            return

        question = QMessageBox.question(None,"Remove User",
             "Do you want to remove user? " + item.text(),
             QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if question == QMessageBox.StandardButton.Yes:
            item = self.ui.usersList.takeItem(currentIndex)
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


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())