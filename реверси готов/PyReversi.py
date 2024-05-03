################################################################################
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <https://www.gnu.org/licenses/>.
#
################################################################################

APPLICATION_NAME = "PyReversi"
APPLICATION_VERSION = "1.0.0.0"

import random
import os
import copy
import math

from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

################################################################################

BLACK = -1
WHITE = 1
HINT = 2
MOVE = 2

class Board:
    def __init__(self):
        self.state = []
        for i in range(8):
            self.state.append([0, 0, 0, 0, 0, 0, 0, 0])
        self.reset()
        
    def reset(self):
        for y in range(8):
            for x in range(8):
                self.state[y][x] = 0
        self.state[3][3] = WHITE
        self.state[3][4] = BLACK
        self.state[4][3] = BLACK
        self.state[4][4] = WHITE
        
    def make_move(self, x, y, color):
        self.state[y][x] = color
        flips = self.get_flips(x, y)
        for x, y in flips:
            self.state[y][x] = color
    
    def is_neighboring_line(self, x, y, dirx, diry, color):
        posx = x + dirx
        posy = y + diry
        while posx >= 0 and posx < 8 and posy >= 0 and posy < 8:
            if self.state[posy][posx] != color:
                return False
            posx += dirx
            posy += diry
        return True
    
    def neighbor_count(self, x, y, color):
        n = 0
        if self.is_neighboring_line(x, y, -1,  0, color):
            n += 1
        if self.is_neighboring_line(x, y, -1, -1, color):
            n += 1
        if self.is_neighboring_line(x, y,  0, -1, color):
            n += 1
        if self.is_neighboring_line(x, y, +1, -1, color):
            n += 1
        if self.is_neighboring_line(x, y, +1,  0, color):
            n += 1
        if self.is_neighboring_line(x, y, +1, +1, color):
            n += 1
        if self.is_neighboring_line(x, y,  0, +1, color):
            n += 1
        if self.is_neighboring_line(x, y, -1, +1, color):
            n += 1
        return n
        
    def think(self):
        moves = self.find_next_moves(WHITE)
        if len(moves) == 0:
            return -1, -1
        # ------- create list of possible moves -------
        db = []
        for move in moves:
            x, y = move
            self.state[y][x] = WHITE
            flips = self.get_flips(x, y)
            self.state[y][x] = 0
            db.append((move, self.neighbor_count(x, y, WHITE), len(flips)))
        # ------- corners first -------
        lst = []
        for e in db:
            if e[0] in ((0, 0), (0, 7), (7, 0), (7, 7)):
                lst.append(e)
        if len(lst) > 0:
            max_lst = max(lst, key=lambda x: x[2])
            return max_lst[0]
        # ------- then edges, except cells that neighbor corners  -------
        lst.clear()
        for e in db:
            x, y = e[0]
            if ((x >= 2 and x <= 5) and (y == 0 or y == 7)) or \
               ((y >= 2 and y <= 5) and (x == 0 or x == 7)):
                lst.append(e)
        if len(lst) > 0:
            max_lst = max(lst, key=lambda x: x[2])
            return max_lst[0]
        # ------- else choose move closest to the middle -------
        min_dist = 100
        min_move = None
        for e in db:
            x, y = e[0]
            d = math.sqrt((x - 3.5) ** 2 + (y - 3.5) ** 2)
            if d < min_dist:
                min_dist = d
                min_move = e[0]
        return min_move
            
    def disk_count(self, color):
        bc = 0
        wc = 0
        for y in range(8):
            for x in range(8):
                if self.state[y][x] == BLACK:
                    bc += 1
                elif self.state[y][x] == WHITE:
                    wc += 1
        if color == BLACK:
            return bc
        elif color == WHITE:
            return wc
        elif color == BLACK + WHITE:
            return bc + wc
    
    def at(self, x, y):
        return self.state[y][x]
    
    def set(self, x, y, color):
        self.state[y][x] = color

    def find_next_move(self, x, y, incx, incy):
        color = self.state[y][x]
        n = 0
        x += incx
        y += incy
        while (x >= 0 and x < 8 and y >= 0 and y < 8) and \
              (self.state[y][x] == -color):
            n += 1
            x += incx
            y += incy
        if (n > 0) and (x >= 0 and x < 8 and y >= 0 and y < 8) and \
           (self.state[y][x] == 0):
            return x, y
        else:
            return -1, -1
            
    def find_next_moves(self, color):
        
        def add_move(l, xy):
            if xy[0] != -1:
                l.append(xy)
                
        moves = []
        for y in range(8):
            for x in range(8):
                if self.state[y][x] == color:
                    add_move(moves, self.find_next_move(x, y,  0, -1))
                    add_move(moves, self.find_next_move(x, y, +1, -1))
                    add_move(moves, self.find_next_move(x, y, +1,  0))
                    add_move(moves, self.find_next_move(x, y, +1, +1))
                    add_move(moves, self.find_next_move(x, y,  0, +1))
                    add_move(moves, self.find_next_move(x, y, -1, +1))
                    add_move(moves, self.find_next_move(x, y, -1,  0))
                    add_move(moves, self.find_next_move(x, y, -1, -1))
        return moves

    def get_flips(self, x, y):

        def add_flips(flips, x, y, incx, incy):
            color = self.state[y][x]
            x += incx
            y += incy
            while (x >= 0 and x < 8 and y >= 0 and y < 8) and \
                  (self.state[y][x] == -color):
                x += incx
                y += incy
            if (x >= 0 and x < 8 and y >= 0 and y < 8) and \
               (self.state[y][x] == color):
                x -= incx
                y -= incy
                while self.state[y][x] == -color:
                    flips.append((x, y))
                    x -= incx
                    y -= incy

        flips = []
        add_flips(flips, x, y,  0, -1)
        add_flips(flips, x, y, +1, -1)
        add_flips(flips, x, y, +1,  0)
        add_flips(flips, x, y, +1, +1)
        add_flips(flips, x, y,  0, +1)
        add_flips(flips, x, y, -1, +1)
        add_flips(flips, x, y, -1,  0)
        add_flips(flips, x, y, -1, -1)
        return flips


class ReversiWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.grid_x = 0
        self.grid_y = 0
        self.tile_size = 0
        self.border_width = 1
        self.grid = []
        self.recalc_layout()
        # Enable mouse move events without buttons pressed.
        self.setMouseTracking(True)
        self.board = Board()
        self.thinking = False
        self.timer_id = 0
        self.pass_flag = False
        self.game_over_flag = False
        self.valid_moves = self.board.find_next_moves(BLACK)
        
    def reset(self):
        self.board.reset()
        self.thinking = False
        self.pass_flag = False
        self.game_over_flag = False
        self.valid_moves = self.board.find_next_moves(BLACK)
        if self.timer_id > 0:
            self.killTimer(self.timer_id)
            self.timer_id = 0
        self.repaint()
        
    def recalc_layout(self):
        grid_size = min(self.width(), self.height())
        grid_size -= 9 * self.border_width
        grid_size -= 2 * round(self.fontMetrics().height())
        self.tile_size = grid_size // 8
        self.grid_x = (self.width() - 8 * (self.tile_size + self.border_width) -\
                      self.border_width) // 2
        self.grid_y = (self.height() - 8 * (self.tile_size + self.border_width) -\
                      self.border_width) // 2
    
    def get_tile_rect(self, x, y):
        x = self.grid_x + (1 + x) * self.border_width + x * self.tile_size
        y = self.grid_y + (1 + y) * self.border_width + y * self.tile_size
        w = self.tile_size
        h = self.tile_size
        return QRect(x, y, w, h)
        
    def draw_background(self, qpainter):
        qpainter.save()
        qpainter.setBrush(QBrush(QColor(0,128,0)))
        qpainter.drawRect(self.rect())
        qpainter.restore()

    def resizeEvent(self, event):
        self.recalc_layout()
        QWidget.resizeEvent(self, event)

    def draw_grid(self, qpainter):
        qpainter.save()
        pen = QPen()
        pen.setStyle(Qt.PenStyle.NoPen)
        qpainter.setPen(pen)
        qpainter.setBrush(QBrush(QColor(0,0,0)))
        # Vertical lines.
        for i in range(9):
            r = QRect(self.grid_x + i * (self.tile_size + self.border_width), \
                      self.grid_y, \
                      self.border_width, \
                      8 * self.tile_size + 9 * self.border_width)
            qpainter.drawRect(r)
        # Horizontal lines.
        for i in range(9):
            r = QRect(self.grid_x + self.border_width, \
                      self.grid_y + i * (self.tile_size + self.border_width), \
                      8 * (self.tile_size + self.border_width), \
                      self.border_width)
            qpainter.drawRect(r)
        # Draw four dots.
        qpainter.drawEllipse(self.grid_x + 2 * (self.tile_size + self.border_width) - 3, \
                             self.grid_y + 2 * (self.tile_size + self.border_width) - 3, \
                             7, 7)
        qpainter.drawEllipse(self.grid_x + 6 * (self.tile_size + self.border_width) - 3, \
                             self.grid_y + 2 * (self.tile_size + self.border_width) - 3, \
                             7, 7)
        qpainter.drawEllipse(self.grid_x + 2 * (self.tile_size + self.border_width) - 3, \
                             self.grid_y + 6 * (self.tile_size + self.border_width) - 3, \
                             7, 7)
        qpainter.drawEllipse(self.grid_x + 6 * (self.tile_size + self.border_width) - 3, \
                             self.grid_y + 6 * (self.tile_size + self.border_width) - 3, \
                             7, 7)                             
        qpainter.restore()

    def draw_disk(self, qpainter, x, y, color):
        qpainter.setBrush(QColorConstants.Black)
        if color == WHITE:
            qpainter.setBrush(QColorConstants.White)
        elif color == MOVE:
            qpainter.setBrush(QBrush(QColorConstants.Black, style=Qt.BrushStyle.BDiagPattern))
        r = self.get_tile_rect(x, y)
        t = round(r.width() * 0.9) # Trim r by t.
        qpainter.drawEllipse(r.marginsRemoved(QMargins(t, t, t, t)))

    def draw_disks(self, qpainter):
        qpainter.save()
        pen = QPen()
        pen.setStyle(Qt.PenStyle.NoPen)
        qpainter.setPen(pen)
        for y in range(8):
            for x in range(8):
                color = self.board.at(x, y)
                if color != 0:
                    self.draw_disk(qpainter, x, y, color)
        qpainter.restore()
        
    def draw_valid_moves(self, qpainter):
        qpainter.save()
        pen = QPen()
        pen.setStyle(Qt.PenStyle.NoPen)
        qpainter.setPen(pen)
        qpainter.setBrush(QBrush(QColorConstants.Black, style=Qt.BrushStyle.BDiagPattern))
        for x, y in self.valid_moves:
            self.draw_disk(qpainter, x, y, MOVE)
        qpainter.restore()

    def paintEvent(self, event):
        qpainter = QPainter(self)
        qpainter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform|QPainter.RenderHint.Antialiasing)
        self.draw_background(qpainter)
        self.draw_grid(qpainter)
        self.draw_disks(qpainter)
        if not self.thinking and not self.game_over_flag:
            self.draw_valid_moves(qpainter)
        
    def get_tile_at(self, x, y):
        for i in range(8):
            for j in range(8):
                if self.get_tile_rect(i, j).contains(x, y, False):
                    return i, j
        return -1, -1
    
    def start_thinking(self):
        # Set thinking flag to block user input.
        self.thinking = True
        self.timer_id = self.startTimer(random.randint(400, 1000))           

    def stop_thinking(self):
        self.thinking = False
        self.valid_moves = self.board.find_next_moves(BLACK)
        self.repaint()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            x = int(event.position().x())
            y = int(event.position().y())
            tx, ty = self.get_tile_at(x, y)
            if not self.thinking and not self.game_over_flag and \
               (tx, ty) in self.valid_moves:
                    self.board.make_move(tx, ty, BLACK)
                    self.repaint()
                    self.pass_flag = False
                    if self.board.disk_count(BLACK + WHITE) == 64:
                        self.end_game()
                    else:
                        self.start_thinking()
                        self.repaint()  # Hide valid moves.
                        
    def timerEvent(self, event):
        self.killTimer(self.timer_id)
        self.timer_id = 0
        x, y = self.board.think()
        if x != -1:
            self.board.make_move(x, y, WHITE)
            self.repaint()
            self.pass_flag = False
            if self.board.disk_count(BLACK + WHITE) == 64:
                self.end_game()
            else:
                self.stop_thinking()
        else:
            if self.pass_flag:
                self.end_game()
            else:
                self.pass_flag = True
                mb = QMessageBox()
                mb.setIcon(QMessageBox.Icon.Information)
                mb.setWindowTitle(self.window().windowTitle())
                mb.setText("I'll have to pass. Your turn.")
                mb.exec()
                self.stop_thinking()

    def end_game(self):
        mb = QMessageBox()
        mb.setIcon(QMessageBox.Icon.Information)
        mb.setWindowTitle(self.window().windowTitle())
        bc = self.board.disk_count(BLACK)
        wc = self.board.disk_count(WHITE)
        if bc > wc:
            text = "Black wins."
        elif bc < wc:
            text = "White wins."
        else:
            text = "The game is a tie."        
        mb.setText(text)
        info = f"Black: {bc} / White: {wc}"
        mb.setInformativeText(info)
        mb.exec()
        self.game_over_flag = True
        
    def mouseMoveEvent(self, event):
        x = int(event.position().x())
        y = int(event.position().y())
        if x >= self.grid_x and \
           x < self.grid_x + 9 * self.border_width + 8 * self.tile_size and \
           y >= self.grid_y and \
           y < self.grid_y + 9 * self.border_width + 8 * self.tile_size:
            self.setCursor(Qt.CursorShape.CrossCursor)
        else:
            self.unsetCursor()
                 
