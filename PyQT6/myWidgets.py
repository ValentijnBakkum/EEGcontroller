from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QTextEdit, QVBoxLayout, QWidget)
import csv
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

# For user name text editing
class UserTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.user_id = None

    # when a key is pressed
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            user_name = self.toPlainText().strip()
            if user_name:
                self.setHtml(f"<html><font size='100'><b>{user_name}</b></font></html>")
                self.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Align text center horizontally
                rows = []
                with open('users.csv', newline='') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        if row['ID'] == self.user_id:  # Update the name for the corresponding user ID
                            row['Name'] = user_name
                        rows.append(row)
                with open('users.csv', 'w', newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=['Name', 'ID'])
                    writer.writeheader()
                    writer.writerows(rows)
            self.clearFocus()  # Remove focus from the QTextEdit
        else:
            # Handle other key press events
            super().keyPressEvent(event)

    def set_user_id(self, id):
        self.user_id = id

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=1, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)
        