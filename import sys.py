import graphlib
import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QLabel, QVBoxLayout
from PyQt6 import uic

class pravilaWind(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setWindowTitle('pravila')
        window.setGeometry(300, 250, 700, 800)
        self.label = QLabel("Another Window")
        layout.addWidget(self.label)
        self.setLayout(layout)
       
      



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("C:\\Users\\finch\\OneDrive\\Рабочий стол\\pyqt progect\\first.ui" , self)
        
        
        self.pravilaBt.clicked.connect(self.pravilno_kliknuto)


    def  pravilno_kliknuto(self) :
        window = pravilaWind()
        window.show()


app= QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()








#функ цикл отоборазить ячейку \\ матрица 