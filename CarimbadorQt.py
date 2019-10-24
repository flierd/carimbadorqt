import sys
from os import listdir
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
        self.im = self.img.copy()
        self.im.thumbnail([500,500],Image.ANTIALIAS)

        self.logo = Image.open('./res/vazio.png')
        self.imlogo = self.logo.copy()
        self.imlogo.thumbnail([100,100],Image.ANTIALIAS)        

        btnAbrir = QPushButton('Abrir')
        btnAbrir.clicked.connect(self.eventoOpen)

        btnCapturar = QPushButton('Capturar')
        btnCapturar.clicked.connect(self.eventoCaptura)

        self.spinEscala = QDial()
        self.spinEscala.setValue(30)
        self.spinEscala.setNotchesVisible(True)
        self.spinEscala.setToolTip('Escala do Logo')

        self.labelImagem = QLabel()
        self.imagemqt = ImageQt.ImageQt(self.img)
        self.labelImagem.setPixmap(QPixmap.fromImage(self.imagemqt))
        self.labelImagem.setObjectName("image")

        self.listaLogo = QListWidget()
        self.listaLogo.addItems(self.getLogoList())
        self.listaLogo.clicked.connect(self.eventoMudaLogo)

        self.labelLogo = QLabel()
        self.logoqt = ImageQt.ImageQt(self.imlogo)
        self.labelLogo.setPixmap(QPixmap.fromImage(self.logoqt))

        self.setGeometry(100, 30, 500, 500)
        self.setWindowTitle("Carimbador Qt")
        self.setWindowIcon(QIcon('./res/nova200.png'))

        layout = QGridLayout()
        layout.addWidget(btnAbrir, 0, 0,Qt.AlignTop)
        layout.addWidget(btnCapturar, 0, 0,Qt.AlignVCenter)
        layout.addWidget(self.labelImagem,0,1,1,1)
        layout.addWidget(self.spinEscala,0,0,Qt.AlignBottom)


        layout.addWidget(self.listaLogo,1,0,Qt.AlignVCenter)
        layout.addWidget(self.labelLogo,1,1,1,1)


        self.setLayout(layout)
        self.show()

    def eventoOpen(self):
        f = QFileDialog.getOpenFileName(None,'Abrir',str(Path.home())+'/Pictures','PNG (*.png);;JPEG (*.jpg)')
        self.img = Image.open(f[0],'r')
        im = self.img.copy()
        im.thumbnail([500,500],Image.ANTIALIAS)
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
        im = self.img.copy()
        im.thumbnail([500,500],Image.ANTIALIAS)
        self.imagemqt = ImageQt.ImageQt(im)
        self.labelImagem.setPixmap(QPixmap.fromImage(self.imagemqt))
    
    def getLogoList(self):
        arqsLogos=[]
        for f in listdir('./res'):
            if f.endswith('.jpg') or f.endswith('.png') or f.endswith('.PNG') or f.endswith('.JPG'):
                arqsLogos.append(f)
        return arqsLogos

    def eventoMudaLogo(self):
        self.logo = Image.open('./res/'+self.listaLogo.currentItem().text())
        self.imlogo = self.logo.copy()
        self.imlogo.thumbnail([100,100],Image.ANTIALIAS)
        self.logoqt = ImageQt.ImageQt(self.imlogo)
        self.labelLogo.setPixmap(QPixmap.fromImage(self.logoqt))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = CarimbadorQt()
    sys.exit(app.exec_())
