import sys
import random
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout, QWidget, QMessageBox
from PyQt6.QtCore import QSize, QTimer
from PyQt6.QtGui import QFont

class TicTacToeGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tic-Tac-Toe")
        self.setGeometry(100, 100, 300, 300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.grid_layout = QGridLayout(self.central_widget)

        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_over = False

        for row in range(3):
            for col in range(3):
                button = QPushButton("")
                button.setFixedSize(QSize(100, 100))
                font = button.font()
                font.setPointSize(24)
                button.setFont(font)
                button.clicked.connect(lambda _, r=row, c=col: self.on_button_clicked(r, c))
                self.grid_layout.addWidget(button, row, col)
                self.buttons[row][col] = button

    def on_button_clicked(self, row, col):
        if self.game_over or self.buttons[row][col].text():
            return

        self.buttons[row][col].setText(self.current_player)
        if self.check_winner():
            self.show_winner(self.current_player)
            self.game_over = True
        elif self.is_draw():
            self.show_winner("No one")
            self.game_over = True
        else:
            self.current_player = 'O' if self.current_player == 'X' else 'X'

    def check_winner(self):
        for row in range(3):
            if self.buttons[row][0].text() == self.buttons[row][1].text() == self.buttons[row][2].text() != '':
                return True
        for col in range(3):
            if self.buttons[0][col].text() == self.buttons[1][col].text() == self.buttons[2][col].text() != '':
                return True
        if self.buttons[0][0].text() == self.buttons[1][1].text() == self.buttons[2][2].text() != '':
            return True
        if self.buttons[0][2].text() == self.buttons[1][1].text() == self.buttons[2][0].text() != '':
            return True
        return False

    def is_draw(self):
        for row in range(3):
            for col in range(3):
                if not self.buttons[row][col].text():
                    return False
        return True

    def show_winner(self, winner):
        msg = QMessageBox()
        msg.setWindowTitle("Game Over")
        msg.setText(f"{winner} wins!")
        msg.exec()


class MemoryMatchGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Memory Match")
        self.setGeometry(100, 100, 400, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.grid_layout = QGridLayout(self.central_widget)

        self.buttons = [[None for _ in range(4)] for _ in range(4)]
        self.values = list(range(1, 9)) * 2
        random.shuffle(self.values)
        self.current_pair = []
        self.matched_pairs = 0

        for row in range(4):
            for col in range(4):
                button = QPushButton("")
                button.setFixedSize(QSize(100, 100))
                font = button.font()
                font.setPointSize(24)
                button.setFont(font)
                button.clicked.connect(lambda _, r=row, c=col: self.on_button_clicked(r, c))
                self.grid_layout.addWidget(button, row, col)
                self.buttons[row][col] = button

    def on_button_clicked(self, row, col):
        button = self.buttons[row][col]
        if button.text() or len(self.current_pair) == 2:
            return

        button.setText(str(self.values[row * 4 + col]))
        self.current_pair.append((row, col))

        if len(self.current_pair) == 2:
            QTimer.singleShot(1000, self.check_pair)

    def check_pair(self):
        row1, col1 = self.current_pair[0]
        row2, col2 = self.current_pair[1]

        if self.values[row1 * 4 + col1] == self.values[row2 * 4 + col2]:
            self.buttons[row1][col1].setEnabled(False)
            self.buttons[row2][col2].setEnabled(False)
            self.matched_pairs += 1
            if self.matched_pairs == 8:
                self.show_winner()
        else:
            self.buttons[row1][col1].setText("")
            self.buttons[row2][col2].setText("")

        self.current_pair = []

    def show_winner(self):
        msg = QMessageBox()
        msg.setWindowTitle("Game Over")
        msg.setText("You found all pairs!")
        msg.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    #game = TicTacToeGame()
    game = MemoryMatchGame()
    game.show()
    sys.exit(app.exec())
