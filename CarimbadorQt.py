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
        self.img = Image.open('./res/vazio.png')

        btnAbrir = QPushButton('Abrir')
        btnAbrir.clicked.connect(self.eventoOpen)

        btnCapturar = QPushButton('Capturar')
        btnCapturar.clicked.connect(self.eventoCaptura)

        self.labelImagem = QLabel()
        self.imagemqt = ImageQt.ImageQt(self.img)
        self.labelImagem.setPixmap(QPixmap.fromImage(self.imagemqt))
        self.labelImagem.setObjectName("image")

        self.setGeometry(100, 30, 500, 500)
        self.setWindowTitle("Carimbador Qt")
        self.setWindowIcon(QIcon('./res/nova200.png'))

        layout = QGridLayout()
        layout.addWidget(btnAbrir, 0, 0,Qt.AlignTop)
        layout.addWidget(btnCapturar, 0, 0,Qt.AlignTrailing)
        layout.addWidget(self.labelImagem,0,1,1,1)


        self.setLayout(layout)
        self.show()

    def eventoOpen(self):
        f = QFileDialog.getOpenFileName(None,'Abrir',str(Path.home())+'/Pictures','PNG (*.png);;JPEG (*.jpg)')
        self.img = Image.open(f[0],'r')
        im = self.img.copy()
        im.thumbnail([600,600],Image.ANTIALIAS)
        self.imagemqt = ImageQt.ImageQt(im)
        self.labelImagem.setPixmap(QPixmap.fromImage(self.imagemqt))
    
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
                QMessageBox.question(self, 'Aviso', "Primeiro ponto definido,pressione OK e escolha o segundo", QMessageBox.Ok)
                a = 1
        
        while (a==1):
            if is_pressed('ctrl+shift+a'):
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
