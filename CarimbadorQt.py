import sys
from os import listdir
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from PIL import Image, ImageQt, ImageGrab
from pathlib import Path
from keyboard import is_pressed
from pyautogui import position
import numpy as np

class CarimbadorQt(QWidget):

    def __init__(self):
        super().__init__()
        self.initui()

    def initui(self):
        self.img = Image.open('./res/vazio.png')
        self.im = self.img.copy()
        self.im.thumbnail([500,500],Image.ANTIALIAS)
        
        self.imagemResultado = Image.open('./res/vazio.png')

        self.logo = Image.open('./res/vazio.png')
        self.imlogo = self.logo.copy()
        self.imlogo.thumbnail([100,100],Image.ANTIALIAS)        

        btnAbrir = QPushButton('Abrir')
        btnAbrir.clicked.connect(self.eventoOpen)

        btnCapturar = QPushButton('Capturar')
        btnCapturar.clicked.connect(self.eventoCaptura)

        btnSalvar = QPushButton('Salvar')
        btnSalvar.clicked.connect(self.eventoSave)

        self.spinEscala = QDial()
        self.spinEscala.setValue(30)
        self.spinEscala.setMinimum(10)
        self.spinEscala.setNotchesVisible(True)
        self.spinEscala.setToolTip('Escala do Logo')

        self.labelImagem = QLabel()
        self.imagemqt = ImageQt.ImageQt(self.img)
        self.labelImagem.setPixmap(QPixmap.fromImage(self.imagemqt))
        self.labelImagem.setObjectName("image")
        self.labelImagem.mousePressEvent = self.getPos

        self.listaLogo = QListWidget()
        self.listaLogo.addItems(self.getLogoList())
        self.listaLogo.clicked.connect(self.eventoMudaLogo)

        self.btnCor = QPushButton('Cor')
        self.btnCor.clicked.connect(self.eventoCorLogo)

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


        layout.addWidget(btnSalvar, 1, 0,Qt.AlignTop)
        layout.addWidget(self.listaLogo,2,0,Qt.AlignBottom)
        layout.addWidget(self.labelLogo,2,1,1,1)
        layout.addWidget(self.btnCor,2,1,Qt.AlignRight)


        self.setLayout(layout)
        self.show()

    def getPos(self,event):
        a = event.pos().x()
        b = event.pos().y()
        self.wajustado = a/self.im.width
        self.hajustado = b/self.im.height
        self.imagemResultado = self.inseremarca(self.img,self.logo,[a,b])
        self.thumbResultado = self.imagemResultado.copy()
        self.thumbResultado.thumbnail([500,500],Image.ANTIALIAS)
        self.imagemResqt = ImageQt.ImageQt(self.thumbResultado)
        self.labelImagem.setPixmap(QPixmap.fromImage(self.imagemResqt))


    def eventoCorLogo(self):
        cor = QColorDialog.getColor()
        a = (cor.red(),cor.green(),cor.blue())
        print(a)
        #Ver qual é a imagem do logo
        im = Image.open('./res/'+self.listaLogo.currentItem().text())
        im = im.convert('RGBA')

        data = np.array(im)   # "data" is a height x width x 4 numpy array
        red, green, blue, alpha = data.T # Temporarily unpack the bands for readability

        # Replace white with red... (leaves alpha values alone...)
        black_areas = (red == 0) & (blue == 0) & (green == 0)
        data[..., :-1][black_areas.T] = a # Transpose back needed

        im2 = Image.fromarray(data)
        self.logo = im2
        self.imlogo = self.logo.copy()
        self.imlogo.thumbnail([100,100],Image.ANTIALIAS)
        self.logoqt = ImageQt.ImageQt(self.imlogo)
        self.labelLogo.setPixmap(QPixmap.fromImage(self.logoqt))
        

    def eventoOpen(self):
        f,_ = QFileDialog.getOpenFileName(None,'Abrir',str(Path.home())+'/Pictures','Todos (*.*);;PNG (*.png);;JPEG (*.jpg)')
        print(f+" - "+_)
        if (f):
            self.img = Image.open(f,'r')
            self.im = self.img.copy()
            self.im.thumbnail([500,500],Image.ANTIALIAS)
            self.imagemqt = ImageQt.ImageQt(self.im)
            self.labelImagem.setPixmap(QPixmap.fromImage(self.imagemqt))
        else:
            print('erro de arquivo')
    
    def eventoSave(self):
        localsalvar,_ = QFileDialog.getSaveFileName(None,'Salvar',str(Path.home())+'/Pictures','PNG (*.png);;JPEG (*.jpg)')
        print (localsalvar+' - '+_)
        if (localsalvar):
            self.imagemResultado.save(localsalvar)
        else:
            print ('erro ao salvar')
    
    def eventoCaptura(self):
        a = 0
        x1 = 0
        y1 = 0
        x2 = 0
        y2 = 0
        QMessageBox.question(self, 'Aviso', "Posicione o mouse no primeiro ponto e pressione ctrl+shift+a", QMessageBox.Ok)
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
        self.im = self.img.copy()
        self.im.thumbnail([500,500],Image.ANTIALIAS)
        self.imagemqt = ImageQt.ImageQt(self.im)
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

    def inseremarca(self,imagem,watermark,posicao=[0,0]):
        base_image = imagem
        width, height = base_image.size
        marca = watermark.copy()
        escalaLogo = int(self.spinEscala.value())
        marca.thumbnail([int(width*(escalaLogo/100)),int(width*(escalaLogo/100))],Image.ANTIALIAS)
        cx=posicao
        cx[0]=int(width*self.wajustado)
        cx[1]=int(height*self.hajustado)
        cx[0]=cx[0]-int(marca.size[0]/2)
        cx[1]=cx[1]-int(marca.size[1]/2)
        transparent = Image.new('RGBA', (width, height), (0,0,0,0))    
        transparent.paste(base_image,[0,0])
        if (cx[0]>width-marca.size[0]):
                cx[0] = width-marca.size[0]
        if (cx[1]>height-marca.size[1]):
                cx[1] = height-marca.size[1]
        if (cx[0]<0):
                cx[0] = 0
        if (cx[1]<0):
                cx[1] = 0
        transparent.paste(marca, cx, mask=marca)
        return transparent


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = CarimbadorQt()
    sys.exit(app.exec_())
