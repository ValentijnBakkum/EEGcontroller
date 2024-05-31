import sys
import random
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout, QWidget, QMessageBox
from PyQt6.QtCore import QSize, QTimer
from PyQt6.QtGui import QFont
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

class SnakeGame(QMainWindow):
    def __init__(self):
        super(SnakeGame, self).__init__()
 
        # creating a board object
        self.board = Board(self)
 
        # creating a status bar to show result
        self.statusbar = self.statusBar()
 
        # adding border to the status bar
        self.statusbar.setStyleSheet("& quot border: 2px solid black & quot")
 
        # calling showMessage method when signal received by board
        self.board.msg2statusbar[str].connect(self.statusbar.showMessage)
 
        # adding board as a central widget
        self.setCentralWidget(self.board)
 
        # setting title to the window
        self.setWindowTitle('Snake game')
 
        # setting geometry to the window
        self.setGeometry(100, 100, 600, 400)
 
        # starting the board object
        self.board.start()
 
        # showing the main window
        self.show()
 
# creating a board class
# that inherits QFrame
 
 
class Board(QFrame):
 
    # creating signal object
    msg2statusbar = pyqtSignal(str)
 
    # speed of the snake
    # timer countdown time
    SPEED = 80
 
    # block width and height
    WIDTHINBLOCKS = 60
    HEIGHTINBLOCKS = 40
 
    # constructor
    def __init__(self, parent):
        super(Board, self).__init__(parent)
 
        # creating a timer
        self.timer = QBasicTimer()
 
        # snake
        self.snake = [[5, 10], [5, 11]]
 
        # current head x head
        self.current_x_head = self.snake[0][0]
        # current y head
        self.current_y_head = self.snake[0][1]
 
        # food list
        self.food = []
 
        # growing is false
        self.grow_snake = False
 
        # board list
        self.board = []
 
        # direction
        self.direction = 1
 
        # called drop food method
        self.drop_food()
 
        # setting focus
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
 
    # square width method
    def square_width(self):
        return self.contentsRect().width() / Board.WIDTHINBLOCKS
 
    # square height
    def square_height(self):
        return self.contentsRect().height() / Board.HEIGHTINBLOCKS
 
    # start method
    def start(self):
        # msg for status bar
        # score = current len - 2
        self.msg2statusbar.emit(str(len(self.snake) - 2))
 
        # starting timer
        self.timer.start(Board.SPEED, self)
 
    # paint event
    def paintEvent(self, event):
 
        # creating painter object
        painter = QPainter(self)
 
        # getting rectangle
        rect = self.contentsRect()
 
        # board top
        boardtop = rect.bottom() - Board.HEIGHTINBLOCKS * self.square_height()
 
        # drawing snake
        for pos in self.snake:
            self.draw_square(painter, rect.left() + pos[0] * self.square_width(),
                             boardtop + pos[1] * self.square_height())
 
        # drawing food
        for pos in self.food:
            self.draw_square(painter, rect.left() + pos[0] * self.square_width(),
                             boardtop + pos[1] * self.square_height())
 
    # drawing square
    def draw_square(self, painter, x, y):
        # color
        color = QColor(0x228B22)
 
        # painting rectangle
        painter.fillRect(x + 1, y + 1, self.square_width() - 2,
                         self.square_height() - 2, color)
 
    # key press event
    def keyPressEvent(self, event):
 
        # getting key pressed
        key = event.key()
 
        # if left key pressed
        if key == Qt.Key.Key_Left:
            # if direction is not right
            if self.direction != 2:
                # set direction to left
                self.direction = 1
 
        # if right key is pressed
        elif key == Qt.Key.Key_Right:
            # if direction is not left
            if self.direction != 1:
                # set direction to right
                self.direction = 2
 
        # if down key is pressed
        elif key == Qt.Key.Key_Down:
            # if direction is not up
            if self.direction != 4:
                # set direction to down
                self.direction = 3
 
        # if up key is pressed
        elif key == Qt.Key.Key_Up:
            # if direction is not down
            if self.direction != 3:
                # set direction to up
                self.direction = 4
 
    # method to move the snake
    def move_snake(self):
 
        # if direction is left change its position
        if self.direction == 1:
            self.current_x_head, self.current_y_head = self.current_x_head - 1, self.current_y_head
 
        # if direction is right change its position
        if self.direction == 2:
            self.current_x_head, self.current_y_head = self.current_x_head + 1, self.current_y_head
            # if it goes beyond right wall
            if self.current_x_head == Board.WIDTHINBLOCKS:
                self.current_x_head = 0
 
        # if direction is down change its position
        if self.direction == 3:
            self.current_x_head, self.current_y_head = self.current_x_head, self.current_y_head + 1
            # if it goes beyond down wall
            if self.current_y_head == Board.HEIGHTINBLOCKS:
                self.current_y_head = 0
 
        # if direction is up change its position
        if self.direction == 4:
            self.current_x_head, self.current_y_head = self.current_x_head, self.current_y_head - 1
 
        # changing head position
        head = [self.current_x_head, self.current_y_head]
        # inset head in snake list
        self.snake.insert(0, head)
 
        # if snake grow is False
        if not self.grow_snake:
            # pop the last element
            self.snake.pop()
 
        else:
            # show msg in status bar
            self.msg2statusbar.emit(str(len(self.snake)-2))
            # make grow_snake to false
            self.grow_snake = False
 
    # time event method
    def timerEvent(self, event):
 
        # checking timer id
        if event.timerId() == self.timer.timerId():
 
            # call move snake method
            self.move_snake()
            # call food collision method
            self.is_food_collision()
            # call is suicide method
            self.is_suicide()
            # update the window
            self.update()
 
    # method to check if snake collides itself
    def is_suicide(self):
        # traversing the snake
        for i in range(1, len(self.snake)):
            # if collision found
            if self.snake[i] == self.snake[0]:
                # show game ended msg in status bar
                self.msg2statusbar.emit(str("& quot Game Ended & quot"))
                # making background color black
                self.setStyleSheet("& quotbackground-color: black& quot")
                # stopping the timer
                self.timer.stop()
                # updating the window
                self.update()
 
    # method to check if the food cis collied
    def is_food_collision(self):
 
        # traversing the position of the food
        for pos in self.food:
            # if food position is similar of snake position
            if pos == self.snake[0]:
                # remove the food
                self.food.remove(pos)
                # call drop food method
                self.drop_food()
                # grow the snake
                self.grow_snake = True
 
    # method to drop food on screen
    def drop_food(self):
        # creating random co-ordinates
        x = random.randint(3, 58)
        y = random.randint(3, 38)
 
        # traversing if snake position is not equal to the
        # food position so that food do not drop on snake
        for pos in self.snake:
            # if position matches
            if pos == [x, y]:
                # call drop food method again
                self.drop_food()
 
        # append food location
        self.food.append([x, y])

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
    #game = MemoryMatchGame()
    game = SnakeGame()
    game.show()
    sys.exit(app.exec())