################################################################################

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setStyleSheet("font-size: 10pt;")
        self.load_settings()
        self.init_ui()
        self.setWindowTitle("PyReversi")
        self.setWindowIcon(QIcon("PyReversi.ico"))
        self.show()

    def init_ui(self):
        self.reversi_widget = ReversiWidget()
        self.setCentralWidget(self.reversi_widget)
        menu_bar = self.menuBar()
        # ------- Game -------
        game_menu = menu_bar.addMenu("&Game")
        game_menu.aboutToShow.connect(self.game_menu_about_to_show)
        menu_item = QAction("&New", self)
        menu_item.triggered.connect(self.on_game_new)
        game_menu.addAction(menu_item)
        self.pass_action = QAction("&Pass", self)
        self.pass_action.triggered.connect(self.on_game_pass)
        game_menu.addAction(self.pass_action)
        game_menu.addSeparator()
        menu_item = QAction("E&xit", self)
        menu_item.triggered.connect(self.close)
        game_menu.addAction(menu_item)
        # ------- Help -------
        help_menu = menu_bar.addMenu("&Help")
        menu_item = QAction("&About...", self)
        menu_item.triggered.connect(self.on_help_about)
        help_menu.addAction(menu_item)

    def game_menu_about_to_show(self):
        self.pass_action.setEnabled(len(self.reversi_widget.valid_moves) == 0) 
     
    def on_game_pass(self, s):
        self.reversi_widget.pass_flag = True
        self.reversi_widget.start_thinking()

    def on_game_new(self, s):
        self.reversi_widget.reset()
        
    def on_help_about(self, s):
        QMessageBox.aboutQt(self, "PyReversi")
        
    def load_settings(self):
        settings = QSettings("PyReversi", "PyReversi")
        self.resize(settings.value("size", QSize(800, 600)))
        self.move(settings.value("pos", QPoint(0, 0)))

    def save_settings(self):
        settings = QSettings("PyReversi", "PyReversi")
        settings.setValue("size", self.size())
        settings.setValue("pos", self.pos())

    def closeEvent(self, event):
        self.save_settings()

# ################################################################################

def main():
    app = QApplication([])
    app.setApplicationName(APPLICATION_NAME)
    app.setApplicationVersion(APPLICATION_VERSION)
    app.setWindowIcon(QIcon("PyReversi.ico"))
    main_window = MainWindow()
    main_window.show()
    app.exec()

if __name__ == "__main__":
    main()

