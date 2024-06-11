import sys
from PySide6.QtCore import Qt, QMimeData, QEvent
from PySide6.QtGui import QDrag, QDropEvent
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit

class DraggableWidget(QWidget):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: lightblue; padding: 10px;")
        self.setFixedSize(150, 100)
        
        layout = QVBoxLayout()
        self.label = QLabel(text, self)
        self.label.setStyleSheet("background-color: lightgreen; padding: 5px;")
        self.line_edit = QLineEdit(self)
        self.button = QPushButton("Click Me", self)
        self.button.clicked.connect(self.on_button_clicked)
        
        layout.addWidget(self.label)
        layout.addWidget(self.line_edit)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            drag = QDrag(self)
            mime_data = QMimeData()
            mime_data.setText(self.label.text())
            drag.setMimeData(mime_data)
            drag.exec_(Qt.MoveAction)

    def on_button_clicked(self):
        self.label.setText(self.line_edit.text())

class DropArea(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setStyleSheet("background-color: lightgrey; padding: 10px;")
        self.setFixedSize(300, 300)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        text = event.mimeData().text()
        widget = DraggableWidget(text)
        self.layout.addWidget(widget)
        event.acceptProposedAction()

class MainWindow(QMainWindow):
    def __init__(self, title):
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(100, 100, 400, 300)
        self.drop_area = DropArea()
        self.setCentralWidget(self.drop_area)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window1 = MainWindow("Main Window 1")
    main_window2 = MainWindow("Main Window 2")

    draggable_widget = DraggableWidget("Drag Me")
    main_window1.drop_area.layout.addWidget(draggable_widget)

    main_window1.show()
    main_window2.show()

    sys.exit(app.exec())
