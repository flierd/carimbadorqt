import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from PIL import Image, ImageQt, ImageGrab
from pathlib import Path
from keyboard import is_pressed
from pyautogui import position


class CarimbadorQt(QWidget):

    def __init__(self):
        super().__init__()
        self.initui()

    def initui(self):

        btnAbrir = QPushButton('Abrir')
        btnAbrir.clicked.connect(self.eventoOpen)

        btnCapturar = QPushButton('Capturar')
        btnCapturar.clicked.connect(self.eventoCaptura)

        layout = QGridLayout()
        layout.addWidget(btnAbrir, 0, 0, 5, 10)
        layout.addWidget(btnCapturar, 0, 0, 10, 10)

        self.setGeometry(100, 30, 200, 200)

        self.setLayout(layout)
        self.show()

    def eventoOpen(self):
        f = QFileDialog.getOpenFileName(None,'Abrir',str(Path.home())+'/Pictures','PNG (*.png);;JPEG (*.jpg)')
        print (f)
    
    def eventoCaptura(self):
        a = 0
        x1 = 0
        y1 = 0
        x2 = 0
        y2 = 0
        while (a==0):
            if is_pressed('ctrl+shift+a'):
                x1, y1 = position()
                print (str(x1)+':'+str(y1))
                a = 1
        
        while (a==1):
            if is_pressed('ctrl+shift+s'):
                x2, y2 = position()
                print (str(x2)+':'+str(y2))
                a = 0
                
        box = (x1,y1,x2,y2)
        self.img = ImageGrab.grab(box)
        self.img.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = CarimbadorQt()
    sys.exit(app.exec_())
