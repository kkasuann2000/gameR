import graphlib
import sys
from PyQt6.QtGui import QGuiApplication
import os 
from PyQt6.QtCore import QUrl
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QLabel, QVBoxLayout, QScrollArea, QDialog
from PyQt6 import uic

# словарь свой ств игры:
size_field = {1: 6,
              2: 8,
              3: 10,
              4: 12}

collor = {1:'classic',
          2:'dark',
          3:'light',
          4:'blue'}


settings = {'collor': 1, 
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
        self.setPixmap(QPixmap('images\\WhiteToken.png'))

        

class pole6x6classic(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('QTdisignerrrrr\\pole66_classic.ui' , self)

class pole6x6dark(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('QTdisignerrrrr\\pole66_dark.ui' , self)

class pole6x6light(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('QTdisignerrrrr\\pole66_light.ui' , self)

class pole6x6blue(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('QTdisignerrrrr\\pole66_blue.ui' , self)

class pole8x8classic(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('QTdisignerrrrr\\pole88_classic.ui' , self)

class pole8x8dark(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('QTdisignerrrrr\\pole88_dark.ui' , self)

class pole8x8light(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('QTdisignerrrrr\\pole88_light.ui' , self)

class pole8x8blue(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('QTdisignerrrrr\\pole88_blue.ui' , self)

class pole10x10classic(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('QTdisignerrrrr\\pole1010_classic.ui' , self)

class pole10x10dark(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('QTdisignerrrrr\\pole1010_dark.ui' , self)

class pole10x10light(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('QTdisignerrrrr\\pole1010_light.ui' , self)

class pole10x10blue(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('QTdisignerrrrr\\pole1010_blue.ui' , self)

class pole12x12classic(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('QTdisignerrrrr\\pole1212_classic.ui' , self)

class pole12x12dark(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('QTdisignerrrrr\\pole1212_dark.ui' , self)

class pole12x12light(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('QTdisignerrrrr\\pole1212_light.ui' , self)

class pole12x12blue(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('QTdisignerrrrr\\pole1212_blue.ui' , self)



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
       
        self.classic_Bt.clicked.connect(self.classic_Bt_clicnuto)
        self.light_Bt.clicked.connect(self.light_Bt_clicnuto)
        self.blue_Bt.clicked.connect(self.blue_Bt_clicnuto)
        self.dark_Bt.clicked.connect(self.dark_Bt_clicnuto)

        self.x6.clicked.connect(self.x6_clicnuto)
        self.x8.clicked.connect(self.x8_clicnuto)
        self.x10.clicked.connect(self.x10_clicnuto)
        self.x12.clicked.connect(self.x12_clicnuto)

    def play(self):
        if settings['collor'] == 1:
            if settings['size'] == 1:
                self.window = pole6x6classic()
                self.window.show()
        if settings['collor'] == 2:
            if settings['size'] == 1:
                self.window = pole6x6dark()
                self.window.show()
        if settings['collor'] == 3:
            if settings['size'] == 1:
                self.window = pole6x6light()
                self.window.show()
        if settings['collor'] == 4:
            if settings['size'] == 1:
                self.window = pole6x6blue()
                self.window.show()


        if settings['collor'] == 1:
            if settings['size'] == 2:
                self.window = pole8x8classic()
                self.window.show()
        if settings['collor'] == 2:
            if settings['size'] == 2:
                self.window = pole8x8dark()
                self.window.show()
        if settings['collor'] == 3:
            if settings['size'] == 2:
                self.window = pole8x8light()
                self.window.show()
        if settings['collor'] == 4:
            if settings['size'] == 2:
                self.window = pole8x8blue()
                self.window.show()

        if settings['collor'] == 1:
            if settings['size'] == 3:
                self.window = pole10x10classic()
                self.window.show()
        if settings['collor'] == 2:
            if settings['size'] == 3:
                self.window = pole10x10dark()
                self.window.show()
        if settings['collor'] == 3:
            if settings['size'] == 3:
                self.window = pole10x10light()
                self.window.show()
        if settings['collor'] == 4:
            if settings['size'] == 3:
                self.window = pole10x10blue()
                self.window.show()

        if settings['collor'] == 1:
            if settings['size'] == 4:
                self.window = pole12x12classic()
                self.window.show()
        if settings['collor'] == 2:
            if settings['size'] == 4:
                self.window = pole12x12dark()
                self.window.show()
        if settings['collor'] == 3:
            if settings['size'] == 4:
                self.window = pole12x12light()
                self.window.show()
        if settings['collor'] == 4:
            if settings['size'] == 4:
                self.window = pole12x12blue()
                self.window.show()



    def mashtab_kliknuto(self):
        self.mashtab_vibor.setVisible(True)
        self.x6.setEnabled(True)
        self.x8.setEnabled(True)
        self.x10.setEnabled(True)
        self.x12.setEnabled(True)

    def valume_klicnuto(self):
        # self.music = ("sounds\Rmusic.mp3")
        # self.player = QMediaPlayer()
        # self.audio_output = QAudioOutput()
        # self.player.setAudioOutput(self.audio_output)
        # self.player.setSource(QUrl.fromLocalFile(self.music))
        # self.audio_output.setVolume(50)

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
        settings['collor'] = 1
        self.collor_vibor.setVisible(False)
    
    def light_Bt_clicnuto(self):
        global settings
        settings['collor'] = 3
        self.collor_vibor.setVisible(False)

    def blue_Bt_clicnuto(self):
        global settings
        settings['collor'] = 4
        self.collor_vibor.setVisible(False)

    def dark_Bt_clicnuto(self):
        global settings
        settings['collor'] = 2
        self.collor_vibor.setVisible(False)

    
        

     

        # global settings
        # if self.blue_Bt.clicked:
        #     settings['collor'] = 4
        #     print(settings)
        # elif self.light_Bt.clicked:
        #     settings['collor'] = 1
        #     print(settings)
        # elif self.dark_Bt.clicked:
        #     settings['collor'] = 2
        #     print(settings)
        # elif self.classic_Bt.clicked:
        #     settings['collor'] = 3
        
                 
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

