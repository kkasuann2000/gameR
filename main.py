import graphlib
import sys
from PyQt6.QtGui import QGuiApplication, QIcon
import os 
from PyQt6.QtCore import QUrl, QSize, QDateTime
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QLabel, QVBoxLayout, QScrollArea, QDialog
from PyQt6 import uic, QtCore
from datetime import datetime

collor = {1:'classic',
          2:'dark',
          3:'light',
          4:'blue'}


settings = {'collor': 'classic', 
            'size': 6, 
            'volume': True}



class pravilaWind(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setWindowTitle('pravila')
        self.setWindowTitle('правила игры реверси')
        self.label = QLabel(
            "Игра реверси, играется на доске 6х6; 8x8; 10х10; 12х12; клеток \nс черными и белыми фишками Игроки ходят по очереди,\nставя фишки на доску таким образом, \nчтобы окружить фишки противника. Когда фишки противника \nокружены фишками игрока с двух сторон, они переворачиваются \nна другую сторону. Цель игры - иметь больше фишек\n своего цвета на доске, чем у противника, когда все клетки\n заняты. Игра заканчивается, когда ни у одного из игроков \nнет возможности сделать ход, и побеждает \nтот, у кого больше фишек на доске.")
        layout.addWidget(self.label)
        self.setLayout(layout)


        
        

class MainWindow(QMainWindow):#глваное oкно
    def __init__(self):
        super().__init__()
        uic.loadUi("QTdisignerrrrr\\first.ui" , self)
        self.collor_vibor.hide()
        self.mashtab_vibor.hide()  
        self.window = None
        self.play_Bt.clicked.connect(self.play)
        self.pravilaBt.clicked.connect(self.pravilno_kliknuto)
        self.collorBt.clicked.connect(self.collor_kliknuto)
        self.mashtab_Bt.clicked.connect(self.mashtab_kliknuto)
        self.zvuk_Bt.setCheckable(True)
        self.zvuk_Bt.clicked.connect(self.valume_klicnuto)
       
        self.classic_Bt.clicked.connect(self.classic_Bt_clicnuto)
        self.light_Bt.clicked.connect(self.light_Bt_clicnuto)
        self.blue_Bt.clicked.connect(self.blue_Bt_clicnuto)
        self.dark_Bt.clicked.connect(self.dark_Bt_clicnuto)

        self.x6.clicked.connect(self.x6_clicnuto)
        self.x8.clicked.connect(self.x8_clicnuto)
        self.x10.clicked.connect(self.x10_clicnuto)
        self.x12.clicked.connect(self.x12_clicnuto)

    def play(self):
        size = settings['size']
        color = settings['collor']


        class Pole(QDialog):
            def __init__(self):
                super().__init__()
                self.check = 'game'
                self.pauseWind = None
                uic.loadUi(f'QTdisignerrrrr\\pole{size}{size}_{color}.ui', self)
                self.ui = uic.loadUi(f'QTdisignerrrrr\\pole{size}{size}_{color}.ui', self)
                self.current_player = 1
                count = 1
                self.temp = 0
                self.wind = None
                self.timer = QtCore.QTimer(self)
                self.timer.setInterval(1000)
                self.timer.timeout.connect(self.displayTime)
                self.timer.start()
                self.pushButton_4.clicked.connect(self.again)
                self.pushButton_3.clicked.connect(self.pause)

                if size == (6 or 8):
                    self.iconSize = QSize(41, 41)
                else:
                    self.iconSize = QSize(31, 31)

                middle = size // 2
                self.board = [[0] * size for _ in range(size)]
                self.board[middle-1][middle-1] = self.board[middle][middle] = 1
                self.board[middle-1][middle] = self.board[middle][middle-1] = 2

                self.buttons = []
                for i in range(size):
                    row = []
                    for j in range(size):
                        button = getattr(self.ui, f'a{count}')
                        button.clicked.connect(lambda _, row=i, col=j: self.buttonClicked(row, col))
                        row.append(button)
                        count += 1
                    self.buttons.append(row)

                self.buttons[middle-1][middle-1].setIcon(QIcon('images\\BlackToken.png'))
                self.buttons[middle-1][middle-1].setIconSize(self.iconSize)
                self.buttons[middle-1][middle].setIcon(QIcon('images\\WhiteToken.png'))
                self.buttons[middle-1][middle].setIconSize(self.iconSize)
                self.buttons[middle][middle].setIcon(QIcon('images\\BlackToken.png'))
                self.buttons[middle][middle].setIconSize(self.iconSize)
                self.buttons[middle][middle-1].setIcon(QIcon('images\\WhiteToken.png'))
                self.buttons[middle][middle-1].setIconSize(self.iconSize)

            def pause(self):
                self.timer.stop()
                if self.check == 'game':
                    for i in range(size):
                        for j in range(size):
                            self.buttons[i][j].setEnabled(False)
                    self.check = 'pause'
                else:
                    self.check = 'game'
                    for i in range(size):
                        for j in range(size):
                            self.buttons[i][j].setEnabled(True)
                    self.timer.start()
              
            

            def again(self):
                self.wind = Pole()
                self.wind.show()
                self.close()

            def displayTime(self):
                self.textBrowser_3.setText(f'time \n\n\n{datetime.utcfromtimestamp(self.temp).strftime("%H:%M:%S")}')
                self.temp += 1
                score = sum(row.count(0) for row in self.board)
                if score == 0:
                    self.timer.stop()
                    winner = self.check_winner()
                    if winner == 1:
                        print("Победил игрок 1!")
                    elif winner == 2:
                        print("Победил игрок 2!")
                    else:
                        print("Ничья!")

            def count_score(self):
                player1_score = sum(row.count(1) for row in self.board)
                player2_score = sum(row.count(2) for row in self.board)
                return player1_score, player2_score

            def check_winner(self):
                player1_score, player2_score = self.count_score()
                if player1_score > player2_score:
                    return 1
                elif player2_score > player1_score:
                    return 2
                else:
                    return 0 

            def buttonClicked(self, row, col):
                if self.is_valid_move(row, col):
                    self.make_move(row, col)
                    self.current_player = 1 if self.current_player == 2 else 2
                    self.update_board()

            def is_valid_move(self, row, col):
                if self.board[row][col] != 0:
                    return False
                directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
                valid_move = False
                for dr, dc in directions:
                    r, c = row + dr, col + dc
                    while 0 <= r < size and 0 <= c < size:
                        if self.board[r][c] == 0:
                            break
                        if self.board[r][c] == self.current_player:
                            valid_move = True
                            break
                        r, c = r + dr, c + dc
                    if valid_move:
                        break
                return valid_move

            def make_move(self, row, col):
                self.board[row][col] = self.current_player
                directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
                for dr, dc in directions:
                    r, c = row + dr, col + dc
                    to_flip = []
                    while 0 <= r < size and 0 <= c < size and self.board[r][c] != 0 and self.board[r][c] != self.current_player:
                        to_flip.append((r, c))
                        r, c = r + dr, c + dc
                    if 0 <= r < size and 0 <= c < size and self.board[r][c] == self.current_player:
                        for flip_r, flip_c in to_flip:
                            self.board[flip_r][flip_c] = self.current_player

            def update_board(self):
                for i in range(size):
                    for j in range(size):
                        if self.board[i][j] == 0:
                            pass
                        elif self.board[i][j] == 1:
                            self.buttons[i][j].setIcon(QIcon('images\\BlackToken.png'))
                            self.buttons[i][j].setIconSize(self.iconSize)
                        else:
                            self.buttons[i][j].setIcon(QIcon('images\\WhiteToken.png'))
                            self.buttons[i][j].setIconSize(self.iconSize)

        #Запуск поля
        self.window = Pole()
        self.window.show()
        self.close()            
        


            



    def mashtab_kliknuto(self):
        print(settings)
        self.mashtab_vibor.setVisible(True)
        self.x6.setEnabled(True)
        self.x8.setEnabled(True)
        self.x10.setEnabled(True)
        self.x12.setEnabled(True)

    def valume_klicnuto(self):
        if self.zvuk_Bt.isChecked():
            self.music = ("sounds\Rmusic.mp3")
            self.player = QMediaPlayer()
            self.player.setLoops(66)
            self.audio_output = QAudioOutput()
            self.player.setAudioOutput(self.audio_output)
            self.player.setSource(QUrl.fromLocalFile(self.music))
            self.audio_output.setVolume(50)
            self.player.play()
        else:
            self.player.stop()

    def pravilno_kliknuto(self):
        self.window = pravilaWind()
        self.window.setGeometry(700, 150, 400, 200)
        self.window.show()


    def x6_clicnuto(self):
        global settings
        settings['size'] = 6
        self.mashtab_vibor.setVisible(False)

    def x8_clicnuto(self):
        global settings
        settings['size'] = 8
        self.mashtab_vibor.setVisible(False)

    def x10_clicnuto(self):
        global settings
        settings['size'] = 10
        self.mashtab_vibor.setVisible(False)

    def x12_clicnuto(self):
        global settings
        settings['size'] = 12
        self.mashtab_vibor.setVisible(False)

    def classic_Bt_clicnuto(self):
        global settings
        settings['collor'] = 'classic'
        self.collor_vibor.setVisible(False)
    
    def light_Bt_clicnuto(self):
        global settings
        settings['collor'] = 'light'
        self.collor_vibor.setVisible(False)

    def blue_Bt_clicnuto(self):
        global settings
        settings['collor'] = 'blue'
        self.collor_vibor.setVisible(False)

    def dark_Bt_clicnuto(self):
        global settings
        settings['collor'] = 'dark'
        self.collor_vibor.setVisible(False)
             
    def collor_kliknuto(self):
        self.collor_vibor.setVisible(True)
        self.classic_Bt.setEnabled(True)
        self.light_Bt.setEnabled(True)
        self.dark_Bt.setEnabled(True)
        self.blue_Bt.setEnabled(True)

app = QApplication(sys.argv)
# Rmusic = ("sounds\Rmusic.mp3")
# player = QMediaPlayer()
# audio_output = QAudioOutput()
# player.setAudioOutput(audio_output)
# player.setSource(QUrl.fromLocalFile(Rmusic))
# audio_output.setVolume(50)
# player.play()
window = MainWindow()
window.show()
app.exec()


# плашка к цвету поле для размера ыыва