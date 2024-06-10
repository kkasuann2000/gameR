import sys
from PyQt6.QtGui import QGuiApplication
import os
from PyQt6.QtCore import QUrl
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QLabel, QVBoxLayout, QScrollArea, QDialog
from PyQt6 import uic

# словарь свой ств игры:

shashechka = { 0:'black',
               1:'white' }


sizes = {1: 6,
        2: 8,
        3: 10,
        4: 12}

color = {1:'classic',
          2:'dark',
          3:'light',
          4:'blue'}

settings = {'color': 1,
            'size': 2,
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

class shashechka(QLabel):
    def __init__(self):
        super().__init__()
        self.setPixmap('images\WhiteToken.png')
        self.setPixmap('images\BlackToken.png')

class timer(QLabel):
    def __init__(self):
        super().__init__()
        self.timer_bt.setText("score: " + str(score))
    timer = print('i')



    poles = {}
    for size in [6, 8, 10, 12]:
        for color in ['classic', 'dark', 'light', 'blue']:
            class pole(QDialog):
                def __init__(self):
                    super().__init__()
                    uic.loadUi(f'QTdisignerrrrr\\pole{size}{size}_{color}.ui', self)
            poles[(size, color)] = pole

class MainWindow(QMainWindow):#глваное oкно
    def __init__(self):
        super().__init__()
        uic.loadUi("QTdisignerrrrr\\first.ui" , self)
        self.collor_vibor.hide()
        self.mashtab_vibor.hide()

        self.play_Bt.clicked.connect(self.play)
        self.pravilaBt.clicked.connect(self.pravilno_kliknuto)
        self.collorBt.clicked.connect(self.collor_kliknuto)
        self.mashtab_Bt.clicked.connect(self.mashtab_kliknuto)
        self.zvuk_Bt.setCheckable(True)
        self.zvuk_Bt.clicked.connect(self.valume_klicnuto)
        # self.timer_bt.clicked.connect(self.timer)

        self.classic_Bt.clicked.connect(self.classic_Bt_clicnuto)
        self.light_Bt.clicked.connect(self.light_Bt_clicnuto)
        self.blue_Bt.clicked.connect(self.blue_Bt_clicnuto)
        self.dark_Bt.clicked.connect(self.dark_Bt_clicnuto)

        self.x6.clicked.connect(self.x6_clicnuto)
        self.x8.clicked.connect(self.x8_clicnuto)
        self.x10.clicked.connect(self.x10_clicnuto)
        self.x12.clicked.connect(self.x12_clicnuto)

    def play(self):
        global size
        size = sizes[settings['size']]
        global color
        color = color[settings['color']]
        self.window = shashechka.poles[(size, color)]()
        self.window.show()

    def mashtab_kliknuto(self):
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
        settings['size'] = 1
        self.mashtab_vibor.setVisible(False)

    def x8_clicnuto(self):
        global settings
        settings['size'] = 2
        self.mashtab_vibor.setVisible(False)

    def x10_clicnuto(self):
        global settings
        settings['size'] = 3
        self.mashtab_vibor.setVisible(False)

    def x12_clicnuto(self):
        global settings
        settings['size'] = 4
        self.mashtab_vibor.setVisible(False)

    def classic_Bt_clicnuto(self):
        global settings
        settings['color'] = 1
        self.collor_vibor.setVisible(False)

    def light_Bt_clicnuto(self):
        global settings
        settings['color'] = 3
        self.collor_vibor.setVisible(False)

    def blue_Bt_clicnuto(self):
        global settings
        settings['color'] = 4
        self.collor_vibor.setVisible(False)

    def dark_Bt_clicnuto(self):
        global settings
        settings['color'] = 2
        self.collor_vibor.setVisible(False)

    def collor_kliknuto(self):
        self.collor_vibor.setVisible(True)
        self.classic_Bt.setEnabled(True)
        self.light_Bt.setEnabled(True)
        self.dark_Bt.setEnabled(True)
        self.blue_Bt.setEnabled(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())