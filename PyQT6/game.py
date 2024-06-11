import sys
import random
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QLabel
from PySide6.QtCore import QTimer, QSize, Qt


class LavaGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("The Floor is Lava")
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.grid_layout = QGridLayout(self.central_widget)
        self.central_widget.setLayout(self.grid_layout)

        self.create_grid()
        self.create_player()

        self.warning_timer = QTimer(self)
        self.warning_timer.timeout.connect(self.generate_warning)

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
        self.countdown_value = 5  # Increased countdown value to 5 seconds

        # Start the game with countdown
        self.start_countdown()

    def start_countdown(self):
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
            self.start_game()

    def start_game(self):
        self.warning_timer.start(7000)  # Start the warning timer with an initial delay
        self.check_collision_timer.start(50)  # Check collision every 50 milliseconds

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

    def create_player(self):
        self.player = QWidget(self.central_widget)
        self.player.setFixedSize(120, 120)
        self.player.setStyleSheet("background-color: blue; border: 1px solid black;")
        self.player.move(1220, 640)  # Position the player initially

    def generate_warning(self):
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

        QTimer.singleShot(3000, self.generate_lava)  # Schedule turning warning tiles to lava after 3 seconds

    def generate_lava(self):
        for tile in self.red_tiles:
            tile.setStyleSheet("background-color: red; border: 1px solid black;")
        QTimer.singleShot(3000, self.revert_lava)  # Schedule reverting lava tiles to white after 3 seconds

    def revert_lava(self):
        for tile in self.red_tiles:
            tile.setStyleSheet("background-color: white; border: 1px solid black;")
        self.start_game()  # Start a new cycle of the game

    def check_collision(self):
        if not self.game_over:
            player_rect = self.player.geometry()
            for tile in self.red_tiles:
                if tile.styleSheet() == "background-color: red; border: 1px solid black;" and player_rect.intersects(tile.geometry()):
                    self.game_over = True
                    self.player.setFixedSize(1000, 100)
                    self.player.move(self.width() / 2 - self.player.width() / 2, self.height() / 2 - self.player.height() / 2)  # Move player to center
                    self.player.setStyleSheet("background-color: black;")
                    self.game_over_label = QLabel("Game Over", self.central_widget)  # Set the parent to the central widget
                    self.game_over_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.game_over_label.setGeometry(0, 0, self.width(), self.height())  # Position the QLabel to cover the entire window
                    self.game_over_label.setStyleSheet("font-size: 100px; color: red;")
                    self.game_over_label.raise_()  # Raise the QLabel to the top of the z-order
                    self.game_over_label.show()  # Ensure the QLabel is visible
    def keyPressEvent(self, event):
        if not self.game_over:
            self.step = 40  # Define step size for movement
            if event.key() == Qt.Key.Key_W:
                if self.player.y() - self.step + 10 > 0:
                    self.player.move(self.player.x(), self.player.y() - self.step)
            elif event.key() == Qt.Key.Key_A:
                if self.player.x() - self.step > 420:
                    self.player.move(self.player.x() - self.step, self.player.y())
            elif event.key() == Qt.Key.Key_S:
                if self.player.y() + self.step < (self.height() - self.player.height()):
                    self.player.move(self.player.x(), self.player.y() + self.step)
            elif event.key() == Qt.Key.Key_D:
                if self.player.x() + self.step < (self.width() - self.player.width())-420:
                    self.player.move(self.player.x() + self.step, self.player.y())

    def closeEvent(self, event):
        # Stop the game timers when the window is closed
        self.warning_timer.stop()
        self.check_collision_timer.stop()
        self.countdown_timer.stop()
        event.accept()  # Accept the close event

    def showEvent(self, event):
        # Restart the game when the window is shown
        self.start_countdown()
        event.accept()  # Accept the show event:
        # Restart the game when the window is shown
        self.start_countdown()
        event.accept()  # Accept the show event


# importing libraries
from PySide6.QtCore import Qt, QBasicTimer
from PySide6.QtWidgets import QMainWindow, QApplication, QFrame
from PySide6.QtGui import QPainter, QColor, QFont
import random
import sys


# creating game window
class Asteroid(QMainWindow):
    def __init__(self):
        super(Asteroid, self).__init__()

        # creating a board object
        self.game = Game(self)

        # adding board as a central widget
        self.setCentralWidget(self.game)

        # setting title to the window
        self.setWindowTitle('Asteroid Shooter')

        # setting geometry to the window
        self.setGeometry(100, 100, 600, 400)

        # starting the board object
        self.game.start()

        # showing the main window
        self.show()


# The game
class Game(QFrame):
    # timer countdown time
    SPEED = 80

    # meteor settings
    MAXMETEORS = 3
    METEOR_SPEED = 3

    # constructor
    def __init__(self, parent):
        super(Game, self).__init__(parent)

        # creating a timer
        self.timer = QBasicTimer()

        # player location
        self.playerloc = 750

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


    # time event method
    def timerEvent(self, event):
        # checking timer id
        if event.timerId() == self.timer.timerId():
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
                if pos[0] > pos_meteor[0] and pos[0] < pos_meteor[0] + self.cometSize and pos[1] < pos_meteor[1] + self.cometSize:
                    self.bullet.remove(pos)
                    self.meteor.remove(pos_meteor)
                    self.score += 1

# main method
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LavaGame()
    window.showMaximized()
    sys.exit(app.exec())
