import graphlib
import sys
import os
from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QLabel, QVBoxLayout
from PyQt6 import uic


class pravilaWind(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setWindowTitle('pravila')
        self.label = QLabel(
            "Игра реверси, играется на доске 6х6; 8x8; 10х10; 12х12; клеток \nс черными и белыми фишками Игроки ходят по очереди,\nставя фишки на доску таким образом, \nчтобы окружить фишки противника. Когда фишки противника \nокружены фишками игрока с двух сторон, они переворачиваются \nна другую сторону. Цель игры - иметь больше фишек\n своего цвета на доске, чем у противника, когда все клетки\n заняты. Игра заканчивается, когда ни у одного из игроков \nнет возможности сделать ход, и побеждает \nтот, у кого больше фишек на доске.")
        layout.addWidget(self.label)
        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("C:\\Users\\finch\\OneDrive\\Рабочий стол\\pyqt progect\\gameR\\first.ui" , self)

        self.pravilaBt.clicked.connect(self.pravilno_kliknuto)

    def pravilno_kliknuto(self):
        self.window = pravilaWind()
        self.window.setGeometry(700, 150, 400, 200)
        self.window.show()


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()

# функ цикл отоборазить ячейку \\ матрица
